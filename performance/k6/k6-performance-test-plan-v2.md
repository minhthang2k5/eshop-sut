# Kế hoạch k6 v2 — phạm vi hiện tại

Cập nhật: 02/11/2026. Trọng tâm: stress và CPU/RAM của tiến trình Node.js.

## Mục tiêu

Quan sát mức tải bắt đầu vi phạm SLO, diễn biến CPU/RAM theo phase và trạng thái sau giảm tải. Khi đối chiếu gốc/tuned, dùng cùng fixture, profile và cách đo.

## Workload stress

| Thao tác | Xác suất | Think time |
|---|---:|---:|
| Search | 40% | 1–3s |
| Detail | 20% | 2–5s |
| Cart | 22% | 1–3s |
| Checkout | 18% | 3–6s |

Mỗi iteration chọn một thao tác độc lập. Account luân phiên theo iteration; Cart/Checkout login trong iteration, token cục bộ. Login lỗi tính một request nghiệp vụ lỗi và một thao tác thất bại; vẫn nghỉ think time, không gửi HTTP nghiệp vụ hoặc retry.

Fixture: 10.000 account, 200 sản phẩm, 12 keyword có trọng số. Search dùng keyword; Detail/Cart chọn sản phẩm từ fixture. Checkout độc lập với giỏ.

## Profile và đo tài nguyên

- 15 bậc 200–3000 VU, bước 200; ramp 30s + hold 120s/bậc.
- Recovery: target 50 VU trong 60s. Nominal 38m30s; grace cuối tối đa 60s.
- CPU/RAM Node.js: một mẫu/giây; thu 30s trước, trong bài và 60s sau.
- CPU 100% = một core; RAM = RSS (MiB).
- Chia mẫu theo mốc scenario thực và profile; setup/grace tách khỏi các phase tải.

## Tiêu chí

Mỗi hold/recovery: p95 <500ms, HTTP error <1%, checks ≥99%, từng endpoint có request, tỷ lệ thao tác thất bại <1%, skipped =0. Login được đánh giá riêng cùng các API nghiệp vụ.

RPS hold = request count/120s; recovery = count/60s. Không abort vì SLO fail để tiếp tục quan sát recovery. Percentile cả phút không xác định chính xác giây phục hồi; RAM tăng riêng lẻ chưa chứng minh memory leak.

## Thực hiện và kết quả

1. Mở backend → seed → chạy stress; [lệnh chi tiết](README.md#stress).
2. Giữ backend chạy đến khi thu thêm 60s sau tải hoàn tất.
3. Xem kết quả k6 trong thư mục run; điền báo cáo.
4. Hai bảng CPU/RAM tự cập nhật tại mục 6.3 của [báo cáo stress](reports/03-stress-test-report.md); lần chạy mới thay phần này.

Output gồm log/raw/summary k6, mẫu CPU/RAM JSONL/CSV, hai bảng CSV theo phase và trước–trong–sau, mốc thời gian đo. [Chi tiết CPU/RAM](telemetry/README.md).

## Trạng thái

- Đã có: seed, workload/profile stress và tổng hợp CPU/RAM. Code có sẵn không đồng nghĩa SUT đạt SLO.
- Baseline/spike còn yêu cầu fixture 50 account, chưa tương thích CSV 10.000 account.
- Chưa có script soak hoặc bộ đo stress v2 chính thức lặp theo cặp gốc/tuned.
- Luồng hiện tại mở/seed backend thủ công và chỉ đo tài nguyên tiến trình Node.js.
