# Stress Test Report — EShop

Báo cáo tự động từ dữ liệu đã lưu. [Biểu đồ HTML](stress_report.html).

## 1. Thông tin lần đo

| Trường | Giá trị |
|---|---|
| Run ID | stress-20261102-203241-jaeFhM |
| Loại test | stress |
| Scenario bắt đầu (UTC+7) | 2026-11-02T20:33:14.707+07:00 |
| k6 kết thúc (UTC+7) | 2026-11-02T21:11:50.601+07:00 |
| Độ đầy đủ lần đo | COMPLETE |
| Môi trường / phiên bản | Không được lưu trong dữ liệu đầu vào; chưa xác nhận |

## 2. Tiêu chí đánh giá

Đánh giá theo cấu hình stress trong analyze/profiles.json, không dùng cờ threshold của summary. Skipped chỉ để theo dõi; login lỗi đã tính vào tỷ lệ thao tác thất bại. INCOMPLETE nghĩa là thiếu bằng chứng để xác nhận đạt. COMPLETE/PARTIAL/UNKNOWN mô tả độ đầy đủ lịch tải, độc lập với vi phạm SLO đã quan sát.

| Metric | Ngưỡng | Phạm vi | Endpoint |
|---|---|---|---|
| http_req_duration | p(95) < 500 | các phase đánh giá | tổng, login, search, detail, cart, checkout |
| http_req_failed | rate < 0.01 | các phase đánh giá | tổng, login, search, detail, cart, checkout |
| checks | rate >= 0.99 | các phase đánh giá | tổng, login, search, detail, cart, checkout |
| http_reqs | count > 0 | các phase đánh giá | tổng, login, search, detail, cart, checkout |
| business_operations_failed | rate < 0.01 | các phase đánh giá | tổng |

## 3. Profile và cách chạy

| Phase | Giây danh định | VU target |
|---|---|---|
| ramp_200 | 30.00 | 200 |
| hold_200 | 120.00 | 200 |
| ramp_400 | 30.00 | 400 |
| hold_400 | 120.00 | 400 |
| ramp_600 | 30.00 | 600 |
| hold_600 | 120.00 | 600 |
| ramp_800 | 30.00 | 800 |
| hold_800 | 120.00 | 800 |
| ramp_1000 | 30.00 | 1,000 |
| hold_1000 | 120.00 | 1,000 |
| ramp_1200 | 30.00 | 1,200 |
| hold_1200 | 120.00 | 1,200 |
| ramp_1400 | 30.00 | 1,400 |
| hold_1400 | 120.00 | 1,400 |
| ramp_1600 | 30.00 | 1,600 |
| hold_1600 | 120.00 | 1,600 |
| ramp_1800 | 30.00 | 1,800 |
| hold_1800 | 120.00 | 1,800 |
| ramp_2000 | 30.00 | 2,000 |
| hold_2000 | 120.00 | 2,000 |
| ramp_2200 | 30.00 | 2,200 |
| hold_2200 | 120.00 | 2,200 |
| ramp_2400 | 30.00 | 2,400 |
| hold_2400 | 120.00 | 2,400 |
| ramp_2600 | 30.00 | 2,600 |
| hold_2600 | 120.00 | 2,600 |
| ramp_2800 | 30.00 | 2,800 |
| hold_2800 | 120.00 | 2,800 |
| ramp_3000 | 30.00 | 3,000 |
| hold_3000 | 120.00 | 3,000 |
| unload | 0.00 | 50 |
| recovery_1 | 60.00 | 50 |

[Script stress](../stress.js) · [Hướng dẫn analyzer](../analyze/README.md).

## 4. Nguồn dữ liệu

[summary.json](../output/stress-20261102-203241-jaeFhM/summary.json) · [measurement-timeline.json](../output/stress-20261102-203241-jaeFhM/measurement-timeline.json) · [node-cpu-ram.jsonl](../output/stress-20261102-203241-jaeFhM/node-cpu-ram.jsonl) · [k6.log](../output/stress-20261102-203241-jaeFhM/k6.log) · [node-cpu-ram.csv](node-cpu-ram.csv) · [cpu-ram-phases.csv](cpu-ram-phases.csv) · [cpu-ram-before-during-after.csv](cpu-ram-before-during-after.csv) · [profiles.json](../analyze/profiles.json)

