# AI k6 Script Audit — AUD-20261023-E85CDC

- Date: 2026-10-23T02:50:07.105Z
- Reviewer: Thành viên C
- Rubric: k6-ai-audit-v1 v1.0
- HAR: localhost.har (redacted by submitter)
- Smoke profile: 1 VU × 1 iteration, base URL http://localhost:3000

- Script 1: gemini_script_real.js

## Script 1 — 10/10

| # | Tiêu chí | Điểm | Evidence | Cách sửa |
| --- | --- | :---: | --- | --- |
| 1 | Endpoint tồn tại thật | 1 | Dùng đúng nhóm endpoint EShop. | Dùng POST /api/login, GET /api/products, GET /api/products/:id và POST /api/checkout. |
| 2 | Method và body đúng | 1 | Login và checkout có JSON body bắt buộc. | Dùng http.post(..., JSON.stringify({...}), { headers: { "Content-Type": "application/json" } }). |
| 3 | Thứ tự flow hợp lý | 1 | Có guard dừng flow khi thiếu token lấy từ login. | Chỉ gọi checkout trong nhánh token hợp lệ sau login. |
| 4 | Correlation token đúng | 1 | Trích xuất token và truyền Authorization Bearer. | Lấy loginRes.json("token") rồi đặt Authorization: `Bearer ${token}` khi checkout. |
| 5 | Think-time hợp lý | 1 | Có think-time random đúng khoảng cho search/detail/checkout. | Dùng random 1–3s cho search, 2–5s cho detail, 3–6s cho checkout. |
| 6 | Workload đúng | 1 | Có nhánh random với ngưỡng 55% và 80%. | Dùng r < 0.55 cho search, r < 0.80 cho detail, còn lại checkout. |
| 7 | Dữ liệu được parameterize | 1 | Keyword và product ID được parameterize. | Khai báo mảng 5 keyword và dùng Math.floor(Math.random() * 5) + 1 cho product ID. |
| 8 | Có checks cần thiết | 1 | Có check status, token và orderId. | Thêm check cho login status/token, response product và checkout status/orderId. |
| 9 | Có thresholds SLO | 1 | Có ngưỡng p95 và check rate SLO. | Thêm thresholds: { http_req_duration: ['p(95)<500'], checks: ['rate>=0.99'] }. |
| 10 | Chạy được | 1 | k6 smoke pass trên nhánh đã chạy; chưa chứng minh mọi nhánh nghiệp vụ. | Không cần sửa smoke run. |

### Smoke evidence

- k6 smoke pass trên nhánh đã chạy; chưa chứng minh mọi nhánh nghiệp vụ.
- Exit code: 0; checks: 1; failed requests: 0; p95: 33.619499999999995 ms

- Script 2: claude_scipt_real.js

## Script 2 — 10/10

| # | Tiêu chí | Điểm | Evidence | Cách sửa |
| --- | --- | :---: | --- | --- |
| 1 | Endpoint tồn tại thật | 1 | Dùng đúng nhóm endpoint EShop. | Dùng POST /api/login, GET /api/products, GET /api/products/:id và POST /api/checkout. |
| 2 | Method và body đúng | 1 | Login và checkout có JSON body bắt buộc. | Dùng http.post(..., JSON.stringify({...}), { headers: { "Content-Type": "application/json" } }). |
| 3 | Thứ tự flow hợp lý | 1 | Có guard dừng flow khi thiếu token lấy từ login. | Chỉ gọi checkout trong nhánh token hợp lệ sau login. |
| 4 | Correlation token đúng | 1 | Trích xuất token và truyền Authorization Bearer. | Lấy loginRes.json("token") rồi đặt Authorization: `Bearer ${token}` khi checkout. |
| 5 | Think-time hợp lý | 1 | Có think-time random đúng khoảng cho search/detail/checkout. | Dùng random 1–3s cho search, 2–5s cho detail, 3–6s cho checkout. |
| 6 | Workload đúng | 1 | Có nhánh random với ngưỡng 55% và 80%. | Dùng r < 0.55 cho search, r < 0.80 cho detail, còn lại checkout. |
| 7 | Dữ liệu được parameterize | 1 | Keyword và product ID được parameterize. | Khai báo mảng 5 keyword và dùng Math.floor(Math.random() * 5) + 1 cho product ID. |
| 8 | Có checks cần thiết | 1 | Có check status, token và orderId. | Thêm check cho login status/token, response product và checkout status/orderId. |
| 9 | Có thresholds SLO | 1 | Có ngưỡng p95 và check rate SLO. | Thêm thresholds: { http_req_duration: ['p(95)<500'], checks: ['rate>=0.99'] }. |
| 10 | Chạy được | 1 | k6 smoke pass trên nhánh đã chạy; chưa chứng minh mọi nhánh nghiệp vụ. | Không cần sửa smoke run. |

### Smoke evidence

- k6 smoke pass trên nhánh đã chạy; chưa chứng minh mọi nhánh nghiệp vụ.
- Exit code: 0; checks: 1; failed requests: 0; p95: 3.921535 ms

## Ghi chú

Không có ghi chú bổ sung.
