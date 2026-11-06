# Stress sau tuning Test Report — eShop

## 1. Lần đo và nguồn dữ liệu

| Trường | Giá trị |
|---|---|
| Run ID | `stress-20261106-201722-ryYFCZ` |
| Ngày / múi giờ | 06/11/2026, UTC+07:00 |
| Scenario bắt đầu | 2026-11-06T20:17:55+07:00 |
| k6 bắt đầu / kết thúc | 2026-11-06T20:17:52+07:00 / 2026-11-06T20:44:00+07:00 |
| Thời lượng tiến trình k6 | 1,567.921 s |
| Interrupted (timeline) | False |
| Telemetry backend | `server-tuned-backend-112748-1793970905073.jsonl` |
| Phiên bản/build/máy chạy | Không được xác nhận trong bộ kết quả; chưa có checksum build và snapshot DB |

Nguồn: [summary.json](../output/stress-20261106-201722-ryYFCZ/summary.json), [timeline](../output/stress-20261106-201722-ryYFCZ/measurement-timeline.json), [biểu đồ K6](../output/stress-20261106-201722-ryYFCZ/stress_report.html), [CPU/RAM JSONL](../output/telemetry/server-tuned-backend-112748-1793970905073.jsonl), [biểu đồ CPU/RAM](../output/telemetry/server-tuned-backend-112748-1793970905073.html). `telemetry/` chứa bộ thu; dữ liệu đo nằm ở `output/telemetry/`.

## 2. Mục tiêu, workload và cách đánh giá

Đánh giá stress sau tuning và đối chiếu trực tiếp với run trước tuning ngày 06/11.

Mix Search/Detail/Cart/Checkout = 40/20/22/18%. Theo script hiện có, mỗi iteration chọn một nghiệp vụ; Cart/Checkout login riêng trước mỗi thao tác. Think time Search/Detail/Cart/Checkout lần lượt 1–3/2–5/1–3/3–6 giây; timeout HTTP 10 giây. Đây là closed model `ramping-vus`; VU mục tiêu không tương đương số request/giây. Cấu hình mã hiện tại dùng để giải thích workload, không thay thế bằng chứng build tại thời điểm đo.

Ngưỡng trong summary cho từng steady/hold/recovery: p95 <500 ms, HTTP lỗi <1%, checks ≥99%, request count >0 cho tổng và từng API login/search/detail/cart/checkout; business_operations_failed <1% cho tổng phase. Đánh giá trực tiếp giá trị đo và đối chiếu cờ threshold: định dạng summary này dùng `true` cho vi phạm, `false` cho đạt. Skipped là chỉ số chẩn đoán, không có threshold riêng.

## 3. Profile thực đo

| Phase | VU target | Giây | Khoảng từ scenario start (s) |
|---|---|---|---|
| ramp_200 | 200 | 30 | 0.000–30.000 |
| hold_200 | 200 | 120 | 30.000–150.000 |
| ramp_400 | 400 | 30 | 150.000–180.000 |
| hold_400 | 400 | 120 | 180.000–300.000 |
| ramp_600 | 600 | 30 | 300.000–330.000 |
| hold_600 | 600 | 120 | 330.000–450.000 |
| ramp_800 | 800 | 30 | 450.000–480.000 |
| hold_800 | 800 | 120 | 480.000–600.000 |
| ramp_1000 | 1000 | 30 | 600.000–630.000 |
| hold_1000 | 1000 | 120 | 630.000–750.000 |
| ramp_1200 | 1200 | 30 | 750.000–780.000 |
| hold_1200 | 1200 | 120 | 780.000–900.000 |
| ramp_1400 | 1400 | 30 | 900.000–930.000 |
| hold_1400 | 1400 | 120 | 930.000–1,050.000 |
| ramp_1600 | 1600 | 30 | 1,050.000–1,080.000 |
| hold_1600 | 1600 | 120 | 1,080.000–1,200.000 |
| ramp_1800 | 1800 | 30 | 1,200.000–1,230.000 |
| hold_1800 | 1800 | 120 | 1,230.000–1,350.000 |
| ramp_2000 | 2000 | 30 | 1,350.000–1,380.000 |
| hold_2000 | 2000 | 120 | 1,380.000–1,500.000 |
| unload | 50 | 0 | 1,500.000–1,500.000 |
| recovery_1 | 50 | 60 | 1,500.000–1,560.000 |

