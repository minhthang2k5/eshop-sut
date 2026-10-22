# Stress Test Report – eshop-sut – 2026-10-22

> **Từ ngưỡng 1.500 VUs, ứng dụng bắt đầu hoạt động không ổn định trong môi trường thử nghiệm chung máy này.** Các bậc 500–1.250 VUs đạt mọi SLO; tại 1.500 VUs, p95 tăng lên 5.380,45 ms và error rate 2,659%. Những bậc cao hơn xen kẽ đạt/không đạt, thể hiện bất ổn chứ không phải hệ thống luôn lỗi ở mọi tải từ 1.500 trở lên. Recovery 1 phút ở 50 VUs đạt SLO.

## 1. Metadata và bằng chứng

| Trường | Giá trị |
|---|---|
| Run ID | stress-20261022-181718-lx8F4c |
| Ngày theo thư mục | 22/10/2026; summary không chứa timestamp bắt đầu/kết thúc |
| Nguồn | [summary.json](../output/stress-20261022-181718-lx8F4c/summary.json) |
| Môi trường | k6 và server chung một máy |
| Profile | 11 bậc 500–2.800 VUs; ramp 30s + giữ 60s/bậc; recovery 60s |
| Lịch tải / thời lượng suy ra count/rate | 17m30s / khoảng 1.054,91s (17m34,91s) |
| Công cụ / build / endpoint | Phiên bản k6, SUT và BASE_URL thực tế không có trong summary |
| Cấu hình tham chiếu | [stress.js](../stress.js), [run-stress.sh](../run-stress.sh); chưa có snapshot gắn với run |

Báo cáo chỉ dùng summary.json cho các kết quả định lượng, không suy diễn loại lỗi/status, thời điểm lỗi hoặc crash từ nguồn này. Các lần chạy cũ khác profile/môi trường không được gộp vào số liệu hiện tại.

## 2. Mục tiêu và tiêu chí

Xác định mức tải bắt đầu gây bất ổn, mức suy giảm và trạng thái sau giảm tải. Phạm vi gồm Search, Detail, Cart, Checkout và lazy Login.

| Tiêu chí | Ngưỡng | Phạm vi |
|---|---|---|
| HTTP latency p95 | < 500 ms | Mỗi plateau/recovery, tổng hợp và từng API nghiệp vụ |
| HTTP error rate | < 1% | Như trên |
| Checks thành công | >= 99% | Status và nội dung response |
| Request count | > 0 | Mỗi cửa sổ và từng API nghiệp vụ |
| Nghiệp vụ skipped do login | = 0 | Mỗi plateau/recovery |

Nguồn latency/error SLO: [Tool Analysis and Theory](../../../../4_ZipTool/Tool_Analysis_and_Theory.md). Login nằm trong tổng phase nếu phát sinh và có thống kê riêng. Ramp không có threshold riêng; summary không xác định VUs/thời điểm chính xác khi vượt SLO trong ramp.

**Entry:** đủ mẫu Login và bốn API; chưa có bằng chứng smoke trước chạy hoặc DB ban đầu. **Exit:** 521.600 iterations hoàn thành, có dữ liệu recovery; **51 threshold thất bại, 201 đạt, tổng 252**. Summary không xác nhận exit code hoặc số iteration gián đoạn.

## 3. Môi trường và tài nguyên

Load generator và server chạy chung host. Chưa có telemetry CPU/RAM/swap, CPU từng core/process, DB locks, disk I/O, event-loop lag hoặc socket limits của run này; không tái sử dụng số tài nguyên cũ. Vì k6 và backend có thể cạnh tranh tài nguyên, ngưỡng 1.500 VUs là nhận định trong cấu hình thử nghiệm hiện tại, chưa đại diện cho công suất backend độc lập hoặc production.

50 tài khoản chia sẻ vòng tròn, tối đa 56 VUs/tài khoản ở 2.800 VUs. Chưa có cấu hình phần cứng, build và trạng thái DB được lưu cùng summary để tái lập đầy đủ.

## 4. Workload và profile

Closed model `ramping-vus`; mỗi iteration chọn một nghiệp vụ, nghỉ sau request kể cả khi lỗi:

| API | Mix Black Friday | Think-time |
|---|---:|---:|
| Search | 40% | 1–3s |
| Detail | 20% | 2–5s |
| Cart | 22% | 1–3s |
| Checkout | 18% | 3–6s |

Lazy Login trước API cần xác thực nếu VU chưa có token; token riêng VU. Login lỗi thì skip nghiệp vụ, vẫn nghỉ. Không retry write tự động. SUT hiện tạo đơn độc lập với nội dung giỏ hàng; mix API không đồng nghĩa giao dịch mua hàng end-to-end có giỏ riêng từng VU.

