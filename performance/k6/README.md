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
| Stress | 500/750/1000/1250/1500/1750/2000/2200/2400/2600/2800 VUs; ramp 30s + giữ 60s/bậc; recovery 50 VUs: 60s (tổng 17m30s) | Mỗi plateau/recovery, tổng + từng API nghiệp vụ: p95 < 500 ms, HTTP lỗi < 1%, checks ≥ 99%, requests > 0; skipped = 0 mỗi phase |
| Spike | 50 VUs: 30s → 1500: 60s → 50: 60s, chuyển tức thời (tổng 2m30s) | Mỗi phase, tổng + từng API nghiệp vụ: p95 < 500 ms, HTTP lỗi < 1%, checks ≥ 99%, requests > 0; skipped = 0 mỗi phase |

Baseline mix Search/Detail/Cart/Checkout = **55/25/14/6**; stress/spike = **40/20/22/18**. Login là lưu lượng bổ sung. Stress/spike chỉ thống kê Login riêng, không đặt SLO riêng; không ngắt sớm khi threshold fail để đo recovery. Grace period có thể kéo dài thời gian thực chạy.

## D8a — SQLite index + WAL

`tuned-backend/` sao chép mã nguồn, dependencies và CSV seed của `backend/`. Hai server đều dùng `require("./database")`: bản gốc mở `backend/database.sqlite`; bản tune mở `tuned-backend/database_tuned.sqlite`. Đường dẫn tính theo `__dirname`, không phụ thuộc thư mục chạy lệnh; không cần `DB_MODE` hay `database-tune.js`.

Từ `eshop-sut`, dừng backend gốc rồi chạy bản tune (cùng cổng 3000):

```bash
cd tuned-backend
npm ci
node server.js
```

`tuned-backend/database.js` reset/seed như bản gốc, sau đó trực tiếp bật `PRAGMA journal_mode=WAL` và tạo `idx_products_name ON products(name)`. Index được tạo lại sau mỗi restart. Ở terminal khác, từ `eshop-sut` seed tài khoản k6 vào đúng bản tune rồi chạy:

```bash
node performance/k6/data/seed.js tuned-backend/database_tuned.sqlite
bash performance/k6/run-baseline.sh
bash performance/k6/run-spike.sh
bash performance/k6/run-stress.sh
```

Khi đối chiếu, chạy lần lượt hai backend với dữ liệu khởi đầu tương đương. Đã có kết quả baseline, spike và stress sau tune ngày 23/10/2026; xem bảng run bên dưới. Cấu hình được mô tả theo source hiện tại và ghi nhận người thực hiện; chưa lưu PRAGMA/index thực tế hoặc snapshot build/DB gắn với thời điểm chạy.

`LIKE '%keyword%'` vẫn full-scan dù có index. WAL cho phép đọc song song với ghi nhưng vẫn chỉ có một writer; SUT dùng chung một connection nên cần đo mức cải thiện thực tế. Xem [giải thích WAL](tune-db/WAL.md).

## Kết quả thực đo ngày 22–23/10/2026

Bảng dưới dùng đúng profile của run đã lưu, không chạy lại tải để biên soạn báo cáo. Profile stress thực đo và script hiện tại đều có 11 bậc 500–2800 VUs, ramp 30s và giữ 60s/bậc. Mô tả cũ 500–1500 VUs/hold 2 phút không áp dụng cho các run này. Baseline dùng mix 55/25/14/6; stress/spike 40/20/22/18. Không thực hiện soak; `reports/05-soak-test-report.md` chỉ là template.

