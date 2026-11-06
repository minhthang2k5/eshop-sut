# Spike Test Report — eShop

## 1. Lần đo và nguồn dữ liệu

| Trường | Giá trị |
|---|---|
| Run ID | `spike-20261106-182250-CyyDmN` |
| Ngày / múi giờ | 06/11/2026, UTC+07:00 |
| Scenario bắt đầu | 2026-11-06T18:23:21+07:00 |
| k6 bắt đầu / kết thúc | 2026-11-06T18:23:20+07:00 / 2026-11-06T18:25:56+07:00 |
| Thời lượng tiến trình k6 | 156.268 s |
| Interrupted (timeline) | False |
| Telemetry backend | `server-backend-42648-1793964155093.jsonl` |
| Phiên bản/build/máy chạy | Không được xác nhận trong bộ kết quả; chưa có checksum build và snapshot DB |

Nguồn: [summary.json](../output/spike-20261106-182250-CyyDmN/summary.json), [timeline](../output/spike-20261106-182250-CyyDmN/measurement-timeline.json), [biểu đồ K6](../output/spike-20261106-182250-CyyDmN/spike_report.html), [CPU/RAM JSONL](../output/telemetry/server-backend-42648-1793964155093.jsonl), [biểu đồ CPU/RAM](../output/telemetry/server-backend-42648-1793964155093.html). `telemetry/` chứa bộ thu; dữ liệu đo nằm ở `output/telemetry/`.

## 2. Mục tiêu, workload và cách đánh giá

Đánh giá phản ứng trước tải tăng đột ngột và kết quả trong các cửa sổ recovery.

Mix Search/Detail/Cart/Checkout = 40/20/22/18%. Theo script hiện có, mỗi iteration chọn một nghiệp vụ; Cart/Checkout login riêng trước mỗi thao tác. Think time Search/Detail/Cart/Checkout lần lượt 1–3/2–5/1–3/3–6 giây; timeout HTTP 10 giây. Đây là closed model `ramping-vus`; VU mục tiêu không tương đương số request/giây. Cấu hình mã hiện tại dùng để giải thích workload, không thay thế bằng chứng build tại thời điểm đo.

Ngưỡng trong summary cho từng steady/hold/recovery: p95 <500 ms, HTTP lỗi <1%, checks ≥99%, request count >0 cho tổng và từng API login/search/detail/cart/checkout; business_operations_failed <1% cho tổng phase. Đánh giá trực tiếp giá trị đo và đối chiếu cờ threshold: định dạng summary này dùng `true` cho vi phạm, `false` cho đạt. Skipped là chỉ số chẩn đoán, không có threshold riêng.

## 3. Profile thực đo

| Phase | VU target | Giây | Khoảng từ scenario start (s) |
|---|---|---|---|
| hold_50 | 50 | 30 | 0.000–30.000 |
| burst | 800 | 0 | 30.000–30.000 |
| hold_800 | 800 | 60 | 30.000–90.000 |
| unload | 50 | 0 | 90.000–90.000 |
| recovery_1 | 50 | 60 | 90.000–150.000 |

## 4. Kết quả K6

### 4.1 Toàn bài (gồm ramp và grace)

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | 27,109.000 |
| HTTP RPS toàn bài | 175.068 |
| Iterations hoàn tất | 19,333.000 |
| VU max quan sát | 800.000 |
| Latency avg (ms) | 8.271 |
| Latency median (ms) | 2.176 |
| Latency p95 (ms) | 13.515 |
| Latency p99 (ms) | 234.371 |
| Latency max (ms) | 694.251 |
| HTTP request lỗi | 1.000 |
| Checks thất bại | 2.000 |
| Nghiệp vụ skipped | 1.000 |
| HTTP lỗi (%) | 0.004 |
| Checks đạt (%) | 99.996 |
| Nghiệp vụ thất bại (%) | 0.005 |
| Threshold đạt / tổng | 75 / 75 |
| Kết luận theo thresholds | PASS |

`http_req_failed.passes` đếm mẫu lỗi, còn `checks.passes` đếm check thành công. Hai check/request không có nghĩa số check lỗi bằng số HTTP lỗi. HTTP requests bao gồm login.

### 4.2 Theo cửa sổ đánh giá

| Phase | VU target | Requests | RPS¹ | p95 ms | p99 ms | HTTP lỗi % | Checks % | Nghiệp vụ lỗi % | Kết quả² |
|---|---|---|---|---|---|---|---|---|---|
| hold_50 | 50 | 793 | 26.433 | 26.542 | 29.550 | 0.000 | 100.000 | 0.000 | PASS |
| hold_800 | 800 | 24796 | 413.267 | 10.476 | 244.433 | 0.004 | 99.996 | 0.006 | PASS |
| recovery_1 | 50 | 1507 | 25.117 | 29.915 | 209.717 | 0.000 | 100.000 | 0.000 | PASS |

