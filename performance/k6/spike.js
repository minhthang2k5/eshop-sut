import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { Counter } from 'k6/metrics';
import exec from 'k6/execution';

const BASE_URL = __ENV.BASE_URL || 'http://100.91.155.71:3000'.replace(/\/$/, '');
// This fixture uses four unquoted columns; reject malformed input before sending load.
const accounts = new SharedArray('spike accounts', () => {
  const lines = open('./data/test_accounts.csv').replace(/^\uFEFF/, '').trim().split(/\r?\n/);
  if (lines.shift() !== 'email,password,name,role') throw new Error('Invalid accounts CSV header');
  const rows = lines.map((line, index) => {
    const fields = line.split(',');
    if (fields.length !== 4 || fields.some((value) => !value.trim() || value.includes('"'))) {
      throw new Error(`Invalid accounts CSV row ${index + 2}: expected four nonempty unquoted fields`);
    }
    return { email: fields[0].trim(), password: fields[1] };
  });
  if (rows.length !== 50 || new Set(rows.map((row) => row.email)).size !== 50) {
    throw new Error('Spike requires exactly 50 unique accounts');
  }
  return rows;
});

// Module state is isolated per VU; never return or share JWTs through setup().
let authToken = null;
const skippedRequests = new Counter('business_requests_skipped');
const endpoints = ['search', 'detail', 'cart', 'checkout'];
// One source of truth for both executor stages and request-start phase tags.
const profile = [
  { duration: '30s', seconds: 30, target: 50, phase: 'hold_50' },
  { duration: '0s', seconds: 0, target: 500, phase: 'burst' },
  { duration: '1m', seconds: 60, target: 500, phase: 'hold_500' },
  { duration: '0s', seconds: 0, target: 50, phase: 'unload' },
  { duration: '1m', seconds: 60, target: 50, phase: 'recovery_1' },
];
// End the scenario after recovery; gracefulStop lets in-flight work finish.

const thresholds = {};
// Failed thresholds identify degradation; never abort before observing recovery.
for (const stage of profile.filter((s) => /^(hold_|recovery_)/.test(s.phase))) {
  for (const endpoint of [null, ...endpoints]) {
    const filter = `phase:${stage.phase}${endpoint ? `,endpoint:${endpoint}` : ''}`;
    thresholds[`http_req_duration{${filter}}`] = ['p(95)<500'];
    thresholds[`http_req_failed{${filter}}`] = ['rate<0.01'];
    thresholds[`checks{${filter}}`] = ['rate>=0.99'];
    // Empty windows must not count as evidence of a healthy system.
    thresholds[`http_reqs{${filter}}`] = ['count>0'];
  }
  thresholds[`business_requests_skipped{phase:${stage.phase}}`] = ['count==0'];
}
// Lazy Login is extra traffic; expose its results separately.
for (const metric of ['http_req_duration', 'http_req_failed', 'checks', 'http_reqs']) {
  thresholds[`${metric}{endpoint:login}`] = [];
}

export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-vus',
      startVUs: 50,
      stages: profile.map(({ duration, target }) => ({ duration, target })),
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
  const account = accounts[(exec.vu.idInTest - 1) % accounts.length];
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
  // Select one business operation per iteration. Lazy Login is additional traffic;
  // it does not participate in the 40/20/22/18 selection probabilities.
  const r = Math.random();
  let endpoint;
  let name;
  let response;
  let body;
  let minThink;
  let maxThink;
  let validBody;
  if (r < 0.40) {
    endpoint = 'search'; name = 'GET /api/products?search';
    minThink = 1; maxThink = 3;
  } else if (r < 0.60) {
    endpoint = 'detail'; name = 'GET /api/products/:id';
    minThink = 2; maxThink = 5;
  } else if (r < 0.82) {
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
  skippedRequests.add(0, { phase: phase(), endpoint });
  // Recompute phase AFTER Login, which may cross a stage boundary.
  const tags = { phase: phase(), endpoint, name };
  const params = { tags, timeout: '10s', headers: {
    'Content-Type': 'application/json',
  } };
  if (needsAuth) params.headers.Authorization = `Bearer ${authToken}`;
  if (endpoint === 'search') {
    response = http.get(`${BASE_URL}/api/products?search=iPhone`, params);
    body = jsonBody(response);
    validBody = Array.isArray(body) && body.length > 0;
  } else if (endpoint === 'detail') {
    response = http.get(`${BASE_URL}/api/products/1`, params);
    body = jsonBody(response);
    validBody = !!body && body.id === 1;
  } else if (endpoint === 'cart') {
    response = http.post(`${BASE_URL}/api/cart`, JSON.stringify({
      id: 1, name: 'iPhone 15 Pro Max', price: 30000000, quantity: 1,
    }), params);
    body = jsonBody(response);
    validBody = !!body && body.message === 'Added to cart';
  } else {
    // Current SUT creates orders independently of cart contents.
    response = http.post(`${BASE_URL}/api/checkout`, JSON.stringify({
      total_amount: 30000000, shipping_address: '123 Le Loi, TP.HCM',
    }), params);
    body = jsonBody(response);
    validBody = !!body && Number.isInteger(body.orderId) && body.orderId > 0;
  }
  // Retry authentication on the NEXT protected iteration after rejection.
  // Do not retry writes: a timed-out checkout may already have created an order.
  if (needsAuth && response.status === 401) authToken = null;
  check(response, {
    [`${endpoint}: status is 200`]: (res) => res.status === 200,
    [`${endpoint}: valid response body`]: () => validBody,
  }, tags);
  // Sleep after every request, including failures, to preserve pacing.
  sleep(minThink + Math.random() * (maxThink - minThink));
}
