# k6 — EShop API Performance Testing

## Chuẩn bị

Chạy lệnh từ `eshop-sut`. Cần Node.js, k6; bốn runner baseline/stress/spike/soak cần thêm Python 3 để lưu timeline.

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

Mix Search/Detail/Cart/Checkout 55/25/14/6; keyword có trọng số và sản phẩm ngẫu nhiên từ fixture chung. Account luân phiên theo iteration; login mỗi lượt Cart/Checkout. Preflight kiểm tra catalogue trước khi chạy.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-baseline.sh
```

Runner thu CPU/RAM 30s trước và 60s sau tải khi tìm thấy telemetry backend. Giữ backend chạy đến khi runner kết thúc. `TELEMETRY=0 bash performance/k6/run-baseline.sh` bỏ thu telemetry và thời gian chờ trước/sau, vẫn lưu kết quả k6.

Mỗi run lưu timeline (scenario/profile), summary, raw metrics, log và dashboard `baseline_report.html`. SLO pha steady tổng/từng API (kể cả login): p95 <500ms, HTTP lỗi <1%, checks ≥99%, count >0; tỷ lệ thao tác thất bại <1%. Skipped dùng để theo dõi. Runner không gọi analyzer và không cập nhật báo cáo trong `reports/`.

## Stress

15 bậc **200–3000 VU**, bước 200; mỗi bậc ramp 30s + hold 120s; recovery 50 VU/60s. Lịch tải **38m30s**, chưa tính grace cuối tối đa 60s.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-stress.sh
```

`run-stress.sh` thu telemetry trước/sau tải như baseline và lưu dashboard `stress_report.html`. Runner không gọi analyzer. PASS/FAIL do thresholds trong k6 quyết định.

- Mix Search/Detail/Cart/Checkout: **40/20/22/18**; login riêng mỗi Cart/Checkout.
- Login lỗi tính là request nghiệp vụ lỗi và một thao tác thất bại; không gửi HTTP Cart/Checkout khi thiếu token.
- SLO mỗi hold/recovery: p95 <500ms, HTTP lỗi <1%, checks ≥99%, từng endpoint có mẫu; tỷ lệ thao tác thất bại <1%; skipped chỉ để theo dõi.
- CPU 100% = một core; RAM = RSS, đơn vị MiB. [Chi tiết đo](telemetry/README.md).

Chỉ chạy k6:

```bash
TELEMETRY=0 bash performance/k6/run-stress.sh
```

## Spike

50 VU/30s → 1000 VU/60s → 50 VU/60s.

Dùng chung workload Black Friday với stress (40/20/22/18), fixture và business metrics. Login mỗi lượt Cart/Checkout; preflight kiểm tra catalogue trước khi chạy. Profile nằm trong `lib/spike-test-profiles.js`.

Terminal 2, sau khi backend khởi động:

```bash
node performance/k6/data/seed.js
bash performance/k6/run-spike.sh
```

## Soak

Soak rút gọn theo `docs/Tool_Survey_Proposal.md`: ramp-up 60 giây → 30 VU trong 15 phút → ramp-down 60 giây (tổng 17 phút, chưa gồm preflight/graceful stop).

Dùng chung workload ngày thường với baseline (55/25/14/6), dữ liệu, login mỗi lượt Cart/Checkout và business metrics. Thresholds đánh giá pha `steady`; `SOAK_TIMELINE` ghi mốc scenario và profile. Profile nằm trong `lib/soak-test-profiles.js`.

```bash
node performance/k6/data/seed.js
bash performance/k6/run-soak.sh
```

Runner lưu kết quả k6, dashboard, timeline và CPU/RAM khi có telemetry vào thư mục `output/soak-.../`, cùng cách thu trước/sau tải như baseline/stress/spike. [Report 05](reports/05-soak-test-report.md) là mẫu báo cáo.

## Chạy với tuned

Mở `node tuned-backend/server.js` ở Terminal 1. Với baseline/stress/spike/soak, Terminal 2 seed đúng DB rồi chạy runner của bài tương ứng:

```bash
node performance/k6/data/seed.js tuned-backend/database_tuned.sqlite
```

Smoke chạy trực tiếp. Tuned dùng WAL và index tên sản phẩm; xem [WAL](tune-db/WAL.md).

## Kết quả

Bốn file `run-baseline.sh`, `run-stress.sh`, `run-spike.sh`, `run-soak.sh` chạy độc lập, cùng lưu kết quả vào `performance/k6/output/<loại>-.../`. Không runner nào gọi analyzer.

Khi có telemetry backend: thu 30 giây trước tải và 60 giây sau tải. `TELEMETRY=0` tắt thu telemetry và hai khoảng chờ này; `TELEMETRY_FILE` chỉ định file telemetry, `TELEMETRY_DIR` đổi thư mục tìm kiếm. Nếu không tìm thấy telemetry, bài test vẫn chạy và lưu kết quả k6. [Chi tiết telemetry](telemetry/README.md).

| File | Nội dung |
|---|---|
| `summary.json`, `metrics.json`, `k6.log` | Tổng hợp, raw metrics và log k6 |
| `<loại>_report.html` | Dashboard k6 của bài test |
| `node-cpu-ram.jsonl` | Mẫu CPU/RAM trong cửa sổ thu thập, nếu có telemetry backend |
| `measurement-timeline.json` | Mốc thời gian chia cửa sổ đo |


Exit 99 = threshold fail. Ctrl-C dừng bài test, backend vẫn chạy. Đổi địa chỉ bằng `BASE_URL`, mặc định `http://localhost:3000`.

RPS hold stress = count/120s; recovery = count/60s. Login là request bổ sung. Các báo cáo v1 trong [reports/](reports/) dùng profile cũ; xem đúng run khi đối chiếu.

Tài liệu: [seed](data/README.md) · [kế hoạch hiện tại](k6-performance-test-plan-v2.md) · [báo cáo seminar](../../submission/Bao_cao_seminar_Performance_Testing.md).

## Kiểm tra runner

```bash
python3 -m unittest discover -s performance/k6/tests -v
for type in baseline stress spike soak; do
  bash -n "performance/k6/run-$type.sh"
done
```

Kiểm thử dùng k6 và telemetry giả để xác minh artifact, timeline, exit code và xử lý ngắt; không chạy tải lên backend.
