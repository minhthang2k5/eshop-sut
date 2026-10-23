# Tool Survey Proposal — T05: Performance Testing (EShop)

- **Môn học:** CS423/CSC15003 – Software Testing (Seminar Track, 2026 AI-First)
- **Giai đoạn nộp:** Stage S1
- **Nhóm:** 3 thành viên (A, B, C), kế hoạch thực hiện 3 tuần
- **Công cụ traditional:** k6 (chính) + Apache JMeter (phụ)
- **Hướng AI hiện tại của C:** hai script Gemini/Claude từ HAR; web audit React/Express chạy Acorn + k6; ChatGPT kết nối Luna để nhận xét và đề xuất threshold/correlation.
- **Chi phí:** k6, JMeter và mã nguồn web dùng công cụ mã nguồn mở; phần AI phụ thuộc quyền tài khoản/dịch vụ được sử dụng.

**Phạm vi thực hiện của C ngày 23/10/2026:** D1 là HAR và chuẩn bị input; D5 là hai script thực tế `gemini_script_real.js` và `claude_scipt_real.js`; D6 là web audit 10 tiêu chí, chạy smoke, duyệt điểm và xuất scorecard; D7 là Luna đề xuất threshold/correlation thành bảng. Phần C trong báo cáo chính dùng phạm vi này; các bảng kế hoạch ban đầu bên dưới được đọc cùng bản phân công cập nhật. Báo cáo và evidence: `submission/Bao_cao_seminar_Performance_Testing.md`.

---

## 1. Giới thiệu Framework/Công cụ

| Công cụ | Vai trò trong demo | Chi phí | Lý do chọn / không chọn |
| --- | --- | --- | --- |
| **k6** (Grafana Labs) | Công cụ chính: baseline, spike, stress, mixed workload, thresholds, dashboard | Mã nguồn mở, miễn phí | Script JavaScript gọn, dễ audit/diff với script AI; threshold khai báo ngay trong code (khớp SLO p95 < 500ms, lỗi < 1%); có web dashboard xuất báo cáo HTML sẵn. |
| **Apache JMeter** | Công cụ phụ: dựng lại cùng workload bằng file `.jmx`, đối chiếu số liệu với k6 | Mã nguồn mở, miễn phí | Brief yêu cầu mỗi thành viên phải triển khai được ở cả JMeter (.jmx) và k6. Có GUI để ghi/sửa, có HTML report dựng sẵn qua CLI. |
| **Locust** | Chỉ so sánh trên giấy, không chạy | Miễn phí | Không chọn vì nhóm đã có 2 công cụ; thêm công cụ thứ ba làm loãng thời gian của 3 người trong 3 tuần. |
| Chrome DevTools (tab Network) | Capture HAR từ phiên thao tác thật trên frontend-web (`http://localhost:5173`) | Miễn phí | Có sẵn trong trình duyệt, không cần cài thêm. |
| k6 Studio hoặc `har-to-k6` *(tùy chọn — cần kiểm tra còn hoạt động)* | Chuyển HAR → k6 theo cách phi-AI để làm mốc so sánh với script AI | Mã nguồn mở, miễn phí | Có mốc "máy móc không AI" thì mới đánh giá được AI hơn/kém ở đâu. **Cảnh báo:** k6 Studio đã ngừng phát triển riêng; `har-to-k6` cần kiểm tra npm còn dùng được không trước khi demo. Nếu cài không được thì bỏ, không ảnh hưởng demo chính. |
| **Gemini** | Sinh script đầu vào thực tế từ HAR và prompt | Phụ thuộc tài khoản | Artifact: `gemini_script_real.js`; đánh giá cùng rubric với Claude. |
| **Claude** | Sinh script đầu vào thực tế từ HAR và prompt | Phụ thuộc tài khoản | Artifact: `claude_scipt_real.js`; giữ nguyên source để audit. |
| **Luna qua kết nối ChatGPT** | Nhận xét source và đề xuất threshold/correlation trên web | Phụ thuộc quyền tài khoản | Source + k6 evidence được gửi cho model; output JSON được kiểm tra rồi hiển thị thành bảng. |
| Akamas | Chỉ thảo luận (discuss only) | Không chạy | Brief không yêu cầu chạy. Nhóm dùng phần tinh chỉnh SQLite thủ công (D8) làm ví dụ minh họa ý tưởng "tune tham số DB". |
| Task Manager / Resource Monitor, SQLite CLI | Theo dõi CPU/RAM của Node và k6 khi chạy; kiểm tra query chậm bằng `EXPLAIN QUERY PLAN` | Có sẵn | Để giải thích nguyên nhân suy giảm, không chỉ báo con số. |

