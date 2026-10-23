# Kiểm chứng kết quả k6 trước và sau tối ưu SQLite trên máy khác

Ngày chạy: 23/10/2026. Người thực thi: trợ lý Codex trên môi trường Windows của Võ Hữu Thắng. Trong báo cáo, máy A là môi trường Linux đo k6 ban đầu; máy B là môi trường Windows chạy lại để kiểm chứng. “Tuned” là backend bật SQLite WAL và thêm index tên sản phẩm. Nhiệm vụ này có mã D8b trong bảng phân công.

Các lần chạy cung cấp bằng chứng kỹ thuật về khả năng tái lập. Việc từng thành viên tự chạy công cụ của người khác và xác nhận hiểu kết quả (cross-run) được theo dõi riêng tại [bảng xác nhận](cross_run_signoff.md).

## Phương pháp và môi trường

Chạy bằng Windows PowerShell, k6 2.2.0 (windows/amd64), Node.js v24.20.0, SQLite 3.52.0. Máy Windows 10.0.26200 x64, AMD Ryzen 7 5700U, 16 logical CPUs, RAM 7893950464 bytes (khoảng 7.35 GiB). SUT và k6 cùng máy; các ứng dụng desktop vẫn hoạt động. Không thu telemetry CPU/RAM/DB đồng bộ nên không quy số liệu tài nguyên riêng cho backend hoặc k6.

Source base commit: `f445dbb861ff211c1f56883e9a238cf89455fe10`. Worktree có các file untracked đã tồn tại; không reset worktree. Metadata từng run lưu commit, trạng thái Git, SHA-256 source SUT, script, seed và CSV. Hai package-lock của backend gốc/tuned giống nhau; cả hai dùng dependency backend đã cài. Source A không bị thay đổi để chạy tải.

Mỗi run có bản sao SUT/DB mới dưới `local-runs/`. Sau start/seed, seed 50 account k6 vào đúng DB bản sao. DB trước chạy có 52 users tổng cộng, 5 products, 0 orders; cart là RAM trong process mới. Bản gốc xác nhận journal `delete`, không có index tên sản phẩm; bản tuned xác nhận journal `wal` và index `idx_products_name ON products(name)`. Cả hai query plan với `LIKE '%iPhone%'` đều ghi `SCAN products`. Các hash file SQLite nguồn được kiểm tra không đổi sau run.

## Profile và tiêu chí

- Smoke: 1 VU, 1 iteration; Login → Search → Detail → Cart → Checkout; 5 HTTP requests, 10 checks. Dùng làm entry check, không đánh giá công suất.
- Baseline: ramp 0→50 trong 60s; steady 50 VUs 300s; giảm tải 60s. Mix Search/Detail/Cart/Checkout=55/25/14/6.
- Spike: giữ 50 VUs 30s → chuyển tức thời lên 1500, giữ 60s → chuyển về 50, recovery 60s. Graceful ramp-down/stop 30s, nên VUs đang hoàn tất iteration có thể chưa giảm ngay theo target. Mix=40/20/22/18.
- Dữ liệu fixed keyword iPhone, ID 1, giá 30000000; lazy login, token riêng VU. Baseline 50 account riêng; spike chia sẻ 50 account theo modulo. Think-time giữ nguyên sau request (Search/Cart 1–3s, Detail 2–5s, Checkout 3–6s); timeout 10s.
- SLO theo tổng và từng API nghiệp vụ: p95 <500ms, HTTP error <1%, checks ≥99%, count >0; skipped=0 theo cấu hình từng script. Baseline có thresholds Login riêng; spike chỉ thống kê Login riêng.

Số thập phân dùng dấu chấm. Tổng phase có cả Login khi phát sinh. Latency lấy trực tiếp từ metric k6, p50=med; RPS=count/300s baseline steady, count/30s hoặc /60s cho phase spike. Không dùng rate toàn run hoặc trung bình percentile endpoint làm percentile tổng.