¹ Count chia thời lượng phase danh định trong timeline; không dùng rate submetric vì mẫu số có thể là toàn run. Phase gắn khi request bắt đầu; đây không phải completion throughput thuần. ² Kết quả xét cả từng API và business_operations_failed, không chỉ hàng tổng. Không cộng hoặc lấy trung bình các percentile.

### 4.3 Chi tiết từng API

| Phase | API | Requests | p95 ms | HTTP lỗi % | Checks % |
|---|---|---|---|---|---|
| hold_50 | login | 231 | 26.303 | 0.000 | 100.000 |
| hold_50 | search | 213 | 28.244 | 0.000 | 100.000 |
| hold_50 | detail | 118 | 27.331 | 0.000 | 100.000 |
| hold_50 | cart | 121 | 2.588 | 0.000 | 100.000 |
| hold_50 | checkout | 110 | 28.911 | 0.000 | 100.000 |
| hold_800 | login | 7114 | 12.829 | 0.014 | 99.986 |
| hold_800 | search | 7094 | 17.565 | 0.000 | 100.000 |
| hold_800 | detail | 3477 | 15.139 | 0.000 | 100.000 |
| hold_800 | cart | 3862 | 3.108 | 0.000 | 100.000 |
| hold_800 | checkout | 3249 | 11.592 | 0.000 | 100.000 |
| recovery_1 | login | 419 | 17.223 | 0.000 | 100.000 |
| recovery_1 | search | 462 | 13.553 | 0.000 | 100.000 |
| recovery_1 | detail | 205 | 19.223 | 0.000 | 100.000 |
| recovery_1 | cart | 232 | 1.493 | 0.000 | 100.000 |
| recovery_1 | checkout | 189 | 42.637 | 0.000 | 100.000 |

### 4.4 Điều kiện vi phạm

Không có threshold vi phạm trong summary.

## 5. CPU và RAM của tiến trình backend

CPU 100% tương đương một core; RAM là RSS MiB, không phải RAM toàn máy hay heap. TB là trung bình mẫu, không có trọng số thời gian. Chia cửa sổ theo timestamp timeline [bắt đầu, kết thúc); trong k6 có setup và grace. Không dùng mốc 30/60 giây tính từ đầu/cuối file telemetry vì file có thể chứa dữ liệu ngoài run.

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| Trước k6 | 30.012 | 30 | 0.047 | 0.150 | 67.730 | 67.730 | 67.730 | 67.730 | 1.002 |
| Trong k6 | 156.268 | 156 | 21.893 | 60.621 | 170.230 | 208.945 | 67.730 | 208.945 | 1.003 |
| Sau k6 | 60.012 | 60 | 0.107 | 4.028 | 96.142 | 208.945 | 208.945 | 94.230 | 1.002 |

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| hold_50 | 30.000 | 30 | 6.228 | 10.084 | 76.674 | 80.836 | 73.762 | 80.836 | 1.001 |
| hold_800 | 60.000 | 60 | 47.808 | 60.621 | 177.105 | 208.445 | 93.156 | 208.445 | 1.003 |
| recovery_1 | 60.000 | 60 | 5.961 | 17.304 | 208.614 | 208.945 | 208.445 | 208.945 | 1.001 |

Mẫu tại đầu/cuối là mẫu đầu/cuối có trong cửa sổ. Khoảng trễ lấy mẫu có thể bỏ sót đỉnh CPU/RAM; không nội suy phần thiếu. Không có telemetry của DB, k6, disk I/O, event-loop lag hay CPU từng core trong bảng này.

## 7. Nhận xét và kết luận

**PASS: 75/75 thresholds đạt.** Các cửa sổ đánh giá và từng API đều đạt ngưỡng đã cấu hình. Recovery: recovery_1 PASS. Chỉ xác nhận trong cửa sổ đã đo, chưa xác định thời gian phục hồi chính xác hoặc hết backlog. 

Không suy ra nguyên nhân nghẽn, crash hoặc loại mã lỗi HTTP từ summary và CPU/RSS. Cần log backend, DB latency/locks và event-loop lag để xác minh nguyên nhân. Dùng lần đo này làm mốc đối chiếu; chạy lặp cùng môi trường/dữ liệu trước khi dùng kết quả làm cam kết năng lực.
