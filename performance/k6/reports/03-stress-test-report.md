# Stress Test Report — eShop

## 1. Lần đo và nguồn dữ liệu

| Trường | Giá trị |
|---|---|
| Run ID | `stress-20261106-185434-JpCHYG` |
| Ngày / múi giờ | 06/11/2026, UTC+07:00 |
| Scenario bắt đầu | 2026-11-06T18:55:06+07:00 |
| k6 bắt đầu / kết thúc | 2026-11-06T18:55:04+07:00 / 2026-11-06T19:21:12+07:00 |
| Thời lượng tiến trình k6 | 1,568.278 s |
| Interrupted (timeline) | False |
| Telemetry backend | `server-backend-63962-1793966059878.jsonl` |
| Phiên bản/build/máy chạy | Không được xác nhận trong bộ kết quả; chưa có checksum build và snapshot DB |

Nguồn: [summary.json](../output/stress-20261106-185434-JpCHYG/summary.json), [timeline](../output/stress-20261106-185434-JpCHYG/measurement-timeline.json), [biểu đồ K6](../output/stress-20261106-185434-JpCHYG/stress_report.html), [CPU/RAM JSONL](../output/telemetry/server-backend-63962-1793966059878.jsonl), [biểu đồ CPU/RAM](../output/telemetry/server-backend-63962-1793966059878.html). `telemetry/` chứa bộ thu; dữ liệu đo nằm ở `output/telemetry/`.

## 2. Mục tiêu, workload và cách đánh giá

Xác định bậc tải bắt đầu vi phạm và khả năng đáp ứng sau giảm tải.

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
| HTTP requests | 663,083.000 |
| HTTP RPS toàn bài | 423.794 |
| Iterations hoàn tất | 477,101.000 |
| VU max quan sát | 2,000.000 |
| Latency avg (ms) | 412.001 |
| Latency median (ms) | 3.239 |
| Latency p95 (ms) | 2,428.076 |
| Latency p99 (ms) | 7,193.319 |
| Latency max (ms) | 10,058.657 |
| HTTP request lỗi | 10,711.000 |
| Checks thất bại | 21,422.000 |
| Nghiệp vụ skipped | 4,472.000 |
| HTTP lỗi (%) | 1.615 |
| Checks đạt (%) | 98.385 |
| Nghiệp vụ thất bại (%) | 2.245 |
| Threshold đạt / tổng | 199 / 275 |
| Kết luận theo thresholds | FAIL |

`http_req_failed.passes` đếm mẫu lỗi, còn `checks.passes` đếm check thành công. Hai check/request không có nghĩa số check lỗi bằng số HTTP lỗi. HTTP requests bao gồm login.

### 4.2 Theo cửa sổ đánh giá

| Phase | VU target | Requests | RPS¹ | p95 ms | p99 ms | HTTP lỗi % | Checks % | Nghiệp vụ lỗi % | Kết quả² |
|---|---|---|---|---|---|---|---|---|---|
| hold_200 | 200 | 10999 | 91.658 | 381.965 | 2,909.103 | 0.164 | 99.836 | 0.226 | PASS |
| hold_400 | 400 | 24057 | 200.475 | 96.243 | 431.058 | 0.008 | 99.992 | 0.012 | PASS |
| hold_600 | 600 | 34690 | 289.083 | 718.715 | 1,968.122 | 0.098 | 99.902 | 0.137 | FAIL |
| hold_800 | 800 | 48949 | 407.908 | 8.411 | 17.486 | 0.002 | 99.998 | 0.003 | PASS |
| hold_1000 | 1000 | 53976 | 449.800 | 945.520 | 3,752.538 | 0.741 | 99.259 | 1.032 | FAIL |
| hold_1200 | 1200 | 64917 | 540.975 | 1,139.754 | 5,403.491 | 0.747 | 99.253 | 1.042 | FAIL |
| hold_1400 | 1400 | 66963 | 558.025 | 2,540.663 | 9,218.821 | 0.811 | 99.189 | 1.131 | FAIL |
| hold_1600 | 1600 | 64593 | 538.275 | 3,940.081 | 9,173.026 | 1.584 | 98.416 | 2.207 | FAIL |
| hold_1800 | 1800 | 92310 | 769.250 | 2,433.126 | 4,046.695 | 0.564 | 99.436 | 0.783 | FAIL |
| hold_2000 | 2000 | 64688 | 539.067 | 6,640.532 | 10,000.505 | 10.932 | 89.068 | 14.587 | FAIL |
| recovery_1 | 50 | 1611 | 26.850 | 320.834 | 941.833 | 0.062 | 99.938 | 0.105 | PASS |

