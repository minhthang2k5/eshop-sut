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

`run-stress.sh` điều khiển trực tiếp: `sleep 30` → `k6 run stress.js` → `sleep 60` → `analyze.py` tổng hợp CPU/RAM. Giữ backend chạy đến khi runner kết thúc. Hai bảng CPU/RAM tự cập nhật tại **mục 6.3** của [báo cáo stress](reports/03-stress-test-report.md); lần chạy mới thay số liệu CPU/RAM của lần trước. Các kết quả k6 và nhận xét điền thủ công.

- Mix Search/Detail/Cart/Checkout: **40/20/22/18**; login riêng mỗi Cart/Checkout.
- Login lỗi tính là request nghiệp vụ lỗi và một thao tác thất bại; không gửi HTTP Cart/Checkout khi thiếu token.
- SLO mỗi hold/recovery: p95 <500ms, HTTP lỗi <1%, checks ≥99%, từng endpoint có mẫu; tỷ lệ thao tác thất bại <1%, skipped =0.
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
| `node-cpu-ram.jsonl`, `node-cpu-ram.csv` | Mẫu CPU/RAM của stress |
| `cpu-ram-phases.csv` | Bảng CPU/RAM từng phase |
| `cpu-ram-before-during-after.csv` | Bảng CPU/RAM trước–trong–sau stress |
| `measurement-timeline.json` | Mốc thời gian chia cửa sổ đo |

Exit 99 = threshold fail. Ctrl-C dừng bài test, backend vẫn chạy. Đổi địa chỉ bằng `BASE_URL`, mặc định `http://localhost:3000`.

RPS hold stress = count/120s; recovery = count/60s. Login là request bổ sung. Các báo cáo v1 trong [reports/](reports/) dùng profile cũ; xem đúng run khi đối chiếu.

Tài liệu: [seed](data/README.md) · [kế hoạch hiện tại](k6-performance-test-plan-v2.md) · [báo cáo seminar](../../submission/Bao_cao_seminar_Performance_Testing.md).
