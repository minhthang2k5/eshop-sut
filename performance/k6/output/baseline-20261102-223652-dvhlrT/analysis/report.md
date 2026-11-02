# Baseline Test Report — EShop

Báo cáo tự động từ dữ liệu đã lưu. [Biểu đồ HTML](report.html).

## 1. Thông tin lần đo

| Trường | Giá trị |
|---|---|
| Run ID | baseline-20261102-223652-dvhlrT |
| Loại test | baseline |
| Scenario bắt đầu (UTC+7) | 2026-11-02T22:37:22.657+07:00 |
| k6 kết thúc (UTC+7) | 2026-11-02T22:44:25.974+07:00 |
| Độ đầy đủ lần đo | COMPLETE |
| Môi trường / phiên bản | Không được lưu trong dữ liệu đầu vào; chưa xác nhận |

## 2. Tiêu chí đánh giá

Đánh giá theo cấu hình baseline trong analyze/profiles.json, không dùng cờ threshold của summary. 50 VU dùng 50 account đầu từ fixture đã kiểm tra; mix 55/25/14/6, lazy login riêng từng VU, sản phẩm 1 / iPhone. Đánh giá steady và login toàn bài; không yêu cầu login trong steady. Skipped = 0 toàn bài. INCOMPLETE nghĩa là thiếu bằng chứng để xác nhận đạt. COMPLETE/PARTIAL/UNKNOWN mô tả độ đầy đủ lịch tải, độc lập với vi phạm SLO đã quan sát.

| Metric | Ngưỡng | Phạm vi | Endpoint |
|---|---|---|---|
| http_req_duration | p(95) < 500 | các phase đánh giá | tổng, search, detail, cart, checkout |
| http_req_failed | rate < 0.01 | các phase đánh giá | tổng, search, detail, cart, checkout |
| checks | rate >= 0.99 | các phase đánh giá | tổng, search, detail, cart, checkout |
| http_reqs | count > 0 | các phase đánh giá | tổng, search, detail, cart, checkout |
| http_req_duration | p(95) < 500 | toàn bài | login |
| http_req_failed | rate < 0.01 | toàn bài | login |
| checks | rate >= 0.99 | toàn bài | login |
| http_reqs | count > 0 | toàn bài | login |
| business_requests_skipped | count == 0 | toàn bài | tổng |

## 3. Profile và cách chạy

| Phase | Giây danh định | VU target |
|---|---|---|
| ramp_up | 60.00 | 50 |
| steady | 300.00 | 50 |
| ramp_down | 60.00 | 0 |

[Script baseline](../../../baseline.js) · [Hướng dẫn analyzer](../../../analyze/README.md).

## 4. Nguồn dữ liệu

[summary.json](../summary.json) · [measurement-timeline.json](../measurement-timeline.json) · [node-cpu-ram.jsonl](../node-cpu-ram.jsonl) · [k6.log](../k6.log) · [node-cpu-ram.csv](node-cpu-ram.csv) · [cpu-ram-phases.csv](cpu-ram-phases.csv) · [cpu-ram-before-during-after.csv](cpu-ram-before-during-after.csv) · [profiles.json](../../../analyze/profiles.json)

## 5. Cách đọc kết quả

RPS = request / thời lượng phase: dùng cửa sổ quan sát khi có timeline, nếu thiếu thì dùng thời lượng danh định và ghi rõ trong bảng. VU là mục tiêu profile, không phải VU thực đo. Không cộng hoặc lấy trung bình percentile của các phase. Thứ tự phase theo cấu hình; bảng profile bên dưới ghi lịch của run nếu có, nếu không thì dùng cấu hình.

## 6. Kết quả đo

### 6.1 Tổng quan

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | 7,172 |
| Throughput (requests/s) | 16.967 |
| HTTP lỗi (%) | 0.000 |
| Checks đạt (%) | 100.000 |
| Iterations hoàn tất | 7,122 |
| Nghiệp vụ skipped | 0 |
| Latency avg (ms) | 2.857 |
| Latency med (ms) | 1.961 |
| Latency p(95) (ms) | 3.168 |
| Latency p(99) (ms) | 6.309 |
| Latency max (ms) | 658.372 |
| Threshold đạt / không đạt / thiếu dữ liệu | 25 / 0 / 0 |
| SLO trên dữ liệu quan sát | PASS |