## 4. Kết quả K6

### 4.1 Toàn bài (gồm ramp và grace)

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | 805,693.000 |
| HTTP RPS toàn bài | 514.971 |
| Iterations hoàn tất | 575,759.000 |
| VU max quan sát | 2,000.000 |
| Latency avg (ms) | 50.346 |
| Latency median (ms) | 1.799 |
| Latency p95 (ms) | 264.619 |
| Latency p99 (ms) | 1,035.038 |
| Latency max (ms) | 8,496.775 |
| HTTP request lỗi | 220.000 |
| Checks thất bại | 440.000 |
| Nghiệp vụ skipped | 220.000 |
| HTTP lỗi (%) | 0.027 |
| Checks đạt (%) | 99.973 |
| Nghiệp vụ thất bại (%) | 0.038 |
| Threshold đạt / tổng | 260 / 275 |
| Kết luận theo thresholds | FAIL |

`http_req_failed.passes` đếm mẫu lỗi, còn `checks.passes` đếm check thành công. Hai check/request không có nghĩa số check lỗi bằng số HTTP lỗi. HTTP requests bao gồm login.

### 4.2 Theo cửa sổ đánh giá

| Phase | VU target | Requests | RPS¹ | p95 ms | p99 ms | HTTP lỗi % | Checks % | Nghiệp vụ lỗi % | Kết quả² |
|---|---|---|---|---|---|---|---|---|---|
| hold_200 | 200 | 12168 | 101.400 | 5.056 | 10.042 | 0.000 | 100.000 | 0.000 | PASS |
| hold_400 | 400 | 24321 | 202.675 | 15.020 | 405.812 | 0.004 | 99.996 | 0.006 | PASS |
| hold_600 | 600 | 34220 | 285.167 | 768.405 | 2,972.039 | 0.158 | 99.842 | 0.221 | FAIL |
| hold_800 | 800 | 48485 | 404.042 | 59.030 | 291.441 | 0.006 | 99.994 | 0.009 | PASS |
| hold_1000 | 1000 | 61214 | 510.117 | 4.292 | 9.982 | 0.000 | 100.000 | 0.000 | PASS |
| hold_1200 | 1200 | 72147 | 601.225 | 117.396 | 265.226 | 0.012 | 99.988 | 0.017 | PASS |
| hold_1400 | 1400 | 85092 | 709.100 | 6.228 | 19.496 | 0.001 | 99.999 | 0.002 | PASS |
| hold_1600 | 1600 | 97774 | 814.783 | 6.636 | 30.199 | 0.000 | 100.000 | 0.000 | PASS |
| hold_1800 | 1800 | 103440 | 862.000 | 758.822 | 1,088.245 | 0.063 | 99.937 | 0.088 | FAIL |
| hold_2000 | 2000 | 112395 | 936.625 | 1,021.388 | 1,400.202 | 0.068 | 99.932 | 0.095 | FAIL |
| recovery_1 | 50 | 1586 | 26.433 | 13.328 | 107.698 | 0.000 | 100.000 | 0.000 | PASS |

¹ Count chia thời lượng phase danh định trong timeline; không dùng rate submetric vì mẫu số có thể là toàn run. Phase gắn khi request bắt đầu; đây không phải completion throughput thuần. ² Kết quả xét cả từng API và business_operations_failed, không chỉ hàng tổng. Không cộng hoặc lấy trung bình các percentile.

### 4.3 Chi tiết từng API

