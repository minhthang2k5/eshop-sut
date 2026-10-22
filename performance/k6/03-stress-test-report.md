# Stress Test Report – eshop-sut – 2026-10-22

> **FAIL SLO tại bậc 4.000 VUs; phục hồi về trạng thái đạt SLO trong cửa sổ 1 phút sau giảm tải.** Bậc 2.000 VUs vẫn đạt SLO, nhưng đã tăng latency và có lỗi kết nối lẻ tẻ. Chưa có bằng chứng server crash/OOM; không đồng nhất request timeout với ứng dụng sập.

## 1. Metadata và bằng chứng

| Trường | Giá trị |
|---|---|
| Run ID | stress-20261022-125734-TX7V6o |
| Ngày / múi giờ | 22/10/2026, UTC+07:00 |
| HTTP sample đầu / cuối (timestamp hoàn tất) | 12:57:35.423 / 13:10:35.256 |
| Thời lượng theo log | 13 phút 04,6 giây, lịch phát tải 13 phút |
| Script / runner | [stress.js](stress.js) / [run-stress.sh](run-stress.sh) |
| Công cụ | k6; artifact không lưu phiên bản binary |
| BASE_URL / build SUT | Script mặc định localhost:3000; chưa có metadata xác nhận env override/build |
| Người thực hiện | Người dùng chạy test và cung cấp quan sát tài nguyên |

Nguồn: [summary.json](output/stress-20261022-125734-TX7V6o/summary.json), [metrics.json](output/stress-20261022-125734-TX7V6o/metrics.json), [k6.log](output/stress-20261022-125734-TX7V6o/k6.log). Đã đối chiếu raw request counts theo phase/status với summary. Report này thay kết quả run 50–400 VUs trước đó bằng lần chạy mới, không trộn số liệu hai run.

## 2. Mục tiêu, phạm vi và tiêu chí

Tìm bậc bắt đầu vi phạm SLO, quan sát dạng lỗi khi tăng tải và trạng thái sau rút tải. Phạm vi HTTP API Search, Detail, Cart, Checkout và lazy Login; không đo UI hay tự động đối soát DB.

| Tiêu chí | Ngưỡng | Phạm vi |
|---|---|---|
| Latency p95 | < 500 ms | Từng bậc giữ tải/recovery, tổng hợp và từng API nghiệp vụ |
| HTTP error rate | < 1% | Như trên; status khác 200 là lỗi |
| Checks thành công | >= 99% | Kiểm tra status và nội dung response |
| Request count | > 0 | Mỗi cửa sổ và từng API nghiệp vụ |
| Nghiệp vụ skipped vì login thất bại | = 0 | Mỗi cửa sổ giữ tải/recovery |

Nguồn SLO: [Tool Analysis and Theory](../../../4_ZipTool/Tool_Analysis_and_Theory.md). Login được tính trong tổng phase và thống kê riêng. Các ramp có raw metrics nhưng không có threshold riêng trong script; kết luận “bậc đầu vi phạm” bên dưới áp dụng cho các plateau, không phải thời điểm chính xác trong ramp.

**Entry:** run có login thành công và đủ bốn nghiệp vụ; artifact không chứng minh smoke đã chạy trước test hoặc cấu hình DB ban đầu. **Exit:** 378.538 iterations hoàn thành, 0 interrupted; bài test đi hết recovery dù threshold bị vượt. Log xác nhận 16 threshold thất bại, 89 đạt, tổng 105; không lưu exit code của shell riêng.

## 3. Môi trường và tài nguyên

Server và k6 chạy chung một máy. Người dùng cung cấp các quan sát toàn máy sau; không phải số liệu riêng process server/k6.

