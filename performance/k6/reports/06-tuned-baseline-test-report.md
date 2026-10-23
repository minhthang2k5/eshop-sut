# Baseline Test Report – eShop sau tune database (D8a)

> **PASS — một lần đo**, run `baseline-20261023-084311-TSxg2P`. 25/25 thresholds đạt, đủ bốn API nghiệp vụ, không có HTTP lỗi hoặc request nghiệp vụ bị bỏ qua. Chưa đánh giá độ lặp lại.

## 1. Metadata và mục tiêu

| Trường | Giá trị |
|---|---|
| Thời gian | 23/10/2026, khoảng 08:43:11–08:50:12, UTC+07:00 |
| Run ID | `baseline-20261023-084311-TSxg2P` |
| Người thực hiện | Người dùng chạy test; chưa cung cấp tên |
| SUT | Tuned database theo người thực hiện; cấu trúc hiện tại là `tuned-backend/`, SQLite `database_tuned.sqlite` |
| Thay đổi dự kiến | `PRAGMA journal_mode=WAL`; index `idx_products_name ON products(name)` trong `tuned-backend/database.js` |
| Script | [baseline.js](../baseline.js), [runner](../run-baseline.sh) |
| Môi trường | Chưa lưu phiên bản k6/Node.js/SQLite, CPU model, source checksum hoặc snapshot DB kèm run |
| URL | Mặc định script `http://localhost:3000`; không có bản ghi biến môi trường để xác nhận override |
| Nguồn | [summary.json](../output/baseline-20261023-084311-TSxg2P/summary.json), [metrics.json](../output/baseline-20261023-084311-TSxg2P/metrics.json), [k6.log](../output/baseline-20261023-084311-TSxg2P/k6.log), [HTML dashboard](../output/baseline-20261023-084311-TSxg2P/baseline_report.html) |

Mục tiêu: xác nhận SLO ở tải baseline sau tune và đối chiếu ngắn với [baseline trước tune](02-baseline-test-report.md). Cấu hình WAL/index mô tả theo mã nguồn hiện tại và thông tin người thực hiện; bộ kết quả k6 không tự chứng minh PRAGMA/index thực tế tại thời điểm chạy.

## 2. Workload và điều kiện đánh giá

Closed workload, tối đa 50 VUs: ramp-up 1 phút, steady 50 VUs trong 5 phút, ramp-down 1 phút; grace period 30 giây. Mỗi iteration chọn một API nghiệp vụ, lazy login nếu cần token, kiểm tra status/body rồi sleep.

| API | Mix mục tiêu | Think time |
|---|---:|---|
| Search: GET /api/products?search=iPhone | 55% | 1–3 s |
| Detail: GET /api/products/1 | 25% | 2–5 s |
| Cart: POST /api/cart | 14% | 1–3 s |
| Checkout: POST /api/checkout | 6% | 3–6 s |

50 tài khoản CSV, token riêng từng VU; Login là lưu lượng bổ sung. Phạm vi không bao gồm browser rendering hay xác định tải tối đa. Không có snapshot/số orders ban đầu hoặc log smoke kèm run để xác nhận trạng thái dữ liệu ban đầu.

SLO: p95 <500 ms, HTTP lỗi <1%, checks ≥99%, count >0 cho tổng steady và từng API nghiệp vụ; cùng bộ ngưỡng cho Login toàn run. Request nghiệp vụ bị bỏ qua phải bằng 0. CPU/RAM không có threshold tự động.

## 3. Kết quả đo

Số liệu baseline lọc `phase:steady`, cửa sổ [60,360) s, mẫu số throughput **300 giây**; không dùng trường `rate` của summary cho RPS steady vì trường đó tính theo toàn run. p50 lấy từ `med`; latency tính bằng ms. Mẫu HTTP steady đầu/cuối ghi lúc 08:44:11.295 / 08:49:11.262; đây là thời điểm phát mẫu, không dùng khoảng cách hai mẫu để tính throughput.

### 3.1 Tổng quan steady

| Chỉ số | Kết quả |
|---|---:|
| HTTP requests gồm Login | 5942 |
| Throughput tổng | 19.807 requests/s |
| Requests nghiệp vụ / throughput | 5933 / 19.777 requests/s |
| Latency avg / p50 | 2.382 / 2.062 ms |
| p90 / p95 / p99 / max | 2.993 / 6.328 / 10.586 / 12.675 ms |
| HTTP lỗi | 0/5942 (0%) |
| Checks đạt | 11884/11884 (100%) |

### 3.2 Chi tiết API steady

| API | Count | Mix nghiệp vụ (%) | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | RPS | HTTP lỗi | Checks đạt |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Search | 3258 | 54.913 | 2.016 | 2.777 | 2.996 | 4.208 | 10.860 | 0% | 100% |
| Detail | 1480 | 24.945 | 1.975 | 2.714 | 2.904 | 3.930 | 4.933 | 0% | 100% |
| Cart | 829 | 13.973 | 1.988 | 2.602 | 2.768 | 3.344 | 2.763 | 0% | 100% |
| Checkout | 366 | 6.169 | 9.364 | 10.881 | 11.239 | 11.649 | 1.220 | 0% | 100% |
| Login | 9 | N/A | 2.421 | 3.655 | 3.731 | 3.791 | 0.030 | 0% | 100% |