| Phase | API | Requests | p95 ms | HTTP lỗi % | Checks % |
|---|---|---|---|---|---|
| hold_200 | login | 3483 | 4.804 | 0.000 | 100.000 |
| hold_200 | search | 3496 | 3.627 | 0.000 | 100.000 |
| hold_200 | detail | 1706 | 3.520 | 0.000 | 100.000 |
| hold_200 | cart | 1922 | 1.513 | 0.000 | 100.000 |
| hold_200 | checkout | 1561 | 10.113 | 0.000 | 100.000 |
| hold_400 | login | 6924 | 14.402 | 0.014 | 99.986 |
| hold_400 | search | 7007 | 11.632 | 0.000 | 100.000 |
| hold_400 | detail | 3468 | 14.967 | 0.000 | 100.000 |
| hold_400 | cart | 3830 | 2.511 | 0.000 | 100.000 |
| hold_400 | checkout | 3092 | 23.450 | 0.000 | 100.000 |
| hold_600 | login | 9828 | 921.574 | 0.549 | 99.451 |
| hold_600 | search | 9765 | 744.646 | 0.000 | 100.000 |
| hold_600 | detail | 4853 | 1,084.814 | 0.000 | 100.000 |
| hold_600 | cart | 5264 | 98.569 | 0.000 | 100.000 |
| hold_600 | checkout | 4510 | 1,074.724 | 0.000 | 100.000 |
| hold_800 | login | 13875 | 81.878 | 0.022 | 99.978 |
| hold_800 | search | 13866 | 80.028 | 0.000 | 100.000 |
| hold_800 | detail | 6872 | 76.613 | 0.000 | 100.000 |
| hold_800 | cart | 7566 | 10.146 | 0.000 | 100.000 |
| hold_800 | checkout | 6306 | 69.550 | 0.000 | 100.000 |
| hold_1000 | login | 17477 | 4.770 | 0.000 | 100.000 |
| hold_1000 | search | 17608 | 3.989 | 0.000 | 100.000 |
| hold_1000 | detail | 8653 | 3.845 | 0.000 | 100.000 |
| hold_1000 | cart | 9736 | 1.828 | 0.000 | 100.000 |
| hold_1000 | checkout | 7740 | 5.258 | 0.000 | 100.000 |
| hold_1200 | login | 20558 | 129.098 | 0.044 | 99.956 |
| hold_1200 | search | 20558 | 124.185 | 0.000 | 100.000 |
| hold_1200 | detail | 10483 | 122.390 | 0.000 | 100.000 |
| hold_1200 | cart | 11189 | 22.124 | 0.000 | 100.000 |
| hold_1200 | checkout | 9359 | 141.580 | 0.000 | 100.000 |
| hold_1400 | login | 24154 | 6.960 | 0.004 | 99.996 |
| hold_1400 | search | 24455 | 6.215 | 0.000 | 100.000 |
| hold_1400 | detail | 12330 | 6.160 | 0.000 | 100.000 |
| hold_1400 | cart | 13248 | 2.371 | 0.000 | 100.000 |
| hold_1400 | checkout | 10905 | 8.827 | 0.000 | 100.000 |
| hold_1600 | login | 28048 | 7.441 | 0.000 | 100.000 |
| hold_1600 | search | 27783 | 6.854 | 0.000 | 100.000 |
| hold_1600 | detail | 13892 | 7.336 | 0.000 | 100.000 |
| hold_1600 | cart | 15396 | 2.499 | 0.000 | 100.000 |
| hold_1600 | checkout | 12655 | 8.395 | 0.000 | 100.000 |
| hold_1800 | login | 29584 | 778.921 | 0.220 | 99.780 |
| hold_1800 | search | 29526 | 778.784 | 0.000 | 100.000 |
| hold_1800 | detail | 14807 | 787.181 | 0.000 | 100.000 |
| hold_1800 | cart | 16223 | 256.628 | 0.000 | 100.000 |
| hold_1800 | checkout | 13300 | 872.599 | 0.000 | 100.000 |
| hold_2000 | login | 32134 | 1,075.559 | 0.237 | 99.763 |
| hold_2000 | search | 32129 | 1,071.210 | 0.000 | 100.000 |
| hold_2000 | detail | 16108 | 1,098.189 | 0.000 | 100.000 |
| hold_2000 | cart | 17496 | 409.102 | 0.000 | 100.000 |
| hold_2000 | checkout | 14528 | 1,091.116 | 0.000 | 100.000 |
| recovery_1 | login | 449 | 5.936 | 0.000 | 100.000 |
| recovery_1 | search | 430 | 3.201 | 0.000 | 100.000 |
| recovery_1 | detail | 222 | 7.054 | 0.000 | 100.000 |
| recovery_1 | cart | 259 | 5.401 | 0.000 | 100.000 |
| recovery_1 | checkout | 226 | 107.708 | 0.000 | 100.000 |

### 4.4 Điều kiện vi phạm

