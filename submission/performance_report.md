# EShop — Kiểm chứng hiệu năng trước và sau tối ưu SQLite

**23/10/2026 · Confirmation trên Windows/PowerShell · Kết luận: tái lập một phần.**

Phép đo này chạy lại cùng script k6 trên hai môi trường: máy A chạy Linux là nơi đo ban đầu; máy B chạy Windows là nơi kiểm chứng. Baseline là tải bình thường, spike là tải tăng đột biến; bản tuned là backend bật SQLite WAL và thêm index tên sản phẩm. p95 là thời gian phản hồi mà 95% request không vượt quá; SLO là mục tiêu chất lượng cần đạt.

**Môi trường:** Windows 10.0.26200 x64, Ryzen 7 5700U/16 logical CPUs, RAM 7.35 GiB; Node 24.20.0, k6 2.2.0, SQLite 3.52.0. SUT và k6 cùng máy. Mỗi run dùng SUT bản sao mới, 50 account k6, 5 sản phẩm, 0 orders ban đầu. Đã xác nhận bản gốc journal DELETE; tuned WAL + index tên sản phẩm. Query `LIKE '%iPhone%'` vẫn `SCAN products` ở cả hai.

**Workload:** giữ nguyên script A. Baseline ramp 60s + steady 50 VUs/300s + giảm tải 60s, mix Search/Detail/Cart/Checkout=55/25/14/6. Spike 50 VUs/30s →1500/60s →50/60s, mix=40/20/22/18. Lazy login, dữ liệu cố định, think-time và timeout không đổi.

| Cửa sổ đo | Requests | p50/p95/p99 (ms) | RPS | HTTP lỗi | SLO |
| --- | ---: | --- | ---: | ---: | --- |
| Baseline gốc steady | 5967 | 1.806 / 12.381 / 16.353 | 19.890 | 0% | PASS |
| Baseline tuned steady | 5972 | 1.656 / 5.524 / 9.010 | 19.907 | 0% | PASS |
| Spike gốc đỉnh | 27791 | 627.172 / 1948.729 / 2581.905 | 463.183 | 4.674% | FAIL |
| Spike tuned đỉnh | 34644 | 3.799 / 93.402 / 319.655 | 577.400 | 3.360% | FAIL |

SLO: p95 <500ms, HTTP lỗi <1%, checks ≥99%, có mẫu tổng/từng API, skipped=0. Tổng phase gồm Login; RPS chia thời lượng phase. Baseline đạt 25/25 thresholds mỗi bản. Spike gốc/tuned đạt 51/63 và 56/63; skipped=480/444. Recovery cả hai đạt SLO trong 60s, p95=17.369/8.997ms, lỗi 0%.

**Đối chiếu A/B:** baseline cùng đạt, latency sau tune thấp hơn. Spike tuned của A PASS (p95 6.849ms, lỗi 0%); B đạt latency nhưng FAIL lỗi/checks/skipped. Vì vậy chưa xác nhận kết quả spike tuned độc lập môi trường. Raw B ghi 1299/1164 lỗi transport ở spike gốc/tuned, chủ yếu connection refused; không có HTTP 4xx/5xx.

**Chạy lại spike lần 2:** gốc p95 1360.578ms, lỗi 4.622%, skipped 474; tuned p95 59.286ms, lỗi 3.434%, skipped 490. Cả hai vẫn FAIL, recovery đều PASS. Tỷ lệ lỗi gần lần đầu, latency có biến thiên; kết luận chưa tái lập PASS tuned của A được giữ nguyên.

**Phân tích và khuyến nghị:** tuning đi cùng latency thấp hơn, nhưng chưa tách tác động WAL/index; chưa có bằng chứng xác định DB là bottleneck. Thu socket/backlog, event-loop, CPU/RAM từng process và DB I/O đồng thời; chạy lặp cùng snapshot, đối soát orders sau lỗi kết nối. Baseline một lần và spike hai lần mỗi cấu hình trên B; hai máy khác OS, reference thiếu metadata đầy đủ; recovery 60s không chứng minh ổn định dài hạn.

Nguồn số liệu, mã lần chạy và cách chạy lại: [báo cáo kiểm chứng](../performance/verification/verification_report.md), [bằng chứng thực nghiệm](evidence/assignee-b/README.md). Hai bài kiểm tra nhanh (smoke) đều đủ 5 request/10 checks; DB nguồn không bị reset. Trợ lý Codex thực hiện trên máy B; các thành viên chưa trực tiếp xác nhận việc tự chạy và đọc kết quả của công cụ do người khác chuẩn bị (cross-run).
