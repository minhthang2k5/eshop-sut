import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { Counter } from 'k6/metrics';
import exec from 'k6/execution';

const BASE_URL = (__ENV.BASE_URL || 'http://localhost:3000').replace(/\/+$/, '');
// Single-line CSV contract matches seed.js; quoted commas and escaped quotes supported.
function csv(text, header) {
  const pattern = /(?:^|,)(?:"((?:[^"]|"")*)"|([^",\r\n]*))(?=,|$)/gy;
  const rows = text.replace(/^\uFEFF/, '').split(/\r?\n/).filter(line => line.trim()).map((line, index) => {
    pattern.lastIndex = 0;
    const fields = [];
    let match, end = 0;
    while ((match = pattern.exec(line)) !== null) {
      fields.push(match[1] === undefined ? match[2] : match[1].replace(/""/g, '"'));
      end = pattern.lastIndex;
      if (end === line.length) break;
    }
    if (end !== line.length || fields.length !== header.split(',').length) throw new Error(`Invalid CSV row ${index + 1}`);
    return fields;
  });
  if (!rows.length || rows.shift().join(',') !== header) throw new Error(`Invalid CSV header: ${header}`);
  return rows;
}
const accounts = new SharedArray('baseline accounts', () => {
  const seen = new Set();
  const rows = csv(open('./data/test_accounts.csv'), 'email,password,name,role').map(([email, password, name, role]) => {
    if (![email, password, name, role].every(v => v.trim()) || !['user', 'admin'].includes(role) || seen.has(email)) throw new Error('Invalid/duplicate account');
    seen.add(email);
    return { email, password };
  });
  if (rows.length < 50) throw new Error('Baseline requires at least 50 unique accounts');
  return rows.slice(0, 50);
});
const products = new SharedArray('baseline products', () => {
  const ids = new Set();
  const rows = csv(open('./data/test_product.csv'), 'product_id,name,price,description,image_url,category_id,search_keyword')
    .map(([id, name, price, description, imageUrl, category, keyword]) => {
      id = Number(id); price = Number(price); category = Number(category);
      if (![name, description, imageUrl, keyword].every(v => v.trim()) || !Number.isSafeInteger(id) || id <= 0 || ids.has(id) || !Number.isSafeInteger(price) || price <= 0 || !Number.isSafeInteger(category) || category <= 0) throw new Error('Invalid/duplicate product');
      ids.add(id);
      return { id, name, price, keyword };
    });
  if (!rows.some(p => p.id === 1 && p.keyword === 'iPhone' && p.name.toLowerCase().includes('iphone'))) throw new Error('Missing baseline product 1 / iPhone');
  return rows;
});
const profile = [
  { phase: 'ramp_up', seconds: 60, target: 50 },
  { phase: 'steady', seconds: 300, target: 50 },
  { phase: 'ramp_down', seconds: 60, target: 0 },
];
let timelineLogged = false;

// Module state is isolated per VU; never return or share JWTs through setup().
let authToken = null;
const skippedRequests = new Counter('business_requests_skipped');
const endpoints = ['search', 'detail', 'cart', 'checkout'];
const thresholds = {
  'http_req_duration{endpoint:login}': ['p(95)<500'],
  'http_req_failed{endpoint:login}': ['rate<0.01'],
  'checks{endpoint:login}': ['rate>=0.99'],
  'http_reqs{endpoint:login}': ['count>0'],
  // Expose steady Login separately without requiring it to occur in this window.
  'http_req_duration{phase:steady,endpoint:login}': [],
  'http_req_failed{phase:steady,endpoint:login}': [],
  'checks{phase:steady,endpoint:login}': [],
  'http_reqs{phase:steady,endpoint:login}': [],
  business_requests_skipped: ['count==0'],
  'http_req_duration{phase:steady}': ['p(95)<500'],
  'http_req_failed{phase:steady}': ['rate<0.01'],
  'checks{phase:steady}': ['rate>=0.99'],
  'http_reqs{phase:steady}': ['count>0'],
};
// Per-API thresholds prevent the frequent Search requests from hiding a slow Checkout.
for (const endpoint of endpoints) {
  const filter = `phase:steady,endpoint:${endpoint}`;
  thresholds[`http_req_duration{${filter}}`] = ['p(95)<500'];
  thresholds[`http_req_failed{${filter}}`] = ['rate<0.01'];
  thresholds[`checks{${filter}}`] = ['rate>=0.99'];
  thresholds[`http_reqs{${filter}}`] = ['count>0'];
}

export const options = {
  scenarios: {
    baseline: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: profile.map(({ seconds, target }) => ({ duration: `${seconds}s`, target })),
      gracefulRampDown: '30s',
      gracefulStop: '30s',
    },
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  thresholds,
};

