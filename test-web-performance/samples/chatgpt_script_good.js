import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    http_req_duration: ['p(95)<500'],
    checks: ['rate>=0.99']
  }
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const KEYWORDS = ['iPhone', 'Samsung', 'MacBook', 'AirPods', 'Keychron'];

export default function () {
  const loginRes = http.post(`${BASE_URL}/api/login`, JSON.stringify({
    email: 'test@eshop.com',
    password: 'Test1234!'
  }), { headers: { 'Content-Type': 'application/json' } });

  check(loginRes, {
    'login status is 200': (response) => response.status === 200,
    'login token exists': (response) => Boolean(response.json('token'))
  });

  const token = loginRes.json('token');
  if (!token) return;

  const action = Math.random();
  const keyword = KEYWORDS[Math.floor(Math.random() * KEYWORDS.length)];
  const productId = Math.floor(Math.random() * 5) + 1;

  if (action < 0.55) {
    const searchRes = http.get(`${BASE_URL}/api/products?search=${encodeURIComponent(keyword)}`);
    check(searchRes, { 'search status is 200': (response) => response.status === 200 });
    sleep(1 + Math.random() * 2);
  } else if (action < 0.80) {
    const detailRes = http.get(`${BASE_URL}/api/products/${productId}`);
    check(detailRes, { 'detail status is 200': (response) => response.status === 200 });
    sleep(2 + Math.random() * 3);
  } else {
    const checkoutRes = http.post(`${BASE_URL}/api/checkout`, JSON.stringify({
      total_amount: 30000000,
      shipping_address: '42 Nguyen Hue, Quan 1, Ho Chi Minh City'
    }), { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } });
    check(checkoutRes, {
      'checkout status is 200': (response) => response.status === 200,
      'checkout orderId exists': (response) => Boolean(response.json('orderId'))
    });
    sleep(3 + Math.random() * 3);
  }
}
