# Cross-run — cách thực hiện và trạng thái xác nhận

## Cross-run dùng để xác nhận điều gì?

Theo phân công, cả A/B/C cần sử dụng được k6 và JMeter. Thành viên chạy script do người khác chuẩn bị, tự xác định đúng SUT/dataset, chạy được và giải thích output. Mỗi người cần có bằng chứng cho công cụ mình chưa phụ trách; không dùng một lần trợ lý chạy trên máy B để suy cả nhóm đã biết thao tác.

Quy ước thành viên: A phụ trách script k6 và tối ưu SQLite; B phụ trách JMeter và kiểm chứng kết quả; C phụ trách đánh giá script AI. Máy A chạy Linux; máy B chạy Windows. D8b là mã nhiệm vụ kiểm chứng khả năng tái lập kết quả k6 trước và sau tối ưu SQLite. Sign-off là xác nhận trực tiếp của người thực hiện, kèm bằng chứng lần chạy.

D8b hỏi kết quả trước/sau tuning có tái lập trên môi trường B không. Cross-run hỏi quy trình/script có chuyển giao cho người khác sử dụng được không. Một run có thể phục vụ cả hai nếu người thực hiện, cấu hình và bằng chứng được ghi rõ. SLO FAIL là kết quả hiệu năng; người thực hiện vẫn có thể hoàn thành cross-run nếu phát đủ workload, lưu và giải thích kết quả đúng. Lỗi cài đặt khiến không chạy được plan thì chưa hoàn thành.

## Trạng thái hiện tại

| Hạng mục | Bằng chứng | Trạng thái |
| --- | --- | --- |
| Chạy k6 A trên môi trường B, D8b | [Confirmation report](verification_report.md), metadata và logs | Đã có bằng chứng kỹ thuật do Codex thực thi |
| B trực tiếp thao tác k6 và xác nhận hiểu kết quả | Chưa có xác nhận thao tác trực tiếp của B | Chờ B xác nhận bằng run thực tế |
| A tự chạy JMeter của B | Chưa nhận log/run ID gắn với người chạy | Pending |
| C tự chạy JMeter và chứng minh sử dụng cả hai công cụ | Chưa có sign-off liên công cụ; evidence web audit không tự thay thế xác nhận này | Pending |

Không ký thay A/B/C. Metadata các confirmation run đã ghi người thực thi là Codex trong workspace B. Đây là trạng thái bàn giao, chưa phải chứng nhận hoàn thành cross-run toàn nhóm.

## Thao tác cho người nhận

1. Ghi tên, ngày, commit và phiên bản công cụ.
2. k6: dùng [README verification](README.md), bắt đầu bằng smoke; đọc summary/exit code. Nếu làm D8b thì giữ đúng baseline/spike, gốc/tuned và dữ liệu tương đương.
3. JMeter: dùng [README CLI](../jmeter/README.md), chuẩn bị backend và CSV, chạy smoke CLI rồi baseline nếu cần evidence đo chính thức. Mỗi run có output mới, tắt GUI listeners; không dùng GUI để phát tải.
4. Người chạy tự đọc count, Login, error, p95 và kết luận. Với smoke, xác nhận các action xuất hiện; nếu ít mẫu thì tăng thời lượng phù hợp trước khi xác nhận đủ luồng.
5. Gửi lại log/summary, cấu hình và đường dẫn report; không đưa token/password vào bằng chứng. Điền bảng xác nhận bên dưới.

Chỉ ghi hoàn tất khi người thực sự chạy đã cung cấp bằng chứng. Chạy smoke kiểm tra chuyển giao không thay cho baseline/spike đủ profile khi dùng làm kết quả D8b.

## Mẫu sign-off để thành viên điền

| Người thực sự chạy | Công cụ / người viết script | Commit / tool version | Ngày và môi trường | Lệnh / cấu hình | Run ID + evidence | Nhận xét / xác nhận |
| --- | --- | --- | --- | --- | --- | --- |
| B — chờ thao tác | k6 / A | Chờ điền | Chờ điền | Chờ điền | Chờ điền | Pending |
| A — chờ thao tác | JMeter / B | Chờ điền | Chờ điền | Chờ điền | Chờ điền | Pending |
| C — chờ thao tác | JMeter / B và k6 theo yêu cầu nhóm | Chờ điền | Chờ điền | Chờ điền | Chờ điền | Pending |