| Thời gian scenario | VUs | Phase |
|---|---|---|
| 00:00–00:30 | 0→500 | ramp_500 |
| 00:30–01:30 | 500 | hold_500 |
| 01:30–02:00 | 500→750 | ramp_750 |
| 02:00–03:00 | 750 | hold_750 |
| 03:00–03:30 | 750→1000 | ramp_1000 |
| 03:30–04:30 | 1000 | hold_1000 |
| 04:30–05:00 | 1000→1250 | ramp_1250 |
| 05:00–06:00 | 1250 | hold_1250 |
| 06:00–06:30 | 1250→1500 | ramp_1500 |
| 06:30–07:30 | 1500 | hold_1500 |
| 07:30–08:00 | 1500→1750 | ramp_1750 |
| 08:00–09:00 | 1750 | hold_1750 |
| 09:00–09:30 | 1750→2000 | ramp_2000 |
| 09:30–10:30 | 2000 | hold_2000 |
| 10:30–11:00 | 2000→2200 | ramp_2200 |
| 11:00–12:00 | 2200 | hold_2200 |
| 12:00–12:30 | 2200→2400 | ramp_2400 |
| 12:30–13:30 | 2400 | hold_2400 |
| 13:30–14:00 | 2400→2600 | ramp_2600 |
| 14:00–15:00 | 2600 | hold_2600 |
| 15:00–15:30 | 2600→2800 | ramp_2800 |
| 15:30–16:30 | 2800 | hold_2800 |
| 16:30–17:30 | 50 | recovery_1 |

Tổng 17m30s, tối đa thêm 30s gracefulStop. Giảm về 50 dùng stage 0s; gracefulRampDown 30s cho iteration đang chạy hoàn tất. Phase gắn theo lúc request bắt đầu; request cũ hoàn tất trong recovery vẫn thuộc phase cũ. Mỗi plateau/recovery dài 60s, RPS cửa sổ = count/60.

## 5. Kết quả

### 5.1 Tổng quan

| Chỉ số | Giá trị |
|---|---:|
| HTTP requests | 524.400 |
| Request không lỗi / lỗi theo k6 | 514.390 / 10.010 |
| HTTP error rate | 1,909% |
| Checks đạt / thất bại | 1.028.780 / 20.020 |
| Check success rate | 98,091% |
| Iterations hoàn thành | 521.600 |
| VUs cực đại | 2.800 |
| Throughput toàn bài | 497,10 requests/s |
| Latency avg / median | 289,27 / 3,21 ms |
| Latency p90 / p95 / p99 | 417,00 / 1.749,33 / 6.448,43 ms |
| Latency max | 10.005,74 ms |
| Login attempts | 2.926 |
| Login không lỗi / lỗi | 2.800 / 126 |
| Nghiệp vụ skipped vì login | 126 |

Trong metric `http_req_failed`, `passes` đếm mẫu lỗi và `fails` đếm mẫu không lỗi. Không nhầm với checks. Summary không phân loại status/error code nên không khẳng định 10.010 lỗi là timeout hay connection reset.

524.400 − 2.926 = **521.474 request nghiệp vụ**, bằng 521.600 iterations trừ 126 skipped. Mix ngẫu nhiên có thể lệch trong mẫu hữu hạn và bị ảnh hưởng khi login lỗi.

### 5.2 Theo bậc tải và recovery

| Phase | Request | RPS | p95 ms | p99 ms | HTTP lỗi | Checks đạt | Skipped | Kết quả |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| hold_500 | 10,933 | 182.22 | 8.35 | 12.70 | 1 (0.009%) | 99.991% | 0 | PASS |
| hold_750 | 16,285 | 271.42 | 8.61 | 14.38 | 1 (0.006%) | 99.994% | 0 | PASS |
| hold_1000 | 21,922 | 365.37 | 8.62 | 14.34 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_1250 | 27,196 | 453.27 | 11.08 | 25.83 | 1 (0.004%) | 99.996% | 0 | PASS |
| hold_1500 | 21,922 | 365.37 | 5380.45 | 9999.62 | 583 (2.659%) | 97.341% | 0 | FAIL |
| hold_1750 | 38,012 | 633.53 | 43.27 | 116.08 | 0 (0.000%) | 100.000% | 0 | PASS |
| hold_2000 | 42,870 | 714.50 | 272.74 | 935.95 | 10 (0.023%) | 99.977% | 0 | PASS |
| hold_2200 | 33,232 | 553.87 | 4955.39 | 6794.84 | 1,157 (3.482%) | 96.518% | 101 | FAIL |
| hold_2400 | 51,601 | 860.02 | 268.21 | 486.28 | 15 (0.029%) | 99.971% | 0 | PASS |
| hold_2600 | 19,463 | 324.38 | 10000.07 | 10000.90 | 7,352 (37.774%) | 62.226% | 14 | FAIL |
| hold_2800 | 57,791 | 963.18 | 815.11 | 2156.68 | 70 (0.121%) | 99.879% | 0 | FAIL |
| recovery_1 | 1,079 | 17.98 | 15.03 | 93.50 | 0 (0.000%) | 100.000% | 0 | PASS |

