# CPU/RAM Node.js

Chạy stress theo [README](../README.md): mở backend → seed → chạy `run-stress.sh`.

## Cách đo

- `node.cjs` lấy mẫu của chính tiến trình backend mỗi giây.
- CPU = chênh lệch thời gian CPU user + system / thời gian thực; 100% = một core.
- RAM = RSS qua `process.memoryUsage.rss()`, đổi sang MiB.
- Runner thu **30s trước tải → trong stress → 60s sau tải**; giữ backend chạy nguyên trạng.
- Mốc scenario và profile chia mẫu theo ramp/hold/recovery; grace cuối ghi riêng. Chu kỳ lấy mẫu có thể trễ khi Node bận.

## Kết quả

Hai bảng tự cập nhật ở **mục 6.3** của [03-stress-test-report.md](../reports/03-stress-test-report.md):

1. CPU/RAM từng phase.
2. CPU/RAM trước–trong–sau stress và chênh lệch sau − trước.

Bảng gồm số mẫu, CPU TB/max, RAM TB/max/đầu/cuối. TB là trung bình mẫu; thiếu dữ liệu hiển thị `—`. Trong stress gồm recovery và grace, setup được tách riêng.

Thư mục run giữ `node-cpu-ram.jsonl`, `node-cpu-ram.csv`, hai bảng `cpu-ram-*.csv` và `measurement-timeline.json`. Lần chạy mới thay phần CPU/RAM trong báo cáo, giữ các phần khác.

## Tùy chọn

- `TELEMETRY=0 bash performance/k6/run-stress.sh`: chỉ chạy k6, bỏ thời gian thu trước/sau.
- `TELEMETRY=0 node backend/server.js`: tắt đo ở backend.
- Đường dẫn riêng: truyền cùng `TELEMETRY_FILE` cho backend và runner; mặc định runner tìm file của backend đang chạy trong `output/telemetry/`.

Ctrl-C dừng bài test, backend vẫn chạy. Nếu không tìm thấy file đo, k6 vẫn chạy và báo thiếu dữ liệu CPU/RAM.
