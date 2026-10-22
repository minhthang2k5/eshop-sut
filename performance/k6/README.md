# Tổng quan nội dung triển khai

Phạm vi 5 API kiểm thử (khớp mục 2 của Proposal & server.js):

- `POST /api/login`: Đăng nhập với tài khoản test@eshop.com / Test1234!, kiểm tra HTTP status 200 và trích xuất JWT Bearer token (response.token).
- `GET /api/products?search=iPhone`: Tìm kiếm sản phẩm, kiểm tra status 200 và kết quả trả về mảng danh sách sản phẩm.
- `GET /api/products/:id` (/api/products/1): Xem chi tiết sản phẩm iPhone 15 Pro Max, kiểm tra status 200 và đúng id: 1.
- `POST /api/cart`: Thêm sản phẩm vào giỏ hàng với header Authorization: Bearer <token>, body gồm id, name, price, quantity. Kiểm tra response message "Added to cart".
- `POST /api/checkout`: Tạo đơn hàng với header Authorization: Bearer <token>, body gồm total_amount, shipping_address. Kiểm tra HTTP 200 và response có trường orderId.

## Cấu hình Smoke Test

- **Profile:** 1 VU chạy trong 30 giây (hoặc 1 iteration với think-time sleep(1) giữa các bước).
- **Thresholds:**
  - `checks: ['rate==1.0']` (100% checks thành công).
  - `http_req_duration: ['p(95)<500']` (SLO p95 < 500ms).
- Hỗ trợ biến môi trường `BASE_URL` (mặc định: http://localhost:3000).

## Run
- Run server
```
cd backend
npm install
node database.js
node server.js
```

- Download K6 and run
```
cd test
k6 run smoke.js
```
## Stress test (Black Friday)

Script [stress.js](stress.js) dùng mix Search/Detail/Cart/Checkout = 40/20/22/18,
think-time theo tài liệu, 50 tài khoản CSV phân bổ vòng tròn và lazy login riêng từng VU.
Profile 13 phút: bắt đầu ở 0 VUs, ramp-up 1 phút đến mỗi bậc 500/1000/2000/4000,
giữ mỗi bậc 2 phút; giảm trực tiếp về 50 VUs, giữ 1 phút đo phục hồi rồi kết thúc.

| Thời gian | VUs | Phase |
|---|---|---|
| 00:00–01:00 | 0→500 | ramp_500 |
| 01:00–03:00 | 500 | hold_500 |
| 03:00–04:00 | 500→1000 | ramp_1000 |
| 04:00–06:00 | 1000 | hold_1000 |
| 06:00–07:00 | 1000→2000 | ramp_2000 |
| 07:00–09:00 | 2000 | hold_2000 |
| 09:00–10:00 | 2000→4000 | ramp_4000 |
| 10:00–12:00 | 4000 | hold_4000 |
| 12:00–13:00 | 50 | recovery_1 |

50 tài khoản được dùng bởi tối đa 80 VUs/tài khoản ở đỉnh tải.
Recovery chỉ quan sát 1 phút; 30s đầu có thể còn iteration của VUs đang rút tải.
Đạt SLO trong cửa sổ này chưa chứng minh phục hồi bền vững; không đạt nghĩa là
chưa chứng minh phục hồi trong thời gian quan sát. Máy phát tải/server chung máy:
cần đối chiếu tài nguyên để phân biệt nghẽn k6 với nghẽn ứng dụng.

Cho phép tối đa 30s để iteration đang chạy hoàn tất khi giảm tải/kết thúc.

Khi môi trường sẵn sàng:

```bash
BASE_URL=http://localhost:3000 bash sut/eshop-sut/test/run-stress.sh
```

Kết quả ở `test/output/stress-<timestamp>-<suffix>/`: `metrics.json`, `summary.json`, `k6.log`.
Threshold theo từng bậc/API giúp phát hiện vi phạm SLO, không ngắt sớm bài đo recovery.
Exit code 99 có thể là vi phạm SLO dưới stress; không tự đồng nghĩa server crash.
Xem [kế hoạch và mẫu report](03-stress-test-report.md) để phân tích điểm gãy/phục hồi.
Kiểm tra cấu hình không phát tải: `k6 inspect --execution-requirements sut/eshop-sut/test/stress.js`.

500
memory: 4.73 GB / 7.39 GB · 64 %
swap: 2.28 GB / 8.59 GB · 27 %
CPU: 6~9%

1000
4.93 GB / 7.39 GB · 67 %
2.27 GB / 8.59 GB · 26 %
CPU: 8~12%

2000
4.85 GB / 7.39 GB · 66 %
2.27 GB / 8.59 GB · 26 %
CPU: 11~13~16%

4000
5.15 GB / 7.39 GB · 70 %
2.27 GB / 8.59 GB · 26 %
CPU: 12~17~19%