# Soak (Endurance) Test Report – <Tên hệ thống> – <YYYY-MM-DD>

## 1. Metadata

| Trường | Giá trị |
|---|---|
| Người thực hiện  | |
| Công cụ   | |
| Test run ID  | |

## 2. Mục tiêu và phạm vi

- **Mục tiêu level này:** Phát hiện suy giảm hiệu năng và rò rỉ tài nguyên khi chạy tải bình thường trong thời gian dài
- **Câu hỏi cần trả lời:** <...>
- **Trong phạm vi:** <API / luồng nghiệp vụ>
- **Ngoài phạm vi:** <...>

**SLO / NFR cần đạt**

| Chỉ số | Ngưỡng | Nguồn (SLA, NFR-xx) |
|---|---|---|
| Response time p95 | < ... ms | |
| Error rate | < ...% | |
| Throughput | >= ... RPS | |
| CPU / RAM | < ...% | |

**Entry criteria:** <build ổn định, data sẵn sàng, smoke test pass...>
**Exit criteria:** <điều kiện kết thúc test>

## 3. Môi trường test

| Thành phần | Cấu hình |
|---|---|
| App server (CPU/RAM/số instance) | |
| Database (loại, version, cấu hình) | |
| Cache / Queue / Gateway | |
| Load generator (số máy, vị trí) | |
| Tỷ lệ so với production | ...% |
| Khối lượng test data | |
| Monitoring (Grafana, Prometheus, APM...) | |
| Config quan trọng (heap, pool size, thread...) | |

## 4. Workload model

- **Load profile (tải bình thường, vài giờ đến 24h+):** <mô tả>
- **Kịch bản:** <tên script / luồng>, tỷ lệ mix: <...>
- **Think time / pacing:** <...>
- **Số VU hoặc arrival rate:** <...>
- **Ramp-up / steady / ramp-down:** <... / ... / ...>
- **Tổng thời lượng:** <...>
- **Test data:** <nguồn, số lượng, cách tránh cache hit giả>

## 5. Kết quả

### 5.1 Chỉ số chính (cửa sổ steady-state)

| Chỉ số | Giá trị |
|---|---|
| Tổng request | |
| Throughput (RPS/TPS) | |
| Response time avg / median | |
| Response time p90 / p95 / p99 / max | |
| Error rate | |
| Concurrency (VU) tối đa | |

**Phân loại lỗi:**

| Mã lỗi / loại | Số lượng | % |
|---|---|---|
| | | |

### 5.2 Tài nguyên

| Thành phần | CPU | RAM | GC | Disk I/O | Network | Pool/Queue |
|---|---|---|---|---|---|---|
| App | | | | | | |
| DB | | | | | | |

### 5.3 Phần riêng của Soak test

**So sánh đầu kỳ và cuối kỳ**

| Chỉ số | Giờ đầu | Giữa kỳ | Giờ cuối | Độ lệch |
|---|---|---|---|---|
| RT p95 | | | | |
| RT p99 | | | | |
| Throughput | | | | |
| Error % | | | | |

**Xu hướng tài nguyên theo thời gian**

| Chỉ số | Xu hướng (tăng / ổn định / dao động) | Slope (đơn vị / giờ) | Ghi chú |
|---|---|---|---|
| Heap sau full GC (nghi memory leak) | | | |
| Tần suất / thời gian GC pause | | | |
| Số thread | | | |
| DB connection (đang dùng / pool) | | | |
| File descriptor / socket | | | |
| Dung lượng disk, log | | | |
| Kích thước cache, queue | | | |

**Độ ổn định**

- Response time drift: <có / không; từ thời điểm nào>
- Throughput có giảm dần không: <...>
- Sự kiện bất thường trong thời gian chạy (restart, failover, job định kỳ, backup, cert/token hết hạn): <...>

**Kết luận về rò rỉ tài nguyên:** <có / không / nghi ngờ; bằng chứng (heap dump, profiler)>

## 6. Đối chiếu tiêu chí (Pass / Fail)

| Tiêu chí | Ngưỡng | Kết quả | Pass/Fail |
|---|---|---|---|
| | | | |

**Kết luận chung của level:** PASS / FAIL / PASS có điều kiện

## 7. Phân tích

- **Bottleneck / bất thường:** <...>
- **Nguyên nhân (kèm bằng chứng, biểu đồ):** <...>

## 8. Sai lệch, hạn chế, rủi ro

- **Sai lệch so với kế hoạch:** <...>
- **Hạn chế của môi trường / dữ liệu:** <...>
- **Mức độ tin cậy của kết quả:** <...>

## 9. Kết luận và khuyến nghị

- **Kết luận:** <...>
- **Khuyến nghị / việc cần làm tiếp:** <...>
- **Quyết định:** <go / no-go cho bước tiếp theo>

## 10. Phụ lục

- Biểu đồ (RT, TPS, error, tài nguyên theo thời gian)
- Raw data / file kết quả: <link>
- Script test: <link repo + commit>
- File config môi trường: <link>
