# Spike Test Report – eShop sau tune database (D8a)

> **PASS — spike 50 → 1500 VUs (30×), một lần đo.** Tất cả 63/63 thresholds đạt. Đỉnh tải có p95 6.849 ms, HTTP lỗi 0%, checks 100%, không skipped. Recovery 60 giây đạt SLO; chưa đánh giá độ lặp lại hoặc ổn định dài hạn.

## 1. Metadata và bằng chứng

| Trường | Giá trị |
|---|---|
| Run ID | `spike-20261023-085706-BOOKoc` |
| Ngày / múi giờ | 23/10/2026, UTC+07:00 |
| Thời gian | Khoảng 08:57:06–08:59:41; profile 150s, log kết thúc sau 2m34.4s |
| Công cụ | k6 local; chưa lưu phiên bản |
| SUT | Tuned database theo người thực hiện; mã hiện tại tại `tuned-backend/` |
| Thay đổi dự kiến | WAL và `idx_products_name ON products(name)` trong `tuned-backend/database.js` |
| Phiên bản / snapshot | Chưa lưu checksum source, phiên bản Node.js/SQLite hoặc snapshot DB kèm run |
| Người thực hiện | Người dùng chạy test; chưa cung cấp tên |
| Script / runner | [spike.js](../spike.js), [run-spike.sh](../run-spike.sh) |
| Bằng chứng | [Summary](../output/spike-20261023-085706-BOOKoc/summary.json), [log](../output/spike-20261023-085706-BOOKoc/k6.log), [raw metrics](../output/spike-20261023-085706-BOOKoc/metrics.json) |

Báo cáo phân tích kết quả đã có, không chạy lại tải. Cấu hình WAL/index được mô tả theo mã nguồn và thông tin người thực hiện; HTTP artifacts không xác nhận trực tiếp journal mode/index tại thời điểm chạy. Summary export dùng `thresholds: false` cho điều kiện không bị vi phạm; đối chiếu kết quả đạt trong log, không diễn giải giá trị này thành FAIL. Mã thoát shell không được lưu riêng.

## 2. Mục tiêu và tiêu chí

Đánh giá suy giảm ở đỉnh tải đột ngột và khả năng phục hồi sau giảm tải, trên Search, Detail, Cart, Checkout cùng lazy Login. Không đo browser rendering hoặc hành trình mua hàng end-to-end.

| Tiêu chí | Ngưỡng | Phạm vi |
|---|---|---|
| Latency p95 | <500 ms | Tổng và từng API nghiệp vụ trong mỗi phase |
| HTTP lỗi | <1% | Như trên |
| Checks đạt | ≥99% | Như trên, status và nội dung response |
| Request count | >0 | Tổng và từng API nghiệp vụ trong mỗi phase |
| Nghiệp vụ skipped | =0 | Mỗi phase |

Login có thống kê riêng, tính vào tổng phase nhưng không có SLO riêng. Không đặt ngưỡng CPU/RAM/RPS. Có mẫu cả năm API; chưa có log smoke hoặc trạng thái DB ban đầu kèm run. Exit: hoàn tất profile và recovery, đánh giá tất cả 63 thresholds.

## 3. Workload và profile

Closed model `ramping-vus`; một spike, stage tăng/giảm tải 0s:

| Thời gian scenario | VUs | Phase | Cửa sổ |
|---|---:|---|---:|
| [0,30) s | 50 | hold_50 | 30s |
| [30,90) s | 1500 | hold_1500 | 60s |
| [90,150) s | 50 | recovery_1 | 60s |

Graceful ramp-down/stop 30s cho iteration đang chạy hoàn tất; VUs thực tế có thể chưa giảm ngay về 50 khi target thay đổi.

| API | Mix nghiệp vụ | Think time |
|---|---:|---|
| Search | 40% | 1–3s |
| Detail | 20% | 2–5s |
| Cart | 22% | 1–3s |
| Checkout | 18% | 3–6s |

Mỗi iteration chọn một nghiệp vụ, lazy login khi cần token rồi sleep; Login là lưu lượng bổ sung. 50 tài khoản CSV được chia vòng tròn, tối đa 30 VUs/tài khoản ở đỉnh; token riêng VU. Dữ liệu sản phẩm cố định, không đại diện toàn bộ dữ liệu/cache production.

