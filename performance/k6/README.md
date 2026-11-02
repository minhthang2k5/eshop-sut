# k6 — EShop API Performance Testing

## Chuẩn bị

Chạy lệnh từ `eshop-sut`. Cần Node.js, k6; runner baseline/stress và analyzer cần thêm Python 3. Analyzer dùng thư viện chuẩn Python.

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

Đọc toàn bộ CSV để kiểm tra, cấp 50 account đầu cho 50 VU (mỗi VU một account). Giữ mix 55/25/14/6, lazy login và sản phẩm ID 1 / iPhone từ fixture.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-baseline.sh
```

Runner baseline thu CPU/RAM 30s trước và 60s sau tải khi tìm thấy telemetry backend, rồi tự gọi analyzer. Giữ backend chạy đến khi runner kết thúc. `TELEMETRY=0 bash performance/k6/run-baseline.sh` bỏ thu trước/sau, vẫn tạo báo cáo HTTP.

Mỗi run lưu timeline (scenario/profile, grace tối đa 30s), summary, raw metrics, log, dashboard `baseline_report.html` và tự cập nhật hai đầu ra chính: [02-baseline-test-report.md](reports/02-baseline-test-report.md), [baseline_report.html](reports/baseline_report.html). Dashboard k6 vẫn nằm trong thư mục run; báo cáo trong `reports/` được tạo lại từ cùng run. SLO steady tổng/từng API: p95 <500ms, HTTP lỗi <1%, checks ≥99%, count >0. Login đánh giá toàn bài; không bắt buộc có Login trong steady. Skipped phải bằng 0 toàn bài. HTTP được gắn phase tại lúc bắt đầu; RPS dùng thời lượng cửa sổ quan sát.

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

Analyzer mặc định xuất `report.md`, `report.html` và CSV vào thư mục `analysis/` của run. Runner baseline/stress truyền `--report-dir performance/k6/reports` để cập nhật hai báo cáo chính. Analyzer chỉ dùng Python chuẩn, không đọc raw `metrics.json`. Thiếu dữ liệu hiển thị N/A/INCOMPLETE; vi phạm đã quan sát vẫn là FAIL khi run bị ngắt. [Hướng dẫn analyzer dùng chung](analyze/README.md).

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

Baseline tự thu CPU/RAM và gọi analyzer; spike vẫn cần phân tích summary thủ công. Analyzer ghi rõ phần tài nguyên thiếu và RPS theo thời lượng danh định nếu không có timeline. Khi sửa threshold trong script k6, cập nhật `analyze/profiles.json` tương ứng và chạy kiểm thử đối chiếu.

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
| `node-cpu-ram.jsonl` | Mẫu CPU/RAM gốc của baseline/stress |
| `measurement-timeline.json` | Mốc thời gian chia cửa sổ đo |
| `analysis/report.md`, `analysis/report.html` | Báo cáo do analyzer tạo mặc định |
| `analysis/node-cpu-ram.csv`, `analysis/cpu-ram-*.csv` | Mẫu và thống kê tài nguyên do analyzer tạo |

Khi dùng `--report-dir`, báo cáo và CSV được ghi vào thư mục đích đó; runner baseline/stress dùng `reports/`.

Exit 99 = threshold fail. Ctrl-C dừng bài test, backend vẫn chạy. Đổi địa chỉ bằng `BASE_URL`, mặc định `http://localhost:3000`.

RPS hold stress = count/120s; recovery = count/60s. Login là request bổ sung. Các báo cáo v1 trong [reports/](reports/) dùng profile cũ; xem đúng run khi đối chiếu.

Tài liệu: [seed](data/README.md) · [kế hoạch hiện tại](k6-performance-test-plan-v2.md) · [báo cáo seminar](../../submission/Bao_cao_seminar_Performance_Testing.md).

## Kiểm tra khi sửa baseline

```bash
python3 -m unittest discover -s performance/k6/analyze -v
node performance/k6/analyze/test_baseline_runtime.cjs
bash -n performance/k6/run-baseline.sh
```

Kiểm thử runtime dùng HTTP/clock giả để kiểm tra fixture, login lỗi, 401, pacing và ranh giới phase. Kiểm thử runner kiểm tra exit 0/99, Ctrl-C, timeline và báo cáo khi telemetry tắt. Chúng không thay thế việc chạy k6 với backend đã seed.
