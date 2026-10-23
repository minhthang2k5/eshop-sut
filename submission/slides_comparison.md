# Nội dung slides — D2/D3 và D8b

Võ Hữu Thắng — Assignee B · 23/10/2026. Bản Markdown theo yêu cầu, dùng để trình bày hoặc chuyển sang slide sau này. Số thập phân dùng dấu chấm, latency đơn vị ms.

## Slide 1 — Mục tiêu và bằng chứng

- D2: k6 viết tay của A, baseline tải bình thường.
- D3: JMeter của B, API workload có JWT, dữ liệu CSV và assertions.
- D8b: dùng **k6 của A** trên máy Windows B để xác minh trước/sau SQLite tuning.
- SLO latency/error: p95 <500ms, lỗi <1%. k6 có thêm checks/count/skipped thresholds.

Nguồn: [D2](evidence/k6/summaries/baseline-20261022-110446-eGLTX1/summary.json), [D3](../performance/jmeter/results/baseline-summary.json), [D8b](../performance/verification/verification_report.md).

Lời trình bày: D3 đối chiếu hai công cụ; D8b đối chiếu khả năng tái lập của cùng script trên môi trường khác. Hai mục đích cần được trình bày riêng.

## Slide 2 — Hai workload D2/D3 khác nhau ở đâu?

| Thành phần | D2 k6 A | D3 JMeter B |
| --- | --- | --- |
| Tải | Ramp 60s, steady 50 VUs/300s, giảm tải 60s | 50 threads, ramp 10s trong tổng 300s |
| API/mix | Search/Detail/Cart/Checkout=55/25/14/6 | Search/Detail/Checkout=55/25/20 |
| Dữ liệu | iPhone, ID 1, giá cố định | Keyword/product ngẫu nhiên từ CSV ID 1–5 |
| Login | Lazy trước Cart/Checkout | Một lần khi thread bắt đầu |
| Think-time | Search 1–3s, Detail 2–5s, Cart 1–3s, Checkout 3–6s; sau request | Ba API tương ứng cùng khoảng thời gian; timer trước request |
| Chọn action | Một nhánh ngẫu nhiên mỗi iteration | Throughput Controllers độc lập, Percent Executions/Per User |
| Môi trường | Linux, SUT/k6 cùng máy | Windows, SUT/JMeter cùng máy |
| Phạm vi tổng | Steady, có Cart và Login phát sinh | Toàn lịch tải, actions loại Login |

Lời trình bày: cả hai là closed workload có think-time. VUs bằng nhau chưa tạo điều kiện benchmark tương đương; không suy JMeter/k6 nhanh hơn từ bảng latency.

## Slide 3 — Kết quả D2/D3

| API | D2 p95 | D2 HTTP lỗi | D3 p95 | D3 sample failure |
| --- | ---: | ---: | ---: | ---: |
| Search | 3.071 | 0% | 5 | 0% |
| Detail | 3.031 | 0% | 5 | 0% |
| Cart | 2.770 | 0% | N/A | N/A |
| Checkout | 16.006 | 0% | 21 | 0% |

| Login toàn run, báo riêng | D2 | D3 |
| --- | ---: | ---: |
| Count | 50 | 50 |
| p95 | 4.820 | 157 |
| Lỗi | 0% | 0% |

D3 actions: 5140 mẫu, p50/p95/p99=2/16/21ms, lỗi 0%; tỷ lệ thực tế 55.253/24.961/19.786%. D2 tổng steady: 5925 mẫu, p50/p95/p99=2.034/8.122/14.546ms, HTTP lỗi 0%; có 6 Login và Cart. Hai tổng này không cùng phạm vi mẫu.

Lời trình bày: cả hai đạt SLO của lần đo tương ứng. JMeter sample failure gồm assertion; k6 tách HTTP failure và checks. Số liệu không đủ để quy chênh lệch cho connection pooling.

## Slide 4 — D8b: baseline tái lập được gì?

| Máy / cấu hình | p95 steady | HTTP lỗi | Kết quả |
| --- | ---: | ---: | --- |
| A gốc | 8.122 | 0% | PASS |
| A tuned | 6.328 | 0% | PASS |
| B gốc | 12.381 | 0% | PASS |
| B tuned | 5.524 | 0% | PASS |

B chạy k6 2.2.0, Node 24.20.0, SQLite 3.52.0 trên Windows; source và môi trường lưu trong metadata. Bản gốc journal DELETE, bản tuned WAL + index tên sản phẩm, mỗi run có DB bản sao mới. Query plan `LIKE '%iPhone%'` vẫn `SCAN products` ở cả hai.

Lời trình bày: baseline có cùng kết luận PASS và xu hướng latency thấp hơn sau tuning. Chưa tách riêng tác dụng WAL/index hoặc biến động máy; chưa chứng minh quan hệ nhân quả từ một cặp baseline.

## Slide 5 — D8b: spike chạy hai lần trên B

Đỉnh tải 1500 VUs trong 60s, cùng script/profile với A.

| Cấu hình | Lượt | p95 | HTTP lỗi | Skipped | Kết quả |
| --- | --- | ---: | ---: | ---: | --- |
| Gốc | B1 | 1948.729 | 4.674% | 480 | FAIL |
| Gốc | B2 | 1360.578 | 4.622% | 474 | FAIL |
| Tuned | B1 | 93.402 | 3.360% | 444 | FAIL |
| Tuned | B2 | 59.286 | 3.434% | 490 | FAIL |

A tuned PASS: p95 6.849ms, HTTP lỗi 0%. B tuned đạt latency nhưng fail error/checks/skipped. Mọi cửa sổ recovery trên B đạt SLO trong 60s. Raw B chủ yếu connection refused/reset; không có HTTP 4xx/5xx trong các spike này.

Lời trình bày: kết quả spike tuned PASS của A chưa tái lập sau hai lần trên B. Khác môi trường là yếu tố cần điều tra, chưa có telemetry để khẳng định Windows/phần cứng hoặc SQLite là nguyên nhân duy nhất.

## Slide 6 — Cross-run và kết luận bàn giao

**Cross-run:** thành viên khác tự chạy script của người viết, biết chuẩn bị SUT/dữ liệu và đọc output. Mục tiêu là kiểm tra khả năng chuyển giao công cụ, không yêu cầu mọi timing giống nhau hoặc mọi bài tải đều PASS.

- Đã có: trợ lý chạy k6 A trong workspace B, metadata/log đầy đủ; đây là evidence kỹ thuật D8b.
- Còn cần: B trực tiếp xác nhận chạy k6; A/C tự chạy JMeter và các lượt còn lại theo phân công, lưu người chạy, phiên bản, lệnh, run ID và output.
- Chưa được đánh dấu cả nhóm hoàn thành cross-run; không ký thay người khác.

Kết luận: D3 đạt SLO của workload đã đo; D8b tái lập được baseline và xu hướng latency, chưa tái lập PASS spike tuned. Ưu tiên đo socket/backlog, event-loop, DB I/O và tài nguyên từng process, rồi đối soát orders sau lỗi transport.

Hướng dẫn/sign-off: [cross_run_signoff.md](../performance/verification/cross_run_signoff.md). Báo cáo ngắn: [performance_report.md](performance_report.md).