---

## 2. Phạm vi test trong SUT (eshop-sut)

SUT là EShop với backend Node.js + SQLite (1 connection, không pool), frontend-web tại `http://localhost:5173`, frontend-admin tại `http://localhost:5174`. Giỏ hàng của frontend-web lưu trong React state; điểm nghẽn ghi thật tập trung ở `POST /api/checkout` (INSERT bảng `orders`). Bảng `products` không có cột `stock`, không có race condition trừ tồn kho. Các endpoint dưới đây đã đối chiếu với `server.js` và hành vi frontend-web.

| Luồng | Endpoint thật (đã xác minh) | Trang frontend-web | Vì sao test |
| --- | --- | --- | --- |
| Đăng nhập (1 lần/VU, lấy token) | `POST /api/login`<br>Body: `{"email":"test@eshop.com","password":"Test1234!"}`<br>Response: `{"token":"<jwt>","user":{...}}`<br>*JWT không có expiresIn — dùng suốt phiên test.* | `/login` (Login.jsx) | Lấy JWT token, truyền vào header `Authorization: Bearer <token>` cho checkout. Đây là điểm cần correlation trong script — nếu AI bỏ qua bước này thì `POST /api/checkout` trả 401. |
| Tìm kiếm sản phẩm | `GET /api/products?search=iPhone`<br>Không cần token. Response: JSON array sản phẩm. | `/` (Home.jsx) — thanh tìm kiếm | Chiếm tỷ lệ cao nhất; truy vấn dùng `LIKE '%keyword%'` nối chuỗi trực tiếp — full-table scan, không index, lỗ hổng SQL Injection. Điểm nghẽn #1 khi workload nặng về tìm kiếm. |
| Xem chi tiết sản phẩm | `GET /api/products/:id`<br>Ví dụ: `GET /api/products/1` (iPhone 15 Pro Max, 30.000.000đ). Không cần token. ID seed: 1–5. | `/product/:id` (ProductDetail.jsx) | Đọc đơn giản bằng PK, làm mốc "luồng nhẹ" để đối chiếu với các luồng nặng hơn. |
| Checkout / tạo đơn hàng | `POST /api/checkout` (yêu cầu token)<br>Body: `{"total_amount":30000000,"shipping_address":"123 Le Loi, TP.HCM"}`<br>Response: `{"message":"Checkout successful","orderId":<id>}` | `/checkout` (Checkout.jsx) | Luồng ghi nặng nhất: INSERT vào bảng `orders` trong SQLite (writer-lock). Dự đoán là điểm gãy đầu tiên khi spike. Lưu ý: backend nhận `total_amount` từ client, không tự tính lại (lỗi logic theo spec FR-08). |
| (Mở rộng) Admin xem danh sách đơn hàng | `GET /api/admin/orders` (yêu cầu token admin: `admin@eshop.com` / `Admin123!`)<br>Query thực tế: `SELECT orders.*, users.name FROM orders LEFT JOIN users ON orders.user_id = users.id ORDER BY id DESC` | Frontend-admin `http://localhost:5174` | Truy vấn đọc có JOIN chạy song song với INSERT của checkout — mô phỏng kịch bản hỗn hợp (mixed read/write) ngày Flash Sale; SQLite single-writer có thể gây lock contention rõ ràng. |