¹ Count chia thời lượng phase danh định trong timeline; không dùng rate submetric vì mẫu số có thể là toàn run. Phase gắn khi request bắt đầu; đây không phải completion throughput thuần. ² Kết quả xét cả từng API và business_operations_failed, không chỉ hàng tổng. Không cộng hoặc lấy trung bình các percentile.

### 4.3 Chi tiết từng API

| Phase | API | Requests | p95 ms | HTTP lỗi % | Checks % |
|---|---|---|---|---|---|
| hold_200 | login | 3066 | 495.365 | 0.554 | 99.446 |
| hold_200 | search | 3273 | 423.435 | 0.000 | 100.000 |
| hold_200 | detail | 1610 | 407.010 | 0.000 | 100.000 |
| hold_200 | cart | 1635 | 79.105 | 0.061 | 99.939 |
| hold_200 | checkout | 1415 | 433.835 | 0.000 | 100.000 |
| hold_400 | login | 6831 | 115.466 | 0.029 | 99.971 |
| hold_400 | search | 6918 | 105.367 | 0.000 | 100.000 |
| hold_400 | detail | 3478 | 110.933 | 0.000 | 100.000 |
| hold_400 | cart | 3720 | 19.405 | 0.000 | 100.000 |
| hold_400 | checkout | 3110 | 137.528 | 0.000 | 100.000 |
| hold_600 | login | 9985 | 886.179 | 0.341 | 99.659 |
| hold_600 | search | 9841 | 946.372 | 0.000 | 100.000 |
| hold_600 | detail | 4913 | 739.458 | 0.000 | 100.000 |
| hold_600 | cart | 5478 | 150.889 | 0.000 | 100.000 |
| hold_600 | checkout | 4473 | 878.681 | 0.000 | 100.000 |
| hold_800 | login | 14048 | 8.586 | 0.007 | 99.993 |
| hold_800 | search | 14008 | 7.548 | 0.000 | 100.000 |
| hold_800 | detail | 6847 | 7.515 | 0.000 | 100.000 |
| hold_800 | cart | 7718 | 2.667 | 0.000 | 100.000 |
| hold_800 | checkout | 6328 | 12.309 | 0.000 | 100.000 |
| hold_1000 | login | 15406 | 1,056.096 | 1.103 | 98.897 |
| hold_1000 | search | 15570 | 1,149.665 | 1.002 | 98.998 |
| hold_1000 | detail | 7766 | 1,037.485 | 0.953 | 99.047 |
| hold_1000 | cart | 8223 | 254.107 | 0.000 | 100.000 |
| hold_1000 | checkout | 7011 | 1,096.053 | 0.000 | 100.000 |
| hold_1200 | login | 18471 | 1,268.504 | 1.099 | 98.901 |
| hold_1200 | search | 18723 | 1,301.788 | 0.945 | 99.055 |
| hold_1200 | detail | 9335 | 1,349.431 | 1.125 | 98.875 |
| hold_1200 | cart | 9933 | 81.688 | 0.000 | 100.000 |
| hold_1200 | checkout | 8455 | 1,111.975 | 0.000 | 100.000 |
| hold_1400 | login | 19221 | 2,733.347 | 1.285 | 98.715 |
| hold_1400 | search | 19147 | 2,919.901 | 1.024 | 98.976 |
| hold_1400 | detail | 9623 | 2,951.610 | 1.039 | 98.961 |
| hold_1400 | cart | 10473 | 853.605 | 0.000 | 100.000 |
| hold_1400 | checkout | 8499 | 2,431.083 | 0.000 | 100.000 |
| hold_1600 | login | 18525 | 4,025.601 | 2.440 | 97.560 |
| hold_1600 | search | 18599 | 4,347.038 | 2.178 | 97.822 |
| hold_1600 | detail | 9223 | 4,285.947 | 1.800 | 98.200 |
| hold_1600 | cart | 10046 | 1,449.179 | 0.000 | 100.000 |
| hold_1600 | checkout | 8200 | 3,961.030 | 0.000 | 100.000 |
| hold_1800 | login | 26346 | 2,555.070 | 0.846 | 99.154 |
| hold_1800 | search | 26914 | 2,636.154 | 0.691 | 99.309 |
| hold_1800 | detail | 13285 | 2,648.037 | 0.843 | 99.157 |
| hold_1800 | cart | 14143 | 819.970 | 0.000 | 100.000 |
| hold_1800 | checkout | 11622 | 2,584.423 | 0.000 | 100.000 |
| hold_2000 | login | 19320 | 7,455.148 | 14.767 | 85.233 |
| hold_2000 | search | 19494 | 7,964.398 | 13.917 | 86.083 |
| hold_2000 | detail | 9669 | 7,901.465 | 13.673 | 86.327 |
| hold_2000 | cart | 9038 | 1,104.386 | 0.177 | 99.823 |
| hold_2000 | checkout | 7167 | 5,618.966 | 2.344 | 97.656 |
| recovery_1 | login | 393 | 478.051 | 0.254 | 99.746 |
| recovery_1 | search | 375 | 320.180 | 0.000 | 100.000 |
| recovery_1 | detail | 188 | 363.724 | 0.000 | 100.000 |
| recovery_1 | cart | 344 | 175.553 | 0.000 | 100.000 |
| recovery_1 | checkout | 311 | 468.791 | 0.000 | 100.000 |