| VUs | RAM dùng / tổng | RAM % | Swap dùng / tổng | Swap % | CPU |
|---|---|---|---|---|---|
| 500 | 4,73 / 7,39 GB | 64% | 2,28 / 8,59 GB | 27% | 6–9% |
| 1.000 | 4,93 / 7,39 GB | 67% | 2,27 / 8,59 GB | 26% | 8–12% |
| 2.000 | 4,85 / 7,39 GB | 66% | 2,27 / 8,59 GB | 26% | 11–16% |
| 4.000 | 5,15 / 7,39 GB | 70% | 2,27 / 8,59 GB | 26% | 12–19% |

RAM tăng khoảng 0,42 GB từ bậc 500 đến 4.000; swap đang dùng không tăng. Không có bằng chứng bão hòa toàn bộ RAM/CPU tại các thời điểm quan sát. Tuy nhiên CPU tổng thấp không loại trừ nghẽn một core/event loop, SQLite, connection/socket hoặc máy phát tải. Swap đang dùng không đo tốc độ swap-in/out. Không suy ra bottleneck hoặc loại trừ memory pressure chỉ từ bảng này.

Chưa có telemetry recovery, CPU từng core, disk I/O, event-loop lag, DB locks, socket/file descriptor, log OOM/restart; chưa xác nhận riêng việc có/không can thiệp thủ công. Phiên bản Node/SQLite, journal mode, CPU model/số core và dung lượng DB chưa được lưu cùng run.

## 4. Workload và load profile

Closed model `ramping-vus`; mỗi iteration chọn một nghiệp vụ ngẫu nhiên, sau đó think-time kể cả khi lỗi:

| API | Xác suất Black Friday | Think-time |
|---|---:|---:|
| Search | 40% | 1–3s |
| Detail | 20% | 2–5s |
| Cart | 22% | 1–3s |
| Checkout | 18% | 3–6s |

50 tài khoản trong [CSV](data/test_accounts.csv), ánh xạ vòng tròn theo VU ID; tối đa 80 VUs/tài khoản. Token riêng từng VU, lazy login trước Cart/Checkout; login lỗi thì bỏ qua nghiệp vụ và vẫn nghỉ. HTTP 401 xóa token để đăng nhập ở iteration cần xác thực tiếp theo; không retry write tự động. SUT có giỏ hàng theo user, checkout độc lập với giỏ hàng; đây là mix API, không phải giao dịch mua hàng end-to-end có giỏ riêng cho từng VU.

| Thời gian scenario | VUs | Phase |
|---|---|---|
| 00:00–01:00 | 0→500 | ramp_500 |
| 01:00–03:00 | 500 | hold_500 |
| 03:00–04:00 | 500→1000 | ramp_1000 |
| 04:00–06:00 | 1000 | hold_1000 |
| 06:00–07:00 | 1000→2000 | ramp_2000 |
| 07:00–09:00 | 2000 | hold_2000 |
| 09:00–10:00 | 2000→4000 | ramp_4000 |
| 10:00–12:00 | 4000 | hold_4000 |
| 12:00–13:00 | 50 | recovery_1 |

Chuyển 4.000→50 dùng stage 0s. `gracefulRampDown: 30s` cho iteration đang chạy hoàn tất, nên 30s đầu recovery có thể còn VUs rút tải. `gracefulStop: 30s` áp dụng khi kết thúc. Tag phase tính theo lúc **bắt đầu request**, timestamp HTTP metric là lúc hoàn tất: request bắt đầu ở hold_4000 và kết thúc sau lúc giảm tải vẫn thuộc hold_4000.

## 5. Kết quả

### 5.1 Toàn bài

| Chỉ số | Giá trị |
|---|---:|
| HTTP requests | 382.538 |
| HTTP 200 | 373.499 |
| Status 0 / HTTP lỗi | 9.039 / 2,363% |
| Checks đạt | 746.998 / 765.076 = 97,637% |
| Iterations hoàn thành / gián đoạn | 378.538 / 0 |
| VUs cực đại | 4.000 |
| RPS toàn bài theo summary | 487,59 |
| Latency avg / median | 390,42 / 3,55 ms |
| Latency p90 / p95 / p99 | 961,84 / 2.052,64 / 9.373,01 ms |
| Latency max | 10.012,45 ms |
| Login attempts | 4.152 (4.000 thành công, 152 thất bại) |
| Nghiệp vụ skipped vì login | 152 |