// This SUT returns 200 for every successful endpoint in this test.
http.setResponseCallback(http.expectedStatuses(200));

function jsonBody(response) {
  try {
    return response.json();
  } catch (_) {
    return null;
  }
}

function ensureLoggedIn() {
  if (authToken) return true;
  const account = accounts[exec.vu.idInTest - 1];
  if (!account) throw new Error('VU ID outside the 50-account baseline allocation');
  const tags = { phase: phase(), endpoint: 'login', name: 'POST /api/login' };
  const response = http.post(`${BASE_URL}/api/login`, JSON.stringify({
    email: account.email,
    password: account.password,
  }), { headers: { 'Content-Type': 'application/json' }, tags, timeout: '10s' });
  const body = jsonBody(response);
  const valid = check(response, {
    'login: status is 200': (r) => r.status === 200,
    'login: token exists': () => !!body && typeof body.token === 'string' && body.token.length > 0,
  }, tags);
  if (valid) authToken = body.token;
  return valid;
}

function phase() {
  // Scenario clock excludes setup. Classify by request START, not iteration end.
  const elapsed = Date.now() - exec.scenario.startTime;
  let end = 0;
  for (const stage of profile) {
    end += stage.seconds * 1000;
    if (elapsed < end) return stage.phase;
  }
  return 'graceful_stop';
}

export default function () {
  if (!timelineLogged && exec.vu.idInTest === 1) {
    console.log('BASELINE_TIMELINE ' + JSON.stringify({ start_ms: exec.scenario.startTime, profile }));
    timelineLogged = true;
  }
  const product = products.find(p => p.id === 1);
  // Select one business operation per iteration. Lazy Login is additional traffic;
  // it does not participate in the 55/25/14/6 selection probabilities.
  const r = Math.random();
  let endpoint;
  let name;
  let response;
  let body;
  let minThink;
  let maxThink;
  let validBody;
  if (r < 0.55) {
    endpoint = 'search'; name = 'GET /api/products?search';
    minThink = 1; maxThink = 3;
  } else if (r < 0.80) {
    endpoint = 'detail'; name = 'GET /api/products/:id';
    minThink = 2; maxThink = 5;
  } else if (r < 0.94) {
    endpoint = 'cart'; name = 'POST /api/cart';
    minThink = 1; maxThink = 3;
  } else {
    endpoint = 'checkout'; name = 'POST /api/checkout';
    minThink = 3; maxThink = 6;
  }
  const needsAuth = endpoint === 'cart' || endpoint === 'checkout';
  if (needsAuth && !ensureLoggedIn()) {
    skippedRequests.add(1, { phase: phase(), endpoint });
    sleep(minThink + Math.random() * (maxThink - minThink));
    return;
  }
  // Recompute phase AFTER Login, which may cross a stage boundary.
  const tags = { phase: phase(), endpoint, name };
  skippedRequests.add(0, { phase: tags.phase, endpoint });
  const params = { tags, timeout: '10s', headers: {
    'Content-Type': 'application/json',
  } };
  if (needsAuth) params.headers.Authorization = `Bearer ${authToken}`;
  if (endpoint === 'search') {
    response = http.get(`${BASE_URL}/api/products?search=${encodeURIComponent(product.keyword)}`, params);
    body = jsonBody(response);
    validBody = Array.isArray(body) && body.some(p => p && p.id === product.id) && body.every(p => p && typeof p.name === 'string' && p.name.toLowerCase().includes(product.keyword.toLowerCase()));
  } else if (endpoint === 'detail') {
    response = http.get(`${BASE_URL}/api/products/${product.id}`, params);
    body = jsonBody(response);
    validBody = !!body && body.id === product.id && body.name === product.name && Number(body.price) === product.price;
  } else if (endpoint === 'cart') {
    response = http.post(`${BASE_URL}/api/cart`, JSON.stringify({
      id: product.id, name: product.name, price: product.price, quantity: 1,
    }), params);
    body = jsonBody(response);
    validBody = !!body && body.message === 'Added to cart';
  } else {
    // Current SUT creates orders independently of cart contents.
    response = http.post(`${BASE_URL}/api/checkout`, JSON.stringify({
      total_amount: product.price, shipping_address: '123 Le Loi, TP.HCM',
    }), params);
    body = jsonBody(response);
    validBody = !!body && Number.isInteger(body.orderId) && body.orderId > 0;
  }
  if (needsAuth && response.status === 401) authToken = null;
  check(response, {
    [`${endpoint}: status is 200`]: (res) => res.status === 200,
    [`${endpoint}: valid response body`]: () => validBody,
  }, tags);
  // Sleep after every request, including failures, to preserve pacing.
  sleep(minThink + Math.random() * (maxThink - minThink));
}
