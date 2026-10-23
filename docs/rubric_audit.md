# Rubric Audit — AI-generated k6 Scripts

**Mục đích:** đánh giá hai script k6 từ HAR đã redacted và prompt theo cùng contract. Giao diện dùng Script 1 / Script 2, không gắn cứng nhà cung cấp; hai artifact thực tế hiện có là Gemini và Claude.

**Quy ước:** mỗi tiêu chí đạt = **1 điểm**, không đạt = **0 điểm**. Tổng tối đa: **10 điểm/script**.

**Cách triển khai:** web `test-web-performance/` chấm source bằng Acorn, chạy k6 smoke, lưu evidence và cho phép người chấm duyệt điểm. Cách viết tương đương qua hàm hỗ trợ/hằng số được phân tích; trường hợp chưa nhận diện cần đối chiếu source. Kết quả 1 iteration chỉ chứng minh nhánh đã chạy. AI nhận xét và đề xuất threshold/correlation không tự đổi điểm.

## Thông tin lần chấm

| Trường | Giá trị |
| --- | --- |
| Ngày chấm | `YYYY-MM-DD` |
| Người chấm | Thành viên C |
| HAR đầu vào | `localhost.har` (redacted) |
| Prompt đầu vào | `ai_prompt_template.txt` |
| Lệnh smoke | `k6 run <script>.js` |

## Tiêu chí chấm

| # | Tiêu chí | Đạt khi | Điểm Script 1 | Điểm Script 2 | Bằng chứng / lỗi phát hiện |
| --- | --- | --- | :---: | :---: | --- |
| 1 | Endpoint tồn tại thật | Chỉ dùng `POST /api/login`, `GET /api/products?search=…`, `GET /api/products/:id` với ID 1–5, và `POST /api/checkout`; không dùng `/api/auth/login` hay `/api/orders`. |  |  |  |
| 2 | Method và body đúng | Login gửi `email`, `password`; checkout gửi tối thiểu `total_amount`, `shipping_address`; JSON POST được `JSON.stringify()`. |  |  |  |
| 3 | Thứ tự flow hợp lý | Login xảy ra trước checkout; search/detail không cần token; script không checkout khi login thất bại hoặc token rỗng. |  |  |  |
| 4 | Correlation token đúng | Lấy `token` từ JSON response login và gửi `Authorization: Bearer <token>` cho checkout. |  |  |  |
| 5 | Think-time hợp lý | Có `sleep()` ngẫu nhiên: search 1–3 giây, detail 2–5 giây, checkout 3–6 giây. |  |  |  |
| 6 | Workload đúng | Chọn action gần đúng: search 55%, detail 25%, checkout 20%. |  |  |  |
| 7 | Dữ liệu được parameterize | Keyword được chọn ngẫu nhiên từ `iPhone`, `Samsung`, `MacBook`, `AirPods`, `Keychron`; product ID ngẫu nhiên trong 1–5. |  |  |  |
| 8 | Có checks cần thiết | Có check status 200; login kiểm tra token tồn tại; checkout kiểm tra `orderId` tồn tại. |  |  |  |
| 9 | Có thresholds SLO | Có `http_req_duration: ['p(95)<500']` và `checks: ['rate>=0.99']`. |  |  |  |
| 10 | Chạy được | `k6 run <script>.js` hoàn tất smoke test không lỗi syntax/runtime và không có lỗi request do script tạo ra. |  |  |  |
|  | **Tổng** | **/10** | **/10** | **/10** |  |

## Kết quả smoke test

| Script | Lệnh chạy | Kết quả | Lỗi HTTP/runtime | Ghi chú |
| --- | --- | --- | --- | --- |
| `gemini_script_real.js` | `k6 run gemini_script_real.js` | Pass / Fail |  |  |
| `claude_scipt_real.js` | `k6 run claude_scipt_real.js` | Pass / Fail |  |  |

## Mẫu ghi lỗi để sửa ở D6

| Script | Tiêu chí không đạt | Lỗi cụ thể | Cách sửa | File sau sửa |
| --- | --- | --- | --- | --- |
| `chatgpt_script.js` |  |  |  | `chatgpt_script_fixed.js` |
| `claude_script.js` |  |  |  | `claude_script_fixed.js` |

## Kết luận

- Script tốt hơn trước audit: `TBD`
- Lỗi lặp lại giữa hai AI: `TBD`
- Việc cần sửa trước baseline 50 VU: `TBD`
