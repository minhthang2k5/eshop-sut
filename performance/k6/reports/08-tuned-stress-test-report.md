# Stress Test Report – eShop sau tune database (D8a)

> **FAIL tại bậc 2800 VUs; 247/252 thresholds đạt.** Các plateau 500–2600 VUs đạt mọi ngưỡng cấu hình. Ở 2800 VUs, p95 tổng 5288.187 ms và cả bốn API vượt 500 ms. Recovery 50 VUs trong 60s đạt SLO. Đây là kết quả một lần đo, không phải giới hạn công suất cố định.

## 1. Metadata và bằng chứng

| Trường | Giá trị |
|---|---|
| Run ID | `stress-20261023-090531-KgTWyh` |
| Ngày / múi giờ | 23/10/2026, UTC+07:00 |
| Mốc chạy | Khoảng 09:05:31–09:23:07; log hoàn tất sau 17m34.6s |
| Profile thực đo | 11 bậc 500–2800 VUs; ramp 30s + giữ 60s/bậc; recovery 60s |
| Công cụ | k6 local; chưa lưu phiên bản |
| SUT | Tuned database theo người thực hiện; mã hiện tại trong `tuned-backend/` |
| Thay đổi dự kiến | WAL và `idx_products_name ON products(name)` trong `database.js` |
| Build / database | Chưa lưu checksum build, snapshot DB, phiên bản Node.js/SQLite hoặc PRAGMA/index tại thời điểm chạy |
| Nguồn | [Summary](../output/stress-20261023-090531-KgTWyh/summary.json), [log](../output/stress-20261023-090531-KgTWyh/k6.log), [raw metrics](../output/stress-20261023-090531-KgTWyh/metrics.json) |
| Người thực hiện | Người dùng chạy test; chưa cung cấp tên |

Số liệu định lượng lấy từ summary và đối chiếu kết thúc/thresholds trong log. Không đọc toàn bộ raw metrics 2.4 GB để phân loại mã lỗi; không suy ra timeout/reset hoặc HTTP status từ summary. Không chạy lại tải hay thay đổi dữ liệu ứng dụng.

## 2. Mục tiêu và tiêu chí

Xác định bậc bắt đầu vi phạm SLO sau tune, mức suy giảm và trạng thái sau giảm tải. Phạm vi gồm Search, Detail, Cart, Checkout và lazy Login.

| Tiêu chí | Ngưỡng | Phạm vi |
|---|---|---|
| Latency p95 | <500 ms | Tổng và từng API nghiệp vụ mỗi plateau/recovery |
| HTTP lỗi | <1% | Như trên |
| Checks đạt | ≥99% | Như trên |
| Request count | >0 | Tổng và từng API nghiệp vụ mỗi cửa sổ |
| Business requests skipped | =0 | Mỗi plateau/recovery |

Login tính vào tổng phase và có thống kê riêng, không có SLO riêng. Ramp không có threshold riêng; một run có plateau đạt không đồng nghĩa mọi request trong ramp đạt. Entry có đủ mẫu năm API, chưa có log smoke hoặc trạng thái DB ban đầu kèm run. Summary dùng `thresholds: true` cho điều kiện bị vi phạm; log xác nhận 5 vi phạm latency ở `hold_2800`. Chưa lưu mã thoát shell riêng.

## 3. Workload và profile

Closed model `ramping-vus`, mix Search/Detail/Cart/Checkout = 40/20/22/18%, think time tương ứng 1–3 / 2–5 / 1–3 / 3–6 giây. Lazy Login bổ sung khi VU cần token; token riêng VU, 50 tài khoản chia vòng tròn (tối đa 56 VUs/tài khoản tại 2800). Login lỗi làm skip nghiệp vụ, không tự retry write. Dữ liệu sản phẩm cố định, không đại diện phân bố production.

| Bậc | Ramp | Hold |
|---|---|---|
| 500 VUs | 00:00–00:30 | 00:30–01:30 |
| 750 VUs | 01:30–02:00 | 02:00–03:00 |
| 1000 VUs | 03:00–03:30 | 03:30–04:30 |
| 1250 VUs | 04:30–05:00 | 05:00–06:00 |
| 1500 VUs | 06:00–06:30 | 06:30–07:30 |
| 1750 VUs | 07:30–08:00 | 08:00–09:00 |
| 2000 VUs | 09:00–09:30 | 09:30–10:30 |
| 2200 VUs | 10:30–11:00 | 11:00–12:00 |
| 2400 VUs | 12:00–12:30 | 12:30–13:30 |
| 2600 VUs | 13:30–14:00 | 14:00–15:00 |
| 2800 VUs | 15:00–15:30 | 15:30–16:30 |
| Recovery 50 VUs | Giảm tải mục tiêu 0s | 16:30–17:30 |

