# D8b — Confirmation runs trên Windows/PowerShell

Phạm vi: D8b theo [phân công Week 3](../../docs/Task_Assignment_Detail.md). Chạy lại k6 của A trên backend gốc và tuned; không thay workload JMeter.

## Trạng thái Week 3 của B

| Task | Trạng thái | Output |
| --- | --- | --- |
| D8b — xác minh tái lập | Hoàn tất chạy và phân tích; tái lập một phần kết quả A | [Verification report](verification_report.md), summary/log/metadata: baseline gốc/tuned mỗi bản một lần, spike mỗi bản hai lần, hai smoke entry |
| Báo cáo hiệu năng một trang | Hoàn tất | [performance_report.md](../../submission/performance_report.md) |
| Slides D2/D3 | Hoàn tất dạng Markdown theo yêu cầu, không xuất PPTX | [slides_comparison.md](../../submission/slides_comparison.md) |
| Phần B trong báo cáo chung | Đã điền chương 5, bài tập 2 và kết luận liên quan | [Báo cáo chung](../../submission/Bao_cao_seminar_Performance_Testing.md) |
| Cross-run | Chưa hoàn tất sign-off trực tiếp của thành viên | [Hướng dẫn và bảng Pending](cross_run_signoff.md) |

D8b hoàn tất công việc kiểm chứng dù spike SLO fail: hai baseline đạt, spike gốc/tuned đều fail sau hai lượt trên B. Không coi đây là bằng chứng PASS spike tuned của A đã tái lập. D6/D7 thuộc C theo phân công mới.

Để hoàn tất cross-run: B cần cung cấp xác nhận lượt k6 trực tiếp, A/C cung cấp các lượt chạy công cụ theo yêu cầu cùng log/run ID và nhận xét. Run do trợ lý thực thi đã có evidence nhưng chưa thay sign-off của thành viên.

## Phạm vi file cho lần commit Week 3 sau này

Chỉ chọn `performance/verification/` (trừ `local-runs/` đã ignore), `submission/evidence/assignee-b/`, `submission/performance_report.md`, `submission/slides_comparison.md` và các thay đổi phần B trong `submission/Bao_cao_seminar_Performance_Testing.md`, `submission/README.md`. Chưa stage hoặc commit trong lượt dọn này.

Giữ summary/log/metadata gốc để truy số liệu và trạng thái WAL/index; giữ cả hai lượt spike, hai smoke entry và bộ tổng hợp/checksum. Raw metrics, DB/SUT bản sao và native dashboard nằm ở `local-runs/`, chỉ giữ local để điều tra/tính lại, không đưa vào commit. Các tài liệu kế hoạch/khảo sát đã hết vai trò và output không được dùng trong báo cáo đã chuyển ra kho lưu ngoài repo để có thể khôi phục.

## Chuẩn bị

Từ repo root `eshop-sut-main`, kiểm tra:

```powershell
node --version
npm.cmd --version
k6 version
```

Cần k6 trong PATH và dependency backend. Nếu chưa cài dependency:

```powershell
Push-Location backend
npm.cmd ci
Pop-Location
```

Đảm bảo port 3000 chưa có server khác chạy. Runner sẽ báo lỗi khi port bận; không tự dừng server của bạn.

Runner copy source và test-data vào `local-runs/<run-id>/sut`, dùng dependency đã cài ở `backend/node_modules` qua NODE_PATH. Không copy/reset DB nguồn và không sửa source A. Mỗi run mới khởi tạo DB mới, đợi seed xong, chạy seed account k6 vào đúng DB của bản sao rồi kiểm tra PRAGMA/index/query plan và orders=0. Có 52 user seed tổng cộng, trong đó 50 account phục vụ k6.

## Chạy lại

Chạy từng lệnh và chờ kết thúc trước lệnh kế tiếp:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File performance/verification/run-verification.ps1 -Variant original -Test smoke
powershell -NoProfile -ExecutionPolicy Bypass -File performance/verification/run-verification.ps1 -Variant tuned -Test smoke
powershell -NoProfile -ExecutionPolicy Bypass -File performance/verification/run-verification.ps1 -Variant original -Test baseline
powershell -NoProfile -ExecutionPolicy Bypass -File performance/verification/run-verification.ps1 -Variant tuned -Test baseline
powershell -NoProfile -ExecutionPolicy Bypass -File performance/verification/run-verification.ps1 -Variant original -Test spike
powershell -NoProfile -ExecutionPolicy Bypass -File performance/verification/run-verification.ps1 -Variant tuned -Test spike
node performance/verification/summarize-verification.cjs
node performance/verification/summarize-transport.cjs
node performance/verification/summarize-verification.cjs
```

ExecutionPolicy Bypass chỉ áp dụng process PowerShell này. Không thay policy toàn máy. Smoke thất bại thì đọc log và khắc phục trước khi chạy tải.

`summarize-transport.cjs` đọc raw metrics sau khi tải kết thúc để phân loại status/error code; lần gọi summarizer cuối cập nhật SHA256SUMS gồm cả kết quả transport. Chỉ chạy helper này trên máy còn giữ raw output.

Baseline: ramp 60s, steady 300s, ramp-down 60s, mix 55/25/14/6. Spike: 50 VUs 30s → 1500 VUs 60s → 50 VUs 60s, mix 40/20/22/18. Giữ nguyên code A, lazy login, timeout, account và think-time. Bốn bài tải có lịch tổng 19 phút cộng grace period/khởi tạo.

Màn hình in START/END. Log k6 được lưu trong evidence thay vì stream mọi dòng tiến độ. k6 exit 99 là threshold fail: runner vẫn lưu kết quả và cho phép bước tiếp theo. Lỗi hạ tầng khiến runner trả khác 0. Nếu dừng cưỡng bức terminal, kiểm tra process server bản sao và port trước khi chạy tiếp; đừng dùng output thiếu metadata.endUtc như run hoàn chỉnh.

## Đầu ra và cách đọc

- `local-runs/<run-id>/`: DB/SUT bản sao, raw metrics JSON và baseline dashboard. Git ignored. Không dùng DB này cho dữ liệu cá nhân.
- `../../submission/evidence/assignee-b/<run-id>/`: metadata, k6 summary/log và server startup log.
- `../../submission/evidence/assignee-b/verification-summary.json`: tổng hợp số liệu B và reference A, tổng/per-API/Login, SLO theo phase, skipped và threshold results.
- [verification_report.md](verification_report.md): kết luận tái lập.
- [performance_report.md](../../submission/performance_report.md): báo cáo một trang.

Latency đơn vị ms; errorPct/checksPct đơn vị %. p50 là med; p95/p99 lấy trực tiếp từ k6. Tổng phase gồm Login nếu phát sinh. RPS=counts/300s baseline steady hoặc /30s,/60s theo phase spike. Không lấy rate toàn run làm RPS riêng phase. Không tính percentile tổng bằng trung bình percentile từng API.

Legacy k6 summary export: `thresholds: false` nghĩa không vi phạm; parser cũng hỗ trợ object `{ok}`. HTTP lỗi và checks là metric khác nhau; body sai không nhất thiết là HTTP lỗi. Không dùng exit 99 để suy server crash. So sánh máy B với A là so xu hướng và SLO, không đòi con số trùng nhau.

Đã chọn Windows/PowerShell theo yêu cầu triển khai; chưa cung cấp/chạy kiểm chứng runner Bash. Số liệu này do trợ lý chạy trên workspace B, không phải sign-off thao tác của A/C.
