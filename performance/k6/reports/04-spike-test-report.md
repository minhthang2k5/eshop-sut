# Spike Test Report – eshop-sut – 2026-10-22

> **FAIL khi tăng đột biến từ 50 lên 1.500 VUs (30×).** Trong spike, p95 đạt 5.344,45 ms, HTTP error rate 1,486% và có 1 nghiệp vụ bị skipped do login lỗi. Cả bốn API nghiệp vụ đều vi phạm latency/error/checks. Sau khi giảm về 50 VUs, cửa sổ recovery 60s đạt mọi threshold: p95 13,04 ms, lỗi 0%. Đây là bằng chứng phục hồi trong cửa sổ quan sát, chưa chứng minh ổn định dài hạn.

## 1. Metadata và bằng chứng

| Trường | Giá trị |
|---|---|
| Run ID | spike-20261022-190641-UgVeF4 |
| Ngày / múi giờ | 22/10/2026, UTC+07:00 |
| Mốc chạy | Thư mục tạo lúc 19:06:41; log kết thúc lúc 19:09:17 |
| Công cụ | k6, execution local; chưa lưu phiên bản |
| Endpoint thực tế | `http://localhost:3000` (log và raw metrics) |
| Lịch tải / thời lượng thực tế | 150s / khoảng 154,90s (count/rate toàn bài; log hiển thị 2m34,9s) |
| Kết thúc | 23.511 iterations hoàn thành, 0 interrupted theo log |
| Thresholds | 16 thất bại, 47 đạt, tổng 63 điều kiện có ngưỡng |
| Cấu hình tham chiếu | [spike.js](../spike.js), [run-spike.sh](../run-spike.sh); chưa có snapshot/build gắn với run |
| Người thực hiện | Chưa được ghi trong artifacts |

Số liệu lấy từ [summary.json](../output/spike-20261022-190641-UgVeF4/summary.json), đối chiếu [k6.log](../output/spike-20261022-190641-UgVeF4/k6.log) và [metrics.json](../output/spike-20261022-190641-UgVeF4/metrics.json). Trong summary export này, giá trị `thresholds: true` nghĩa là điều kiện đã bị vi phạm; kết quả đã đối chiếu dấu ✗ trong log. Log xác nhận thresholds bị vượt, nhưng artifacts không ghi mã thoát shell thực tế.

## 2. Mục tiêu và tiêu chí

Đánh giá mức suy giảm khi tải tăng đột biến, các lỗi phát sinh và khả năng phục hồi sau giảm tải. Phạm vi: Search, Detail, Cart, Checkout cùng lazy Login; không đo trải nghiệm trình duyệt hoặc giao dịch mua hàng end-to-end.

| Tiêu chí | Ngưỡng | Phạm vi |
|---|---|---|
| HTTP latency p95 | < 500 ms | Trước/trong/sau spike, tổng hợp và từng API nghiệp vụ |
| HTTP error rate | < 1% | Như trên |
| Checks thành công | >= 99% | Status 200 và nội dung response |
| HTTP request count | > 0 | Mỗi phase và từng API nghiệp vụ |
| Business requests skipped | = 0 | Mỗi phase |

Ngưỡng thực thi theo script và threshold trong artifacts. Login được tính trong tổng phase nếu phát sinh và có thống kê riêng; không có SLO riêng cho Login. Không có ngưỡng RPS, CPU/RAM hoặc thời gian phục hồi định lượng trong script.

**Entry:** có dữ liệu cả năm API; chưa có bằng chứng smoke ngay trước run hoặc trạng thái DB ban đầu. **Exit:** hoàn thành lịch tải và recovery, không bị ngắt sớm bởi threshold; kết quả chung FAIL vì vi phạm ở đỉnh tải.

## 3. Môi trường và tài nguyên

Backend được gọi qua localhost và k6 chạy local, phù hợp bối cảnh thử nghiệm chung máy. Chưa có cấu hình CPU/RAM, phiên bản backend/DB, pool, instance count, telemetry CPU/RAM/swap, disk I/O, event-loop lag hoặc DB locks lưu kèm run. Không dùng số tài nguyên lịch sử của run khác để kết luận cho run này.

Chưa có bằng chứng autoscaling, queue/backlog, rate limiting hoặc circuit breaker. Không thể xác định bottleneck thuộc backend, DB, hệ điều hành hay cạnh tranh tài nguyên với k6 chỉ từ HTTP metrics; không quy đổi kết quả này thành năng lực production.

## 4. Workload và profile