| Metric / phạm vi | Ngưỡng | Giá trị |
|---|---|---|
| `http_req_duration{phase:hold_2000,endpoint:detail}` | p(95)<500 | 1,098.189 |
| `http_req_duration{phase:hold_1800,endpoint:detail}` | p(95)<500 | 787.181 |
| `http_req_duration{phase:hold_1800,endpoint:checkout}` | p(95)<500 | 872.599 |
| `http_req_duration{phase:hold_600,endpoint:search}` | p(95)<500 | 744.646 |
| `http_req_duration{phase:hold_600,endpoint:detail}` | p(95)<500 | 1,084.814 |
| `http_req_duration{phase:hold_1800,endpoint:search}` | p(95)<500 | 778.784 |
| `http_req_duration{phase:hold_2000,endpoint:search}` | p(95)<500 | 1,071.210 |
| `http_req_duration{phase:hold_600}` | p(95)<500 | 768.405 |
| `http_req_duration{phase:hold_1800}` | p(95)<500 | 758.822 |
| `http_req_duration{phase:hold_2000,endpoint:login}` | p(95)<500 | 1,075.559 |
| `http_req_duration{phase:hold_600,endpoint:login}` | p(95)<500 | 921.574 |
| `http_req_duration{phase:hold_2000}` | p(95)<500 | 1,021.388 |
| `http_req_duration{phase:hold_1800,endpoint:login}` | p(95)<500 | 778.921 |
| `http_req_duration{phase:hold_2000,endpoint:checkout}` | p(95)<500 | 1,091.116 |
| `http_req_duration{phase:hold_600,endpoint:checkout}` | p(95)<500 | 1,074.724 |

## 5. CPU và RAM của tiến trình backend

CPU 100% tương đương một core; RAM là RSS MiB, không phải RAM toàn máy hay heap. TB là trung bình mẫu, không có trọng số thời gian. Chia cửa sổ theo timestamp timeline [bắt đầu, kết thúc); trong k6 có setup và grace. Không dùng mốc 30/60 giây tính từ đầu/cuối file telemetry vì file có thể chứa dữ liệu ngoài run.

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| Trước k6 | 30.013 | 30 | 0.036 | 0.071 | 82.227 | 82.227 | 82.227 | 82.227 | 1.002 |
| Trong k6 | 1,567.921 | 1553 | 40.975 | 77.898 | 141.410 | 218.906 | 82.227 | 105.242 | 2.875 |
| Sau k6 | 60.029 | 59 | 0.042 | 0.074 | 105.242 | 105.242 | 105.242 | 105.242 | 1.002 |

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| ramp_200 | 30.000 | 30 | 10.522 | 26.029 | 74.561 | 84.074 | 67.727 | 84.074 | 1.001 |
| hold_200 | 120.000 | 120 | 18.785 | 28.725 | 115.440 | 141.262 | 85.199 | 127.629 | 1.002 |
| ramp_400 | 30.000 | 30 | 22.965 | 30.365 | 126.829 | 128.754 | 127.754 | 126.379 | 1.026 |
| hold_400 | 120.000 | 119 | 25.960 | 38.100 | 81.853 | 128.379 | 126.379 | 65.953 | 1.198 |
| ramp_600 | 30.000 | 30 | 26.097 | 37.214 | 71.912 | 73.449 | 65.953 | 73.449 | 1.001 |
| hold_600 | 120.000 | 115 | 27.900 | 44.572 | 87.155 | 96.602 | 73.449 | 96.602 | 2.875 |
| ramp_800 | 30.000 | 30 | 38.618 | 49.525 | 95.766 | 97.852 | 96.602 | 95.215 | 1.001 |
| hold_800 | 120.000 | 119 | 39.561 | 50.475 | 96.633 | 121.375 | 95.465 | 121.375 | 1.086 |
| ramp_1000 | 30.000 | 30 | 45.868 | 53.560 | 123.450 | 124.625 | 122.500 | 124.625 | 1.010 |
| hold_1000 | 120.000 | 120 | 49.844 | 60.334 | 126.353 | 128.375 | 124.625 | 128.375 | 1.002 |
| ramp_1200 | 30.000 | 30 | 46.520 | 53.713 | 129.971 | 131.375 | 128.375 | 131.375 | 1.080 |
| hold_1200 | 120.000 | 120 | 49.725 | 62.965 | 132.226 | 132.500 | 131.375 | 132.500 | 1.095 |
| ramp_1400 | 30.000 | 30 | 56.031 | 64.696 | 133.279 | 134.125 | 132.500 | 134.125 | 1.001 |
| hold_1400 | 120.000 | 120 | 56.761 | 66.285 | 159.934 | 186.375 | 134.125 | 183.750 | 1.001 |
| ramp_1600 | 30.000 | 30 | 59.168 | 67.192 | 184.521 | 185.750 | 183.750 | 185.750 | 1.037 |
| hold_1600 | 120.000 | 120 | 59.367 | 73.302 | 186.893 | 188.125 | 185.750 | 188.125 | 1.002 |
| ramp_1800 | 30.000 | 30 | 60.646 | 71.907 | 189.300 | 190.375 | 188.125 | 190.375 | 1.001 |
| hold_1800 | 120.000 | 116 | 49.899 | 70.980 | 201.233 | 208.406 | 190.500 | 208.406 | 1.595 |
| ramp_2000 | 30.000 | 30 | 52.113 | 74.042 | 208.960 | 209.906 | 208.406 | 209.906 | 1.131 |
| hold_2000 | 120.000 | 115 | 50.160 | 77.898 | 215.830 | 217.781 | 210.031 | 217.781 | 1.604 |
| recovery_1 | 60.000 | 60 | 6.211 | 42.009 | 211.186 | 218.906 | 217.781 | 104.859 | 1.016 |