Kết quả và đối chiếu được bổ sung từ các summary hoàn tất, bằng [summarizer](summarize-verification.cjs). Evidence: [thư mục Assignee B](../../submission/evidence/assignee-b/README.md).

## Baseline — kết quả trên máy B

| Cấu hình | Request steady | p50 ms | p95 ms | p99 ms | RPS | HTTP lỗi | Checks | Thresholds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Gốc | 5967 | 1.806 | 12.381 | 16.353 | 19.890 | 0% | 100% | 25/25 đạt |
| Tuned | 5972 | 1.656 | 5.524 | 9.010 | 19.907 | 0% | 100% | 25/25 đạt |

Mỗi cấu hình có 12 Login steady; business count lần lượt 5955 và 5960, business RPS 19.850 và 19.867. Toàn run có 50 Login mỗi cấu hình, p95 Login lần lượt 5.653/4.817ms, lỗi 0%. Không có business skipped.

| API steady | Count gốc/tuned | p95 gốc ms | p95 tuned ms | HTTP lỗi gốc/tuned |
| --- | --- | ---: | ---: | --- |
| Search | 3286 / 3283 | 3.661 | 2.353 | 0% / 0% |
| Detail | 1483 / 1431 | 4.068 | 2.487 | 0% / 0% |
| Cart | 844 / 862 | 3.107 | 2.182 | 0% / 0% |
| Checkout | 342 / 384 | 20.014 | 9.251 | 0% / 0% |

Tất cả API nghiệp vụ có checks 100% và đạt SLO. Baseline gốc/tuned có 7153/7149 iterations hoàn tất, đều 0 interrupted. p95 tổng trên máy B giảm khoảng 55.39%; không coi tỷ lệ này là mức cải thiện bảo đảm trên môi trường khác.

## Spike — kết quả trên máy B

| Cấu hình / phase | Requests | p50 ms | p95 ms | p99 ms | RPS | HTTP lỗi | Checks | Skipped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gốc / hold_50 | 618 | 2.128 | 58.777 | 69.177 | 20.600 | 0% | 100% | 0 |
| Gốc / hold_1500 | 27791 | 627.172 | 1948.729 | 2581.905 | 463.183 | 4.674% | 95.326% | 480 |
| Gốc / recovery_1 | 1088 | 2.227 | 17.369 | 214.799 | 18.133 | 0% | 100% | 0 |
| Tuned / hold_50 | 632 | 2.465 | 54.423 | 66.151 | 21.067 | 0% | 100% | 0 |
| Tuned / hold_1500 | 34644 | 3.799 | 93.402 | 319.655 | 577.400 | 3.360% | 96.640% | 444 |
| Tuned / recovery_1 | 1097 | 1.919 | 8.997 | 14.488 | 18.283 | 0% | 100% | 0 |

**Cả hai spike FAIL**, exit 99: bản gốc đạt 51/63 thresholds, tuned đạt 56/63. Bản tuned đạt latency nhưng fail HTTP error/checks tổng và Search/Detail; vẫn có skipped. Trước spike và recovery đều đạt thresholds trên tổng và từng API. Iterations hoàn tất gốc/tuned=27997/34873, đều 0 interrupted; thời lượng theo log khoảng 2m35.7s/2m34.8s.

| API tại hold_1500 | p95 gốc/tuned ms | HTTP lỗi gốc/tuned |
| --- | --- | --- |
| Search | 2078.159 / 71.123 | 4.585% / 3.654% |
| Detail | 2104.589 / 79.657 | 4.638% / 3.469% |
| Cart | 743.427 / 37.920 | 0.912% / 0% |
| Checkout | 2054.479 / 84.200 | 0.970% / 0.034% |

Login toàn spike gốc/tuned có 1980/1944 attempts, p95=1295.407/366.516ms, HTTP lỗi=24.242%/22.840%. Attempts lớn hơn 1500 vì login thất bại được thử lại ở protected iteration sau. Login theo phase được suy từ tổng trừ bốn API vì script không export đủ submetric phase+login; không tự tạo latency/error riêng Login phase. Business RPS đỉnh gốc/tuned=431.017/545.817; RPS tổng trong bảng có Login.