| Loại / cấu hình | Run ID | Cửa sổ và kết quả | Report |
| --- | --- | --- | --- |
| Smoke | `smoke-20261022-195537-4es3Xy` | 1 VU × 1 iteration; 5 requests, 10/10 checks; p95 47.895 ms; 2/2 thresholds đạt | [Summary](output/smoke-20261022-195537-4es3Xy/summary.json) |
| Baseline trước | `baseline-20261022-110446-eGLTX1` | Steady 50 VUs/300s, p95 8.122 ms; lỗi 0%; PASS 25/25 | [Report 02](reports/02-baseline-test-report.md) |
| Stress trước | `stress-20261022-181718-lx8F4c` | 11 bậc/hold 60s; fail đầu 1500, còn fail 2200/2600/2800; recovery đạt; FAIL 201/252 | [Report 03](reports/03-stress-test-report.md) |
| Spike trước | `spike-20261022-190641-UgVeF4` | 50/1500/50 VUs trong 30/60/60s; p95 đỉnh 5344.455 ms, lỗi 1.486%; recovery đạt; FAIL 47/63 | [Report 04](reports/04-spike-test-report.md) |
| Baseline sau | `baseline-20261023-084311-TSxg2P` | Cùng profile baseline; p95 steady 6.328 ms, lỗi 0%; PASS 25/25 | [Report 06](reports/06-tuned-baseline-test-report.md) |
| Spike sau | `spike-20261023-085706-BOOKoc` | Cùng profile spike; p95 đỉnh 6.849 ms, lỗi 0%; recovery đạt; PASS 63/63 | [Report 07](reports/07-tuned-spike-test-report.md) |
| Stress sau | `stress-20261023-090531-KgTWyh` | Cùng profile stress; 500–2600 đạt, 2800 fail p95 5288.187 ms; recovery đạt; FAIL 247/252 | [Report 08](reports/08-tuned-stress-test-report.md) |

Report smoke cũ dùng run ID chung `SMOKE_TEST` và p95 17.81 ms, không khớp summary đang lưu; dùng summary run cụ thể ở bảng này, không ghép số liệu/ghi chép tài nguyên cũ. Run smoke diễn ra sau các run tải cùng ngày, không chứng minh entry smoke trước các run đó.

Baseline lấy `phase:steady`, RPS = count/300s. Stress lấy từng plateau/recovery, RPS = count/60s; spike dùng 30/60/60s theo phase. Không dùng `rate` submetric toàn run làm RPS phase. Phase gắn theo lúc bắt đầu request. Trong summary export, `thresholds: true` là vi phạm; `false` là không vi phạm. `http_req_failed.passes` là số request lỗi, khác ý nghĩa checks.passes.

Sau tune, bậc fail đầu stress chuyển 1500 → 2800 và tổng lỗi giảm, nhưng p95 tại 2800 tăng từ 815.113 lên 5288.187 ms; không kết luận cải thiện đồng đều. Các kết quả là một lần đo mỗi loại/cấu hình, thiếu snapshot/build và telemetry đồng bộ; chưa chứng minh toàn bộ chênh lệch do WAL/index. Tài nguyên trong reports là quan sát thủ công toàn máy, không phải avg/max hoặc số riêng backend. Các cửa sổ recovery đạt trong 60s chưa xác định thời gian phục hồi chính xác hay hết backlog.

## Báo cáo seminar và evidence

- [Chương 4 báo cáo seminar](../../submission/Bao_cao_seminar_Performance_Testing.md#4-thực-nghiệm-k6-của-lê-nguyễn-quốc-thái): phương pháp, lệnh thực hành, dữ liệu/correlation/checks, kết quả và tuning.
- [Manifest evidence k6](../../submission/evidence/k6/README.md): bảy summary, bốn HTML tổng hợp và sáu hình. Bộ evidence này không kèm log hoặc raw metrics và không include dashboard baseline trong output.
- [HTML baseline trước tune](reports/baseline_report.html), [stress](reports/stress_report.html), [spike](reports/spike_report.html), [đối chiếu cả ba loại trước–sau](reports/tuned_baseline_report.html): biểu đồ tổng hợp từ kết quả đã lưu, không phải dashboard gốc.
- [Đối chiếu k6/JMeter](../jmeter/comparison_d2_vs_d3.md): đọc cùng khác biệt workload/môi trường, không xếp hạng công cụ chỉ từ RPS.
