# k6 — EShop API Performance Testing

## Chuẩn bị

Chạy lệnh từ `eshop-sut`. Cần Node.js, k6; stress cần thêm Python 3.

```bash
npm ci --prefix backend
npm ci --prefix tuned-backend
```

Terminal 1 mở một backend:

```bash
node backend/server.js
# Hoặc:
node tuned-backend/server.js
```

Backend reset database khi khởi động. Trước mỗi bài mới, restart backend rồi seed lại; smoke dùng dữ liệu startup nên không cần seed.

## Smoke

1 VU × 1 iteration, kiểm tra Login → Search → Detail → Cart → Checkout.

Terminal 2:

```bash
bash performance/k6/run-smoke.sh
```

## Baseline

Ramp lên 50 VU trong 1 phút → giữ 5 phút → hạ tải 1 phút.

**Hiện chưa tương thích fixture:** script yêu cầu đúng 50 account, còn CSV hiện có 10.000. Các lệnh dưới áp dụng với fixture 50 account tương ứng.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-baseline.sh
```

## Stress

15 bậc **200–3000 VU**, bước 200; mỗi bậc ramp 30s + hold 120s; recovery 50 VU/60s. Lịch tải **38m30s**, chưa tính grace cuối tối đa 60s.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-stress.sh
```

`run-stress.sh` điều khiển trực tiếp: `sleep 30` → `k6 run stress.js` → `sleep 60` → `analyze.py` tổng hợp k6 và CPU/RAM, tạo báo cáo Markdown/HTML cùng biểu đồ SVG. Giữ backend chạy đến khi runner kết thúc. Toàn bộ [báo cáo stress](reports/03-stress-test-report.md) và [biểu đồ HTML](reports/stress_report.html) được tạo lại từ cùng run; chỉnh sửa thủ công trong hai tệp sẽ bị thay thế. PASS/FAIL tính theo cấu hình stress trong `analyze/profiles.json`; skipped chỉ để theo dõi. Có thể tạo lại mà không chạy tải:

```bash
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type stress
# Xuất sang thư mục riêng:
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type stress --report-dir /tmp/stress-report
```

Analyzer mặc định xuất `report.md`, `report.html` và CSV vào thư mục `analysis/` của run. Runner stress truyền `--report-dir performance/k6/reports` để cập nhật hai báo cáo chính. Analyzer chỉ dùng Python chuẩn, không đọc raw `metrics.json`. Thiếu dữ liệu hiển thị N/A/INCOMPLETE; vi phạm đã quan sát vẫn là FAIL khi run bị ngắt. [Hướng dẫn analyzer dùng chung](analyze/README.md).

- Mix Search/Detail/Cart/Checkout: **40/20/22/18**; login riêng mỗi Cart/Checkout.
- Login lỗi tính là request nghiệp vụ lỗi và một thao tác thất bại; không gửi HTTP Cart/Checkout khi thiếu token.
- SLO mỗi hold/recovery: p95 <500ms, HTTP lỗi <1%, checks ≥99%, từng endpoint có mẫu; tỷ lệ thao tác thất bại <1%; skipped chỉ để theo dõi.
- CPU 100% = một core; RAM = RSS, đơn vị MiB. [Chi tiết đo](telemetry/README.md).

Chỉ chạy k6:

```bash
TELEMETRY=0 bash performance/k6/run-stress.sh
```

## Spike

50 VU/30s → 1500 VU/60s → 50 VU/60s.

**Hiện chưa tương thích fixture:** script yêu cầu đúng 50 account, còn CSV hiện có 10.000. Các lệnh dưới áp dụng với fixture 50 account tương ứng.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-spike.sh
```

## Phân tích dữ liệu đã lưu

Từ `eshop-sut`:

```bash
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type baseline
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type spike
```

Baseline/spike hiện chưa thu CPU/RAM và chưa tự gọi analyzer; dùng dữ liệu summary đã lưu để tạo báo cáo thủ công. Analyzer ghi rõ phần tài nguyên thiếu và RPS theo thời lượng danh định nếu không có timeline. Khi sửa threshold trong script k6, cập nhật `analyze/profiles.json` tương ứng và chạy kiểm thử đối chiếu.

## Soak

Chưa có script/runner. [Report 05](reports/05-soak-test-report.md) là mẫu báo cáo.

## Chạy với tuned

Mở `node tuned-backend/server.js` ở Terminal 1. Với baseline/stress/spike, Terminal 2 seed đúng DB rồi chạy runner của bài tương ứng:

```bash
node performance/k6/data/seed.js tuned-backend/database_tuned.sqlite
```

Smoke chạy trực tiếp. Tuned dùng WAL và index tên sản phẩm; xem [WAL](tune-db/WAL.md).

## Kết quả

Mỗi lần chạy lưu vào `performance/k6/output/<loại>-.../`.

| File | Nội dung |
|---|---|
| `summary.json`, `metrics.json`, `k6.log` | Tổng hợp, raw metrics và log k6 |
| `baseline_report.html` | Dashboard baseline |
| `node-cpu-ram.jsonl` | Mẫu CPU/RAM gốc của stress |
| `measurement-timeline.json` | Mốc thời gian chia cửa sổ đo |
| `analysis/report.md`, `analysis/report.html` | Báo cáo do analyzer tạo mặc định |
| `analysis/node-cpu-ram.csv`, `analysis/cpu-ram-*.csv` | Mẫu và thống kê tài nguyên do analyzer tạo |

Khi dùng `--report-dir`, báo cáo và CSV được ghi vào thư mục đích đó; runner stress dùng `reports/`.

Exit 99 = threshold fail. Ctrl-C dừng bài test, backend vẫn chạy. Đổi địa chỉ bằng `BASE_URL`, mặc định `http://localhost:3000`.

RPS hold stress = count/120s; recovery = count/60s. Login là request bổ sung. Các báo cáo v1 trong [reports/](reports/) dùng profile cũ; xem đúng run khi đối chiếu.

Tài liệu: [seed](data/README.md) · [kế hoạch hiện tại](k6-performance-test-plan-v2.md) · [báo cáo seminar](../../submission/Bao_cao_seminar_Performance_Testing.md).
