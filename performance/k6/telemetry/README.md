# Thu CPU/RAM Node.js

`telemetry/` giữ phần thu tài nguyên. Phần phân tích và tạo báo cáo nằm trong [analyze/](../analyze/README.md).

## Cách đo

- `node.cjs` lấy mẫu của chính tiến trình backend mỗi giây.
- CPU = chênh lệch thời gian CPU user + system / thời gian thực; 100% = một core.
- RAM = RSS qua `process.memoryUsage.rss()`, ghi bytes và được analyzer đổi sang MiB.
- Chu kỳ lấy mẫu có thể trễ khi Node bận; không giả định một mẫu luôn tương ứng đúng một giây.

Chạy stress theo [README](../README.md): mở backend → seed → chạy `run-stress.sh`. Runner thu 30s trước → chạy k6 → thu 60s sau → gọi `analyze/analyze.py`. Giữ backend đến khi runner kết thúc.

Run lưu `node-cpu-ram.jsonl` và `measurement-timeline.json`. Analyzer dùng mốc scenario/profile để chia ramp, hold, recovery; grace cuối và setup được tách riêng. Thống kê dùng cửa sổ [bắt đầu, kết thúc), TB là trung bình mẫu. Các CSV phân tích được ghi vào thư mục đích analyzer cùng báo cáo.

## File cục bộ và Git

Log trong `output/telemetry/` và bản mẫu từng run `node-cpu-ram.jsonl` được [Git ignore](../../../.gitignore). Ba CSV `node-cpu-ram.csv`, `cpu-ram-phases.csv`, `cpu-ram-before-during-after.csv` cũng được ignore ở mọi thư mục. Ignore không tắt bộ thu, không ngăn analyzer ghi CSV và không xóa file đã có.

Nếu cần lưu hoặc gửi lại kết quả đo, giữ riêng mẫu JSONL của run và timeline; giữ thêm `k6.log` nếu mốc scenario/profile chỉ nằm trong log. CSV có thể tạo lại từ các dữ liệu này bằng [analyzer](../analyze/README.md#cách-chạy); summary k6 không chứa mẫu CPU/RAM. Mẫu gốc đã mất thì không thể khôi phục tài nguyên chỉ từ báo cáo hoặc summary.

## Tùy chọn

- `TELEMETRY=0 bash performance/k6/run-stress.sh`: bỏ thời gian thu trước/sau; vẫn tạo báo cáo HTTP.
- `TELEMETRY=0 node backend/server.js`: tắt đo ở backend.
- Đường dẫn riêng: truyền cùng `TELEMETRY_FILE` cho backend và runner; mặc định runner tìm file của backend đang chạy trong `output/telemetry/`.

Ctrl-C dừng bài test, backend vẫn chạy. Nếu không tìm thấy file đo, k6 vẫn chạy và analyzer ghi thiếu CPU/RAM. Baseline cũng thu 30s trước / 60s sau tải, lưu timeline và tự gọi analyzer để cập nhật `reports/02-baseline-test-report.md` và `reports/baseline_report.html`. Dùng `TELEMETRY=0 bash performance/k6/run-baseline.sh` để chỉ đo HTTP. Spike chưa tích hợp tự động phần thu này; analyzer vẫn đọc được summary.
