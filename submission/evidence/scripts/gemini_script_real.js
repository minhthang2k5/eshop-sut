import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    http_req_duration: ['p(95)<500'],
    checks: ['rate>=0.99'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const EMAIL = __ENV.EMAIL || 'test@eshop.com';
const PASSWORD = __ENV.PASSWORD || 'Test1234!';

const SEARCH_KEYWORDS = ['iPhone', 'Samsung', 'MacBook', 'AirPods', 'Keychron'];

function parseJSON(response) {
  if (!response || !response.body) {
    return null;
  }
  try {
    return JSON.parse(response.body);
  } catch (e) {
    return null;
  }
}

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomFloat(min, max) {
  return Math.random() * (max - min) + min;
}

export default function () {
  // 1. Login
  const loginPayload = JSON.stringify({
    email: EMAIL,
    password: PASSWORD,
  });

  const loginParams = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const loginRes = http.post(`${BASE_URL}/api/login`, loginPayload, loginParams);
  const loginJson = parseJSON(loginRes);

  const loginSuccess = check(loginRes, {
    'login status is 200': (r) => r.status === 200,
    'login token exists': () => loginJson !== null && typeof loginJson.token === 'string' && loginJson.token.length > 0,
  });

  if (!loginSuccess || !loginJson || !loginJson.token) {
    return;
  }

  const token = loginJson.token;

  // 2. Branch selection
  const rand = Math.random();

  if (rand < 0.55) {
    // Search (55%)
    const keyword = getRandomElement(SEARCH_KEYWORDS);
    const encodedKeyword = encodeURIComponent(keyword);

    const searchRes = http.get(`${BASE_URL}/api/products?search=${encodedKeyword}`);

    check(searchRes, {
      'search status is 200': (r) => r.status === 200,
    });

    sleep(getRandomFloat(1, 3));
  } else if (rand < 0.80) {
    // Detail (25%)
    const productId = getRandomInt(1, 5);

    const detailRes = http.get(`${BASE_URL}/api/products/${productId}`);

    check(detailRes, {
      'product detail status is 200': (r) => r.status === 200,
    });

    sleep(getRandomFloat(2, 5));
  } else {
    // Checkout (20%)
    const checkoutPayload = JSON.stringify({
      total_amount: 30000000,
      shipping_address: '123 Le Loi, TP.HCM',
    });

    const checkoutParams = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    };

    const checkoutRes = http.post(`${BASE_URL}/api/checkout`, checkoutPayload, checkoutParams);
    const checkoutJson = parseJSON(checkoutRes);

    check(checkoutRes, {
      'checkout status is 200': (r) => r.status === 200,
      'checkout orderId exists': () => checkoutJson !== null && checkoutJson.orderId !== undefined && checkoutJson.orderId !== null,
    });

    sleep(getRandomFloat(3, 6));
  }
}