Mẫu tại đầu/cuối là mẫu đầu/cuối có trong cửa sổ. Khoảng trễ lấy mẫu có thể bỏ sót đỉnh CPU/RAM; không nội suy phần thiếu. Không có telemetry của DB, k6, disk I/O, event-loop lag hay CPU từng core trong bảng này.

## 6. So sánh stress trước / sau tuning

Hai run có cùng profile timeline 200–2000 VUs, hold 120s/bậc, recovery 50 VUs/60s. Đây là so sánh hai lượt đo; chưa có chạy lặp, snapshot DB hoặc bằng chứng cấu hình tuning thực thi để quy toàn bộ khác biệt cho tuning.

| Phase | p95 trước ms | p95 sau ms | RPS trước | RPS sau | HTTP lỗi trước % | HTTP lỗi sau % |
|---|---|---|---|---|---|---|
| hold_200 | 381.965 | 5.056 | 91.658 | 101.400 | 0.164 | 0.000 |
| hold_400 | 96.243 | 15.020 | 200.475 | 202.675 | 0.008 | 0.004 |
| hold_600 | 718.715 | 768.405 | 289.083 | 285.167 | 0.098 | 0.158 |
| hold_800 | 8.411 | 59.030 | 407.908 | 404.042 | 0.002 | 0.006 |
| hold_1000 | 945.520 | 4.292 | 449.800 | 510.117 | 0.741 | 0.000 |
| hold_1200 | 1,139.754 | 117.396 | 540.975 | 601.225 | 0.747 | 0.012 |
| hold_1400 | 2,540.663 | 6.228 | 558.025 | 709.100 | 0.811 | 0.001 |
| hold_1600 | 3,940.081 | 6.636 | 538.275 | 814.783 | 1.584 | 0.000 |
| hold_1800 | 2,433.126 | 758.822 | 769.250 | 862.000 | 0.564 | 0.063 |
| hold_2000 | 6,640.532 | 1,021.388 | 539.067 | 936.625 | 10.932 | 0.068 |
| recovery_1 | 320.834 | 13.328 | 26.850 | 26.433 | 0.062 | 0.000 |

Số threshold vi phạm giảm từ 76 xuống 15. p95 toàn bài giảm từ 2,428.076 xuống 264.619 ms, nhưng vẫn có các bậc vi phạm riêng; chưa thể kết luận tuning đáp ứng toàn bộ profile. Xem [stress trước tuning](03-stress-test-report.md).

## 7. Nhận xét và kết luận

**FAIL: 260/275 thresholds đạt.** Các cửa sổ vi phạm: `hold_600`, `hold_1800`, `hold_2000`. Bậc vi phạm đầu theo thứ tự lịch tải là `hold_600`; kết quả có thể không đơn điệu theo VU, nên không coi bậc PASS cao hơn là công suất bền vững. Recovery: recovery_1 PASS. Chỉ xác nhận trong cửa sổ đã đo, chưa xác định thời gian phục hồi chính xác hoặc hết backlog. 

Không suy ra nguyên nhân nghẽn, crash hoặc loại mã lỗi HTTP từ summary và CPU/RSS. Cần log backend, DB latency/locks và event-loop lag để xác minh nguyên nhân. Ưu tiên chạy lặp quanh các bậc vi phạm với cùng build/dữ liệu, kéo dài hold và recovery trước khi chốt giới hạn tải.
