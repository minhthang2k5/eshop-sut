# So sánh kiểm thử hiệu năng bằng k6 và JMeter

Võ Hữu Thắng · 23/10/2026. Nội dung trình bày kết quả kiểm thử ứng dụng EShop và kiểm chứng kết quả trước–sau tối ưu SQLite trên hai máy. Số thập phân dùng dấu chấm, thời gian phản hồi đơn vị ms.

Quy ước: **máy A** là môi trường Linux thực hiện phép đo k6 ban đầu; **máy B** là môi trường Windows chạy JMeter và chạy lại k6 để kiểm chứng. A/B chỉ người và môi trường thực hiện, không phải tên công cụ.

## Slide 1 — Mục tiêu và bằng chứng

- **k6:** đo hiệu năng ở tải bình thường bằng script do thành viên A viết.
- **JMeter:** đo các thao tác API với token đăng nhập JWT, dữ liệu CSV và kiểm tra nội dung phản hồi.
- **Kiểm chứng trên máy khác:** chạy lại script k6 trên máy B với backend gốc và backend đã tối ưu SQLite.
- **Mục tiêu chất lượng (SLO):** p95 <500ms và tỷ lệ lỗi <1%. p95 là mức thời gian mà 95% request có thời gian phản hồi không vượt quá. k6 còn kiểm tra tỷ lệ checks thành công, số request và số thao tác bị bỏ qua.

Nguồn: [Kết quả k6](evidence/k6/summaries/baseline-20261022-110446-eGLTX1/summary.json), [Kết quả JMeter](../performance/jmeter/results/baseline-summary.json), [Báo cáo kiểm chứng trên máy B](../performance/verification/verification_report.md).

Lời trình bày: phần đầu so sánh hai bài kiểm thử k6/JMeter; phần sau kiểm tra cùng script k6 có cho kết luận tương tự trên máy khác hay không.

## Slide 2 — Hai bài kiểm thử tạo tải khác nhau ở đâu?

| Thành phần | k6 trên máy A | JMeter trên máy B |
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

## Slide 3 — Kết quả k6 và JMeter

| API | k6 p95 (ms) | k6 HTTP lỗi | JMeter p95 (ms) | JMeter request thất bại |
| --- | ---: | ---: | ---: | ---: |
| Search | 3.071 | 0% | 5 | 0% |
| Detail | 3.031 | 0% | 5 | 0% |
| Cart | 2.770 | 0% | N/A | N/A |
| Checkout | 16.006 | 0% | 21 | 0% |

| Đăng nhập trong toàn bài, báo riêng | k6 | JMeter |
| --- | ---: | ---: |
| Count | 50 | 50 |
| p95 | 4.820 | 157 |
| Lỗi | 0% | 0% |

JMeter có 5140 request nghiệp vụ, p50/p95/p99=2/16/21ms, lỗi 0%; tỷ lệ Search/Detail/Checkout thực tế là 55.253/24.961/19.786%. k6 có 5925 request trong giai đoạn tải ổn định, p50/p95/p99=2.034/8.122/14.546ms, HTTP lỗi 0%; bao gồm Cart và 6 request Login. Hai tổng này không cùng phạm vi mẫu.

Lời trình bày: cả hai đạt SLO của lần đo tương ứng. JMeter sample failure gồm assertion; k6 tách HTTP failure và checks. Số liệu không đủ để quy chênh lệch cho connection pooling.

## Slide 4 — Chạy lại k6 trên máy khác: kết quả ở tải bình thường

Giữ cùng script k6, chạy backend gốc và backend đã tối ưu trên mỗi máy. “Tuned” trong bảng là bản bật chế độ ghi SQLite WAL và thêm index tên sản phẩm.

| Máy / cấu hình | p95 steady | HTTP lỗi | Kết quả |
| --- | ---: | ---: | --- |
| A gốc | 8.122 | 0% | PASS |
| A tuned | 6.328 | 0% | PASS |
| B gốc | 12.381 | 0% | PASS |
| B tuned | 5.524 | 0% | PASS |

B chạy k6 2.2.0, Node 24.20.0, SQLite 3.52.0 trên Windows; source và môi trường lưu trong metadata. Bản gốc journal DELETE, bản tuned WAL + index tên sản phẩm, mỗi run có DB bản sao mới. Query plan `LIKE '%iPhone%'` vẫn `SCAN products` ở cả hai.

Lời trình bày: baseline có cùng kết luận PASS và xu hướng latency thấp hơn sau tuning. Chưa tách riêng tác dụng WAL/index hoặc biến động máy; chưa chứng minh quan hệ nhân quả từ một cặp baseline.

## Slide 5 — Tải tăng đột biến: hai lần kiểm chứng bằng k6 trên máy B

Spike là bài kiểm thử tăng tải đột ngột. Đỉnh tải ở đây là 1500 người dùng ảo (VUs) trong 60s, cùng script và lịch tải với máy A. B1/B2 là lần chạy thứ nhất/thứ hai trên máy B; Skipped là số thao tác nghiệp vụ bị bỏ qua do đăng nhập thất bại.

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

- Đã có: trợ lý chạy script k6 của A trên môi trường B, lưu thông tin môi trường và log đầy đủ làm bằng chứng kiểm chứng kỹ thuật.
- Còn cần: B trực tiếp xác nhận chạy k6; A/C tự chạy JMeter và các lượt còn lại theo phân công, lưu người chạy, phiên bản, lệnh, run ID và output.
- Chưa được đánh dấu cả nhóm hoàn thành cross-run; không ký thay người khác.

Kết luận: bài JMeter đạt mục tiêu chất lượng của cấu hình đã đo. Chạy lại k6 trên máy B xác nhận được kết quả PASS ở tải bình thường và xu hướng thời gian phản hồi thấp hơn sau tối ưu; kết quả PASS ở tải đột biến của bản tối ưu trên máy A chưa tái lập được trên máy B. Cần đo thêm kết nối mạng, hàng đợi xử lý, hoạt động đọc/ghi DB và tài nguyên từng tiến trình để tìm nguyên nhân, đồng thời đối soát đơn hàng sau lỗi kết nối.

Hướng dẫn/sign-off: [cross_run_signoff.md](../performance/verification/cross_run_signoff.md). Báo cáo ngắn: [performance_report.md](performance_report.md).