**Ngoài phạm vi:** frontend-mobile (dùng chung API backend nên không test riêng), import CSV sản phẩm, quản lý coupon, quên mật khẩu.

---

## 3. Mô hình workload (giả định, sẽ chỉnh sau khi chạy baseline)

| Luồng | Ngày thường | Black Friday | Think-time | Giải thích giả định |
| --- | --- | --- | --- | --- |
| Tìm kiếm (`GET /api/products?search=…`) | 55% | 40% | 1–3 giây | Hầu hết người dùng ghé thăm để duyệt, không nhất thiết mua. Trên SUT đây là truy vấn LIKE full-scan tốn CPU nhất — điểm nghẽn #1. |
| Xem chi tiết (`GET /api/products/:id`) | 25% | 20% | 2–5 giây | Người dùng đọc mô tả sản phẩm trước khi quyết định — think-time dài hơn tìm kiếm. |
| Checkout (`POST /api/checkout`) | 20% | 40% (đột biến) | 3–6 giây | Checkout là hành động cuối. Ngày flash sale, áp lực tăng mạnh; đây là luồng ghi vào SQLite và cần token. |

Tỷ lệ tính theo lượt thao tác mỗi virtual user-minute; mô hình "search-heavy, checkout-bursty" theo đúng mô tả của brief. Phiên bản Black Friday dùng lại cho "Workload Model Bake-off" ở Stage S5.

**Dữ liệu test:** tài khoản seed sẵn `test@eshop.com` / `Test1234!`; từ khóa `["iPhone","Samsung","MacBook","AirPods","Keychron"]`; ID sản phẩm seed: 1 (iPhone 15 Pro Max), 2 (Samsung S24 Ultra), 3 (MacBook Pro M3), 4 (AirPods Pro 2), 5 (Keychron Q1); nạp bằng `SharedArray` của k6 và Parameterized Data trong JMeter. Reset DB trước mỗi lần chạy: `node backend/database.js`.

**Về mức 500 VU trong spike:** SUT chạy Node.js đơn luồng + SQLite 1 writer-lock trên máy local — 500 VU đồng thời sẽ khiến hàng đợi DB bùng phát và Node event-loop nghẽn. Đây chính xác là điều brief yêu cầu quan sát. Nhóm theo dõi CPU/RAM bằng Task Manager; nếu máy test cũng quá tải thì giảm đỉnh xuống 200–300 VU và ghi rõ lý do phần cứng trong báo cáo.

---

## 4. Các profile tải

| Profile | Cấu hình | Mục đích |
| --- | --- | --- |
| Smoke | 1 VU, 1 phút | Kiểm tra script chạy đúng luồng (login → search/detail/checkout), không lỗi cú pháp hay correlation |
| Baseline (theo brief) | 50 VU, 5 phút | Số liệu nền p50/p95/p99, error rate; SLO: p95 < 500ms, error < 1% |
| Stress | 50→100→200→300→400 VU, mỗi bậc 2 phút | Tìm điểm gãy (breakpoint): bậc nào p95 vượt 500ms hoặc error rate > 1% |
| Spike (theo brief) | 50→500 VU trong 30 giây, giữ 1 phút, về 50 trong 1 phút | Quan sát suy giảm đột ngột và khả năng phục hồi sau spike |
| Soak (rút gọn) | 30 VU, 15 phút | Xem latency và RAM Node có tăng dần theo thời gian không. |

---

## 5. Kế hoạch Demo chi tiết (8 phần)

Brief yêu cầu demo có ít nhất 1 tính năng traditional và 1 tính năng AI; kế hoạch dưới có 5 phần traditional và 3 phần AI.

