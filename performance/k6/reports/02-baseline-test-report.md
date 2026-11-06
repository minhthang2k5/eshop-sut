# Baseline Test Report — eShop

## 1. Lần đo và nguồn dữ liệu

| Trường | Giá trị |
|---|---|
| Run ID | `baseline-20261106-180216-cXQggA` |
| Ngày / múi giờ | 06/11/2026, UTC+07:00 |
| Scenario bắt đầu | 2026-11-06T18:02:46+07:00 |
| k6 bắt đầu / kết thúc | 2026-11-06T18:02:46+07:00 / 2026-11-06T18:09:50+07:00 |
| Thời lượng tiến trình k6 | 423.959 s |
| Interrupted (timeline) | False |
| Telemetry backend | `server-backend-28062-1793962904877.jsonl` |
| Phiên bản/build/máy chạy | Không được xác nhận trong bộ kết quả; chưa có checksum build và snapshot DB |

Nguồn: [summary.json](../output/baseline-20261106-180216-cXQggA/summary.json), [timeline](../output/baseline-20261106-180216-cXQggA/measurement-timeline.json), [biểu đồ K6](../output/baseline-20261106-180216-cXQggA/baseline_report.html), [CPU/RAM JSONL](../output/telemetry/server-backend-28062-1793962904877.jsonl), [biểu đồ CPU/RAM](../output/telemetry/server-backend-28062-1793962904877.html). `telemetry/` chứa bộ thu; dữ liệu đo nằm ở `output/telemetry/`.

## 2. Mục tiêu, workload và cách đánh giá

Đánh giá tải thông thường tại 50 VUs.

Mix Search/Detail/Cart/Checkout = 55/25/14/6%. Theo script hiện có, mỗi iteration chọn một nghiệp vụ; Cart/Checkout login riêng trước mỗi thao tác. Think time Search/Detail/Cart/Checkout lần lượt 1–3/2–5/1–3/3–6 giây; timeout HTTP 10 giây. Đây là closed model `ramping-vus`; VU mục tiêu không tương đương số request/giây. Cấu hình mã hiện tại dùng để giải thích workload, không thay thế bằng chứng build tại thời điểm đo.

Ngưỡng trong summary cho từng steady/hold/recovery: p95 <500 ms, HTTP lỗi <1%, checks ≥99%, request count >0 cho tổng và từng API login/search/detail/cart/checkout; business_operations_failed <1% cho tổng phase. Đánh giá trực tiếp giá trị đo và đối chiếu cờ threshold: định dạng summary này dùng `true` cho vi phạm, `false` cho đạt. Skipped là chỉ số chẩn đoán, không có threshold riêng.

## 3. Profile thực đo

| Phase | VU target | Giây | Khoảng từ scenario start (s) |
|---|---|---|---|
| ramp_up | 50 | 60 | 0.000–60.000 |
| steady | 50 | 300 | 60.000–360.000 |
| ramp_down | 0 | 60 | 360.000–420.000 |

## 4. Kết quả K6

### 4.1 Toàn bài (gồm ramp và grace)

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | 8,655.000 |
| HTTP RPS toàn bài | 20.451 |
| Iterations hoàn tất | 7,155.000 |
| VU max quan sát | 50.000 |
| Latency avg (ms) | 2.261 |
| Latency median (ms) | 1.883 |
| Latency p95 (ms) | 4.769 |
| Latency p99 (ms) | 11.915 |
| Latency max (ms) | 41.111 |
| HTTP request lỗi | 0.000 |
| Checks thất bại | 0.000 |
| Nghiệp vụ skipped | 0.000 |
| HTTP lỗi (%) | 0.000 |
| Checks đạt (%) | 100.000 |
| Nghiệp vụ thất bại (%) | 0.000 |
| Threshold đạt / tổng | 25 / 25 |
| Kết luận theo thresholds | PASS |

`http_req_failed.passes` đếm mẫu lỗi, còn `checks.passes` đếm check thành công. Hai check/request không có nghĩa số check lỗi bằng số HTTP lỗi. HTTP requests bao gồm login.

### 4.2 Theo cửa sổ đánh giá

| Phase | VU target | Requests | RPS¹ | p95 ms | p99 ms | HTTP lỗi % | Checks % | Nghiệp vụ lỗi % | Kết quả² |
|---|---|---|---|---|---|---|---|---|---|
| steady | 50 | 7141 | 23.803 | 4.675 | 11.878 | 0.000 | 100.000 | 0.000 | PASS |

¹ Count chia thời lượng phase danh định trong timeline; không dùng rate submetric vì mẫu số có thể là toàn run. Phase gắn khi request bắt đầu; đây không phải completion throughput thuần. ² Kết quả xét cả từng API và business_operations_failed, không chỉ hàng tổng. Không cộng hoặc lấy trung bình các percentile.

### 4.3 Chi tiết từng API

| Phase | API | Requests | p95 ms | HTTP lỗi % | Checks % |
|---|---|---|---|---|---|
| steady | login | 1228 | 4.157 | 0.000 | 100.000 |
| steady | search | 3250 | 3.054 | 0.000 | 100.000 |
| steady | detail | 1435 | 2.686 | 0.000 | 100.000 |
| steady | cart | 845 | 1.590 | 0.000 | 100.000 |
| steady | checkout | 383 | 13.249 | 0.000 | 100.000 |

### 4.4 Điều kiện vi phạm

Không có threshold vi phạm trong summary.

## 5. CPU và RAM của tiến trình backend

CPU 100% tương đương một core; RAM là RSS MiB, không phải RAM toàn máy hay heap. TB là trung bình mẫu, không có trọng số thời gian. Chia cửa sổ theo timestamp timeline [bắt đầu, kết thúc); trong k6 có setup và grace. Không dùng mốc 30/60 giây tính từ đầu/cuối file telemetry vì file có thể chứa dữ liệu ngoài run.

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| Trước k6 | 30.011 | 30 | 0.035 | 0.052 | 67.730 | 67.730 | 67.730 | 67.730 | 1.002 |
| Trong k6 | 423.959 | 424 | 3.760 | 11.893 | 74.900 | 80.270 | 69.223 | 75.629 | 1.007 |
| Sau k6 | 60.028 | 60 | 0.112 | 3.831 | 72.559 | 75.629 | 75.629 | 65.934 | 1.002 |

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| ramp_up | 60.000 | 60 | 2.801 | 8.043 | 73.350 | 76.328 | 69.223 | 76.328 | 1.002 |
| steady | 300.000 | 300 | 4.253 | 11.893 | 75.093 | 80.270 | 76.828 | 74.418 | 1.002 |
| ramp_down | 60.000 | 60 | 2.499 | 6.159 | 75.436 | 75.629 | 74.418 | 75.629 | 1.007 |

Mẫu tại đầu/cuối là mẫu đầu/cuối có trong cửa sổ. Khoảng trễ lấy mẫu có thể bỏ sót đỉnh CPU/RAM; không nội suy phần thiếu. Không có telemetry của DB, k6, disk I/O, event-loop lag hay CPU từng core trong bảng này.

## 7. Nhận xét và kết luận

**PASS: 25/25 thresholds đạt.** Các cửa sổ đánh giá và từng API đều đạt ngưỡng đã cấu hình. 

Không suy ra nguyên nhân nghẽn, crash hoặc loại mã lỗi HTTP từ summary và CPU/RSS. Cần log backend, DB latency/locks và event-loop lag để xác minh nguyên nhân. Dùng lần đo này làm mốc đối chiếu; chạy lặp cùng môi trường/dữ liệu trước khi dùng kết quả làm cam kết năng lực.