Phase chốt theo lúc bắt đầu request; raw point ghi khi request kết thúc. RPS phase = count / 30 hoặc 60s, không dùng `rate` submetric trong summary (mẫu số là toàn run). Đây là tốc độ của nhóm request bắt đầu trong phase, không phải completion throughput thuần trong cùng cửa sổ.

## 4. Kết quả

### 4.1 Toàn run

| Chỉ số | Kết quả |
|---|---:|
| HTTP requests / lỗi | 36292 / 0 |
| Throughput toàn run | 235.013 requests/s |
| Checks đạt | 72584/72584 (100%) |
| Iterations hoàn tất / interrupted | 34792 / 0 |
| VUs cực đại | 1500 |
| Latency avg / p50 (ms) | 8.032 / 1.336 |
| p90 / p95 / p99 / max (ms) | 3.927 / 8.353 / 225.945 / 289.729 |
| Login attempts / lỗi | 1500 / 0 |
| Login p95 (ms) | 260.504 |
| Business requests skipped | 0 |
| Received / sent | 14455371 / 7843695 bytes |

Raw metrics ghi nhận toàn bộ 36292 HTTP response có status 200; không có 4xx/5xx, status 0 hoặc error code. Không ghi nhận timeout/reset hay check status/body thất bại. `http_req_failed.passes` là số request lỗi, không phải số thành công; `fails` là số không thỏa điều kiện failed.

### 4.2 Trước / trong / sau spike

| Chỉ số | Trước: 50 VUs / 30s | Trong: 1500 VUs / 60s | Sau: 50 VUs / 60s |
|---|---:|---:|---:|
| HTTP requests | 622 | 34579 | 1091 |
| Latency avg (ms) | 5.288 | 8.247 | 2.804 |
| Latency p50 (ms) | 2.381 | 1.306 | 1.953 |
| Latency p90 (ms) | 10.854 | 3.822 | 7.782 |
| Latency p95 (ms) | 24.773 | 6.849 | 9.599 |
| Latency p99 (ms) | 40.787 | 229.232 | 10.520 |
| Latency max (ms) | 43.001 | 289.729 | 11.619 |
| RPS tổng | 20.733 | 576.317 | 18.183 |
| HTTP lỗi | 0% | 0% | 0% |
| Checks đạt | 100% | 100% | 100% |
| Skipped | 0 | 0 | 0 |
| Thresholds đạt | 21/21 | 21/21 | 21/21 |

Login trước/trong/sau: 50 / 1450 / 0. RPS nghiệp vụ loại Login lần lượt 19.067 / 552.150 / 18.183. Không so sánh RPS tổng mà bỏ qua làn sóng Login bổ sung; đây là mô hình tải theo VUs, không phải arrival rate cố định.

### 4.3 API trong spike

| API | Requests | RPS / 60s | p50 (ms) | p95 (ms) | p99 (ms) | HTTP lỗi | Checks | SLO |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Search | 13201 | 220.017 | 1.199 | 6.393 | 234.378 | 0% | 100% | PASS |
| Detail | 6664 | 111.067 | 1.207 | 7.961 | 230.017 | 0% | 100% | PASS |
| Cart | 7322 | 122.033 | 0.944 | 2.129 | 3.927 | 0% | 100% | PASS |
| Checkout | 5942 | 99.033 | 2.634 | 5.340 | 9.151 | 0% | 100% | PASS |

### 4.4 API trước và sau spike

| API | Requests trước / sau | p95 trước (ms) | p95 sau (ms) | HTTP lỗi trước / sau | Checks trước / sau |
|---|---:|---:|---:|---|---|
| Search | 220 / 432 | 29.732 | 2.697 | 0% / 0% | 100% / 100% |
| Detail | 127 / 217 | 31.821 | 2.730 | 0% / 0% | 100% / 100% |
| Cart | 123 / 240 | 2.927 | 2.442 | 0% / 0% | 100% / 100% |
| Checkout | 102 / 202 | 11.088 | 10.596 | 0% / 0% | 100% / 100% |

### 4.5 Phục hồi và tài nguyên

Recovery có 1091 requests, p95 tổng 9.599 ms, HTTP lỗi 0%, checks 100%, không skipped; mọi API đạt SLO và có mẫu. Chỉ kết luận các request bắt đầu trong cửa sổ recovery 60s đạt SLO tổng hợp; chưa đo thời gian phục hồi chính xác theo rolling window hoặc backlog server. Recovery không có Login mới nên không đánh giá làn sóng xác thực mới.