| # | Phần demo (công cụ) | Thao tác cụ thể trên EShop | Bằng chứng cần cho thấy | Phụ trách |
| --- | --- | --- | --- | --- |
| D1 | Capture HAR (Chrome DevTools) | Mở `http://localhost:5173`; F12 → tab Network; thực hiện: (1) đăng nhập `test@eshop.com` / `Test1234!` tại `/login`; (2) tìm `?search=iPhone` trên trang `/`; (3) mở `/product/1` (iPhone 15 Pro Max); (4) thêm sản phẩm vào giỏ trên giao diện, vào `/checkout` và đặt hàng → `POST /api/checkout`. Export HAR. | File `.har` chứa đủ 4 request: `POST /api/login`, `GET /api/products?search=iPhone`, `GET /api/products/1`, `POST /api/checkout` với body và response thật | C |
| D2 | k6 baseline viết tay (k6) | Viết script k6 với: (1) hàm `login()`: `POST /api/login`, extract field `token` từ JSON response; (2) hàm `search()`: `GET /api/products?search=${tukhoa_ngaunhien}`; (3) hàm `detail()`: `GET /api/products/${id_ngaunhien_1_5}`; (4) hàm `checkout()`: `POST /api/checkout` với header `Authorization: Bearer ${token}`; chọn luồng theo % mục 3; dữ liệu từ `SharedArray`; `checks` kiểm tra status 200 và field `token`/`orderId`; thresholds `p(95)<500` và `checks>=0.99`; chạy: `k6 run --vus 50 --duration 5m script.js` | Terminal summary và web dashboard (`k6 run --out web-dashboard`) xuất HTML với p50/p95/p99, error rate; so với SLO thresholds | A |
| D3 | JMeter dựng lại workload (JMeter) | Thread Group 50 users, ramp-up 10 giây; Throughput Controller chia % như mục 3; Regular Expression Extractor lấy field `token` từ response `POST /api/login`; HTTP Header Manager set `Authorization: Bearer ${token}`; Response Assertion kiểm tra status 200; chạy CLI: `jmeter -n -t eshop_workload.jmx -e -o ./jmeter-report` | HTML report JMeter trong `./jmeter-report`; bảng đối chiếu p95/error với kết quả k6; giải thích chênh lệch | B |
| D4 | Spike và Stress (k6) | Chạy profile Spike (50→500 VU / 30s, giữ 1 phút, về 50 trong 1 phút) và Stress (50→400 VU từng bậc 2 phút) theo mục 4; mở Task Manager theo dõi CPU/RAM của `node server.js`; sau khi chạy, mở SQLite CLI chạy `EXPLAIN QUERY PLAN SELECT * FROM products WHERE name LIKE '%iPhone%'` để chỉ ra full-table scan (không có index trên cột `name`) | Biểu đồ VU và latency đồng thời; bậc tải p95 vượt 500ms; dự đoán `POST /api/checkout` gây lỗi trước (writer-lock DB), sau đó tìm kiếm LIKE; ảnh chụp Task Manager khi spike đỉnh | A |
| D5 | Hai script Gemini và Claude | HAR và prompt chuẩn làm đầu vào sinh script; lưu hai source thực tế trong samples. | Hai file nguyên bản và tên file hiển thị trên web | C |
| D6 | Web audit và duyệt điểm | Acorn phân tích source; k6 chạy smoke 1 VU x 1 iteration; đọc metric, hiển thị rubric và cho phép duyệt điểm. | Scorecard, log/summary và ảnh web; bộ test evaluator | C |
| D7 | Luna gợi ý hiệu năng | Prompt cố định cấu trúc JSON; Luna tự đề xuất threshold/correlation theo source và evidence. | JSON output và bảng gợi ý trên web | C |
| D8 | Tinh chỉnh SQLite thủ công (mở rộng, k6) | **Trên bản sao SUT** (copy thư mục backend, đổi tên DB thành `database_tuned.sqlite`): (1) mở SQLite CLI: `CREATE INDEX idx_products_name ON products(name);`; (2) bật WAL: `PRAGMA journal_mode=WAL;` (tách read/write lock, giúp đọc song song với ghi); (3) chạy lại k6 baseline 50 VU 5 phút và spike 50→500 VU; đối chiếu với kết quả D2/D4 trên bản gốc. Lưu ý: LIKE `'%keyword%'` với index vẫn là full-scan (chỉ prefix LIKE mới dùng index); WAL chủ yếu giúp luồng đọc (search, detail) song song với checkout mà không bị block. | So sánh p95/error trước và sau; giải thích tại sao WAL giúp luồng đọc nhưng ít giúp checkout; nối với ý tưởng Akamas (discuss only) | B + A |