## 5. Cách đọc kết quả

RPS = request / thời lượng phase: dùng cửa sổ quan sát khi có timeline, nếu thiếu thì dùng thời lượng danh định và ghi rõ trong bảng. VU là mục tiêu profile, không phải VU thực đo. Không cộng hoặc lấy trung bình percentile của các phase. Thứ tự phase theo cấu hình; bảng profile bên dưới ghi lịch của run nếu có, nếu không thì dùng cấu hình.

## 6. Kết quả đo

### 6.1 Tổng quan

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | 1,459,520 |
| Throughput (requests/s) | 630.496 |
| HTTP lỗi (%) | 1.063 |
| Checks đạt (%) | 98.937 |
| Iterations hoàn tất | 1,047,276 |
| Nghiệp vụ skipped | 7,059 |
| Iteration nghiệp vụ bắt đầu | 1,047,276 |
| Iteration nghiệp vụ hoàn tất | 1,047,276 |
| HTTP nghiệp vụ đã gửi | 1,040,217 |
| Request nghiệp vụ lỗi (gồm login chặn thao tác) | 15,519 |
| Thao tác nghiệp vụ thất bại (%) | 1.482 |
| Latency avg (ms) | 406.791 |
| Latency med (ms) | 4.004 |
| Latency p(95) (ms) | 2,994.816 |
| Latency p(99) (ms) | 6,669.119 |
| Latency max (ms) | 10,041.921 |
| Threshold đạt / không đạt / thiếu dữ liệu | 305 / 95 / 0 |
| SLO trên dữ liệu quan sát | FAIL |

### 6.2 Theo phase

| Phase | VU target | Giây | Cơ sở thời lượng | Requests | RPS | p50 ms | p95 ms | p99 ms | HTTP lỗi % | Checks % | Skipped | SLO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hold_200 | 200 | 120.00 | observed | 12,140 | 101.167 | 2.520 | 8.620 | 12.995 | 0.008 | 99.992 | 1 | PASS |
| hold_400 | 400 | 120.00 | observed | 24,331 | 202.758 | 2.341 | 8.017 | 13.421 | 0.000 | 100.000 | 0 | PASS |
| hold_600 | 600 | 120.00 | observed | 35,382 | 294.850 | 3.281 | 367.322 | 1,366.240 | 0.071 | 99.929 | 25 | PASS |
| hold_800 | 800 | 120.00 | observed | 48,925 | 407.708 | 2.032 | 8.135 | 17.030 | 0.000 | 100.000 | 0 | PASS |
| hold_1000 | 1,000 | 120.00 | observed | 56,778 | 473.150 | 3.121 | 544.944 | 4,097.097 | 0.541 | 99.459 | 122 | FAIL |
| hold_1200 | 1,200 | 120.00 | observed | 72,885 | 607.375 | 2.115 | 14.521 | 150.689 | 0.000 | 100.000 | 0 | PASS |
| hold_1400 | 1,400 | 120.00 | observed | 76,040 | 633.667 | 3.014 | 1,145.551 | 4,885.035 | 0.950 | 99.050 | 303 | FAIL |
| hold_1600 | 1,600 | 120.00 | observed | 96,902 | 807.517 | 2.662 | 45.030 | 374.027 | 0.006 | 99.994 | 6 | PASS |
| hold_1800 | 1,800 | 120.00 | observed | 84,628 | 705.233 | 5.402 | 2,988.203 | 6,691.023 | 1.527 | 98.473 | 542 | FAIL |
| hold_2000 | 2,000 | 120.00 | observed | 91,117 | 759.308 | 6.446 | 3,337.049 | 7,624.553 | 1.980 | 98.020 | 772 | FAIL |
| hold_2200 | 2,200 | 120.00 | observed | 113,303 | 944.192 | 11.920 | 2,794.737 | 5,921.013 | 0.439 | 99.561 | 224 | FAIL |
| hold_2400 | 2,400 | 120.00 | observed | 137,413 | 1,145.108 | 5.028 | 586.564 | 1,012.419 | 0.033 | 99.967 | 45 | FAIL |
| hold_2600 | 2,600 | 120.00 | observed | 135,307 | 1,127.558 | 4.712 | 736.124 | 2,585.084 | 0.597 | 99.403 | 588 | FAIL |
| hold_2800 | 2,800 | 120.00 | observed | 124,712 | 1,039.267 | 5.921 | 3,730.599 | 6,444.035 | 1.956 | 98.044 | 1,038 | FAIL |
| hold_3000 | 3,000 | 120.00 | observed | 90,711 | 755.925 | 10.475 | 7,219.140 | 8,993.165 | 4.261 | 95.739 | 1,815 | FAIL |
| recovery_1 | 50 | 60.00 | observed | 1,540 | 25.667 | 2.621 | 12.606 | 15.269 | 0.000 | 100.000 | 0 | PASS |

