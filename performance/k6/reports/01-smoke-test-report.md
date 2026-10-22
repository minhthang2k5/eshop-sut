# Smoke Test Report – eShop

## 1. Metadata

| Trường | Giá trị |
|---|---|
| Người thực hiện | Lê Nguyễn Quốc Thái |
| Công cụ | k6 (chạy script `smoke.js`) |
| Test run ID | SMOKE_TEST |

## 2. Mục tiêu và phạm vi

- **Mục tiêu level này:** Xác nhận script và hệ thống chạy đúng trước khi chạy test nặng
- **Câu hỏi cần trả lời:** Script đi hết luồng nghiệp vụ và các check đều pass.
- **Trong phạm vi:** Luồng nghiệp vụ trong `smoke.js`: login → search → detail → add to cart → checkout (5 request, 10 check)
- **Ngoài phạm vi:** Kiểm tra khả năng chịu tải của hệ thống

**SLO / NFR cần đạt**

| Chỉ số | Ngưỡng | Nguồn (SLA, NFR-xx) |
|---|---|---|
| Response time p95 | < 500 ms | |
| Error rate | 0 |  |

**Entry criteria:** Backend và Database khởi động thành công
**Exit criteria:** Luồng nghiệp vụ PASS 100% sẵn sàn chạy các level performance test tiếp theo

## 3. Môi trường test

| Thành phần | Cấu hình |
|---|---|
| App server (CPU/RAM/số instance) | Chạy trên cùng máy với k6. RAM hệ thống: 7.39 GB (tổng cả server và k6). |
| Database (loại, version, cấu hình) | SQLite |
| Load generator (số máy, vị trí) | 1 máy, chạy local, cùng máy với server |
| Khối lượng test data | 1 user account + 1 product |
| Monitoring (Grafana, Prometheus, APM...) | Resource (on Linux) |

## 4. Workload model

- **Load profile (1 đến vài VU, 1–5 phút):** 1 VU, 1 iteration (shared iterations), max duration 10m, thời gian thực tế 5.1 s
- **Kịch bản:** `smoke.js` (default scenario), luồng login → search → detail → cart → checkout. Tỷ lệ mix: 1 iteration đi qua toàn bộ luồng
- **Số VU hoặc arrival rate:** 1 VU
- **Tổng thời lượng:** 5.05 s cho 1 iteration (gracefulStop 30 s, maxDuration 10 m)
- **Test data:** 1 user account + 1 product

## 5. Kết quả

### 5.1 Chỉ số chính (cửa sổ steady-state)

| Chỉ số | Giá trị |
|---|---|
| Tổng request | 5 |
| Throughput (RPS/TPS) | 0.988 req/s (iteration: 0.198 iter/s) |
| Response time avg / median | 8.93 ms / 5.41 ms |
| Response time p90 / p95 | 16.95 ms / 17.81 ms  |
| Error rate | 0.00% (0 / 5 request) |
| Concurrency (VU) tối đa | 1 |

**Phân loại lỗi:**

| Mã lỗi / loại | Số lượng | % |
|---|---|---|
| Không có lỗi (http_req_failed) | 0 | 0.00% |
| Check thất bại | 0 / 10 | 0.00% |

### 5.2 Tài nguyên

Ghi chú từ ảnh RAM (toàn hệ thống): Memory 3.60 GB / 7.39 GB (49%), tăng đột ngột từ mức thấp khi test bắt đầu rồi giữ ổn định. Swap 301 MB / 8.59 GB (4%), tăng nhẹ cùng thời điểm.

### 5.3 Phần riêng của Smoke test

**Kiểm tra tính đúng đắn của script**

| Hạng mục | Kết quả | Ghi chú |
|---|---|---|
| Assertion / check của từng request đều pass | Pass (10/10) | Toàn bộ check của login, search, detail, cart, checkout đều pass |
| Authentication / token hoạt động | Pass | Check "login: token exists" pass |
| Test data hợp lệ, không bị trùng hoặc hết | Pass | Test data hợp lệ |
| Biến động (correlation / dynamic value) xử lý đúng | Pass (suy ra) | Check "detail: product has correct id" và "checkout: orderId exists" pass, cho thấy dữ liệu động được truyền qua các bước |
| Endpoint nào trả lỗi bất thường | Không có | Tất cả request trả về status 200 (login, search, detail, cart, checkout) |

**Sanity check hiệu năng**

- Error rate ≈ 0%: Có (0.00%)
- Response time ở mức hợp lý so với kỳ vọng: Có, p95 = 17.81 ms, dưới ngưỡng 500 ms.
- Monitoring thu thập được đủ metric: Một phần (chỉ có RAM/Swap, thiếu CPU, DB, GC)

**Kết luận go / no-go:** Go cho bước tiếp theo (Baseline/Load) ở mức đề xuất. Lý do: toàn bộ check pass, không có lỗi HTTP, response time thấp. Quyết định cuối thuộc về người phụ trách test.

## 6. Đối chiếu tiêu chí (Pass / Fail)

| Tiêu chí | Ngưỡng | Kết quả | Pass/Fail |
|---|---|---|---|
| Tỷ lệ check thành công (checks rate) | = 100% | 100.00% (10/10) | Pass |
| Response time p95 | < 500 ms | 17.81 ms | Pass |
| Tỷ lệ request lỗi (http_req_failed) | 0.00% | 0.00% | Pass |

**Kết luận chung của level:** PASS