Raw count theo API: Search 151.239; Detail 75.721; Cart 83.453; Checkout 67.973; Login 4.152. Đây là số request đã gửi, không phải số nghiệp vụ thành công. Tổng request nghiệp vụ = 378.386, thấp hơn 378.538 iterations đúng 152 lần skipped. Lazy login phát sinh thêm 152 lần thử do thất bại; lỗi login làm workload thực tế lệch nhẹ khỏi mix dự kiến.

### 5.2 Bậc giữ tải và recovery

| Phase | Request | RPS | p95 ms | p99 ms | HTTP lỗi | Checks đạt | Skipped | Kết quả |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| hold_500 | 21,711 | 180.93 | 9.32 | 84.33 | 0.000% | 100.000% | 0 | PASS |
| hold_1000 | 43,729 | 364.41 | 8.83 | 17.32 | 0.000% | 100.000% | 0 | PASS |
| hold_2000 | 86,422 | 720.18 | 129.14 | 665.28 | 0.027% | 99.973% | 0 | PASS |
| hold_4000 | 107,701 | 897.51 | 7963.53 | 10000.61 | 8.205% | 91.795% | 134 | FAIL |
| recovery_1 | 1,081 | 18.02 | 14.69 | 17.06 | 0.000% | 100.000% | 0 | PASS |

RPS tính bằng count / 120s cho hold, / 60s cho recovery; không dùng `rate` toàn bài của counter submetric. Bậc 2.000 đạt 720,18 RPS; bậc 4.000 đạt 897,51 RPS: concurrency tăng 2 lần nhưng throughput chỉ tăng khoảng 24,6%, trong khi p95 tăng hơn 61 lần. Đây là dấu hiệu suy giảm hiệu năng rõ rệt trong môi trường đo.

### 5.3 Chi tiết từng API

| Phase | API | Request | p95 ms | p99 ms | Request lỗi | Error % |
|---|---|---:|---:|---:|---:|---:|
| hold_500 | search | 8,647 | 7.44 | 97.92 | 0 | 0.000% |
| hold_500 | detail | 4,311 | 8.33 | 93.19 | 0 | 0.000% |
| hold_500 | cart | 4,743 | 2.38 | 22.69 | 0 | 0.000% |
| hold_500 | checkout | 3,978 | 14.04 | 100.07 | 0 | 0.000% |
| hold_1000 | search | 17,596 | 7.88 | 16.69 | 0 | 0.000% |
| hold_1000 | detail | 8,816 | 8.38 | 19.51 | 0 | 0.000% |
| hold_1000 | cart | 9,548 | 2.69 | 6.96 | 0 | 0.000% |
| hold_1000 | checkout | 7,735 | 12.66 | 23.31 | 0 | 0.000% |
| hold_2000 | search | 34,601 | 141.99 | 821.05 | 0 | 0.000% |
| hold_2000 | detail | 17,225 | 144.46 | 755.35 | 0 | 0.000% |
| hold_2000 | cart | 19,129 | 54.07 | 304.03 | 15 | 0.078% |
| hold_2000 | checkout | 15,405 | 152.18 | 777.30 | 8 | 0.052% |
| hold_4000 | search | 42,801 | 9110.38 | 10000.74 | 3,690 | 8.621% |
| hold_4000 | detail | 21,615 | 9136.11 | 10000.74 | 1,808 | 8.365% |
| hold_4000 | cart | 23,641 | 3148.03 | 6601.37 | 1,584 | 6.700% |
| hold_4000 | checkout | 19,387 | 7528.85 | 10000.56 | 1,642 | 8.470% |
| recovery_1 | search | 400 | 3.51 | 9.11 | 0 | 0.000% |
| recovery_1 | detail | 217 | 3.26 | 4.01 | 0 | 0.000% |
| recovery_1 | cart | 266 | 2.81 | 3.11 | 0 | 0.000% |
| recovery_1 | checkout | 198 | 16.72 | 27.18 | 0 | 0.000% |

