# Spike Test Report – <Tên hệ thống> – <YYYY-MM-DD>

## 1. Metadata

| Trường | Giá trị |
|---|---|
| Người thực hiện  | |
| Công cụ   | |
| Test run ID  | |

## 2. Mục tiêu và phạm vi

- **Mục tiêu level này:** Kiểm tra phản ứng của hệ thống khi tải tăng đột biến rồi giảm
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

- **Load profile (tăng vọt trong thời gian rất ngắn, sau đó giảm):** <mô tả>
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

### 5.3 Phần riêng của Spike test

**Đặc tả spike**

| Hạng mục | Giá trị |
|---|---|
| Tải nền trước spike | |
| Tải đỉnh | |
| Hệ số tăng (đỉnh / nền) | ...x |
| Thời gian tăng (ramp) | |
| Thời gian giữ đỉnh | |
| Thời gian giảm | |
| Số spike lặp lại (nếu có) | |

**So sánh trước / trong / sau spike**

| Chỉ số | Trước spike | Trong spike | Sau spike |
|---|---|---|---|
| RT p95 | | | |
| Throughput | | | |
| Error % | | | |
| CPU app | | | |
| Queue / backlog | | | |

**Hồi phục**

- Thời gian để RT/error trở về mức baseline sau spike: <...>
- Còn tồn dư backlog / lỗi sau spike không: <...>

**Autoscaling (nếu có)**

| Hạng mục | Giá trị |
|---|---|
| Trigger scale-out (metric, ngưỡng) | |
| Độ trễ từ lúc spike đến khi instance mới sẵn sàng | |
| Số instance trước / đỉnh / sau | |
| Scale-in có đúng không | |

**Các cơ chế bảo vệ:** rate limiting, circuit breaker, queue/buffering có hoạt động như thiết kế không: <...>

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
