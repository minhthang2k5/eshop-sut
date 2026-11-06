# Thu và phân tích CPU/RAM Node.js

`node.cjs` lấy mẫu của chính tiến trình backend mỗi giây. Dữ liệu mặc định nằm trong `output/telemetry/server-*.jsonl`; `telemetry/` chứa bộ thu; báo cáo HTML nằm trong `output/telemetry/`.

- CPU = chênh lệch thời gian CPU user + system / thời gian thực. 100% = một core, có thể vượt 100%.
- RAM = RSS, ghi bằng byte và hiển thị bằng MiB.
- Chu kỳ lấy mẫu có thể trễ khi backend bận; biểu đồ dùng timestamp thực tế.

## Tự động sau test

Bốn runner baseline, stress, spike và soak thu 30 giây trước tải, chạy k6, rồi thu thêm 60 giây. Giữ backend chạy đến khi runner kết thúc. Runner lưu `node-cpu-ram.jsonl` và `measurement-timeline.json` trong thư mục output của lần chạy rồi gọi `../lib/server_analyze.py`.

HTML được ghi vào `output/telemetry/`, cùng tên với file telemetry nguồn, đuôi `.html`. Ví dụ: `server-backend-181580-1793633684076.html`.

## Chạy thủ công

Từ thư mục `eshop-sut`:

```bash
python3 performance/k6/lib/server_analyze.py performance/k6/output/telemetry/server-backend-181580-1793633684076.jsonl
# Có thể truyền nhiều file hoặc glob:
python3 performance/k6/lib/server_analyze.py performance/k6/output/telemetry/server-*.jsonl
# Tạo lại báo cáo riêng cho một run, giữ tên nguồn gốc:
python3 performance/k6/lib/server_analyze.py performance/k6/output/<run>/node-cpu-ram.jsonl --source-name server-backend-181580-1793633684076.jsonl --timeline performance/k6/output/<run>/measurement-timeline.json
```

## Tùy chọn bộ thu

- `TELEMETRY=0 node backend/server.js`: tắt đo backend.
- `TELEMETRY=0 bash performance/k6/run-stress.sh`: bỏ thu telemetry và chờ trước/sau.
- `TELEMETRY_FILE`: chỉ định cùng đường dẫn cho backend và runner.
- `TELEMETRY_DIR`: đổi thư mục dữ liệu; mặc định runner tìm file của backend đang chạy trong `output/telemetry/`.

Log telemetry và mẫu JSONL của từng run được Git ignore. Giữ JSONL và timeline nếu cần tạo lại báo cáo; summary k6 không chứa mẫu CPU/RAM.