Ở 4.000 VUs, **cả bốn API đều vượt p95 500 ms và error 1%**. Search/Detail p95 khoảng 9,1s; Checkout khoảng 7,53s; Cart khoảng 3,15s. Vì vậy lỗi không chỉ giới hạn ở luồng tạo đơn.

### 5.4 Phân loại lỗi và điểm gãy

Toàn bộ 9.039 HTTP lỗi có **status 0** (không có HTTP response hợp lệ), gồm **7.965 request timeout** và **1.074 connection reset by peer**. Không có response HTTP 4xx/5xx trong raw data.

| Phase | Lỗi | k6 error code | Số lượng |
|---|---|---|---:|
| ramp_1000 | read: connection reset by peer | 1220 | 1 |
| ramp_2000 | read: connection reset by peer | 1220 | 1 |
| hold_2000 | read: connection reset by peer | 1220 | 23 |
| ramp_4000 | read: connection reset by peer | 1220 | 47 |
| ramp_4000 | request timeout | 1050 | 130 |
| hold_4000 | read: connection reset by peer | 1220 | 1,002 |
| hold_4000 | request timeout | 1050 | 7,835 |

Lỗi đầu tiên kết thúc lúc **13:01:08.030 +07:00**, trong ramp_1000; đó là một connection reset lẻ tẻ, không đủ gọi là điểm gãy. Lỗi cuối cùng kết thúc lúc **13:09:34.874 +07:00**. Timeout request trong script là 10s, phù hợp với đuôi latency gần 10.000 ms; không quy mọi status 0 thành timeout vì có cả reset kết nối.

**Trả lời các câu hỏi stress test:**

1. **Bắt đầu chậm ở đâu?** Bậc 2.000 VUs cho thấy suy giảm rõ: p95 129,14 ms so với 8,83 ms ở 1.000; 23 lỗi kết nối, nhưng mọi threshold plateau vẫn đạt. Đây là dấu hiệu chậm, chưa phải vi phạm SLO.
2. **Điểm gãy theo SLO?** Bậc giữ tải đầu tiên không đạt là **4.000 VUs**: p95 7.963,53 ms, error 8,205%, 134 nghiệp vụ skipped. Bậc trước 2.000 vẫn đạt. Khoảng tải cần khảo sát chi tiết tiếp theo là **trên 2.000 đến 4.000 VUs**, không khẳng định chính xác VU bắt đầu gãy. Ramp_4000 đã có 177 lỗi/64.399 request (khoảng 0,275%); chưa phân tích percentile theo cửa sổ nhỏ trong ramp để xác định thời điểm vượt SLO sớm nhất.
3. **Ứng dụng sập ở đâu?** **Chưa xác định được mức tải gây crash.** Tại hold_4000 vẫn có 98.864/107.701 request thành công (91,795%). Dữ liệu chứng minh suy giảm và lỗi client quan sát được, không chứng minh process chết/OOM. Cần server/process logs để phân biệt quá tải, restart và lỗi kết nối.

## 6. Recovery và đối chiếu tiêu chí

Sau giảm về 50 VUs, các request **bắt đầu trong recovery_1** có:

- 1.081 request, HTTP lỗi 0%, checks 100%, skipped 0.
- p95 tổng **14,69 ms**, p99 **17,06 ms**, max **62,94 ms**; 18,02 RPS.
- Đủ mẫu cả bốn API; p95 cao nhất là Checkout **16,72 ms**.

**Trạng thái đạt SLO được quan sát trong cửa sổ 0–60 giây sau giảm tải.** Không suy ra thời gian phục hồi chính xác hoặc “phục hồi tức thì” từ percentile của cả phút. Các request cũ vẫn được gắn hold_4000, nên bảng recovery không bao gồm mọi request còn đang chạy tại thời điểm giảm tải. Run không có plateau 50 VUs trước stress để so sánh nền cùng lần chạy; đánh giá recovery dựa trên SLO tuyệt đối.