### 6.2 Theo phase

| Phase | VU target | Giây | Cơ sở thời lượng | Requests | RPS | p50 ms | p95 ms | p99 ms | HTTP lỗi % | Checks % | Skipped | SLO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| steady | 50 | 300.00 | observed | 5,890 | 19.633 | 1.973 | 3.103 | 4.387 | 0.000 | 100.000 | N/A | PASS |

Điều kiện toàn bài và các điều kiện phase không đạt/thiếu dữ liệu:

| Phase | Endpoint | Metric | Điều kiện | Giá trị | Kết quả |
|---|---|---|---|---|---|
| toàn bài | login | http_req_duration | p(95) < 500 | 4.674 | PASS |
| toàn bài | login | http_req_failed | rate < 0.01 | 0.000 | PASS |
| toàn bài | login | checks | rate >= 0.99 | 1.000 | PASS |
| toàn bài | login | http_reqs | count > 0 | 50.000 | PASS |
| toàn bài | tổng | business_requests_skipped | count == 0 | 0.000 | PASS |

### 6.3 CPU và RAM Node.js

CPU 100% = một core; RAM = RSS (MiB). TB là trung bình mẫu. Cửa sổ [bắt đầu, kết thúc); trong tải gồm recovery và grace, setup tách riêng. Biểu đồ giữ toàn bộ mẫu và ngắt nét khi khoảng cách vượt 2s. N/A là thiếu dữ liệu, không phải 0.

#### Trước / trong / sau tải

| Giai đoạn | VU target | Giây | Mẫu | CPU TB % | CPU max % | RAM TB MiB | RAM max MiB | RAM đầu MiB | RAM cuối MiB |
|---|---|---|---|---|---|---|---|---|---|
| before_test | N/A | 30.01 | 30 | 0.04 | 0.10 | 67.86 | 67.86 | 67.86 | 67.86 |
| during_test | N/A | 423.32 | 423 | 3.17 | 13.22 | 61.70 | 70.98 | 67.86 | 47.43 |
| after_test | N/A | 60.75 | 60 | 0.02 | 0.09 | 44.46 | 47.43 | 47.43 | 43.18 |

#### Từng phase

| Giai đoạn | VU target | Giây | Mẫu | CPU TB % | CPU max % | RAM TB MiB | RAM max MiB | RAM đầu MiB | RAM cuối MiB |
|---|---|---|---|---|---|---|---|---|---|
| setup | N/A | 0.21 | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| ramp_up | 50 | 60.00 | 60 | 2.51 | 13.22 | 63.65 | 67.86 | 67.86 | 66.81 |
| steady | 50 | 300.00 | 300 | 3.64 | 8.49 | 64.30 | 70.98 | 66.93 | 47.14 |
| ramp_down | 0 | 60.00 | 60 | 1.61 | 5.92 | 47.46 | 48.04 | 47.14 | 47.43 |
| graceful_stop | N/A | 3.32 | 3 | 0.06 | 0.09 | 47.43 | 47.43 | 47.43 | 47.43 |

### 6.4 Nhận xét và kết luận

- Steady: PASS. Login toàn bài được đánh giá riêng; login steady không bắt buộc có mẫu.
- Trong tải: 423 mẫu / 423.32s. TB tài nguyên là trung bình mẫu, không có trọng số thời gian; khoảng thiếu mẫu có thể bỏ sót đỉnh.
- Sau tải: CPU TB 0.02%; RSS TB 44.46 MiB, chênh trước tải -23.40 MiB.
- Kết quả một lượt đo không chứng minh sức tải ổn định; CPU/RAM riêng lẻ không đủ kết luận nguyên nhân nghẽn hoặc memory leak.
