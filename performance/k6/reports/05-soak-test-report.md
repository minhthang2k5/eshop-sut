# Soak Test Report — eShop

## 1. Lần đo và nguồn dữ liệu

| Trường | Giá trị |
|---|---|
| Run ID | `soak-20261106-195208-BINgxV` |
| Ngày / múi giờ | 06/11/2026, UTC+07:00 |
| Scenario bắt đầu | 2026-11-06T19:52:39+07:00 |
| k6 bắt đầu / kết thúc | 2026-11-06T19:52:38+07:00 / 2026-11-06T20:09:44+07:00 |
| Thời lượng tiến trình k6 | 1,025.903 s |
| Interrupted (timeline) | False |
| Telemetry backend | `server-backend-98997-1793969508604.jsonl` |
| Phiên bản/build/máy chạy | Không được xác nhận trong bộ kết quả; chưa có checksum build và snapshot DB |

Nguồn: [summary.json](../output/soak-20261106-195208-BINgxV/summary.json), [timeline](../output/soak-20261106-195208-BINgxV/measurement-timeline.json), [biểu đồ K6](../output/soak-20261106-195208-BINgxV/soak_report.html), [CPU/RAM JSONL](../output/telemetry/server-backend-98997-1793969508604.jsonl), [biểu đồ CPU/RAM](../output/telemetry/server-backend-98997-1793969508604.html). `telemetry/` chứa bộ thu; dữ liệu đo nằm ở `output/telemetry/`.

## 2. Mục tiêu, workload và cách đánh giá

Đánh giá độ ổn định tại 400 VUs trong cửa sổ steady 15 phút.

Mix Search/Detail/Cart/Checkout = 55/25/14/6%. Theo script hiện có, mỗi iteration chọn một nghiệp vụ; Cart/Checkout login riêng trước mỗi thao tác. Think time Search/Detail/Cart/Checkout lần lượt 1–3/2–5/1–3/3–6 giây; timeout HTTP 10 giây. Đây là closed model `ramping-vus`; VU mục tiêu không tương đương số request/giây. Cấu hình mã hiện tại dùng để giải thích workload, không thay thế bằng chứng build tại thời điểm đo.

Ngưỡng trong summary cho từng steady/hold/recovery: p95 <500 ms, HTTP lỗi <1%, checks ≥99%, request count >0 cho tổng và từng API login/search/detail/cart/checkout; business_operations_failed <1% cho tổng phase. Đánh giá trực tiếp giá trị đo và đối chiếu cờ threshold: định dạng summary này dùng `true` cho vi phạm, `false` cho đạt. Skipped là chỉ số chẩn đoán, không có threshold riêng.

## 3. Profile thực đo

| Phase | VU target | Giây | Khoảng từ scenario start (s) |
|---|---|---|---|
| ramp_up | 400 | 60 | 0.000–60.000 |
| steady | 400 | 900 | 60.000–960.000 |
| ramp_down | 0 | 60 | 960.000–1,020.000 |

## 4. Kết quả K6

### 4.1 Toàn bài (gồm ramp và grace)

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | 182,070.000 |
| HTTP RPS toàn bài | 177.719 |
| Iterations hoàn tất | 151,763.000 |
| VU max quan sát | 400.000 |
| Latency avg (ms) | 5.873 |
| Latency median (ms) | 1.605 |
| Latency p95 (ms) | 10.381 |
| Latency p99 (ms) | 99.890 |
| Latency max (ms) | 900.059 |
| HTTP request lỗi | 2.000 |
| Checks thất bại | 4.000 |
| Nghiệp vụ skipped | 2.000 |
| HTTP lỗi (%) | 0.001 |
| Checks đạt (%) | 99.999 |
| Nghiệp vụ thất bại (%) | 0.001 |
| Threshold đạt / tổng | 25 / 25 |
| Kết luận theo thresholds | PASS |

