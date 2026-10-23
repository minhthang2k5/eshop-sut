# Bằng chứng kiểm chứng kết quả k6 trước và sau tối ưu SQLite

Thư mục lưu các lần chạy lại script k6 trên Windows/PowerShell để kiểm tra khả năng tái lập kết quả đo ban đầu trên Linux. Trong tài liệu, A là thành viên đo k6 ban đầu, B là thành viên kiểm chứng trên Windows, C phụ trách đánh giá script AI. Nhiệm vụ kiểm chứng có mã D8b trong bảng phân công. Các lần chạy do trợ lý Codex thực hiện trên môi trường của B; từng thành viên vẫn cần trực tiếp xác nhận việc tự chạy công cụ và đọc kết quả (cross-run).

Mỗi thư mục timestamp chứa:

- `metadata.json`: commit/source SHA-256, công cụ, OS/CPU/RAM, timestamps UTC, variant, vị trí raw metrics, cấu hình và số lượng dữ liệu DB trước/sau, exit code k6, xác nhận DB nguồn không đổi.
- `summary.json`: summary k6 nguyên bản, không thay đổi giá trị.
- `k6.log`: stdout/stderr từ k6; không bật HTTP debug hoặc ghi request/response body.
- `server.log`: log khởi động/seed của SUT bản sao.

`verification-summary.json` tổng hợp từng run cùng reference A. Với spike, source không export đủ submetric phase+login, nên count Login theo phase được suy từ tổng request trừ bốn API nghiệp vụ; đánh dấu `inferredFromTotalMinusBusiness`, latency/error Login phase để null. Thống kê Login toàn run được lấy trực tiếp từ summary. Không suy percentile của tổng mới bằng trung bình percentile endpoint.

`transport-summary.json` phân loại theo phase/endpoint/status/error code từ raw metric `http_reqs`, chỉ đếm một lần mỗi request và đối chiếu tổng count với summary. Không chứa request body/token. Tạo bằng `node performance/verification/summarize-transport.cjs` khi raw output còn ở vị trí metadata ghi nhận.

`SHA256SUMS.txt` ghi hash tất cả file evidence trừ chính manifest. Sau khi thêm/sửa README hoặc chạy thêm, tạo lại bằng:

```powershell
node performance/verification/summarize-verification.cjs
```

Chạy từ repo root. Raw metrics, DB bản sao và native dashboard baseline nằm trong `performance/verification/local-runs/<run-id>/`, được Git ignore. Đây là dữ liệu local, không tự có khi clone repository; vị trí cụ thể được lưu trong metadata.

Giới hạn: SUT và k6 cùng máy; baseline một lần và spike hai lần mỗi cấu hình trên B, chưa có chuỗi telemetry CPU/RAM/DB đồng bộ. Metadata ghi RAM đầu run, không phải peak/average trong toàn run. Reference A thiếu snapshot môi trường/DB đầy đủ nên chỉ đối chiếu số liệu và xu hướng, không khẳng định điều kiện hai máy tương đương.

Hướng dẫn chạy lại: [README verification](../../../performance/verification/README.md). Kết luận: [verification report](../../../performance/verification/verification_report.md).