**Bản rút gọn cho screencast 5–8 phút (Stage S4):** D1 (30 giây) → D2 (2 phút) → D4 spike (1,5 phút) → D5+D6 (2 phút) → D7 (1 phút). D3 và D8 để trong user guide và slides.

---

## 6. Rubric audit script do AI sinh (dùng ở D6)

Mỗi tiêu chí 0/1 điểm, tổng 10:

1. **Endpoint tồn tại thật trong SUT:** phải là `POST /api/login` (không phải `/api/auth/login`), `GET /api/products?search=…`, `GET /api/products/:id` (id 1–5), `POST /api/checkout` (không phải `/api/orders`).
2. **Đúng method và body:** login body có `email` + `password`; checkout body có `total_amount` + `shipping_address`.
3. **Đúng thứ tự luồng:** login trước, dùng token cho checkout; search/detail không cần token.
4. **Lấy và truyền token đúng:** extraction từ field `token` trong JSON response của `POST /api/login`; gửi qua header `Authorization: Bearer <token>`.
5. **Có think-time hợp lý:** sleep giữa các bước (1–3 giây search, 2–5 giây detail, 3–6 giây checkout) theo mục 3.
6. **Tỷ lệ luồng khớp mục 3:** search ~55%, detail ~25%, checkout ~20%.
7. **Tham số hóa dữ liệu:** từ khóa tìm kiếm ngẫu nhiên từ danh sách (iPhone/Samsung/MacBook/AirPods/Keychron), ID sản phẩm ngẫu nhiên 1–5, không cùng một giá trị.
8. **Có `checks`:** kiểm tra status 200, field `token` có giá trị khi login, field `orderId` có giá trị khi checkout.
9. **Có thresholds đúng SLO:** `http_req_duration{p(95)}: ['<500']`, `checks: ['rate>=0.99']`.
10. **Chạy được không cần sửa cú pháp:** `k6 run script.js` hoàn thành ít nhất 1 iteration không có lỗi runtime.

---

## 7. Failure modes sẽ minh họa (phục vụ mục bắt buộc của user guide)

- **Tải ảo do chạy k6 và SUT cùng máy:** máy quá tải làm số liệu xấu hơn thực tế. Cách xử lý: ghi nhận CPU trong Task Manager; nếu được thì chạy k6 trên máy thứ hai trong cùng mạng LAN (trỏ base URL về IP máy chạy SUT).
- **Script AI sai endpoint hoặc thiếu correlation:** ví dụ AI sinh `POST /api/auth/login` (không tồn tại trong SUT) hoặc dùng `POST /api/orders` thay vì `POST /api/checkout` → 404 toàn bộ. Hoặc AI thiếu bước lấy token → `POST /api/checkout` trả 401. Minh họa bằng D6.
- **Script AI gửi token sai vị trí:** SUT kiểm tra header `Authorization: Bearer <token>` (middleware `authenticateToken` trong `server.js`); nếu AI gửi token trong body hoặc query string thì vẫn trả 401.
- **Nhìn trung bình thay vì percentile, hoặc threshold quá lỏng:** test "đạt" nhưng p99 rất tệ; minh họa bằng đối chiếu avg và p99 ở D4.
- **Giới hạn SQLite 1 writer-lock:** suy giảm ở spike phản ánh DB demo (SQLite single-writer), không phải hệ thống production (cần pooled Postgres + connection limit). Minh họa bằng D4 và D8.

---

## 8. Phân công và timeline 3 tuần