Tổng profile 17m30s, grace period 30s. Profile thực đo tương đương run trước tune; không thay bằng profile script hiện tại nếu đã chỉnh sửa sau run. Phase gắn lúc request bắt đầu, raw point khi hoàn tất; RPS plateau/recovery = count/60s, không dùng `rate` submetric (mẫu số toàn run). Đây không phải completion throughput thuần trong cùng cửa sổ. Iteration cũ có thể tiếp tục sau khi target giảm về 50 VUs.

## 4. Kết quả

### 4.1 Toàn run, gồm ramp và recovery

| Chỉ số | Kết quả |
|---|---:|
| HTTP requests | 588550 |
| Request không lỗi / lỗi | 588150 / 400 |
| HTTP error rate | 0.068% |
| Checks đạt / thất bại | 1176300 / 800 |
| Checks success rate | 99.932% |
| Iterations hoàn tất / interrupted | 585750 / 0 theo log |
| Throughput toàn run | 558.077 requests/s |
| Latency avg / p50 (ms) | 73.075 / 1.321 |
| p90 / p95 / p99 / max (ms) | 10.231 / 104.219 / 1512.265 / 10001.525 |
| Login attempts | 2801 |
| Nghiệp vụ skipped vì Login lỗi | 1 |

`http_req_failed.passes` là số mẫu lỗi, `fails` là số mẫu không lỗi; không nhầm với checks. 800 checks lỗi không phải 800 HTTP lỗi. Requests nghiệp vụ = 588550 − 2801 = 585749, bằng iterations trừ 1 skipped. Chưa phân loại HTTP status/error code hoặc nguyên nhân lỗi.

### 4.2 Theo bậc tải và recovery

| Phase | Requests | RPS | p95 (ms) | p99 (ms) | HTTP lỗi | Checks đạt | Skipped | Kết quả |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| hold_500 | 11008 | 183.467 | 4.783 | 8.339 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_750 | 16363 | 272.717 | 3.996 | 6.224 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_1000 | 21838 | 363.967 | 3.974 | 5.812 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_1250 | 26725 | 445.417 | 42.374 | 1988.659 | 11 (0.041%) | 99.959% | 0 | PASS |
| hold_1500 | 32459 | 540.983 | 4.556 | 1313.316 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_1750 | 38116 | 635.267 | 3.997 | 7.018 | 1 (0.003%) | 99.997% | 0 | PASS |
| hold_2000 | 43631 | 727.183 | 4.886 | 14.986 | 1 (0.002%) | 99.998% | 0 | PASS |
| hold_2200 | 47787 | 796.450 | 10.766 | 565.043 | 8 (0.017%) | 99.983% | 0 | PASS |
| hold_2400 | 52452 | 874.200 | 4.191 | 13.593 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_2600 | 56101 | 935.017 | 7.590 | 880.764 | 11 (0.020%) | 99.980% | 0 | PASS |
| hold_2800 | 49022 | 817.033 | 5288.187 | 8115.167 | 292 (0.596%) | 99.404% | 0 | FAIL |
| recovery_1 | 1094 | 18.233 | 9.986 | 10.903 | 0 (0.000%) | 100.000% | 0 | PASS |

Ngoài plateau/recovery, các ramp có tổng 76 HTTP lỗi và 1 skipped (suy ra hiệu giữa tổng run và các cửa sổ hold/recovery). Không bỏ qua lỗi ramp khi diễn giải toàn bài. p95 toàn run đạt 500 ms không thay thế được SLO từng phase.

### 4.3 Chi tiết API