Mix thực tế gần mục tiêu; tổng mix loại 9 Login steady. Login toàn run có 50 mẫu, p95 4.514 ms, HTTP lỗi 0%, checks 100%; 41 Login ngoài steady. Percentile Login steady chỉ dựa trên 9 mẫu nên độ tin cậy hạn chế.

### 3.3 Toàn run và lỗi

| Chỉ số | Kết quả |
|---|---:|
| Thời lượng theo log | 7 phút 01.0 giây |
| HTTP requests / iterations hoàn tất | 7192 / 7142 |
| Iterations bị ngắt / nghiệp vụ bị bỏ qua | 0 / 0 |
| Throughput toàn run | 17.082 requests/s |
| Latency avg / p50 / p90 / p95 / p99 / max (ms) | 2.411 / 2.094 / 3.054 / 6.158 / 10.625 / 32.563 |
| HTTP lỗi | 0/7192 |
| Checks đạt | 14384/14384 |
| Received / sent | 2994705 / 1227975 bytes |

Đối chiếu raw metrics: tất cả 7192 HTTP response có status 200; không ghi nhận 4xx/5xx, lỗi transport/timeout hoặc check thất bại. Chênh lệch HTTP requests và iterations là 50 Login bổ sung. Log đánh dấu đạt toàn bộ 25 thresholds; giá trị `false` trong bản export summary biểu thị threshold không bị vi phạm, không phải FAIL.

### 3.4 Tài nguyên

Nguồn: số liệu người thực hiện cung cấp cho lần baseline này; không có chuỗi thời gian hoặc thống kê riêng từng tiến trình.

| Chỉ số | Quan sát |
|---|---|
| CPU | 2–5% |
| Memory | 3.51 GB / 7.12 GB · 49% |
| Swap | 475.67 MB / 8.59 GB · 6% |
| Disk I/O, swap-in/out, RSS Node.js/k6 | Chưa thu thập |

Không diễn giải các giá trị quan sát thành avg/max hoặc khẳng định ổn định suốt run. Chưa có bằng chứng bão hòa CPU/RAM từ số liệu cung cấp; không đủ để kết luận về memory leak hay mức swap I/O.

## 4. So sánh ngắn trước/sau tune

Reference: `baseline-20261022-110446-eGLTX1` trong báo cáo trước; cùng cách tính steady 300 giây. Chênh lệch tính từ summary hai run, làm tròn khi trình bày.

| Chỉ số steady | Trước tune | Sau tune | Thay đổi |
|---|---:|---:|---:|
| p50 tổng (ms) | 2.034 | 2.062 | +1.37% |
| p95 tổng (ms) | 8.122 | 6.328 | -22.08% |
| p99 tổng (ms) | 14.546 | 10.586 | -27.22% |
| p95 Search (ms) | 3.071 | 2.996 | -2.44% |
| p95 Checkout (ms) | 16.006 | 11.239 | -29.78% |
| Throughput (requests/s) | 19.750 | 19.807 | +0.29% |
| HTTP lỗi / checks đạt | 0% / 100% | 0% / 100% | Không đổi |

p95 tổng giảm khoảng 22.09%, p95 Checkout giảm khoảng 29.78%; throughput gần như không đổi trong workload có think time. Kết quả phù hợp khả năng thay đổi chi phí ghi sau bật WAL, nhưng chưa chứng minh quan hệ nhân quả hoặc tách riêng đóng góp WAL/index. `LIKE '%keyword%'` vẫn full-scan dù có index; không quy mức giảm latency Search cho index này.

CPU quan sát trước là 4–7%, sau là 2–5%; RAM trước 3.20/7.39 GB (43–45%), sau 3.51/7.12 GB (49%); Swap trước 2.03/8.59 GB, sau 475.67 MB/8.59 GB. Tổng RAM được báo khác nhau và monitoring không đồng bộ, vì vậy không kết luận tune làm giảm CPU/Swap hoặc tăng RAM. Mỗi cấu hình mới có một lần đo, chưa lưu đầy đủ build/snapshot/môi trường; mix ngẫu nhiên và trạng thái hệ thống cũng có thể ảnh hưởng chênh lệch.

## 5. Kết luận

**PASS cho baseline sau tune trong một lần đo:** đủ workload bốn API, 25/25 thresholds đạt; p95 tổng steady 6.328 ms, cao nhất theo API là Checkout 11.239 ms, đều dưới 500 ms; HTTP lỗi 0%, checks 100%, không bỏ request hoặc ngắt iteration.

So với reference, latency đuôi tổng và Checkout thấp hơn trong lần đo này, throughput tương đương. Chưa có cơ sở khẳng định cải thiện có tính lặp lại hoặc kết quả ở tải spike; cần giữ điều kiện tương đương và lưu build, trạng thái DB, cấu hình WAL/index cùng monitoring khi đối chiếu tiếp.