| Tuần | Thành viên A (k6, stress/spike) | Thành viên B (JMeter, dữ liệu, SUT) | Thành viên C (AI, HAR, báo cáo) |
| --- | --- | --- | --- |
| 1 | Cài k6; dựng SUT local: `cd backend && node database.js` (seed), sau đó `node server.js`; viết smoke script 4 luồng với endpoint thật; xác nhận correlation token hoạt động | Dựng SUT local; tạo bộ dữ liệu test (CSV 50 tài khoản, danh sách từ khóa, ID 1–5); viết script seed và reset DB; xác nhận endpoint bằng curl/Postman; hoàn thiện proposal | Capture HAR (D1) trên `http://localhost:5173`; soạn prompt chuẩn cho AI kèm spec endpoint thật; xây dựng rubric mục 6; hoàn thiện proposal phần AI |
| 2 | D2 baseline 50 VU 5 phút; D4 spike 50→500 VU và stress 50→400 VU; ghi lại số liệu p50/p95/p99 | D3: dựng file `eshop_workload.jmx`, Regular Expression Extractor lấy token từ `POST /api/login`, chạy CLI `jmeter -n -t eshop_workload.jmx -e -o ./jmeter-report`; đối chiếu số liệu với D2 | D5/D6: hai script Gemini/Claude, React/Express audit, k6 smoke và rubric |
| 3 | D8 (trên bản sao SUT): tạo index, bật WAL, chạy lại baseline và spike; chạy chính thức lấy số liệu cuối; hỗ trợ quay screencast | D8 (kiểm tra tính tái lập kết quả); viết 1-page performance report; chuẩn bị slides đối chiếu D2/D3 | D6/D7: hoàn thiện evaluator, Luna JSON, kiểm thử hồi quy và báo cáo Markdown có evidence |

Khối lượng vừa sức: mỗi tuần mỗi người tập trung 1–2 demo item + task hỗ trợ chung. Tuần 3 có D8 chia cho cả A và B vì cần so sánh song song (A chạy, B xác nhận tái lập).

Chéo vai trò: cuối tuần 3 mỗi thành viên tự chạy script của người khác một lần để đảm bảo cả 3 đều làm được cả k6 lẫn JMeter như brief yêu cầu.

---

## 9. Rủi ro và phương án dự phòng

- **Phiên ChatGPT hết hạn hoặc lỗi mạng:** hiển thị lỗi kết nối AI; audit bằng rule/k6 và tải scorecard vẫn sử dụng được.
- **Backend sập khi spike 500 VU:** giữ sẵn lệnh reset (`node backend/database.js` seed lại; `node backend/server.js` restart); giảm đỉnh xuống 200–300 VU nếu máy không đủ tài nguyên và ghi rõ trong báo cáo.
- **AI sinh script sai endpoint (ví dụ `/api/auth/login` hoặc `/api/orders`):** ghi nhận đó là kết quả thực nghiệm (tính vào rubric tiêu chí 1), sửa tay và chạy lại để có số liệu so sánh trước/sau.
- **Không cài được k6 Studio / har-to-k6:** bỏ mốc "phi-AI", chỉ so sánh với script viết tay D2.
- **Thiếu thời gian:** thứ tự ưu tiên giữ lại D1, D2, D4, D5, D6, D7 (đủ yêu cầu bắt buộc), sau đó D3, cuối cùng D8.
- **Mâu thuẫn mật khẩu admin:** `setup_guide.md` ghi `admin123` nhưng `database.js` seed `Admin123!` — **CẦN XÁC NHẬN** bằng cách thử đăng nhập sau khi chạy `node database.js`; ưu tiên dùng mật khẩu trong file seed.

---

## 10. Đối chiếu yêu cầu của brief

- Workload model % search/detail/checkout → mục 3.
- Triển khai ở JMeter và k6 → D3 và D2.
- Baseline 50 VU và spike 50→500 trong 30 giây → mục 4, D2, D4.
- p50/p95/p99, error rate, báo cáo 1 trang → D2, D3 và kế hoạch tuần 3.
- AI sinh kịch bản từ log, audit và sửa → D5, D6, D7.
- Demo có ≥1 tính năng traditional và ≥1 tính năng AI → D2/D4 và D5/D7.
- Lý do bỏ Locust, Akamas chỉ thảo luận → mục 1.
