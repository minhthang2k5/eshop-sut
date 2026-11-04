import http from 'k6/http';
import { check, sleep } from 'k6';
import exec from 'k6/execution';
import { accounts, products, baseUrl, keyword, json, matchesIds } from './data.js';
import * as metrics from './metrics.js';
const definitions = [
  { endpoint: 'search', name: 'GET /api/products?search', min: 1, max: 3 },
  { endpoint: 'detail', name: 'GET /api/products/:id', min: 2, max: 5 },
  { endpoint: 'cart', name: 'POST /api/cart', min: 1, max: 3 },
  { endpoint: 'checkout', name: 'POST /api/checkout', min: 3, max: 6 },
];
function valid(response, bodyValid, tags) {
  return check(response, {
    [`${tags.endpoint}: status is 200`]: r => r.status === 200,
    [`${tags.endpoint}: valid response body`]: () => bodyValid,
  }, tags);
}
// Inject each test's timeline so requests and metrics use its own phase tags.
export function createIteration({ profile, phaseAt, timelineLabel }) {
  function phase() { return phaseAt(Date.now() - exec.scenario.startTime); }
  return function iteration() {
    if (exec.scenario.iterationInTest === 0) {
      console.log(timelineLabel + ' ' + JSON.stringify({ start_ms: exec.scenario.startTime, profile }));
    }
    const r = Math.random();
    const op = definitions[r < 0.4 ? 0 : r < 0.6 ? 1 : r < 0.82 ? 2 : 3];
    const { endpoint } = op;
    const startTags = { phase: phase(), endpoint };
    metrics.started.add(1, startTags);
    metrics.selected.add(1, startTags);
    const accountIndex = exec.scenario.iterationInTest % accounts.length;
    if (__ENV.ACCOUNT_AUDIT === '1') console.log(JSON.stringify({ event: 'account_allocated', accountIndex, timestamp: Date.now() }));
    let token = null;
    let success = false;
    let skip = false;
    if (endpoint === 'cart' || endpoint === 'checkout') {
      const account = accounts[accountIndex];
      const tags = { phase: phase(), endpoint: 'login', name: 'POST /api/login' };
      const response = http.post(`${baseUrl}/api/login`, JSON.stringify(account), {
        headers: { 'Content-Type': 'application/json' }, timeout: '10s', tags,
      });
      const body = json(response);
      if (valid(response, !!body && typeof body.token === 'string' && body.token.length > 0, tags)) {
        token = body.token;
        if (__ENV.ACCOUNT_AUDIT === '1') console.log(JSON.stringify({ event: 'login_success', accountIndex, timestamp: Date.now() }));
      } else skip = true;
    }
    metrics.skipped.add(skip ? 1 : 0, { ...startTags, reason: skip ? 'login_failed' : 'none' });
    if (!skip) {
      // Login may cross a phase boundary: classify this request independently.
      const tags = { phase: phase(), endpoint, name: op.name };
      const params = { tags, timeout: '10s', headers: { 'Content-Type': 'application/json' } };
      if (token) params.headers.Authorization = `Bearer ${token}`;
      let response, bodyValid;
      metrics.sent.add(1, tags);
      if (endpoint === 'search') {
        const k = keyword();
        response = http.get(`${baseUrl}/api/products?search=${encodeURIComponent(k.keyword)}`, params);
        bodyValid = matchesIds(json(response), k.expectedIds);
      } else if (endpoint === 'detail') {
        const product = products[Math.floor(Math.random() * products.length)];
        response = http.get(`${baseUrl}/api/products/${product.id}`, params);
        const body = json(response);
        bodyValid = !!body && body.id === product.id && body.name === product.name && (typeof body.price === 'string' || typeof body.price === 'number') && Number.isFinite(Number(body.price)) && Number(body.price) > 0;
      } else if (endpoint === 'cart') {
        const product = products[Math.floor(Math.random() * products.length)];
        response = http.post(`${baseUrl}/api/cart`, JSON.stringify({ ...product, quantity: 1 }), params);
        const body = json(response);
        bodyValid = !!body && body.message === 'Added to cart';
      } else {
        response = http.post(`${baseUrl}/api/checkout`, JSON.stringify({ total_amount: 30000000, shipping_address: '123 Le Loi, TP.HCM' }), params);
        const body = json(response);
        bodyValid = !!body && Number.isInteger(body.orderId) && body.orderId > 0;
      }
      success = valid(response, bodyValid, tags);
      metrics.succeeded.add(success ? 1 : 0, tags); // Request-start phase.
    }
    // A failed login counts once as a failed Cart/Checkout attempt, even when no protected HTTP request is sent.
    metrics.requestsFailed.add(success ? 0 : 1, startTags);
    metrics.failed.add(!success, startTags);
    metrics.operationsSucceeded.add(success ? 1 : 0, { phase: phase(), endpoint }); // Completion phase.
    sleep(op.min + Math.random() * (op.max - op.min));
    metrics.completed.add(1, startTags);
  };
}