| Phase | API | Requests | p95 (ms) | HTTP lỗi (%) | Checks đạt (%) |
|---|---|---:|---:|---:|---:|
| hold_500 | search | 4339 | 3.466 | 0.000 | 100.000 |
| hold_500 | detail | 2204 | 3.772 | 0.000 | 100.000 |
| hold_500 | cart | 2481 | 2.309 | 0.000 | 100.000 |
| hold_500 | checkout | 1924 | 7.959 | 0.000 | 100.000 |
| hold_750 | search | 6558 | 3.300 | 0.000 | 100.000 |
| hold_750 | detail | 3316 | 3.335 | 0.000 | 100.000 |
| hold_750 | cart | 3542 | 2.096 | 0.000 | 100.000 |
| hold_750 | checkout | 2913 | 5.252 | 0.000 | 100.000 |
| hold_1000 | search | 8619 | 3.492 | 0.000 | 100.000 |
| hold_1000 | detail | 4361 | 3.680 | 0.000 | 100.000 |
| hold_1000 | cart | 4909 | 2.073 | 0.000 | 100.000 |
| hold_1000 | checkout | 3920 | 5.077 | 0.000 | 100.000 |
| hold_1250 | search | 10704 | 57.386 | 0.000 | 100.000 |
| hold_1250 | detail | 5150 | 71.731 | 0.000 | 100.000 |
| hold_1250 | cart | 5990 | 13.920 | 0.100 | 99.900 |
| hold_1250 | checkout | 4850 | 53.161 | 0.103 | 99.897 |
| hold_1500 | search | 13060 | 4.769 | 0.000 | 100.000 |
| hold_1500 | detail | 6381 | 4.954 | 0.000 | 100.000 |
| hold_1500 | cart | 7121 | 1.961 | 0.000 | 100.000 |
| hold_1500 | checkout | 5868 | 6.208 | 0.000 | 100.000 |
| hold_1750 | search | 15154 | 3.668 | 0.000 | 100.000 |
| hold_1750 | detail | 7658 | 3.809 | 0.000 | 100.000 |
| hold_1750 | cart | 8372 | 2.001 | 0.012 | 99.988 |
| hold_1750 | checkout | 6898 | 5.323 | 0.000 | 100.000 |
| hold_2000 | search | 17403 | 4.700 | 0.000 | 100.000 |
| hold_2000 | detail | 8460 | 5.116 | 0.000 | 100.000 |
| hold_2000 | cart | 9735 | 2.240 | 0.000 | 100.000 |
| hold_2000 | checkout | 8004 | 7.411 | 0.012 | 99.988 |
| hold_2200 | search | 19169 | 10.487 | 0.000 | 100.000 |
| hold_2200 | detail | 9571 | 11.319 | 0.000 | 100.000 |
| hold_2200 | cart | 10489 | 4.597 | 0.029 | 99.971 |
| hold_2200 | checkout | 8542 | 13.338 | 0.059 | 99.941 |
| hold_2400 | search | 20836 | 4.110 | 0.000 | 100.000 |
| hold_2400 | detail | 10516 | 4.176 | 0.000 | 100.000 |
| hold_2400 | cart | 11758 | 2.087 | 0.000 | 100.000 |
| hold_2400 | checkout | 9314 | 5.579 | 0.000 | 100.000 |
| hold_2600 | search | 22494 | 7.809 | 0.000 | 100.000 |
| hold_2600 | detail | 11149 | 8.254 | 0.000 | 100.000 |
| hold_2600 | cart | 12221 | 3.638 | 0.041 | 99.959 |
| hold_2600 | checkout | 10217 | 13.146 | 0.059 | 99.941 |
| hold_2800 | search | 19603 | 6796.876 | 0.587 | 99.413 |
| hold_2800 | detail | 9761 | 6813.620 | 0.410 | 99.590 |
| hold_2800 | cart | 10875 | 2540.743 | 0.726 | 99.274 |
| hold_2800 | checkout | 8751 | 6712.716 | 0.663 | 99.337 |
| recovery_1 | search | 450 | 2.857 | 0.000 | 100.000 |
| recovery_1 | detail | 222 | 2.811 | 0.000 | 100.000 |
| recovery_1 | cart | 234 | 2.466 | 0.000 | 100.000 |
| recovery_1 | checkout | 188 | 10.922 | 0.000 | 100.000 |

### 4.4 Ngưỡng quan sát và recovery

Bậc đầu vi phạm là **2800 VUs**: tổng và bốn API đều fail p95; HTTP lỗi/checks/count/skipped của bậc này vẫn đạt. Các plateau trước đó (500–2600) đạt tất cả thresholds. Khoảng chuyển tiếp quan sát đầu tiên là **trên 2600 đến 2800 VUs**, chưa xác định điểm chính xác trong ramp hoặc mức tải bền vững. PASS không đồng nghĩa không có lỗi: một số bậc có lỗi dưới 1%.

Recovery có 1094 request, không HTTP lỗi, checks 100%, không skipped, p95 tổng 9.986 ms; mọi API có mẫu và đạt SLO. Chỉ kết luận đạt trong cửa sổ request bắt đầu ở recovery 60s, không khẳng định thời gian phục hồi chính xác, hết backlog hoặc ổn định dài hạn. Không có bằng chứng crash hay nguyên nhân bottleneck từ summary/log kết thúc.

## 5. Tài nguyên người thực hiện quan sát

Số liệu máy dùng chung tại từng mức tải, không phải avg/max tính từ telemetry hoặc RSS riêng backend/k6.