Closed model `ramping-vus`, bắt đầu ở 50 VUs; tăng/giảm tải bằng stage `0s`:

| Thời gian scenario | VUs mục tiêu | Phase | Thời lượng |
|---|---:|---|---:|
| 00:00–00:30 | 50 | hold_50 | 30s |
| 00:30 | 50 → 1.500 | burst | 0s |
| 00:30–01:30 | 1.500 | hold_1500 | 60s |
| 01:30 | 1.500 → 50 | unload | 0s |
| 01:30–02:30 | 50 | recovery_1 | 60s |

Một spike, hệ số tăng **30×**. `gracefulRampDown=30s` cho iteration của VUs rút tải hoàn tất; `gracefulStop=30s` ở cuối bài. Vì vậy giảm tải mục tiêu tức thời không đồng nghĩa mọi request đang chạy kết thúc tức thời.

| API | Mix lựa chọn nghiệp vụ | Think-time |
|---|---:|---:|
| Search: GET /api/products?search=iPhone | 40% | 1–3s |
| Detail: GET /api/products/1 | 20% | 2–5s |
| Cart: POST /api/cart | 22% | 1–3s |
| Checkout: POST /api/checkout | 18% | 3–6s |

Mỗi iteration chọn một nghiệp vụ rồi nghỉ kể cả khi lỗi. Lazy Login là lưu lượng bổ sung khi VU cần token; token riêng VU. 50 tài khoản CSV chia vòng tròn, tối đa 30 VUs/tài khoản ở đỉnh. Login lỗi làm skip nghiệp vụ, không retry write tự động. Sản phẩm và dữ liệu ghi cố định; không đại diện đa dạng dữ liệu/cache production. Checkout hiện tạo đơn độc lập nội dung giỏ.

Phase gắn theo lúc **request bắt đầu**, điểm raw HTTP được xuất khi request hoàn tất. Request bắt đầu trong spike nhưng hoàn tất sau giảm tải vẫn thuộc `hold_1500`. RPS từng phase dưới đây = count / thời lượng phase (30/60/60s), không lấy trường `rate` của submetric vì trường đó dùng thời lượng toàn bài. Đây là tốc độ theo nhóm request bắt đầu trong phase, không phải thông lượng completion thuần trong cùng cửa sổ.

## 5. Kết quả

### 5.1 Tổng quan toàn bài

| Chỉ số | Giá trị |
|---|---:|
| HTTP requests | 25.009 |
| HTTP thành công / lỗi theo k6 | 24.663 / 346 |
| HTTP error rate | 1,384% |
| Throughput toàn bài | 161,45 requests/s |
| Checks đạt / thất bại | 49.326 / 692 |
| Check success rate | 98,616% |
| Iterations hoàn thành / interrupted | 23.511 / 0 |
| VUs cực đại | 1.500 |
| Latency avg / median | 1.242,50 / 682,38 ms |
| Latency p90 / p95 / p99 | 3.054,97 / 5.122,03 / 8.604,25 ms |
| Latency max | 10.004,87 ms |
| Login attempts / lỗi | 1.499 / 1 |
| Login p95 | 1.967,03 ms |
| Nghiệp vụ skipped do login lỗi | 1 |

`http_req_failed.passes` đếm request thỏa điều kiện “failed”, tức số lỗi; không phải số thành công. Mỗi request có hai checks, nên 692 checks lỗi tương ứng 346 HTTP lỗi trong run này, không phải 692 request lỗi.

### 5.2 So sánh trước / trong / sau spike

| Chỉ số | Trước: 50 VUs / 30s | Trong: 1.500 VUs / 60s | Sau: 50 VUs / 60s |
|---|---:|---:|---:|
| HTTP requests | 634 | 23.290 | 1.085 |
| Latency avg (ms) | 5,17 | 1.333,90 | 3,62 |
| Latency median (ms) | 2,65 | 849,90 | 2,07 |
| Latency p90 (ms) | 14,40 | 3.165,42 | 11,41 |
| Latency p95 (ms) | 16,96 | 5.344,45 | 13,04 |
| Latency p99 (ms) | 36,82 | 8.653,53 | 15,45 |
| Latency max (ms) | 42,64 | 10.004,87 | 16,64 |
| RPS theo phase (kể cả Login) | 21,13 | 388,17 | 18,08 |
| HTTP error rate | 0,000% | 1,486% | 0,000% |
| Checks thành công | 100,000% | 98,514% | 100,000% |
| HTTP lỗi | 0 | 346 | 0 |
| Nghiệp vụ skipped | 0 | 1 | 0 |
| Thresholds đạt / tổng | 21/21 | 5/21 | 21/21 |

