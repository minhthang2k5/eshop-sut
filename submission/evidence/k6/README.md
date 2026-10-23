# Evidence k6 — Lê Nguyễn Quốc Thái

Bộ evidence cho [chương 4 báo cáo seminar](../../Bao_cao_seminar_Performance_Testing.md#4-thực-nghiệm-k6-của-lê-nguyễn-quốc-thái), tổng hợp ngày 23/10/2026 từ kết quả hiện có; không chạy lại tải. Số liệu latency tính bằng ms, HTTP lỗi/checks bằng phần trăm. Không thực hiện soak.

## Run và nguồn số liệu

Các summary được sao chép nguyên bytes từ `eshop-sut/performance/k6/output/<run-id>/summary.json`. Trong báo cáo, B/T/P lần lượt là baseline/stress/spike; 0 là trước tune, 1 là sau tune. Mỗi run là một lần đo, chưa xác minh độ lặp lại.

| Mã | Run ID / summary | Cửa sổ chính | HTML / hình |
| --- | --- | --- | --- |
| Smoke | [smoke-20261022-195537-4es3Xy](summaries/smoke-20261022-195537-4es3Xy/summary.json) | Toàn run: 1 VU, 5 requests, 10 checks, p95 47.895 ms | Không có HTML/hình riêng |
| B0 | [baseline-20261022-110446-eGLTX1](summaries/baseline-20261022-110446-eGLTX1/summary.json) | `steady`, 300s | [Baseline](html/baseline_report.html), hình 01/02 đối chiếu |
| B1 | [baseline-20261023-084311-TSxg2P](summaries/baseline-20261023-084311-TSxg2P/summary.json) | `steady`, 300s | [Trước–sau](html/tuned_baseline_report.html), hình 01/02 |
| T0 | [stress-20261022-181718-lx8F4c](summaries/stress-20261022-181718-lx8F4c/summary.json) | Mỗi `hold_*` và `recovery_1`, 60s | [Stress](html/stress_report.html), hình 03/05 |
| T1 | [stress-20261023-090531-KgTWyh](summaries/stress-20261023-090531-KgTWyh/summary.json) | Cùng 11 bậc và recovery như T0 | [Trước–sau](html/tuned_baseline_report.html), hình 05 |
| P0 | [spike-20261022-190641-UgVeF4](summaries/spike-20261022-190641-UgVeF4/summary.json) | `hold_50`/`hold_1500`/`recovery_1`: 30/60/60s | [Spike](html/spike_report.html), hình 04/06 |
| P1 | [spike-20261023-085706-BOOKoc](summaries/spike-20261023-085706-BOOKoc/summary.json) | Cùng profile như P0 | [Trước–sau](html/tuned_baseline_report.html), hình 06 |

Smoke report 01 cũ ghi p95 17.81 ms và run ID chung, khác summary đã chọn. Không dùng số liệu/tài nguyên của report này thay cho summary có run ID cụ thể. Smoke lưu ngày 22/10 lúc 19:55 không phải bằng chứng smoke trước các run tải cùng ngày.

## HTML và hình

Bốn HTML lấy từ `eshop-sut/performance/k6/reports/`, hoạt động offline với SVG nội tuyến, không dùng CDN. Các biểu đồ/bảng giữ nguyên nội dung; chỉ sửa liên kết `../output/` thành `../summaries/`, và ba liên kết report tuned thành các tiểu mục 4.4.1–4.4.3 của báo cáo submission. Nhờ vậy bản evidence mở được nguồn mà không phụ thuộc output gốc.

| Hình | SVG nguồn | Vị trí báo cáo |
| --- | --- | --- |
| [01-baseline-percentiles.png](figures/01-baseline-percentiles.png) | `tuned_baseline_report.html`, SVG 0 | K6-3, mục 4.4.1 |
| [02-baseline-api.png](figures/02-baseline-api.png) | `tuned_baseline_report.html`, SVG 1 | K6-4, mục 4.4.1 |
| [03-stress-before.png](figures/03-stress-before.png) | `stress_report.html`, SVG 1 | K6-1, mục 4.3.3 |
| [04-spike-before.png](figures/04-spike-before.png) | `spike_report.html`, SVG 1 | K6-2, mục 4.3.4 |
| [05-stress-comparison.png](figures/05-stress-comparison.png) | `tuned_baseline_report.html`, SVG 2/3/4 | K6-5, mục 4.4.2 |
| [06-spike-comparison.png](figures/06-spike-comparison.png) | `tuned_baseline_report.html`, SVG 5/6/7 | K6-6, mục 4.4.3 |

Chỉ số SVG tính từ 0 theo thứ tự trong HTML. PNG được trích bằng [render_figures.cjs](render_figures.cjs), bổ sung tiêu đề, chú giải trước/sau, run ID và quy tắc phase; không dựng ảnh terminal hay ảnh tài nguyên. Dùng Node.js có package `sharp` để tái tạo: `node render_figures.cjs`. Nếu sharp được cài ở thư mục khác, cấu hình `NODE_PATH` trỏ tới node_modules tương ứng. Các hình chỉ là bản tĩnh; bảng số liệu/tooltip đầy đủ nằm trong HTML và số gốc ở summary.

## Cách đọc và giới hạn

- RPS phase = count/thời lượng phase, không lấy `rate` của submetric toàn run. Phase gắn theo thời điểm bắt đầu request; tổng phase có gồm Login nếu phát sinh. Không tính RPS bằng khoảng cách timestamp của các mẫu đầu/cuối.
- p50 = `med`; HTTP lỗi = `http_req_failed.value`; checks = `checks.value`. Trong bản export này, `thresholds: true` biểu thị vi phạm. `http_req_failed.passes` là số lỗi; không nhầm với checks.passes.
- Hình nối các điểm tổng hợp, không phải chuỗi thời gian. Panel latency so sánh stress/spike dùng log10. Tài nguyên không có ngưỡng PASS/FAIL tự động.
- Nguồn ghi chép tài nguyên: report 02 (baseline trước), 06 (baseline sau), 07 (spike sau tại 1500), 08 (stress sau từng bậc) trong `performance/k6/reports/`. Không có ảnh hoặc telemetry gốc; không dùng như avg/max hay RSS riêng backend. Không ghép số liệu giữa các run thành chuỗi thời gian.
- Không có snapshot DB/build, cấu hình PRAGMA/index thực tế theo run và chạy lặp. Không quy toàn bộ chênh lệch cho tuning, không suy crash hoặc công suất production.

Theo phạm vi đã thống nhất, evidence k6 không chứa hoặc liên kết tới file log chạy/raw metrics, và không include dashboard baseline trong output. Bốn HTML ở đây đều là report tổng hợp từ thư mục reports. Các evidence AI có sẵn bên ngoài thư mục k6 thuộc phần khác của báo cáo, giữ nguyên.

## Toàn vẹn

[SHA256SUMS.txt](SHA256SUMS.txt) ghi SHA-256 của toàn bộ file trong bộ evidence k6, trừ chính manifest hash. Từ thư mục này kiểm tra bằng:

```bash
sha256sum -c SHA256SUMS.txt
```