`http_req_failed.passes` đếm mẫu lỗi, còn `checks.passes` đếm check thành công. Hai check/request không có nghĩa số check lỗi bằng số HTTP lỗi. HTTP requests bao gồm login.

### 4.2 Theo cửa sổ đánh giá

| Phase | VU target | Requests | RPS¹ | p95 ms | p99 ms | HTTP lỗi % | Checks % | Nghiệp vụ lỗi % | Kết quả² |
|---|---|---|---|---|---|---|---|---|---|
| steady | 400 | 170375 | 189.306 | 10.089 | 99.743 | 0.001 | 99.999 | 0.001 | PASS |

¹ Count chia thời lượng phase danh định trong timeline; không dùng rate submetric vì mẫu số có thể là toàn run. Phase gắn khi request bắt đầu; đây không phải completion throughput thuần. ² Kết quả xét cả từng API và business_operations_failed, không chỉ hàng tổng. Không cộng hoặc lấy trung bình các percentile.

### 4.3 Chi tiết từng API

| Phase | API | Requests | p95 ms | HTTP lỗi % | Checks % |
|---|---|---|---|---|---|
| steady | login | 28293 | 8.240 | 0.007 | 99.993 |
| steady | search | 78045 | 7.186 | 0.000 | 100.000 |
| steady | detail | 35745 | 7.019 | 0.000 | 100.000 |
| steady | cart | 19901 | 1.684 | 0.000 | 100.000 |
| steady | checkout | 8391 | 27.399 | 0.000 | 100.000 |

### 4.4 Điều kiện vi phạm

Không có threshold vi phạm trong summary.

## 5. CPU và RAM của tiến trình backend

CPU 100% tương đương một core; RAM là RSS MiB, không phải RAM toàn máy hay heap. TB là trung bình mẫu, không có trọng số thời gian. Chia cửa sổ theo timestamp timeline [bắt đầu, kết thúc); trong k6 có setup và grace. Không dùng mốc 30/60 giây tính từ đầu/cuối file telemetry vì file có thể chứa dữ liệu ngoài run.

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| Trước k6 | 30.026 | 30 | 0.049 | 0.084 | 66.270 | 66.270 | 66.270 | 66.270 | 1.002 |
| Trong k6 | 1,025.903 | 1026 | 22.205 | 42.757 | 111.365 | 169.965 | 66.270 | 115.246 | 1.164 |
| Sau k6 | 60.013 | 60 | 0.027 | 0.157 | 115.246 | 115.246 | 115.246 | 115.246 | 1.002 |

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| ramp_up | 60.000 | 60 | 17.726 | 33.589 | 95.245 | 137.812 | 67.531 | 137.812 | 1.002 |
| steady | 900.000 | 899 | 23.402 | 42.757 | 112.191 | 169.965 | 144.062 | 115.332 | 1.164 |
| ramp_down | 60.000 | 60 | 11.321 | 22.887 | 115.455 | 115.457 | 115.332 | 115.457 | 1.001 |

Mẫu tại đầu/cuối là mẫu đầu/cuối có trong cửa sổ. Khoảng trễ lấy mẫu có thể bỏ sót đỉnh CPU/RAM; không nội suy phần thiếu. Không có telemetry của DB, k6, disk I/O, event-loop lag hay CPU từng core trong bảng này.

## 7. Nhận xét và kết luận

**PASS: 25/25 thresholds đạt.** Các cửa sổ đánh giá và từng API đều đạt ngưỡng đã cấu hình. Cửa sổ steady 15 phút chỉ hỗ trợ nhận xét trong lần đo ngắn này; RSS biến động/giảm sau tải không đủ chứng minh không có memory leak. 

Không suy ra nguyên nhân nghẽn, crash hoặc loại mã lỗi HTTP từ summary và CPU/RSS. Cần log backend, DB latency/locks và event-loop lag để xác minh nguyên nhân. Dùng lần đo này làm mốc đối chiếu; chạy lặp cùng môi trường/dữ liệu trước khi dùng kết quả làm cam kết năng lực.
