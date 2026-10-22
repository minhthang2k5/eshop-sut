import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export default function () {
  // Cố ý sai endpoint và sai field token để minh họa audit.
  const loginRes = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
    email: 'test@eshop.com',
    password: 'Test1234!'
  }), { headers: { 'Content-Type': 'application/json' } });

  check(loginRes, { 'login status is 200': (response) => response.status === 200 });
  const token = loginRes.json('accessToken');

  const checkoutRes = http.post(`${BASE_URL}/api/checkout`, JSON.stringify({
    total_amount: 30000000,
    shipping_address: '42 Nguyen Hue'
  }), { headers: { 'Content-Type': 'application/json', token } });

  check(checkoutRes, { 'checkout status is 200': (response) => response.status === 200 });
  sleep(1);
}