Không lấy trường `rate` toàn bài của submetric làm RPS riêng phase. Plateau fail là **1.500, 2.200, 2.600, 2.800 VUs**; tất cả plateau còn lại và recovery đạt mọi threshold.

### 5.3 Chi tiết API

| Phase | API | Request | p95 ms | HTTP lỗi % |
|---|---|---:|---:|---:|
| hold_500 | search | 4,299 | 6.20 | 0.000% |
| hold_500 | detail | 2,175 | 7.27 | 0.000% |
| hold_500 | cart | 2,384 | 2.39 | 0.042% |
| hold_500 | checkout | 2,010 | 11.89 | 0.000% |
| hold_750 | search | 6,461 | 7.23 | 0.000% |
| hold_750 | detail | 3,232 | 7.65 | 0.000% |
| hold_750 | cart | 3,582 | 2.38 | 0.000% |
| hold_750 | checkout | 2,976 | 13.00 | 0.034% |
| hold_1000 | search | 8,721 | 7.56 | 0.000% |
| hold_1000 | detail | 4,352 | 8.15 | 0.000% |
| hold_1000 | cart | 4,926 | 2.61 | 0.000% |
| hold_1000 | checkout | 3,888 | 12.26 | 0.000% |
| hold_1250 | search | 10,806 | 10.67 | 0.000% |
| hold_1250 | detail | 5,541 | 10.76 | 0.000% |
| hold_1250 | cart | 5,908 | 3.44 | 0.000% |
| hold_1250 | checkout | 4,911 | 15.13 | 0.020% |
| hold_1500 | search | 8,733 | 5707.60 | 2.508% |
| hold_1500 | detail | 4,399 | 5693.18 | 2.523% |
| hold_1500 | cart | 4,893 | 1699.79 | 2.739% |
| hold_1500 | checkout | 3,871 | 5337.58 | 3.074% |
| hold_1750 | search | 15,082 | 46.27 | 0.000% |
| hold_1750 | detail | 7,589 | 48.17 | 0.000% |
| hold_1750 | cart | 8,372 | 18.87 | 0.000% |
| hold_1750 | checkout | 6,940 | 52.71 | 0.000% |
| hold_2000 | search | 17,025 | 328.03 | 0.000% |
| hold_2000 | detail | 8,688 | 353.81 | 0.000% |
| hold_2000 | cart | 9,405 | 119.11 | 0.074% |
| hold_2000 | checkout | 7,718 | 334.20 | 0.039% |
| hold_2200 | search | 13,245 | 5203.35 | 3.088% |
| hold_2200 | detail | 6,722 | 5250.79 | 3.675% |
| hold_2200 | cart | 7,197 | 2030.92 | 3.390% |
| hold_2200 | checkout | 5,897 | 5128.67 | 3.375% |
| hold_2400 | search | 20,737 | 293.56 | 0.000% |
| hold_2400 | detail | 10,248 | 295.66 | 0.000% |
| hold_2400 | cart | 11,272 | 114.89 | 0.080% |
| hold_2400 | checkout | 9,310 | 307.79 | 0.064% |
| hold_2600 | search | 7,860 | 10000.26 | 38.753% |
| hold_2600 | detail | 3,805 | 10000.27 | 38.844% |
| hold_2600 | cart | 4,306 | 5648.73 | 34.138% |
| hold_2600 | checkout | 3,462 | 9917.64 | 38.879% |
| hold_2800 | search | 23,258 | 896.88 | 0.000% |
| hold_2800 | detail | 11,503 | 916.47 | 0.000% |
| hold_2800 | cart | 12,689 | 354.84 | 0.284% |
| hold_2800 | checkout | 10,314 | 865.16 | 0.330% |
| recovery_1 | search | 449 | 2.97 | 0.000% |
| recovery_1 | detail | 181 | 3.16 | 0.000% |
| recovery_1 | cart | 228 | 2.42 | 0.000% |
| recovery_1 | checkout | 221 | 16.71 | 0.000% |

Tại 1.500, 2.200 và 2.600 VUs, cả bốn API đều vi phạm latency/error SLO. Ở 2.800, Search/Detail/Checkout vượt p95 500 ms, Cart vẫn đạt; error các API đều dưới 1% nhưng toàn bậc vẫn fail latency.

### 5.4 Ngưỡng bắt đầu bất ổn

