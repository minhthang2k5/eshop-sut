import { parse } from 'acorn';

// Static analysis only: uploaded code is never evaluated by Node.
export function analyzeSource(source) {
  const comments = [];
  const ast = parse(source, { ecmaVersion: 'latest', sourceType: 'module', locations: true, onComment: comments });
  const scopes = new WeakMap();
  const nodes = [];
  const functions = new Map();
  const global = { parent: null, bindings: new Map() };
  function visit(node, scope) {
    if (!node || typeof node.type !== 'string') return;
    if (node.type === 'FunctionDeclaration' && node.id) {
      functions.set(node.id.name, node);
      scope.bindings.set(node.id.name, node);
    }
    if (/Function/.test(node.type)) {
      scope = { parent: scope, bindings: new Map(), fn: node };
      node.params.forEach((param) => { if (param.type === 'Identifier') scope.bindings.set(param.name, null); });
    }
    scopes.set(node, scope);
    nodes.push(node);
    if (node.type === 'VariableDeclarator' && node.id.type === 'Identifier') scope.bindings.set(node.id.name, node.init);
    for (const [key, value] of Object.entries(node)) {
      if (['loc', 'start', 'end'].includes(key)) continue;
      if (Array.isArray(value)) value.forEach((item) => visit(item, scope));
      else if (value?.type) visit(value, scope);
    }
  }
  visit(ast, global);
  const calls = nodes.filter((node) => node.type === 'CallExpression');
  const range = (min, max) => ({ kind: 'range', min, max });
  const asRange = (v) => typeof v === 'number' ? range(v, v) : v?.kind === 'range' ? v : null;
  function resolve(node, scope = scopes.get(node), depth = 0) {
    if (!node || depth > 24) return undefined;
    const next = (n, s = scope) => resolve(n, s, depth + 1);
    if (node.type === 'Literal') return node.value;
    if (node.type === 'Identifier') {
      for (let s = scope; s; s = s.parent) {
        if (!s.bindings.has(node.name)) continue;
        const binding = s.bindings.get(node.name);
        if (binding?.resolved) return binding.value;
        if (binding) return next(binding, s);
        const position = s.fn?.params.findIndex((param) => param.name === node.name);
        const sites = calls.filter((call) => call.callee.name === s.fn?.id?.name);
        const values = sites.map((call) => next(call.arguments[position], scopes.get(call))).filter((v) => v !== undefined);
        return values.length ? values[0] : undefined;
      }
      return undefined;
    }
    if (node.type === 'ArrayExpression') return node.elements.map((n) => next(n));
    if (node.type === 'ObjectExpression') return { kind: 'object', fields: Object.fromEntries(node.properties.filter((p) => p.type === 'Property').map((p) => [p.key.name || p.key.value, next(p.value)])) };
    if (node.type === 'LogicalExpression' && node.operator === '||') return next(node.left) ?? next(node.right);
    if (node.type === 'TemplateLiteral') {
      const values = node.expressions.map((n) => next(n));
      if (node.quasis[0].value.cooked === 'Bearer ' && values[0]?.kind === 'token') return { kind: 'bearer', token: values[0] };
      return node.quasis.map((q, i) => q.value.cooked + (i < values.length ? typeof values[i] === 'object' ? '<dynamic>' : values[i] ?? '<dynamic>' : '')).join('');
    }
    if (node.type === 'BinaryExpression') {
      const left = next(node.left), right = next(node.right);
      if (node.operator === '+' && left === 'Bearer ' && right?.kind === 'token') return { kind: 'bearer', token: right };
      if (node.operator === '+' && (typeof left === 'string' || typeof right === 'string')) return `${left ?? ''}${right ?? ''}`;
      const a = asRange(left), b = asRange(right);
      if (!a || !b) return undefined;
      let result;
      if (node.operator === '+') result = range(a.min + b.min, a.max + b.max);
      if (node.operator === '-') result = range(a.min - b.max, a.max - b.min);
      if (node.operator === '*') result = range(Math.min(a.min*b.min,a.min*b.max,a.max*b.min,a.max*b.max), Math.max(a.min*b.min,a.min*b.max,a.max*b.min,a.max*b.max));
      return result?.min === result?.max ? result.min : result;
    }
    if (node.type === 'MemberExpression') {
      const object = next(node.object);
      const key = node.computed ? next(node.property) : node.property.name;
      if (Array.isArray(object) && key === 'length') return object.length;
      if (Array.isArray(object) && typeof key === 'number') return object[key];
      if (Array.isArray(object) && key?.kind === 'range') return { kind: 'choice', items: object };
      if (object?.kind === 'response' && key === 'body') return { kind: 'body', endpoint: object.endpoint };
      if (object?.kind === 'json' && key === 'token') return { kind: 'token', endpoint: object.endpoint };
    }
    if (node.type !== 'CallExpression') return undefined;
    const callee = node.callee;
    const method = callee.type === 'MemberExpression' ? callee.property.name : null;
    const owner = callee.object?.name;
    if (owner === 'Math' && method === 'random') return range(0, 1);
    if (owner === 'Math' && method === 'floor') {
      const input = next(node.arguments[0]);
      if (typeof input === 'number') return Math.floor(input);
      // The random upper bound is exclusive for these uniform integer helpers.
      if (input?.kind === 'range') return range(Math.floor(input.min), Math.ceil(input.max) - 1);
    }
    if (owner === 'http' && ['get', 'post'].includes(method)) return { kind: 'response', endpoint: next(node.arguments[0]), method, body: method === 'post' ? next(node.arguments[1]) : null, params: next(node.arguments[method === 'post' ? 2 : 1]) };
    if (owner === 'JSON' && method === 'stringify') {
      const object = next(node.arguments[0]);
      if (object?.kind === 'object') return { kind: 'jsonBody', fields: object.fields };
    }
    if (owner === 'JSON' && method === 'parse') {
      const body = next(node.arguments[0]);
      if (body?.kind === 'body') return { kind: 'json', endpoint: body.endpoint };
    }
    if (method === 'json') {
      const response = next(callee.object);
      if (response?.kind === 'response') return { kind: node.arguments.length && next(node.arguments[0]) === 'token' ? 'token' : 'json', endpoint: response.endpoint };
    }
    if (callee.name === 'encodeURIComponent') return next(node.arguments[0]);
    const fn = functions.get(callee.name);
    if (fn) {
      const fnScope = scopes.get(fn);
      const bound = { ...fnScope, bindings: new Map(fnScope.bindings) };
      fn.params.forEach((param, i) => { if (param.type === 'Identifier') bound.bindings.set(param.name, { resolved: true, value: next(node.arguments[i]) }); });
      const returns = nodes.filter((n) => n.type === 'ReturnStatement' && scopes.get(n) === fnScope);
      // Trace successful return paths; guards are checked separately.
      const values = returns.map((n) => next(n.argument, bound)).filter((v) => v != null);
      return values.at(-1);
    }
    return undefined;
  }
  const requestNodes = calls.filter((node) => node.callee.object?.name === 'http' && ['post', 'get'].includes(node.callee.property?.name));
  function endpoints(branch, seen = new Set()) {
    if (!branch) return [];
    const contained = calls.filter((n) => n.start >= branch.start && n.end <= branch.end);
    return contained.flatMap((call) => {
      const request = resolve(call);
      if (request?.kind === 'response') return [request.endpoint];
      const fn = functions.get(call.callee.name);
      if (!fn || seen.has(fn)) return [];
      return endpoints(fn.body, new Set([...seen, fn]));
    }).filter((value) => typeof value === 'string');
  }
  const hasEndpoint = (branch, pattern) => endpoints(branch).some((value) => pattern.test(value));
  const workload = nodes.some((node) => {
    if (node.type !== 'IfStatement' || node.test.type !== 'BinaryExpression' || node.test.operator !== '<') return false;
    const second = node.alternate;
    if (second?.type !== 'IfStatement' || second.test.type !== 'BinaryExpression' || second.test.operator !== '<') return false;
    if (node.test.left.type !== 'Identifier' || node.test.left.name !== second.test.left.name) return false;
    const random = resolve(node.test.left);
    return random?.kind === 'range' && random.min === 0 && random.max === 1 && Math.abs(resolve(node.test.right) - .55) < 1e-9 && Math.abs(resolve(second.test.right) - .8) < 1e-9 && hasEndpoint(node.consequent, /\/api\/products\?search=/) && hasEndpoint(second.consequent, /\/api\/products\//) && hasEndpoint(second.alternate, /\/api\/checkout/);
  });
  const requests = requestNodes.map((node) => resolve(node));
  const correlation = requests.some((request) => {
    if (request.method !== 'post' || !/\/api\/checkout$/.test(request.endpoint)) return false;
    const headers = request.params?.fields?.headers?.fields || {};
    const value = Object.entries(headers).find(([key]) => key.toLowerCase() === 'authorization')?.[1];
    return value?.kind === 'bearer' && /\/api\/login$/.test(value.token.endpoint);
  });
  const urlDynamic = (url, predicate) => url?.type === 'TemplateLiteral' && url.expressions.some((expression) => predicate(resolve(expression)));
  const keywords = ['iPhone', 'Samsung', 'MacBook', 'AirPods', 'Keychron'];
  const searchRandom = requestNodes.some((call) => /\/api\/products\?search=/.test(resolve(call)?.endpoint) && urlDynamic(call.arguments[0], (value) => value?.kind === 'choice' && keywords.every((word) => value.items.includes(word))));
  const idRandom = requestNodes.some((call) => /\/api\/products\//.test(resolve(call)?.endpoint) && urlDynamic(call.arguments[0], (value) => value?.kind === 'range' && value.min === 1 && value.max === 5));
  const chars = source.split('');
  // Preserve line numbers, but comments must not satisfy rules.
  for (const comment of comments) for (let i = comment.start; i < comment.end; i++) if (chars[i] !== '\n' && chars[i] !== '\r') chars[i] = ' ';
  const apiPaths = requests.map((request) => typeof request.endpoint === 'string' ? request.endpoint.replace(/^https?:\/\/[^/]+/, '') : '');
  const endpointsValid = ['/api/login', '/api/checkout'].every((p) => apiPaths.includes(p)) && apiPaths.some((p) => p.startsWith('/api/products?search=')) && apiPaths.some((p) => p.startsWith('/api/products/')) && apiPaths.every((p) => /^\/api\/(login|checkout|products(?:\?search=.*|\/(?:<dynamic>|[1-5])))$/.test(p));
  const validPost = (endpoint, fields) => requests.some((request) => {
    const headers = request.params?.fields?.headers?.fields || {};
    const contentType = Object.entries(headers).find(([key]) => key.toLowerCase() === 'content-type')?.[1];
    return request.endpoint?.endsWith(endpoint) && request.method === 'post' && request.body?.kind === 'jsonBody' && fields.every((field) => Object.hasOwn(request.body.fields, field)) && contentType === 'application/json';
  });
  const methodsValid = validPost('/api/login', ['email', 'password']) && validPost('/api/checkout', ['total_amount', 'shipping_address']) && requests.filter((request) => request.endpoint?.includes('/api/products')).every((request) => request.method === 'get');
  const sleepCalls = calls.filter((node) => node.callee.name === 'sleep');
  const thinkTimeValid = [[/\/api\/products\?search=/, 1, 3], [/\/api\/products\//, 2, 5], [/\/api\/checkout$/, 3, 6]].every(([pattern, min, max]) => sleepCalls.some((call) => {
    const duration = resolve(call.arguments[0]);
    const block = nodes.filter((n) => n.type === 'BlockStatement' && n.start < call.start && n.end > call.end).sort((a,b) => (a.end-a.start)-(b.end-b.start))[0];
    return duration?.kind === 'range' && duration.min === min && duration.max === max && hasEndpoint(block, pattern);
  }));
  const checks = calls.filter((call) => call.callee.name === 'check').map((call) => {
    const response = resolve(call.arguments[0]);
    const predicates = call.arguments[1]?.type === 'ObjectExpression' ? call.arguments[1].properties.map((p) => p.value).filter(Boolean) : [];
    const inside = predicates.flatMap((predicate) => nodes.filter((n) => n.start >= predicate.start && n.end <= predicate.end));
    const field = (name) => inside.some((n) => n.type === 'MemberExpression' && (n.property.name || n.property.value) === name || n.type === 'CallExpression' && n.callee.property?.name === 'json' && n.arguments[0]?.value === name);
    const status = inside.some((n) => n.type === 'BinaryExpression' && ['==', '==='].includes(n.operator) && n.left.type === 'MemberExpression' && n.left.property.name === 'status' && n.right.value === 200);
    return { endpoint: response?.endpoint, status, token: field('token'), orderId: field('orderId') };
  });
  const checksValid = requests.length > 0 && requests.every((request) => checks.some((check) => check.endpoint === request.endpoint && check.status)) && checks.some((check) => /\/api\/login$/.test(check.endpoint) && check.token) && checks.some((check) => /\/api\/checkout$/.test(check.endpoint) && check.orderId);
  const isLoginToken = (node) => { const value = resolve(node); return value?.kind === 'token' && /\/api\/login$/.test(value.endpoint); };
  const invalidTokenTest = (node) => node?.type === 'UnaryExpression' && node.operator === '!' && isLoginToken(node.argument) || node?.type === 'BinaryExpression' && ['==', '==='].includes(node.operator) && isLoginToken(node.left) && node.right.type === 'Literal' && node.right.value === null || node?.type === 'LogicalExpression' && node.operator === '||' && (invalidTokenTest(node.left) || invalidTokenTest(node.right));
  const flowValid = nodes.some((node) => node.type === 'IfStatement' && invalidTokenTest(node.test) && !hasEndpoint(node.consequent, /\/api\/checkout$/) && nodes.some((ret) => ret.type === 'ReturnStatement' && ret.start >= node.consequent.start && ret.end <= node.consequent.end) && calls.some((call) => {
    if (scopes.get(call) !== scopes.get(node) || call.start < node.end) return false;
    return /\/api\/checkout$/.test(resolve(call)?.endpoint) || hasEndpoint(functions.get(call.callee.name)?.body, /\/api\/checkout$/);
  }));
  const options = nodes.find((node) => node.type === 'VariableDeclarator' && node.id.name === 'options');
  const thresholds = resolve(options?.init)?.fields?.thresholds?.fields;
  const thresholdsValid = Array.isArray(thresholds?.http_req_duration) && thresholds.http_req_duration.some((rule) => /^p\(95\)\s*<\s*500$/.test(rule)) && Array.isArray(thresholds?.checks) && thresholds.checks.some((rule) => /^rate\s*>=\s*0\.99$/.test(rule));
  return { correlation, workload, endpointsValid, methodsValid, checksValid, thinkTimeValid, flowValid, thresholdsValid, parameterization: searchRandom && idRandom, code: chars.join('') };
}