Chỉ quan sát 1 phút, chưa chứng minh duy trì ổn định lâu dài. Chưa có xác nhận về can thiệp thủ công, nên chưa kết luận chắc chắn **tự** phục hồi. Không có đối soát DB/đơn hàng: checkout timeout không bảo đảm đơn chưa được tạo.

| Tiêu chí | Kết quả | Kết luận |
|---|---|---|
| SLO tại 500/1.000/2.000 VUs | Mọi threshold giữ tải đạt | PASS |
| SLO tại 4.000 VUs | 16 threshold fail: latency, errors, checks và skipped | FAIL |
| Recovery 50 VUs / 1 phút | Mọi threshold recovery đạt | PASS trong cửa sổ đo |
| Xác định bậc vi phạm SLO | 2.000 đạt, 4.000 không đạt | Đã xác định khoảng cần thu hẹp |
| Xác định crash/OOM | Không có server/process logs | Chưa xác minh |
| Tự phục hồi không can thiệp | Chưa có xác nhận can thiệp | Chưa xác minh |
| Toàn vẹn dữ liệu sau test | Chưa đối soát DB | Chưa đánh giá |

**Kết luận chung:** bài đo đã tìm thấy giới hạn SLO theo các bậc thử và ghi nhận trạng thái đạt SLO sau rút tải. Kết quả threshold toàn bài là **FAIL**, nhưng mục tiêu khám phá suy giảm đạt một phần; chưa xác định crash, bottleneck hay độ bền phục hồi.

## 7. Hạn chế và khuyến nghị

- Server/k6 chung máy: lỗi/latency có thể chịu ảnh hưởng từ cả load generator và SUT. CPU toàn máy 12–19% ở 4.000 VUs không đủ loại trừ nghẽn từng core, SQLite, socket/file descriptor hoặc k6.
- Chưa có telemetry đồng bộ để quy nguyên nhân cho DB/event loop/GC; không kết luận “SQLite là bottleneck” chỉ từ timeout.
- Closed model với think-time làm throughput tự giảm khi response chậm; đây không phải arrival rate cố định. Tối đa 80 VUs dùng chung tài khoản và giỏ hàng cũng giới hạn tính đại diện.
- Không có snapshot script/build, thông tin DB ban đầu và artifact smoke; khả năng tái lập còn hạn chế.
- Khảo sát thêm các bậc giữa 2.000–4.000 (ví dụ 2.500/3.000/3.500) để thu hẹp ngưỡng; chưa tự sửa script hay chạy thêm trong lần lập báo cáo này.
- Thu CPU từng core/process, RAM k6/server, DB locks/disk I/O, event-loop lag, connection/socket limits và log restart/OOM. Tách máy phát tải khi cần đo công suất SUT độc lập.
- Nếu cần chứng minh tự phục hồi bền vững, kéo dài cửa sổ sau giảm tải và ghi rõ mọi can thiệp; đối soát đơn tạo thành công/timeout để đánh giá dữ liệu.

## 8. Phụ lục

- [Raw metrics](output/stress-20261022-125734-TX7V6o/metrics.json): số request theo phase/API/status và lỗi transport.
- [Summary](output/stress-20261022-125734-TX7V6o/summary.json): percentile và threshold; trong định dạng export này `true` là cờ threshold thất bại, `false` là không thất bại, đã đối chiếu log.
- [Log](output/stress-20261022-125734-TX7V6o/k6.log): hoàn thành 13m04,6s và danh sách 16 threshold bị vượt.
- [Script](stress.js), [runner](run-stress.sh), [CSV](data/test_accounts.csv), [hướng dẫn](README.md).

Báo cáo được lập bằng cách đọc artifacts; không phát tải lại và không thay đổi dữ liệu SUT.
