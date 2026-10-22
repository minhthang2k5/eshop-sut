import http from 'k6/http';
import { check, group, sleep } from 'k6';

// Smoke test options: 1 VU chạy trong thời gian ngắn (1 iteration hoặc 30s-1m) để kiểm tra tính đúng đắn của script và luồng API
export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    // SLO: 100% check phải pass trong smoke test
    checks: ['rate==1.0'],
    // 95% số request phải có thời gian phản hồi dưới 500ms
    http_req_duration: ['p(95)<500'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://100.91.155.71:3000';

// Thông tin tài khoản mặc định theo yêu cầu
const CREDENTIALS = {
  email: 'test@eshop.com',
  password: 'Test1234!',
};

export default function () {
  let authToken = null;

  // -------------------------------------------------------------
  // 1. POST /api/login: Đăng nhập lấy JWT Bearer token
  // -------------------------------------------------------------
  group('1. Login API', () => {
    const loginPayload = JSON.stringify({
      email: CREDENTIALS.email,
      password: CREDENTIALS.password,
    });

    const loginParams = {
      headers: {
        'Content-Type': 'application/json',
      },
      tags: { name: 'POST /api/login' },
    };

    const loginRes = http.post(`${BASE_URL}/api/login`, loginPayload, loginParams);

    const loginSuccess = check(loginRes, {
      'login: status is 200': (r) => r.status === 200,
      'login: token exists': (r) => {
        try {
          const body = r.json();
          return body && typeof body.token === 'string' && body.token.length > 0;
        } catch (e) {
          return false;
        }
      },
    });

    if (loginSuccess) {
      authToken = loginRes.json('token');
    }
  });

  sleep(1);

  // -------------------------------------------------------------
  // 2. GET /api/products?search=iPhone: Tìm kiếm sản phẩm
  // -------------------------------------------------------------
  group('2. Search Products API', () => {
    const keyword = 'iPhone';
    const searchRes = http.get(`${BASE_URL}/api/products?search=${encodeURIComponent(keyword)}`, {
      tags: { name: 'GET /api/products?search' },
    });

    check(searchRes, {
      'search: status is 200': (r) => r.status === 200,
      'search: return array of products': (r) => {
        try {
          const body = r.json();
          return Array.isArray(body) && body.length > 0;
        } catch (e) {
          return false;
        }
      },
    });
  });

  sleep(1);

  // -------------------------------------------------------------
  // 3. GET /api/products/:id: Xem chi tiết sản phẩm (ID: 1)
  // -------------------------------------------------------------
  group('3. Product Detail API', () => {
    const productId = 1;
    const detailRes = http.get(`${BASE_URL}/api/products/${productId}`, {
      tags: { name: 'GET /api/products/:id' },
    });

    check(detailRes, {
      'detail: status is 200': (r) => r.status === 200,
      'detail: product has correct id': (r) => {
        try {
          const body = r.json();
          return body && body.id === productId;
        } catch (e) {
          return false;
        }
      },
    });
  });

  sleep(1);

  // -------------------------------------------------------------
  // 4. POST /api/cart: Thêm vào giỏ hàng (Cần Authorization Bearer)
  // -------------------------------------------------------------
  group('4. Add to Cart API', () => {
    const cartPayload = JSON.stringify({
      id: 1,
      name: 'iPhone 15 Pro Max',
      price: 30000000,
      quantity: 1,
    });

    const cartParams = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
      tags: { name: 'POST /api/cart' },
    };

    const cartRes = http.post(`${BASE_URL}/api/cart`, cartPayload, cartParams);

    check(cartRes, {
      'cart: status is 200': (r) => r.status === 200,
      'cart: message added to cart': (r) => {
        try {
          const body = r.json();
          return body && body.message === 'Added to cart';
        } catch (e) {
          return false;
        }
      },
    });
  });

  sleep(1);

  // -------------------------------------------------------------
  // 5. POST /api/checkout: Đặt hàng / Checkout (Cần Authorization Bearer)
  // -------------------------------------------------------------
  group('5. Checkout API', () => {
    const checkoutPayload = JSON.stringify({
      total_amount: 30000000,
      shipping_address: '123 Le Loi, TP.HCM',
    });

    const checkoutParams = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
      tags: { name: 'POST /api/checkout' },
    };

    const checkoutRes = http.post(`${BASE_URL}/api/checkout`, checkoutPayload, checkoutParams);

    check(checkoutRes, {
      'checkout: status is 200': (r) => r.status === 200,
      'checkout: orderId exists': (r) => {
        try {
          const body = r.json();
          return body && typeof body.orderId === 'number';
        } catch (e) {
          return false;
        }
      },
    });
  });

  sleep(1);
}
