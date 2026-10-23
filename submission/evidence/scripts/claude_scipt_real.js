import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const EMAIL = __ENV.EMAIL || 'test@eshop.com';
const PASSWORD = __ENV.PASSWORD || 'Test1234!';

const KEYWORDS = ['iPhone', 'Samsung', 'MacBook', 'AirPods', 'Keychron'];

const SEARCH_PROBABILITY = 0.55;
const DETAIL_PROBABILITY = 0.25;
// Phần còn lại (0.20) là nhánh Checkout.

export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    http_req_duration: ['p(95)<500'],
    checks: ['rate>=0.99'],
    http_req_failed: ['rate<0.01'],
  },
};

// ---------- Helpers ----------

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomBetween(min, max) {
  return min + Math.random() * (max - min);
}

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Parse JSON an toàn: trả về null nếu body rỗng hoặc JSON không hợp lệ.
function safeJson(res) {
  if (!res || res.body === null || res.body === undefined || res.body === '') {
    return null;
  }
  try {
    return JSON.parse(res.body);
  } catch (e) {
    return null;
  }
}

function hasValue(v) {
  return v !== null && v !== undefined && v !== '';
}

// ---------- Các bước nghiệp vụ ----------

function login() {
  const res = http.post(
    `${BASE_URL}/api/login`,
    JSON.stringify({ email: EMAIL, password: PASSWORD }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'POST /api/login' },
    }
  );

  const body = safeJson(res);

  const ok = check(res, {
    'login: status is 200': (r) => r.status === 200,
    'login: response is valid JSON': () => body !== null && typeof body === 'object',
    'login: token exists': () =>
      body !== null && typeof body.token === 'string' && body.token.length > 0,
  });

  if (!ok || body === null || typeof body.token !== 'string' || body.token.length === 0) {
    return null;
  }
  return body.token;
}

function searchProducts() {
  const keyword = randomItem(KEYWORDS);
  const res = http.get(
    `${BASE_URL}/api/products?search=${encodeURIComponent(keyword)}`,
    { tags: { name: 'GET /api/products?search' } }
  );

  check(res, {
    'search: status is 200': (r) => r.status === 200,
  });

  sleep(randomBetween(1, 3));
}

function productDetail() {
  const id = randomInt(1, 5);
  const res = http.get(`${BASE_URL}/api/products/${id}`, {
    tags: { name: 'GET /api/products/:id' },
  });

  check(res, {
    'detail: status is 200': (r) => r.status === 200,
  });

  sleep(randomBetween(2, 5));
}

function checkout(token) {
  const payload = {
    total_amount: 30000000,
    shipping_address: '123 Le Loi, TP.HCM',
  };

  const res = http.post(`${BASE_URL}/api/checkout`, JSON.stringify(payload), {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    tags: { name: 'POST /api/checkout' },
  });

  const body = safeJson(res);

  check(res, {
    'checkout: status is 200': (r) => r.status === 200,
    'checkout: response is valid JSON': () => body !== null && typeof body === 'object',
    'checkout: orderId exists': () => body !== null && hasValue(body.orderId),
  });

  sleep(randomBetween(3, 6));
}

// ---------- Kịch bản chính ----------

export default function () {
  const token = login();

  // Login thất bại: dừng iteration, không gửi checkout.
  if (token === null) {
    return;
  }

  const r = Math.random();

  if (r < SEARCH_PROBABILITY) {
    searchProducts();
  } else if (r < SEARCH_PROBABILITY + DETAIL_PROBABILITY) {
    productDetail();
  } else {
    checkout(token);
  }
}