**Kết luận của run này: từ 1.500 VUs, ứng dụng bắt đầu hoạt động không ổn định.** Bằng chứng là các plateau 500, 750, 1.000 và 1.250 đạt SLO, sau đó tại 1.500 p95 tăng từ 11,08 ms (1.250) lên **5.380,45 ms**, error **2,659%** (583/21.922 request), checks còn **97,341%**. Đây là bậc vi phạm đầu tiên quan sát được; khoảng chuyển tiếp đầu tiên là **trên 1.250 đến 1.500 VUs**, chưa đo VUs chính xác bên trong khoảng này.

Ở các bậc sau, 1.750 và 2.000 đạt; 2.200 fail; 2.400 đạt; 2.600 và 2.800 fail. Cụm từ “bắt đầu không ổn định từ 1.500” biểu thị các đợt suy giảm xen kẽ khi tiếp tục tăng tải, không khẳng định mọi mức cao hơn đều fail hoặc ứng dụng crash tại 1.500.

**2.600 VUs suy giảm nặng nhất:** p95 **10.000,07 ms**, lỗi **37,774%** (7.352/19.463 request), 14 skipped. Vẫn có 12.111 request không lỗi (62,226%). Sang 2.800, error giảm còn 0,121% nhưng p95 815,11 ms vẫn vượt SLO. Không có bằng chứng process chết/OOM từ summary.

Các đợt suy giảm có thể liên quan khởi động/login, hàng đợi, trạng thái DB hoặc tranh chấp tài nguyên chung máy; chưa đủ bằng chứng xác nhận nguyên nhân. Cần kiểm tra lặp lại trước khi xem ngưỡng quan sát này là giới hạn công suất cố định.

## 6. Recovery và kết luận

Sau giảm về 50 VUs, **1.079 request không lỗi**, checks **100%**, skipped **0**, RPS **17,98**. p95 **15,03 ms**, p99 **93,50 ms**, mọi API có mẫu và đạt threshold; p95 Checkout cao nhất **16,71 ms**.

Hệ thống **đạt lại SLO trong cửa sổ quan sát 1 phút sau giảm tải**. Không xác định thời gian hồi phục chính xác từ percentile cả phút; các request bắt đầu ở phase cũ vẫn được thống kê theo phase cũ. Chưa có xác nhận về can thiệp thủ công nên chưa kết luận tự phục hồi; chưa chứng minh ổn định lâu dài hoặc toàn vẹn dữ liệu đơn hàng.

| Tiêu chí | Kết quả |
|---|---|
| Threshold toàn bài | FAIL: 51/252 threshold không đạt |
| Vùng tải thấp 500–1.250 VUs | Đạt mọi SLO trong các plateau đã đo |
| Ngưỡng bắt đầu hoạt động không ổn định | 1.500 VUs, bậc đầu vi phạm SLO |
| Diễn biến trên ngưỡng | Xen kẽ đạt/không đạt; chưa có ngưỡng công suất cố định |
| Recovery 50 VUs / 60s | PASS trong cửa sổ quan sát |
| Crash / bottleneck / tự phục hồi / toàn vẹn DB | Chưa xác minh |

**Kết luận chung:** trong môi trường chung máy của lần thử này, ứng dụng bắt đầu hoạt động không ổn định từ **1.500 VUs**; suy giảm nghiêm trọng nhất tại 2.600 VUs và đạt lại SLO sau giảm tải trong phút quan sát.

## 7. Hạn chế và khuyến nghị

- Chỉ dùng summary, không xác định nguyên nhân, mã lỗi hoặc thời điểm vi phạm trong ramp.
- Máy phát tải và server chung host; chưa có telemetry từng process/core để phân biệt nghẽn k6, backend, DB hay hệ điều hành.
- Plateau 60s có thể chưa đạt trạng thái ổn định; 50 tài khoản dùng chung, dữ liệu DB tích lũy và closed model có think-time ảnh hưởng tính đại diện.
- Kiểm chứng lặp lại các mức quanh 1.250–1.500 và giữ cố định 1.500 lâu hơn sau warm-up, theo dõi tài nguyên, để đánh giá ngưỡng bắt đầu bất ổn có tái diễn không.
- Ghi can thiệp và kéo dài recovery nếu cần chứng minh tự phục hồi bền vững; đối soát DB nếu đánh giá toàn vẹn dữ liệu.

## 8. Phụ lục

- [Summary hiện tại](../output/stress-20261022-181718-lx8F4c/summary.json): nguồn định lượng duy nhất.
- [README](../README.md), [script](../stress.js), [runner](../run-stress.sh), [CSV](../data/test_accounts.csv).

Chỉ cập nhật tài liệu, không chạy lại tải hay thay đổi ứng dụng.