Điều kiện toàn bài và các điều kiện phase không đạt/thiếu dữ liệu:

| Phase | Endpoint | Metric | Điều kiện | Giá trị | Kết quả |
|---|---|---|---|---|---|
| hold_1000 | tổng | http_req_duration | p(95) < 500 | 544.944 | FAIL |
| hold_1000 | login | http_req_duration | p(95) < 500 | 595.705 | FAIL |
| hold_1000 | search | http_req_duration | p(95) < 500 | 651.466 | FAIL |
| hold_1000 | detail | http_req_duration | p(95) < 500 | 580.896 | FAIL |
| hold_1000 | checkout | http_req_duration | p(95) < 500 | 844.581 | FAIL |
| hold_1400 | tổng | http_req_duration | p(95) < 500 | 1,145.551 | FAIL |
| hold_1400 | login | http_req_duration | p(95) < 500 | 1,220.052 | FAIL |
| hold_1400 | search | http_req_duration | p(95) < 500 | 1,231.031 | FAIL |
| hold_1400 | detail | http_req_duration | p(95) < 500 | 1,274.820 | FAIL |
| hold_1400 | checkout | http_req_duration | p(95) < 500 | 1,192.491 | FAIL |
| hold_1800 | tổng | http_req_duration | p(95) < 500 | 2,988.203 | FAIL |
| hold_1800 | login | http_req_duration | p(95) < 500 | 2,965.680 | FAIL |
| hold_1800 | search | http_req_duration | p(95) < 500 | 3,203.069 | FAIL |
| hold_1800 | detail | http_req_duration | p(95) < 500 | 3,237.785 | FAIL |
| hold_1800 | cart | http_req_duration | p(95) < 500 | 812.049 | FAIL |
| hold_1800 | checkout | http_req_duration | p(95) < 500 | 3,793.885 | FAIL |
| hold_2000 | tổng | http_req_duration | p(95) < 500 | 3,337.049 | FAIL |
| hold_2000 | login | http_req_duration | p(95) < 500 | 3,309.986 | FAIL |
| hold_2000 | search | http_req_duration | p(95) < 500 | 3,426.142 | FAIL |
| hold_2000 | detail | http_req_duration | p(95) < 500 | 3,341.186 | FAIL |
| hold_2000 | cart | http_req_duration | p(95) < 500 | 984.830 | FAIL |
| hold_2000 | checkout | http_req_duration | p(95) < 500 | 3,877.775 | FAIL |
| hold_2200 | tổng | http_req_duration | p(95) < 500 | 2,794.737 | FAIL |
| hold_2200 | login | http_req_duration | p(95) < 500 | 3,118.725 | FAIL |
| hold_2200 | search | http_req_duration | p(95) < 500 | 3,258.070 | FAIL |
| hold_2200 | detail | http_req_duration | p(95) < 500 | 3,193.001 | FAIL |
| hold_2200 | cart | http_req_duration | p(95) < 500 | 1,085.614 | FAIL |
| hold_2200 | checkout | http_req_duration | p(95) < 500 | 3,656.109 | FAIL |
| hold_2400 | tổng | http_req_duration | p(95) < 500 | 586.564 | FAIL |
| hold_2400 | login | http_req_duration | p(95) < 500 | 609.727 | FAIL |
| hold_2400 | search | http_req_duration | p(95) < 500 | 605.992 | FAIL |
| hold_2400 | detail | http_req_duration | p(95) < 500 | 611.672 | FAIL |
| hold_2400 | checkout | http_req_duration | p(95) < 500 | 588.388 | FAIL |
| hold_2600 | tổng | http_req_duration | p(95) < 500 | 736.124 | FAIL |
| hold_2600 | login | http_req_duration | p(95) < 500 | 776.980 | FAIL |
| hold_2600 | search | http_req_duration | p(95) < 500 | 730.649 | FAIL |
| hold_2600 | detail | http_req_duration | p(95) < 500 | 743.003 | FAIL |
| hold_2600 | checkout | http_req_duration | p(95) < 500 | 780.840 | FAIL |
| hold_2800 | tổng | http_req_duration | p(95) < 500 | 3,730.599 | FAIL |
| hold_2800 | login | http_req_duration | p(95) < 500 | 3,818.262 | FAIL |
| hold_2800 | search | http_req_duration | p(95) < 500 | 4,250.192 | FAIL |
| hold_2800 | detail | http_req_duration | p(95) < 500 | 4,200.123 | FAIL |
| hold_2800 | cart | http_req_duration | p(95) < 500 | 821.679 | FAIL |
| hold_2800 | checkout | http_req_duration | p(95) < 500 | 4,938.944 | FAIL |
| hold_3000 | tổng | http_req_duration | p(95) < 500 | 7,219.140 | FAIL |
| hold_3000 | login | http_req_duration | p(95) < 500 | 7,149.928 | FAIL |
| hold_3000 | search | http_req_duration | p(95) < 500 | 7,531.947 | FAIL |
| hold_3000 | detail | http_req_duration | p(95) < 500 | 7,520.314 | FAIL |
| hold_3000 | cart | http_req_duration | p(95) < 500 | 2,473.690 | FAIL |
| hold_3000 | checkout | http_req_duration | p(95) < 500 | 7,279.279 | FAIL |
| hold_1400 | login | http_req_failed | rate < 0.01 | 0.014 | FAIL |
| hold_1400 | search | http_req_failed | rate < 0.01 | 0.013 | FAIL |
| hold_1400 | detail | http_req_failed | rate < 0.01 | 0.012 | FAIL |
| hold_1800 | tổng | http_req_failed | rate < 0.01 | 0.015 | FAIL |
| hold_1800 | login | http_req_failed | rate < 0.01 | 0.022 | FAIL |
| hold_1800 | search | http_req_failed | rate < 0.01 | 0.020 | FAIL |
| hold_1800 | detail | http_req_failed | rate < 0.01 | 0.022 | FAIL |
| hold_2000 | tổng | http_req_failed | rate < 0.01 | 0.020 | FAIL |
| hold_2000 | login | http_req_failed | rate < 0.01 | 0.029 | FAIL |
| hold_2000 | search | http_req_failed | rate < 0.01 | 0.027 | FAIL |
| hold_2000 | detail | http_req_failed | rate < 0.01 | 0.025 | FAIL |
| hold_2600 | login | http_req_failed | rate < 0.01 | 0.015 | FAIL |
| hold_2800 | tổng | http_req_failed | rate < 0.01 | 0.020 | FAIL |
| hold_2800 | login | http_req_failed | rate < 0.01 | 0.029 | FAIL |
| hold_2800 | search | http_req_failed | rate < 0.01 | 0.026 | FAIL |
| hold_2800 | detail | http_req_failed | rate < 0.01 | 0.027 | FAIL |
| hold_3000 | tổng | http_req_failed | rate < 0.01 | 0.043 | FAIL |
| hold_3000 | login | http_req_failed | rate < 0.01 | 0.069 | FAIL |
| hold_3000 | search | http_req_failed | rate < 0.01 | 0.053 | FAIL |
| hold_3000 | detail | http_req_failed | rate < 0.01 | 0.051 | FAIL |
| hold_1400 | login | checks | rate >= 0.99 | 0.986 | FAIL |
| hold_1400 | search | checks | rate >= 0.99 | 0.987 | FAIL |
| hold_1400 | detail | checks | rate >= 0.99 | 0.988 | FAIL |
| hold_1800 | tổng | checks | rate >= 0.99 | 0.985 | FAIL |
| hold_1800 | login | checks | rate >= 0.99 | 0.978 | FAIL |
| hold_1800 | search | checks | rate >= 0.99 | 0.980 | FAIL |
| hold_1800 | detail | checks | rate >= 0.99 | 0.978 | FAIL |
| hold_2000 | tổng | checks | rate >= 0.99 | 0.980 | FAIL |
| hold_2000 | login | checks | rate >= 0.99 | 0.971 | FAIL |
| hold_2000 | search | checks | rate >= 0.99 | 0.973 | FAIL |
| hold_2000 | detail | checks | rate >= 0.99 | 0.975 | FAIL |
| hold_2600 | login | checks | rate >= 0.99 | 0.985 | FAIL |
| hold_2800 | tổng | checks | rate >= 0.99 | 0.980 | FAIL |
| hold_2800 | login | checks | rate >= 0.99 | 0.971 | FAIL |
| hold_2800 | search | checks | rate >= 0.99 | 0.974 | FAIL |
| hold_2800 | detail | checks | rate >= 0.99 | 0.973 | FAIL |
| hold_3000 | tổng | checks | rate >= 0.99 | 0.957 | FAIL |
| hold_3000 | login | checks | rate >= 0.99 | 0.931 | FAIL |
| hold_3000 | search | checks | rate >= 0.99 | 0.947 | FAIL |
| hold_3000 | detail | checks | rate >= 0.99 | 0.949 | FAIL |
| hold_1400 | tổng | business_operations_failed | rate < 0.01 | 0.013 | FAIL |
| hold_1800 | tổng | business_operations_failed | rate < 0.01 | 0.021 | FAIL |
| hold_2000 | tổng | business_operations_failed | rate < 0.01 | 0.028 | FAIL |
| hold_2800 | tổng | business_operations_failed | rate < 0.01 | 0.027 | FAIL |
| hold_3000 | tổng | business_operations_failed | rate < 0.01 | 0.059 | FAIL |