### 4.4 Điều kiện vi phạm

| Metric / phạm vi | Ngưỡng | Giá trị |
|---|---|---|
| `checks{phase:hold_1600,endpoint:search}` | rate>=0.99 | 0.978 |
| `http_req_duration{phase:hold_2000,endpoint:login}` | p(95)<500 | 7,455.148 |
| `http_req_failed{phase:hold_1000,endpoint:search}` | rate<0.01 | 0.010 |
| `http_req_failed{phase:hold_1600}` | rate<0.01 | 0.016 |
| `http_req_failed{phase:hold_1600,endpoint:search}` | rate<0.01 | 0.022 |
| `checks{phase:hold_1600}` | rate>=0.99 | 0.984 |
| `http_req_failed{phase:hold_1200,endpoint:detail}` | rate<0.01 | 0.011 |
| `http_req_duration{phase:hold_1400}` | p(95)<500 | 2,540.663 |
| `http_req_duration{phase:hold_1000,endpoint:login}` | p(95)<500 | 1,056.096 |
| `checks{phase:hold_2000,endpoint:checkout}` | rate>=0.99 | 0.977 |
| `http_req_duration{phase:hold_1200,endpoint:login}` | p(95)<500 | 1,268.504 |
| `http_req_duration{phase:hold_1800,endpoint:search}` | p(95)<500 | 2,636.154 |
| `checks{phase:hold_1600,endpoint:detail}` | rate>=0.99 | 0.982 |
| `http_req_duration{phase:hold_1200,endpoint:detail}` | p(95)<500 | 1,349.431 |
| `http_req_duration{phase:hold_1800,endpoint:login}` | p(95)<500 | 2,555.070 |
| `http_req_duration{phase:hold_1200}` | p(95)<500 | 1,139.754 |
| `http_req_duration{phase:hold_1000,endpoint:search}` | p(95)<500 | 1,149.665 |
| `http_req_duration{phase:hold_1800}` | p(95)<500 | 2,433.126 |
| `http_req_duration{phase:hold_1800,endpoint:checkout}` | p(95)<500 | 2,584.423 |
| `http_req_failed{phase:hold_2000,endpoint:detail}` | rate<0.01 | 0.137 |
| `http_req_failed{phase:hold_2000,endpoint:checkout}` | rate<0.01 | 0.023 |
| `http_req_duration{phase:hold_1600,endpoint:checkout}` | p(95)<500 | 3,961.030 |
| `http_req_duration{phase:hold_600,endpoint:login}` | p(95)<500 | 886.179 |
| `http_req_failed{phase:hold_1600,endpoint:detail}` | rate<0.01 | 0.018 |
| `http_req_duration{phase:hold_2000,endpoint:checkout}` | p(95)<500 | 5,618.966 |
| `http_req_duration{phase:hold_1400,endpoint:search}` | p(95)<500 | 2,919.901 |
| `business_operations_failed{phase:hold_1200}` | rate<0.01 | 0.010 |
| `checks{phase:hold_2000}` | rate>=0.99 | 0.891 |
| `checks{phase:hold_2000,endpoint:detail}` | rate>=0.99 | 0.863 |
| `http_req_duration{phase:hold_2000,endpoint:cart}` | p(95)<500 | 1,104.386 |
| `http_req_failed{phase:hold_2000}` | rate<0.01 | 0.109 |
| `http_req_duration{phase:hold_2000,endpoint:detail}` | p(95)<500 | 7,901.465 |
| `http_req_duration{phase:hold_600}` | p(95)<500 | 718.715 |
| `checks{phase:hold_2000,endpoint:login}` | rate>=0.99 | 0.852 |
| `http_req_duration{phase:hold_1200,endpoint:checkout}` | p(95)<500 | 1,111.975 |
| `checks{phase:hold_2000,endpoint:search}` | rate>=0.99 | 0.861 |
| `http_req_duration{phase:hold_1600,endpoint:login}` | p(95)<500 | 4,025.601 |
| `http_req_failed{phase:hold_2000,endpoint:search}` | rate<0.01 | 0.139 |
| `http_req_failed{phase:hold_1200,endpoint:login}` | rate<0.01 | 0.011 |
| `business_operations_failed{phase:hold_1000}` | rate<0.01 | 0.010 |
| `http_req_failed{phase:hold_1000,endpoint:login}` | rate<0.01 | 0.011 |
| `http_req_duration{phase:hold_1600,endpoint:search}` | p(95)<500 | 4,347.038 |
| `http_req_duration{phase:hold_1600,endpoint:detail}` | p(95)<500 | 4,285.947 |
| `checks{phase:hold_1600,endpoint:login}` | rate>=0.99 | 0.976 |
| `http_req_duration{phase:hold_1400,endpoint:checkout}` | p(95)<500 | 2,431.083 |
| `checks{phase:hold_1400,endpoint:search}` | rate>=0.99 | 0.990 |
| `checks{phase:hold_1000,endpoint:search}` | rate>=0.99 | 0.990 |
| `http_req_failed{phase:hold_1600,endpoint:login}` | rate<0.01 | 0.024 |
| `business_operations_failed{phase:hold_1600}` | rate<0.01 | 0.022 |
| `http_req_duration{phase:hold_600,endpoint:checkout}` | p(95)<500 | 878.681 |
| `business_operations_failed{phase:hold_1400}` | rate<0.01 | 0.011 |
| `checks{phase:hold_1400,endpoint:detail}` | rate>=0.99 | 0.990 |
| `checks{phase:hold_1200,endpoint:detail}` | rate>=0.99 | 0.989 |
| `http_req_duration{phase:hold_1400,endpoint:cart}` | p(95)<500 | 853.605 |
| `http_req_duration{phase:hold_2000}` | p(95)<500 | 6,640.532 |
| `http_req_duration{phase:hold_2000,endpoint:search}` | p(95)<500 | 7,964.398 |
| `http_req_duration{phase:hold_600,endpoint:detail}` | p(95)<500 | 739.458 |
| `checks{phase:hold_1000,endpoint:login}` | rate>=0.99 | 0.989 |
| `http_req_failed{phase:hold_1400,endpoint:login}` | rate<0.01 | 0.013 |
| `http_req_duration{phase:hold_1400,endpoint:detail}` | p(95)<500 | 2,951.610 |
| `http_req_failed{phase:hold_1400,endpoint:search}` | rate<0.01 | 0.010 |
| `http_req_duration{phase:hold_1000,endpoint:detail}` | p(95)<500 | 1,037.485 |
| `http_req_duration{phase:hold_1000}` | p(95)<500 | 945.520 |
| `http_req_duration{phase:hold_1600,endpoint:cart}` | p(95)<500 | 1,449.179 |
| `http_req_duration{phase:hold_1000,endpoint:checkout}` | p(95)<500 | 1,096.053 |
| `http_req_duration{phase:hold_1800,endpoint:detail}` | p(95)<500 | 2,648.037 |
| `http_req_duration{phase:hold_1200,endpoint:search}` | p(95)<500 | 1,301.788 |
| `checks{phase:hold_1400,endpoint:login}` | rate>=0.99 | 0.987 |
| `business_operations_failed{phase:hold_2000}` | rate<0.01 | 0.146 |
| `http_req_failed{phase:hold_1400,endpoint:detail}` | rate<0.01 | 0.010 |
| `http_req_failed{phase:hold_2000,endpoint:login}` | rate<0.01 | 0.148 |
| `http_req_duration{phase:hold_600,endpoint:search}` | p(95)<500 | 946.372 |
| `checks{phase:hold_1200,endpoint:login}` | rate>=0.99 | 0.989 |
| `http_req_duration{phase:hold_1800,endpoint:cart}` | p(95)<500 | 819.970 |
| `http_req_duration{phase:hold_1400,endpoint:login}` | p(95)<500 | 2,733.347 |
| `http_req_duration{phase:hold_1600}` | p(95)<500 | 3,940.081 |