RPS nghiệp vụ (loại Login) trước/trong/sau tương ứng **19,47 / 364,02 / 18,08**. Login tương ứng 50 / 1.449 / 0 requests. So sánh RPS tổng cần tính đến lượng login bổ sung và độ dài cửa sổ khác nhau; tải là số VUs, không phải arrival rate cố định.

### 5.3 Từng API trong spike

| API | Requests | RPS / 60s | p95 (ms) | HTTP lỗi | Error rate | Checks thành công | SLO latency/error/checks |
|---|---:|---:|---:|---:|---:|---:|---|
| Search | 8.728 | 145,47 | 6.035,74 | 117 | 1,341% | 98,659% | FAIL |
| Detail | 4.455 | 74,25 | 6.124,98 | 60 | 1,347% | 98,653% | FAIL |
| Cart | 4.785 | 79,75 | 2.491,63 | 81 | 1,693% | 98,307% | FAIL |
| Checkout | 3.873 | 64,55 | 5.566,19 | 87 | 2,246% | 97,754% | FAIL |

### 5.4 Từng API trước và sau spike

| API | Requests trước / sau | p95 trước (ms) | p95 sau (ms) | Error trước / sau | Checks trước / sau |
|---|---:|---:|---:|---|---|
| Search | 258 / 447 | 16,38 | 2,83 | 0% / 0% | 100% / 100% |
| Detail | 104 / 211 | 17,94 | 3,15 | 0% / 0% | 100% / 100% |
| Cart | 127 / 233 | 2,93 | 2,51 | 0% / 0% | 100% / 100% |
| Checkout | 95 / 194 | 15,74 | 15,42 | 0% / 0% | 100% / 100% |

### 5.5 Phân loại lỗi từ raw metrics

| HTTP status | Error code | Loại lỗi ghi nhận | Số lượng | % trên 25.009 requests |
|---|---|---|---:|---:|
| 0 | 1050 | request timeout | 217 | 0,868% |
| 0 | 1220 | read: connection reset by peer | 129 | 0,516% |
| 200 | — | HTTP thành công | 24.663 | 98,616% |

Mọi HTTP lỗi đều thuộc `hold_1500`; không có HTTP 4xx/5xx trong raw metrics. Status 0 biểu thị không nhận được HTTP response hợp lệ, không phải mã HTTP của server. Phân bổ lỗi: Search 117, Detail 60, Cart 81, Checkout 87, Login 1. Các API nghiệp vụ tổng cộng 345 lỗi; một login lỗi dẫn đến 1 nghiệp vụ skipped.

Thời điểm completion lỗi đầu/cuối ghi nhận: **19:07:18,148 / 19:08:02,311 (UTC+07)**. Đây là thời điểm xuất point khi request kết thúc, không phải thời điểm bắt đầu lỗi hay thời điểm phục hồi được xác nhận. Timeout khi ghi không chứng minh đơn hàng chưa được tạo; cần đối soát DB trước khi retry.

### 5.6 Phục hồi và tài nguyên

Cửa sổ `recovery_1` có 1.085 request, 0 HTTP lỗi, checks 100%, không skipped; tất cả API có mẫu và đạt SLO. Tổng p95 giảm từ 5.344,45 xuống 13,04 ms, thấp hơn p95 trước spike 16,96 ms. Chưa tính thời gian phục hồi chính xác theo rolling window; chỉ kết luận **các request bắt đầu trong cửa sổ recovery 60s đạt SLO tổng hợp**. Không suy ra backlog đã hết hoặc hệ thống ổn định lâu dài từ một cửa sổ này.

CPU/RAM/GC/disk/network theo process, DB pool/queue và autoscaling: **chưa có telemetry**. Log cho thấy VUs trở về 50 sau khi iteration cũ kết thúc; điều này không đo backlog trong server.

## 6. Đối chiếu tiêu chí

| Tiêu chí | Ngưỡng | Trước spike | Trong spike | Recovery |
|---|---|---|---|---|
| p95 tổng hợp + từng API | < 500 ms | PASS | FAIL: tổng 5.344,45 ms; cả 4 API vượt | PASS |
| HTTP error tổng hợp + từng API | < 1% | PASS | FAIL: tổng 1,486%; cả 4 API vượt | PASS |
| Checks tổng hợp + từng API | >= 99% | PASS | FAIL: tổng 98,514%; cả 4 API thấp hơn | PASS |
| Request tổng hợp + từng API | > 0 | PASS | PASS | PASS |
| Business requests skipped | = 0 | PASS | FAIL: 1 | PASS |