### 6.3 CPU và RAM Node.js

CPU 100% = một core; RAM = RSS (MiB). TB là trung bình mẫu. Cửa sổ [bắt đầu, kết thúc); trong tải gồm recovery và grace, setup tách riêng. Biểu đồ giữ toàn bộ mẫu và ngắt nét khi khoảng cách vượt 2s. N/A là thiếu dữ liệu, không phải 0.

#### Trước / trong / sau tải

| Giai đoạn | VU target | Giây | Mẫu | CPU TB % | CPU max % | RAM TB MiB | RAM max MiB | RAM đầu MiB | RAM cuối MiB |
|---|---|---|---|---|---|---|---|---|---|
| before_test | N/A | 30.01 | 30 | 0.05 | 0.07 | 67.71 | 67.71 | 67.71 | 67.71 |
| during_test | N/A | 2,315.89 | 2,126 | 45.10 | 87.24 | 204.54 | 315.81 | 69.41 | 182.11 |
| after_test | N/A | 60.02 | 60 | 0.05 | 0.33 | 182.11 | 182.11 | 182.11 | 182.11 |

#### Từng phase

| Giai đoạn | VU target | Giây | Mẫu | CPU TB % | CPU max % | RAM TB MiB | RAM max MiB | RAM đầu MiB | RAM cuối MiB |
|---|---|---|---|---|---|---|---|---|---|
| setup | N/A | 3.01 | 3 | 0.03 | 0.04 | 67.71 | 67.71 | 67.71 | 67.71 |
| ramp_200 | 200 | 30.00 | 30 | 13.37 | 25.15 | 80.21 | 93.04 | 69.41 | 93.04 |
| hold_200 | 200 | 120.00 | 120 | 20.87 | 30.56 | 147.30 | 196.29 | 93.04 | 196.29 |
| ramp_400 | 400 | 30.00 | 30 | 25.65 | 34.50 | 197.65 | 199.16 | 196.29 | 199.16 |
| hold_400 | 400 | 120.00 | 120 | 33.63 | 45.31 | 140.38 | 200.12 | 199.16 | 99.14 |
| ramp_600 | 600 | 30.00 | 30 | 37.51 | 51.30 | 100.43 | 106.64 | 99.14 | 106.64 |
| hold_600 | 600 | 120.00 | 117 | 37.62 | 48.94 | 112.32 | 131.75 | 106.64 | 130.19 |
| ramp_800 | 800 | 30.00 | 30 | 45.13 | 53.81 | 130.25 | 130.31 | 130.19 | 130.31 |
| hold_800 | 800 | 120.00 | 120 | 47.50 | 56.60 | 117.18 | 131.94 | 130.31 | 113.28 |
| ramp_1000 | 1,000 | 30.00 | 30 | 49.84 | 56.43 | 112.62 | 112.78 | 112.53 | 112.78 |
| hold_1000 | 1,000 | 120.00 | 113 | 44.91 | 60.54 | 121.79 | 138.53 | 112.78 | 138.53 |
| ramp_1200 | 1,200 | 30.00 | 29 | 43.56 | 61.28 | 165.63 | 167.96 | 152.65 | 167.96 |
| hold_1200 | 1,200 | 120.00 | 119 | 55.01 | 66.17 | 169.48 | 169.71 | 167.96 | 169.71 |
| ramp_1400 | 1,400 | 30.00 | 30 | 57.39 | 65.60 | 170.28 | 171.21 | 169.71 | 171.21 |
| hold_1400 | 1,400 | 120.00 | 112 | 50.22 | 70.46 | 205.65 | 237.68 | 171.33 | 237.68 |
| ramp_1600 | 1,600 | 30.00 | 24 | 40.81 | 76.04 | 238.21 | 239.14 | 237.68 | 239.14 |
| hold_1600 | 1,600 | 120.00 | 119 | 58.49 | 69.81 | 238.77 | 239.81 | 239.14 | 239.81 |
| ramp_1800 | 1,800 | 30.00 | 30 | 59.02 | 68.71 | 239.66 | 240.51 | 239.81 | 240.41 |
| hold_1800 | 1,800 | 120.00 | 98 | 47.94 | 72.66 | 260.51 | 267.25 | 240.41 | 266.55 |
| ramp_2000 | 2,000 | 30.00 | 30 | 60.10 | 71.06 | 266.75 | 267.57 | 266.68 | 266.99 |
| hold_2000 | 2,000 | 120.00 | 102 | 47.93 | 78.12 | 205.35 | 274.14 | 266.48 | 274.14 |
| ramp_2200 | 2,200 | 30.00 | 30 | 64.53 | 70.80 | 272.63 | 274.14 | 274.14 | 272.24 |
| hold_2200 | 2,200 | 120.00 | 108 | 51.25 | 73.71 | 237.84 | 274.21 | 272.59 | 246.17 |
| ramp_2400 | 2,400 | 30.00 | 18 | 35.45 | 70.22 | 276.10 | 281.00 | 267.05 | 281.00 |
| hold_2400 | 2,400 | 120.00 | 117 | 57.39 | 76.32 | 280.00 | 281.00 | 281.00 | 280.77 |
| ramp_2600 | 2,600 | 30.00 | 18 | 18.74 | 34.05 | 287.40 | 292.64 | 282.22 | 292.64 |
| hold_2600 | 2,600 | 120.00 | 110 | 59.43 | 87.24 | 291.67 | 295.21 | 293.14 | 291.76 |
| ramp_2800 | 2,800 | 30.00 | 23 | 35.28 | 71.44 | 291.98 | 292.80 | 291.76 | 292.80 |
| hold_2800 | 2,800 | 120.00 | 100 | 54.97 | 86.26 | 297.29 | 298.79 | 292.43 | 297.37 |
| ramp_3000 | 3,000 | 30.00 | 25 | 37.95 | 70.11 | 299.20 | 302.03 | 296.32 | 302.03 |
| hold_3000 | 3,000 | 120.00 | 78 | 42.58 | 81.59 | 312.15 | 315.43 | 308.40 | 315.43 |
| recovery_1 | 50 | 60.00 | 60 | 8.05 | 64.53 | 226.55 | 315.81 | 315.68 | 182.11 |
| graceful_stop | N/A | 5.89 | 6 | 1.22 | 5.49 | 182.11 | 182.11 | 182.11 | 182.11 |

### 6.4 Nhận xét và kết luận

- 6/15 bậc hold PASS. Bậc FAIL đầu tiên: hold_1000.
- Vùng PASS liên tục từ bậc đầu: 200–800 VU.
- Recovery: recovery_1 PASS. Percentile của cửa sổ không xác định chính xác giây phục hồi.
- Trong tải: 2126 mẫu / 2315.89s. TB tài nguyên là trung bình mẫu, không có trọng số thời gian; khoảng thiếu mẫu có thể bỏ sót đỉnh.
- Sau tải: CPU TB 0.05%; RSS TB 182.11 MiB, chênh trước tải +114.39 MiB.
- Kết quả một lượt đo không chứng minh sức tải ổn định; CPU/RAM riêng lẻ không đủ kết luận nguyên nhân nghẽn hoặc memory leak.
