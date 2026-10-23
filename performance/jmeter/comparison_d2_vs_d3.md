# Đối chiếu kết quả kiểm thử hiệu năng k6 và JMeter

Trong bảng phân công, D2 là bài baseline k6 (tải bình thường) và D3 là bài JMeter. p95 là thời gian phản hồi mà 95% request không vượt quá; SLO là mục tiêu chất lượng: p95 <500ms và tỷ lệ lỗi <1%. Các mã D2/D3 bên dưới dùng để truy vết hai bài kiểm thử này.

Nguồn: [k6 summary](../k6/output/baseline-20261022-110446-eGLTX1/summary.json), [JMeter summary](results/baseline-summary.json), [môi trường JMeter](results/run-environment.json).

| Chỉ số | D2 — k6 steady | D3 — JMeter actions (không Login) |
|---|---:|---:|
| VUs / threads | 50 | 50 |
| Cửa sổ | 300s steady, sau ramp 60s | Lịch 300s gồm ramp 10s; mẫu actions trải 296,748s |
| Requests | 5925 (gồm 6 Login) | 5140 |
| p50 / p95 / p99 (ms) | 2,034 / 8,122 / 14,546 | 2 / 16 / 21 |
| HTTP lỗi / JMeter sample failure | 0% | 0% |
| RPS | 19,750 (count/300s) | 17,321 (count/observed span) |
| SLO p95 < 500ms; lỗi < 1% | PASS | PASS |

| API | k6 p95 (ms) | k6 HTTP lỗi | JMeter p95 (ms) | JMeter sample failure |
|---|---:|---:|---:|---:|
| Search | 3,071 | 0% | 5 | 0% |
| Detail | 3,031 | 0% | 5 | 0% |
| Cart | 2,770 | 0% | N/A | N/A |
| Checkout | 16,006 | 0% | 21 | 0% |

Cả hai đạt SLO trong lần đo tương ứng. Chênh lệch không dùng để xếp hạng công cụ:

- k6 chọn Search/Detail/Cart/Checkout = 55/25/14/6; JMeter Search/Detail/Checkout = 55/25/20, tỷ trọng checkout cao hơn và không có Cart.
- Think-time mỗi API tương ứng giống nhau, nhưng mix khác làm thời gian nghỉ trung bình khác. k6 lazy Login; JMeter Login một lần/thread (50 mẫu, toàn bài 5190 requests).
- k6 đo steady sau ramp; JMeter đo cả ramp. JMeter dùng elapsed ms/nearest rank; k6 dùng `http_req_duration` và percentile của k6. JMeter failure gồm assertions, khác HTTP error của k6.
- JMeter chạy Windows ngày 21/10, k6 chạy Linux ngày 22/10; thiếu metadata để xác nhận cùng phần cứng/DB ban đầu. RPS dùng mẫu số khác; chưa có bằng chứng quy chênh lệch cho connection pooling.

D3: [test plan](eshop_workload.jmx), [HTML report](results/jmeter-report/index.html), [JTL](results/baseline.jtl), [hướng dẫn CLI](README.md). Token lấy bằng Regular Expression Extractor, gửi `Authorization: Bearer ${token}` cho Checkout.
