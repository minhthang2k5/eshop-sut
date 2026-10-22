# k6 — EShop API Performance Testing

## Phạm vi API

| API | Kiểm tra chính |
|---|---|
| `POST /api/login` | HTTP 200, trích xuất `response.token` |
| `GET /api/products?search=iPhone` | HTTP 200, mảng sản phẩm không rỗng |
| `GET /api/products/1` | HTTP 200, đúng ID 1 |
| `POST /api/cart` | Bearer token; body `id, name, price, quantity`; message `Added to cart` |
| `POST /api/checkout` | Bearer token; body `total_amount, shipping_address`; có `orderId` |

## Cách chạy

Cần Node.js, dependencies backend và k6 trong `PATH`. Từ thư mục `eshop-sut`, khởi động backend:

```bash
cd backend
npm install
node server.js
```

Ở terminal khác, từ `eshop-sut` seed 50 tài khoản **sau khi backend khởi động xong**, rồi chạy từng bài:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-smoke.sh
bash performance/k6/run-baseline.sh
bash performance/k6/run-stress.sh
bash performance/k6/run-spike.sh
```

Smoke dùng `test@eshop.com / Test1234!`; các bài khác dùng `data/test_accounts.csv` và token riêng từng VU. Backend khởi tạo lại bảng khi start; cần seed lại sau mỗi lần restart. Chạy tuần tự, giữ trạng thái dữ liệu tương đương khi đối chiếu.

Mặc định `BASE_URL=http://localhost:3000`; có thể đổi:

```bash
BASE_URL=http://localhost:3000 bash performance/k6/run-baseline.sh
```

Mỗi runner tạo `output/<loại>-<timestamp>-<suffix>/` chứa `metrics.json`, `summary.json`, `k6.log` và giữ exit code k6. Baseline xuất thêm `baseline_report.html` bằng web-dashboard ở lần chạy mới. Exit code 99 là vi phạm threshold, chưa đủ kết luận server crash.

## Profile và thresholds hiện tại

| Test | Profile trong script | Thresholds |
|---|---|---|
| Smoke | 1 VU × 1 iteration, tuần tự 5 API | p95 < 500 ms; checks = 100% toàn bài |
| Baseline | Ramp 0→50: 1m; giữ 50: 5m; hạ tải: 1m | Steady tổng + từng API nghiệp vụ, và Login toàn bài: p95 < 500 ms, HTTP lỗi < 1%, checks ≥ 99%, requests > 0; skipped = 0 toàn bài |
| Stress | 500/750/1000/1250/1300/1350/1400/1500 VUs; ramp 30s + giữ 2m/bậc; recovery 50 VUs: 1m (tổng 21m) | Mỗi plateau/recovery, tổng + từng API nghiệp vụ: p95 < 500 ms, HTTP lỗi < 1%, checks ≥ 99%, requests > 0; skipped = 0 mỗi phase |
| Spike | 50 VUs: 30s → 1500: 60s → 50: 60s, chuyển tức thời (tổng 2m30s) | Mỗi phase, tổng + từng API nghiệp vụ: p95 < 500 ms, HTTP lỗi < 1%, checks ≥ 99%, requests > 0; skipped = 0 mỗi phase |

Baseline mix Search/Detail/Cart/Checkout = **55/25/14/6**; stress/spike = **40/20/22/18**. Login là lưu lượng bổ sung. Stress/spike chỉ thống kê Login riêng, không đặt SLO riêng; không ngắt sớm khi threshold fail để đo recovery. Grace period có thể kéo dài thời gian thực chạy.

## Kết quả Tuần 2

Dùng kết quả đã đo ngày 21–22/10, không chạy lại tải. Stress report dùng profile cũ **500–2800 VUs, giữ 60s/bậc**, khác script hiện tại. Profile thực đo của stress/spike khác kế hoạch Tuần 2 và được giữ nguyên khi tổng kết.

- [D2 — baseline](reports/02-baseline-test-report.md): PASS; steady p50/p95/p99 = 2,034/8,122/14,546 ms; lỗi 0%.
- [D3 — đối chiếu k6/JMeter](../jmeter/comparison_d2_vs_d3.md): cả hai đạt SLO; workload/môi trường khác nhau.
- [D4 — stress](reports/03-stress-test-report.md): bậc vi phạm đầu tiên 1500 VUs; recovery đạt trong 60s.
- [D4 — spike](reports/04-spike-test-report.md): đỉnh 1500 VUs vi phạm SLO; recovery đạt trong 60s.
- [Tổng kết và deliverables Tuần 2](../../docs/Week2_Summary.md).