### Phân loại lỗi từ raw metrics

Đã stream metric `http_reqs` và đối chiếu counts toàn run với summary; không đếm lặp cùng request từ nhiều metric. Chi tiết: [transport-summary.json](../../submission/evidence/assignee-b/transport-summary.json).

| Spike | HTTP requests toàn run | Status 0 / lỗi transport | Loại lỗi k6 ghi nhận |
| --- | ---: | ---: | --- |
| Gốc | 29497 | 1299 | 1204 connection refused (1212); 95 reset by peer (1220) |
| Tuned | 36373 | 1164 | 1162 connection refused (1212); 1 reset (1220); 1 EOF (1000) |

Các lỗi trên đều ở hold_1500; response còn lại status 200, không có 4xx/5xx. Logs server không có thông báo crash. Đây là bằng chứng lỗi kết nối trong điều kiện tải thực đo, **chưa chứng minh nguyên nhân là DB, server chết hay Windows socket/backlog**. Cần đo socket/backlog, event-loop, tài nguyên từng process và DB I/O/locks để phân biệt. Không retry trực tiếp checkout bị lỗi vì order có thể đã được ghi; chưa đối soát toàn vẹn từng order sau lỗi transport.

## Đối chiếu reference A và confirmation B

| Bài / cấu hình | A p95 ms | B p95 ms | A HTTP lỗi | B HTTP lỗi | A/B kết luận |
| --- | ---: | ---: | ---: | ---: | --- |
| Baseline gốc, steady | 8.122 | 12.381 | 0% | 0% | PASS / PASS |
| Baseline tuned, steady | 6.328 | 5.524 | 0% | 0% | PASS / PASS |
| Spike gốc, hold_1500 | 5344.455 | 1948.729 | 1.486% | 4.674% | FAIL / FAIL |
| Spike tuned, hold_1500 | 6.849 | 93.402 | 0% | 3.360% | PASS / FAIL |

Reference A: baseline gốc `baseline-20261022-110446-eGLTX1`, tuned `baseline-20261023-084311-TSxg2P`; spike gốc `spike-20261022-190641-UgVeF4`, tuned `spike-20261023-085706-BOOKoc`. Nguồn trong [verification-summary.json](../../submission/evidence/assignee-b/verification-summary.json); không ghép raw run khác vào reference.

**Kết luận D8b: đã chạy lại được; xu hướng latency tốt hơn sau tuning được quan sát trên B, nhưng khả năng spike tuned đạt toàn bộ SLO của A chưa tái lập.** Baseline đạt trên cả hai môi trường. Không thể kết luận hiệu năng độc lập máy: A chạy Linux, B chạy Windows; reference thiếu checksum môi trường/DB/công cụ đầy đủ và chưa có chạy lặp. Hai phép so sánh gốc/tuned không tách riêng tác động WAL khỏi index hoặc biến động hệ thống.

## Danh mục lần chạy và kiểm tra bằng chứng

Timestamps trong run ID là UTC; cộng 7 giờ để đọc theo Asia/Bangkok. Toàn bộ lượt chạy khoảng 16:29–16:49 ngày 23/10/2026.

| Run ID | Exit code k6 | Kết quả |
| --- | ---: | --- |
| `smoke-original-2026-10-23T09-29-40-669Z` | 0 | 5 request, 10 checks đạt; p95 39.428ms |
| `smoke-tuned-2026-10-23T09-29-52-855Z` | 0 | 5 request, 10 checks đạt; p95 21.681ms |
| `baseline-original-2026-10-23T09-30-08-179Z` | 0 | 25/25 thresholds đạt |
| `baseline-tuned-2026-10-23T09-37-12-574Z` | 0 | 25/25 thresholds đạt |
| `spike-original-2026-10-23T09-44-14-975Z` | 99 | 51/63 thresholds đạt |
| `spike-tuned-2026-10-23T09-46-52-990Z` | 99 | 56/63 thresholds đạt |

