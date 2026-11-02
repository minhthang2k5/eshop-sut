# Thu CPU/RAM Node.js

`telemetry/` giữ phần thu tài nguyên. Phần phân tích và tạo báo cáo nằm trong [analyze/](../analyze/README.md).

## Cách đo

- `node.cjs` lấy mẫu của chính tiến trình backend mỗi giây.
- CPU = chênh lệch thời gian CPU user + system / thời gian thực; 100% = một core.
- RAM = RSS qua `process.memoryUsage.rss()`, ghi bytes và được analyzer đổi sang MiB.
- Chu kỳ lấy mẫu có thể trễ khi Node bận; không giả định một mẫu luôn tương ứng đúng một giây.

Chạy stress theo [README](../README.md): mở backend → seed → chạy `run-stress.sh`. Runner thu 30s trước → chạy k6 → thu 60s sau → gọi `analyze/analyze.py`. Giữ backend đến khi runner kết thúc.

Run lưu `node-cpu-ram.jsonl` và `measurement-timeline.json`. Analyzer dùng mốc scenario/profile để chia ramp, hold, recovery; grace cuối và setup được tách riêng. Thống kê dùng cửa sổ [bắt đầu, kết thúc), TB là trung bình mẫu. Các CSV phân tích được ghi vào thư mục đích analyzer cùng báo cáo.

## Tùy chọn

- `TELEMETRY=0 bash performance/k6/run-stress.sh`: bỏ thời gian thu trước/sau; vẫn tạo báo cáo HTTP.
- `TELEMETRY=0 node backend/server.js`: tắt đo ở backend.
- Đường dẫn riêng: truyền cùng `TELEMETRY_FILE` cho backend và runner; mặc định runner tìm file của backend đang chạy trong `output/telemetry/`.

Ctrl-C dừng bài test, backend vẫn chạy. Nếu không tìm thấy file đo, k6 vẫn chạy và analyzer ghi thiếu CPU/RAM. Baseline/spike hiện chưa tích hợp tự động phần thu này; analyzer vẫn đọc được summary của chúng.