**Kết luận chung: FAIL — khả năng chịu spike 50 → 1.500 VUs chưa đạt SLO; recovery 60s đạt.** 16 điều kiện thất bại gồm 5 latency + 5 error + 5 checks + 1 skipped trong spike; 47 điều kiện còn lại đạt. Không có bằng chứng server crash chỉ từ threshold fail hoặc connection reset.

## 7. Phân tích

- Latency p95 trong spike khoảng **315×** trước spike và **10,69×** giới hạn 500 ms. Đây là suy giảm rõ khi tăng tải đột ngột; không thể coi RPS tăng là đạt yêu cầu khi latency/error vi phạm.
- Detail có p95 cao nhất (6.124,98 ms); Checkout có tỷ lệ lỗi cao nhất (2,246%). Cart có p95 thấp nhất trong bốn API nhưng vẫn 2.491,63 ms, vượt xa SLO.
- 217 timeout cùng 129 connection reset là bằng chứng lỗi vận chuyển/timeout, chưa xác định nguyên nhân gốc. Cần telemetry và server/DB logs đồng thời để phân biệt nghẽn ứng dụng, DB hay hệ điều hành/load generator.
- Recovery đạt và không có login mới trong phase này. Không nên dùng phase recovery để đánh giá khả năng xử lý làn sóng login mới.
- Kết quả cùng chiều với bất ổn ở 1.500 VUs của [stress run mới nhất](03-stress-test-report.md), nhưng spike và stress có lịch sử tải khác nhau; không gộp số liệu hoặc coi một lần chạy là ngưỡng công suất cố định.

## 8. Hạn chế và rủi ro

- Một spike duy nhất, nền chỉ 30s và recovery 60s; chưa có chạy lặp lại hoặc quan sát phục hồi dài hơn.
- Thiếu snapshot script, phiên bản k6/SUT, trạng thái DB ban đầu và telemetry tài nguyên. Profile 1.500 VUs được đối chiếu script hiện tại, log và tags trong summary; script không được lưu bất biến cùng artifacts.
- 50 tài khoản dùng chung cho 1.500 VUs và dữ liệu sản phẩm cố định có thể ảnh hưởng contention/cache; không đại diện 1.500 người dùng với dữ liệu độc lập.
- Mô hình VUs khép kín làm throughput phụ thuộc thời gian phản hồi và think-time. Các percentile phase tổng hợp không xác định thời điểm bắt đầu suy giảm hoặc thời gian phục hồi chính xác.
- Chưa có bằng chứng tính đúng đắn dữ liệu sau timeout/reset, tồn dư queue hay autoscaling; không kết luận các cơ chế này hoạt động hoặc thất bại.

## 9. Kết luận và khuyến nghị

Chưa nghiệm thu khả năng chịu spike 1.500 VUs theo SLO hiện tại. Hệ thống phục hồi về SLO trong cửa sổ đo sau khi giảm về 50 VUs, nhưng cần xác nhận tính lặp lại.

Ưu tiên chạy lặp cùng profile/dữ liệu và lưu build/config; thu CPU/RAM từng process/core, event-loop lag, DB latency/locks/pool và socket metrics cùng server logs. Sau đó khảo sát các đỉnh thấp hơn để tìm mức spike đạt SLO, kéo dài recovery và dùng rolling windows có đủ mẫu để đo thời gian phục hồi. Đối soát các thao tác ghi bị timeout/reset trước khi quyết định retry hoặc chạy tiếp.

## 10. Phụ lục

- [Summary](../output/spike-20261022-190641-UgVeF4/summary.json)
- [Log k6](../output/spike-20261022-190641-UgVeF4/k6.log)
- [Raw metrics JSON lines](../output/spike-20261022-190641-UgVeF4/metrics.json)
- [Script spike](../spike.js), [wrapper](../run-spike.sh), [CSV accounts](../data/test_accounts.csv)

Tái chạy từ thư mục gốc workspace:

```bash
BASE_URL=http://localhost:3000 bash eshop-sut/performance/k6/run-spike.sh
```

Mỗi lần chạy tạo thư mục `output/spike-<timestamp>-<suffix>/` riêng. Không có biểu đồ tài nguyên vì run chưa lưu telemetry tương ứng.
