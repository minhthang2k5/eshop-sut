# Stress Test Report — EShop

Điền kết quả k6 và nhận xét sau khi đo. Hai bảng CPU/RAM ở mục 6.3 được cập nhật tự động.

## 1. Thông tin lần đo

| Trường | Giá trị |
|---|---|
| Ngày đo / backend (gốc hoặc tuned) | |
| Run ID / thư mục output | |
| Máy đo / CPU / RAM | |
| Node.js / k6 | |
| Bắt đầu / kết thúc / thời lượng thực tế | |

## 2. Mục tiêu và cách đo

Tăng tải để quan sát latency, lỗi, throughput và CPU/RAM Node.js; giảm tải để quan sát recovery. CPU/RAM lấy mẫu mỗi giây: **30s trước → trong stress → 60s sau**. CPU 100% = một core; RAM = RSS (MiB).

## 3. Workload và profile

| Thao tác | Xác suất | Think time |
|---|---:|---:|
| Search | 40% | 1–3s |
| Detail | 20% | 2–5s |
| Cart | 22% | 1–3s |
| Checkout | 18% | 3–6s |

Mỗi iteration chọn một thao tác; account theo iteration. Cart/Checkout login riêng, token cục bộ. Login lỗi tính một request nghiệp vụ lỗi và một thao tác thất bại; bỏ gửi HTTP nghiệp vụ, vẫn nghỉ think time. Không retry. Search có trọng số; Detail/Cart dùng sản phẩm fixture, Checkout độc lập với giỏ.

- Fixture: 10.000 account, 200 sản phẩm, 12 keyword.
- `ramping-vus`: 0 VU → 15 bậc 200–3000, bước 200; ramp 30s + hold 120s/bậc.
- Recovery 50 VU/60s; nominal **38m30s**, grace cuối tối đa 60s; timeout request 10s.

## 4. Cách chạy

Từ `eshop-sut`, mở backend ở Terminal 1; đợi khởi động xong rồi seed và chạy ở Terminal 2:

```bash
# Terminal 1
node backend/server.js

# Terminal 2
node performance/k6/data/seed.js
bash performance/k6/run-stress.sh
```

Với tuned: mở `node tuned-backend/server.js`, seed bằng `node performance/k6/data/seed.js tuned-backend/database_tuned.sqlite`, chạy cùng runner.