Từng thư mục nằm trong [evidence](../../submission/evidence/assignee-b/README.md), gồm metadata/summary/log. Raw metrics và hai dashboard baseline có trong `local-runs/<run-id>/`, không commit. Runner Windows và cách tái chạy: [README](README.md). Báo cáo một trang: [performance_report.md](../../submission/performance_report.md).

Bước 1–5 đã hoàn tất theo phạm vi Windows: môi trường và DB kiểm chứng được, smoke đủ luồng, bốn run đủ profile và raw output, phân tích có nguồn và báo cáo một trang. Parser đã kiểm tra threshold legacy/object, trường hợp thiếu metric, biên p95=500/error=1% và đối chiếu reference PASS/FAIL. Không thêm stress hoặc thay workload khi kết quả xấu. Slides, báo cáo chung và sign-off nhóm chưa thực hiện theo giới hạn lần triển khai này.

## Khuyến nghị

1. Điều tra connection refused/reset bằng telemetry hệ điều hành/Node cùng thời điểm; không chỉnh script để giấu lỗi. Ưu tiên quan sát giai đoạn nhảy 50→1500 và làn sóng lazy login.
2. Chạy lặp với cùng snapshot/build và mức nền tương đương để đánh giá độ biến thiên; có thể tách load generator khỏi SUT cho thí nghiệm tiếp theo, nhưng phải ghi là điều kiện mới.
3. Đối soát orders sau lỗi transport trước khi kết luận đúng dữ liệu; kéo dài recovery nếu cần đánh giá ổn định dài hạn.
4. Giữ kết luận spike tuned chưa đạt trên B trong tài liệu bàn giao, dù latency cải thiện rõ.

## Chạy lại spike lần 2 — 23/10/2026, khoảng 17:13–17:19 (UTC+7)

Theo yêu cầu chạy lại, giữ nguyên script, profile và quy trình tạo SUT/DB sạch. Không thay số liệu lần đầu. SHA-256 script và source SUT của hai lượt được đối chiếu; file SQLite nguồn vẫn không đổi.

| Bản / lượt | Requests đỉnh | p50 ms | p95 ms | p99 ms | RPS đỉnh | HTTP lỗi đỉnh | Skipped | Thresholds đạt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Gốc / 1 | 27791 | 627.172 | 1948.729 | 2581.905 | 463.183 | 4.674% | 480 | 51/63 |
| Gốc / 2 | 27996 | 683.218 | 1360.578 | 2346.788 | 466.600 | 4.622% | 474 | 51/63 |
| Tuned / 1 | 34644 | 3.799 | 93.402 | 319.655 | 577.400 | 3.360% | 444 | 56/63 |
| Tuned / 2 | 35005 | 3.406 | 59.286 | 200.170 | 583.417 | 3.434% | 490 | 56/63 |

Cả hai run mới đều exit 99. Trước spike và recovery đều đạt thresholds; recovery lần 2 gốc/tuned có 1100/1096 request, p95=16.399/9.062ms, HTTP lỗi 0%, checks 100%, skipped 0.

Raw metrics lần 2: gốc có 1294 lỗi transport (1231 refused, 63 reset) trên 29708 request toàn run; tuned có 1202 lỗi (1200 refused, 2 reset) trên 36745 request. Các lỗi đều ở đỉnh; response còn lại status 200. Nguồn: `transport-summary.json`.

**Nhận xét sau hai lần:** kết luận PASS/FAIL và mức HTTP error tương đối nhất quán, trong khi p95 vẫn biến thiên. Tuned tiếp tục có latency thấp hơn và throughput cao hơn bản gốc, nhưng HTTP lỗi khoảng 3.4% và skipped khác 0 khiến spike vẫn không đạt. Kết quả PASS spike tuned của A chưa tái lập sau cả hai lượt trên B. Chưa đủ dữ liệu để xác định nguyên nhân gốc hoặc khẳng định độ ổn định thống kê.

Run IDs mới trong evidence:

- `spike-original-2026-10-23T10-13-44-617Z`
- `spike-tuned-2026-10-23T10-16-21-556Z`