## 5. CPU và RAM của tiến trình backend

CPU 100% tương đương một core; RAM là RSS MiB, không phải RAM toàn máy hay heap. TB là trung bình mẫu, không có trọng số thời gian. Chia cửa sổ theo timestamp timeline [bắt đầu, kết thúc); trong k6 có setup và grace. Không dùng mốc 30/60 giây tính từ đầu/cuối file telemetry vì file có thể chứa dữ liệu ngoài run.

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| Trước k6 | 30.021 | 30 | 0.396 | 10.338 | 70.202 | 81.090 | 65.535 | 81.090 | 1.002 |
| Trong k6 | 1,568.278 | 1433 | 35.074 | 73.573 | 138.256 | 227.910 | 81.090 | 100.184 | 10.043 |
| Sau k6 | 60.027 | 60 | 0.087 | 3.412 | 101.256 | 101.438 | 101.438 | 100.938 | 1.002 |

| Cửa sổ | Giây | Mẫu | CPU TB % | CPU max % | RSS TB MiB | RSS max MiB | RSS đầu MiB | RSS cuối MiB | Gap max s |
|---|---|---|---|---|---|---|---|---|---|
| ramp_200 | 30.000 | 30 | 10.867 | 20.742 | 69.672 | 82.766 | 51.840 | 82.766 | 1.002 |
| hold_200 | 120.000 | 116 | 16.707 | 31.649 | 139.820 | 179.516 | 85.516 | 179.516 | 2.434 |
| ramp_400 | 30.000 | 30 | 24.879 | 32.265 | 180.091 | 181.141 | 179.516 | 181.141 | 1.002 |
| hold_400 | 120.000 | 119 | 28.184 | 38.089 | 102.649 | 182.141 | 181.141 | 73.621 | 1.564 |
| ramp_600 | 30.000 | 30 | 27.687 | 36.952 | 73.734 | 74.121 | 73.621 | 74.121 | 1.001 |
| hold_600 | 120.000 | 116 | 30.888 | 44.828 | 81.256 | 88.898 | 74.246 | 86.273 | 1.758 |
| ramp_800 | 30.000 | 30 | 38.787 | 52.094 | 75.373 | 87.523 | 86.273 | 64.195 | 1.005 |
| hold_800 | 120.000 | 120 | 45.334 | 55.742 | 71.849 | 76.320 | 66.195 | 76.320 | 1.011 |
| ramp_1000 | 30.000 | 30 | 50.699 | 58.154 | 78.362 | 91.070 | 76.320 | 91.070 | 1.002 |
| hold_1000 | 120.000 | 111 | 41.442 | 59.880 | 110.707 | 131.816 | 93.070 | 131.816 | 3.778 |
| ramp_1200 | 30.000 | 27 | 28.531 | 54.357 | 133.978 | 136.566 | 131.816 | 136.566 | 1.345 |
| hold_1200 | 120.000 | 109 | 50.580 | 64.662 | 181.997 | 191.234 | 136.691 | 191.234 | 4.692 |
| ramp_1400 | 30.000 | 30 | 58.257 | 66.488 | 191.705 | 192.734 | 191.234 | 192.734 | 1.006 |
| hold_1400 | 120.000 | 103 | 39.988 | 63.957 | 180.254 | 195.754 | 192.734 | 194.781 | 3.269 |
| ramp_1600 | 30.000 | 26 | 26.909 | 53.868 | 176.633 | 182.285 | 182.285 | 179.941 | 1.652 |
| hold_1600 | 120.000 | 97 | 34.050 | 65.524 | 203.273 | 213.941 | 179.941 | 213.941 | 2.711 |
| ramp_1800 | 30.000 | 30 | 56.323 | 68.727 | 136.079 | 214.441 | 213.941 | 105.738 | 1.010 |
| hold_1800 | 120.000 | 111 | 41.999 | 66.981 | 141.684 | 213.512 | 105.738 | 213.512 | 1.935 |
| ramp_2000 | 30.000 | 24 | 44.517 | 68.340 | 220.146 | 222.773 | 213.762 | 215.148 | 2.360 |
| hold_2000 | 120.000 | 77 | 36.745 | 73.573 | 221.640 | 227.910 | 215.148 | 198.297 | 10.043 |
| recovery_1 | 60.000 | 59 | 6.004 | 45.069 | 170.537 | 211.484 | 199.422 | 100.184 | 1.240 |