Giữ backend đến khi thu sau tải xong. Restart/seed trước lần đo mới. Xem mục 6.3 và điền kết quả k6 còn lại. [Hướng dẫn](../README.md#stress).

## 5. Cách đọc kết quả

- SLO mỗi hold/recovery, tổng và từng endpoint gồm login: p95 <500ms, HTTP lỗi <1%, checks ≥99%, có request; thao tác thất bại <1%, skipped =0.
- Tỷ lệ thao tác thất bại = số thao tác thất bại / số thao tác đã có kết quả; login lỗi của Cart/Checkout tính một lần. Iteration bị ngắt chưa có kết quả không mặc định là thành công.
- `business_requests_failed` gồm lỗi nghiệp vụ và login lỗi chặn thao tác; `business_operations_failed` ghi tỷ lệ. `http_req_failed` chỉ phản ánh HTTP thực gửi.
- RPS hold = count/120s, recovery = count/60s; có login trong tổng. Phase HTTP gắn lúc request bắt đầu.

## 6. Kết quả đo

### 6.1 Tổng quan

| Chỉ số | Kết quả |
|---|---|
| HTTP requests | |
| HTTP error rate | |
| Checks thành công | |
| Iteration bắt đầu / hoàn tất | |
| Latency avg / median | |
| Latency p95 / p99 / max | |
| Throughput toàn bài | |
| Login thành công / thất bại | |
| Nghiệp vụ skipped | |
| Request nghiệp vụ lỗi (gồm login lỗi chặn Cart/Checkout) | |
| Tỷ lệ thao tác nghiệp vụ thất bại | |
| Threshold đạt / không đạt | |

### 6.2 Theo bậc tải và recovery

| Phase | VU target | Request | RPS | p95 (ms) | p99 (ms) | HTTP lỗi (%) | Checks (%) | Skipped | Kết quả |
|---|---:|---|---|---|---|---|---|---|---|
| hold_200 | 200 | | | | | | | | |
| hold_400 | 400 | | | | | | | | |
| hold_600 | 600 | | | | | | | | |
| hold_800 | 800 | | | | | | | | |
| hold_1000 | 1000 | | | | | | | | |
| hold_1200 | 1200 | | | | | | | | |
| hold_1400 | 1400 | | | | | | | | |
| hold_1600 | 1600 | | | | | | | | |
| hold_1800 | 1800 | | | | | | | | |
| hold_2000 | 2000 | | | | | | | | |
| hold_2200 | 2200 | | | | | | | | |
| hold_2400 | 2400 | | | | | | | | |
| hold_2600 | 2600 | | | | | | | | |
| hold_2800 | 2800 | | | | | | | | |
| hold_3000 | 3000 | | | | | | | | |
| recovery_1 | 50 | | | | | | | | |

### 6.3 CPU và RAM Node.js

Các bảng dưới được tự động cập nhật sau mỗi lần chạy stress; lần chạy mới thay phần CPU/RAM của lần trước. Trước khi có kết quả đo, các ô được để trống.

<!-- CPU_RAM_RESULTS_START -->

#### Trước / trong / sau stress

| Giai đoạn | VU target | Giây | Mẫu | CPU TB (%) | CPU max (%) | RAM TB (MiB) | RAM max (MiB) | RAM đầu (MiB) | RAM cuối (MiB) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| before_stress | | | | | | | | | |
| during_stress | | | | | | | | | |
| after_stress | | | | | | | | | |

#### Từng phase

| Giai đoạn | VU target | Giây | Mẫu | CPU TB (%) | CPU max (%) | RAM TB (MiB) | RAM max (MiB) | RAM đầu (MiB) | RAM cuối (MiB) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ramp_200 | 200 | | | | | | | | |
| hold_200 | 200 | | | | | | | | |
| ramp_400 | 400 | | | | | | | | |
| hold_400 | 400 | | | | | | | | |
| ramp_600 | 600 | | | | | | | | |
| hold_600 | 600 | | | | | | | | |
| ramp_800 | 800 | | | | | | | | |
| hold_800 | 800 | | | | | | | | |
| ramp_1000 | 1000 | | | | | | | | |
| hold_1000 | 1000 | | | | | | | | |
| ramp_1200 | 1200 | | | | | | | | |
| hold_1200 | 1200 | | | | | | | | |
| ramp_1400 | 1400 | | | | | | | | |
| hold_1400 | 1400 | | | | | | | | |
| ramp_1600 | 1600 | | | | | | | | |
| hold_1600 | 1600 | | | | | | | | |
| ramp_1800 | 1800 | | | | | | | | |
| hold_1800 | 1800 | | | | | | | | |
| ramp_2000 | 2000 | | | | | | | | |
| hold_2000 | 2000 | | | | | | | | |
| ramp_2200 | 2200 | | | | | | | | |
| hold_2200 | 2200 | | | | | | | | |
| ramp_2400 | 2400 | | | | | | | | |
| hold_2400 | 2400 | | | | | | | | |
| ramp_2600 | 2600 | | | | | | | | |
| hold_2600 | 2600 | | | | | | | | |
| ramp_2800 | 2800 | | | | | | | | |
| hold_2800 | 2800 | | | | | | | | |
| ramp_3000 | 3000 | | | | | | | | |
| hold_3000 | 3000 | | | | | | | | |
| recovery_1 | 50 | | | | | | | | |

<!-- CPU_RAM_RESULTS_END -->

| Quan sát | Ghi nhận |
|---|---|
| CPU khi tăng tải | |
| RAM khi tăng tải | |
| CPU/RAM sau giảm tải | |
| Biến động trùng với latency hoặc lỗi | |

### 6.4 Nhận xét và kết luận

| Nội dung | Kết quả |
|---|---|
| Bậc vi phạm SLO đầu tiên | |
| Vùng PASS liên tục trước bậc fail đầu | |
| Bậc suy giảm rõ nhất | |
| Kết quả recovery trong 60 giây | |
| Nhận xét về CPU/RAM | |
| Kết luận | |

Điền nhận xét theo dữ liệu thực tế. Percentile của cả cửa sổ recovery không xác định chính xác giây phục hồi; CPU/RAM riêng lẻ chưa đủ để kết luận nguyên nhân suy giảm hoặc memory leak.

## 7. File kết quả

| File trong thư mục run | Nội dung |
|---|---|
| `summary.json` | Metrics tổng hợp và thresholds của k6 |
| `metrics.json` | Raw metrics k6 |
| `k6.log` | Log tiến trình chạy và kết quả cuối |
| `node-cpu-ram.jsonl` | Mẫu CPU/RAM Node.js trong lượt đo |
| `node-cpu-ram.csv` | Timestamp, CPU (%), RAM (MiB) |
| `cpu-ram-phases.csv` | Bảng kết quả CPU/RAM từng phase |
| `cpu-ram-before-during-after.csv` | Bảng kết quả CPU/RAM trước, trong và sau stress |
| `measurement-timeline.json` | Mốc thời gian dùng để chia các cửa sổ đo |

Tham chiếu: [README](../README.md), [stress.js](../stress.js), [profile](../lib/stress-test-profiles.js), [runner](../run-stress.sh).