Nguồn tài nguyên: người thực hiện quan sát **ngay lúc 1500 VUs**:

| Chỉ số | Quan sát |
|---|---|
| CPU | 9–14% |
| Memory | 3.62 GB / 7.12 GB · 51% |
| Swap | 1.57 GB / 8.59 GB · 18% |
| RSS từng process/core, DB locks, I/O, event-loop lag | Chưa thu thập |

Đây là quan sát tài nguyên máy, không phải avg/max từ chuỗi thời gian hoặc mức tiêu thụ riêng backend. Không đủ để xác định bottleneck, khẳng định swap ổn định hoặc không có swap I/O. Báo cáo spike trước không có telemetry tương ứng nên không so sánh tài nguyên trước/sau tune.

## 5. So sánh ngắn trước/sau tune

Reference: [spike trước tune](04-spike-test-report.md), run `spike-20261022-190641-UgVeF4`; cùng profile mục tiêu 50 → 1500 → 50 VUs, cửa sổ spike 60s.

| Chỉ số | Trước tune | Sau tune | Thay đổi |
|---|---:|---:|---:|
| p95 spike (ms) | 5344.455 | 6.849 | -99.87% |
| p99 spike (ms) | 8653.534 | 229.232 | -97.35% |
| p95 Checkout spike (ms) | 5566.188 | 5.340 | -99.90% |
| RPS tổng spike | 388.167 | 576.317 | +48.47% |
| p95 recovery (ms) | 13.044 | 9.599 | -26.41% |
| HTTP lỗi spike | 1.486% (346) | 0% (0) | −1.486 điểm % |
| Checks spike | 98.514% | 100% | +1.486 điểm % |
| Skipped spike | 1 | 0 | Giảm 1 |
| Thresholds toàn run | 47/63 | 63/63 | FAIL → PASS |

Sau tune, latency tại spike thấp hơn rõ trong lần đo này; không còn timeout/reset được ghi nhận và throughput cao hơn. Đây là đối chiếu hai run, chưa chứng minh toàn bộ mức cải thiện do WAL/index: thiếu snapshot build/DB, journal mode thực tế và monitoring đồng bộ; chưa có chạy lặp. WAL có thể hỗ trợ đọc song song với ghi nhưng SQLite vẫn chỉ có một writer; SUT dùng một connection chung. Search dùng `LIKE '%keyword%'` vẫn full-scan, không quy mức cải thiện Search cho index tên sản phẩm.

## 6. Đánh giá và giới hạn

**PASS cho profile đã đo:** tổng và từng API đạt p95 <500 ms, HTTP lỗi <1%, checks ≥99%, có request ở cả ba phase và không skipped; đủ 63/63 thresholds. Không có bằng chứng lỗi HTTP hay iteration bị ngắt.

p99 spike 229.232 ms cao hơn nhiều p95 6.849 ms, thể hiện đuôi phân bố vẫn có độ trễ lớn hơn phần lớn request. Toàn run có `http_req_connecting` p99 khoảng 1024.146 ms và max 2087.713 ms; thời gian thiết lập kết nối không nằm trong `http_req_duration`, nên PASS latency HTTP không đồng nghĩa toàn bộ chi phí client dưới 500 ms.

Một spike duy nhất, nền 30s và recovery 60s chưa xác nhận năng lực ổn định lâu dài hoặc tải tối đa. Thiếu phiên bản, snapshot, DB/cart ban đầu, logs server và telemetry theo thời gian; tài khoản chia sẻ/dữ liệu cố định có thể ảnh hưởng contention/cache. Không quy đổi 1500 VUs thành công suất production hoặc kết luận backlog đã hết.

## 7. Kết luận

Bản tuned database đạt SLO của spike 1500 VUs trong lần đo này, với p95 spike 6.849 ms, không HTTP lỗi, checks 100% và recovery đạt. Kết quả tốt hơn reference trước tune (FAIL), nhưng cần giữ nguyên workload/dữ liệu, lưu build/PRAGMA/index và chạy lặp để xác nhận độ cải thiện. Thu thêm tài nguyên từng process, DB latency/locks, event-loop và socket metrics nếu cần xác định nguyên nhân hoặc đánh giá ở đỉnh tải cao hơn.