Mẫu tại đầu/cuối là mẫu đầu/cuối có trong cửa sổ. Khoảng trễ lấy mẫu có thể bỏ sót đỉnh CPU/RAM; không nội suy phần thiếu. Không có telemetry của DB, k6, disk I/O, event-loop lag hay CPU từng core trong bảng này.

## 7. Nhận xét và kết luận

**FAIL: 199/275 thresholds đạt.** Các cửa sổ vi phạm: `hold_600`, `hold_1000`, `hold_1200`, `hold_1400`, `hold_1600`, `hold_1800`, `hold_2000`. Bậc vi phạm đầu theo thứ tự lịch tải là `hold_600`; kết quả có thể không đơn điệu theo VU, nên không coi bậc PASS cao hơn là công suất bền vững. Recovery: recovery_1 PASS. Chỉ xác nhận trong cửa sổ đã đo, chưa xác định thời gian phục hồi chính xác hoặc hết backlog. 

Không suy ra nguyên nhân nghẽn, crash hoặc loại mã lỗi HTTP từ summary và CPU/RSS. Cần log backend, DB latency/locks và event-loop lag để xác minh nguyên nhân. Ưu tiên chạy lặp quanh các bậc vi phạm với cùng build/dữ liệu, kéo dài hold và recovery trước khi chốt giới hạn tải.