| VUs | Memory GB / 7.12 GB | Memory (%) | Swap GB / 8.59 GB | CPU |
|---|---:|---:|---:|---|
| 500 | 4.02 | 56 | 1.52 (18%) | 6–9% |
| 750 | 4.22 | 59 | 1.52 (18%) | 5–7% |
| 1000 | 4.21 | 59 | 1.52 (18%) | 8–12% |
| 1250 | 4.22 | 59 | 1.52 (18%) | 9–11% |
| 1500 | 4.30 | 60 | 1.52 (18%) | 9–13% |
| 1750 | 4.19 | 59 | 1.52 (18%) | 10–11%, đôi khi 18% |
| 2000 | 4.25 | 60 | 1.54 (18%) | 12–13%, đôi khi 23% |
| 2200 | 4.24 | 60 | 1.54 (18%) | 11–13% |
| 2400 | 4.31 | 61 | 1.57 (18%) | 12–13% |
| 2600 | 4.31 | 61 | 1.57 (18%) | 12–13% |
| 2800 | 4.73 | 66 | 1.52 (18%) | 8–9% |

RAM quan sát tăng từ 56% tại 500 lên 66% tại 2800; Swap khoảng 1.52–1.57 GB. CPU thấp hơn tại bậc fail 2800 không chứng minh hệ thống dư năng lực: CPU toàn máy có thể che khuất một core/luồng bị nghẽn hoặc thời gian chờ I/O. Chưa đo swap-in/out, disk I/O, event-loop lag, DB locks và từng process/core nên không kết luận nguyên nhân từ bảng này.

Thông tin baseline (RAM 49%, Swap 6%, CPU 2–5%) và spike (RAM 51%, Swap 18%, CPU 9–14%) thuộc các run riêng; dùng làm bối cảnh, không coi là các mẫu thời gian liên tục của stress. Run stress trước tune không có telemetry tương ứng để so sánh tài nguyên.

## 6. So sánh ngắn trước/sau tune

Reference: [stress trước tune](03-stress-test-report.md), run `stress-20261022-181718-lx8F4c`; cùng bậc tải và hold 60s.

| VUs | p95 trước (ms) | p95 sau (ms) | RPS trước | RPS sau | HTTP lỗi trước (%) | HTTP lỗi sau (%) |
|---|---:|---:|---:|---:|---:|---:|
| 500 | 8.353 | 4.783 | 182.217 | 183.467 | 0.009 | 0.000 |
| 750 | 8.609 | 3.996 | 271.417 | 272.717 | 0.006 | 0.000 |
| 1000 | 8.622 | 3.974 | 365.367 | 363.967 | 0.000 | 0.000 |
| 1250 | 11.083 | 42.374 | 453.267 | 445.417 | 0.004 | 0.041 |
| 1500 | 5380.450 | 4.556 | 365.367 | 540.983 | 2.659 | 0.000 |
| 1750 | 43.271 | 3.997 | 633.533 | 635.267 | 0.000 | 0.003 |
| 2000 | 272.740 | 4.886 | 714.500 | 727.183 | 0.023 | 0.002 |
| 2200 | 4955.390 | 10.766 | 553.867 | 796.450 | 3.482 | 0.017 |
| 2400 | 268.208 | 4.191 | 860.017 | 874.200 | 0.029 | 0.000 |
| 2600 | 10000.070 | 7.590 | 324.383 | 935.017 | 37.774 | 0.020 |
| 2800 | 815.113 | 5288.187 | 963.183 | 817.033 | 0.121 | 0.596 |

Bậc fail đầu tiên chuyển từ 1500 sang 2800 VUs; số điều kiện vi phạm giảm 51 xuống 5, HTTP lỗi toàn run giảm 10010 xuống 400, skipped giảm 126 xuống 1. Tuy vậy, **p95 tại 2800 sau tune cao hơn trước tune** (5288.187 so với 815.11 ms); ở 1250 cũng tăng. Không kết luận cải thiện đồng đều hoặc coi 2800 là công suất đảm bảo. Trước tune đã có diễn biến xen kẽ PASS/FAIL theo bậc.

WAL/index là thay đổi dự kiến, chưa tách được đóng góp từng yếu tố. `LIKE '%keyword%'` vẫn full-scan với index này; WAL vẫn chỉ có một writer. Hai run riêng, thiếu snapshot/build/monitoring đồng bộ và chưa chạy lặp nên không quy toàn bộ khác biệt cho tuning.

## 7. Kết luận và khuyến nghị

**FAIL toàn bài do latency tại 2800 VUs; 247/252 thresholds đạt.** Các bậc 500–2600 và recovery đạt mọi ngưỡng cấu hình. Kết quả tốt hơn reference về bậc fail đầu, tổng lỗi và skipped, nhưng có regression latency ở đỉnh 2800.

Ưu tiên chạy lặp quanh 2600–2800, giữ dữ liệu/build/profile tương đương, kéo dài hold và recovery; thu CPU từng core/process, event-loop, DB latency/locks, swap/disk I/O và logs server. Kiểm tra toàn vẹn thao tác ghi lỗi trước khi retry. Chưa xác nhận tải tối đa production, crash, tự phục hồi hoặc toàn vẹn DB.

Biểu đồ đối chiếu ba loại test: [tuned_baseline_report.html](tuned_baseline_report.html).
