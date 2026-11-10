# Kế hoạch Usability Test – EShop Web Admin (Task 2, Phase 1)

> Soạn theo **kế hoạch 9 phần** của Rubin & Chisnell (slide Usability, trang 35). Bản nháp do Claude Code hỗ trợ soạn ngày 2026-11-11; người kiểm thử rà soát và chốt trước khi chạy pilot.

## 1. Mục đích (Purpose)

Đánh giá khả năng sử dụng của **Web Admin EShop** khi một chủ cửa hàng nhỏ thực hiện các việc quản trị hằng ngày, để tìm điểm nghẽn trong luồng *Dashboard → Danh mục → Đơn hàng → Người dùng* và đo mức độ tin tưởng của người dùng vào giao diện.

## 2. Câu hỏi nghiên cứu (Problem statements)

1. **Rõ ràng (clarity):** người dùng không biết kỹ thuật có tìm đúng chức năng và hiểu đúng các nhãn, trạng thái, con số không?
2. **Phục hồi lỗi (error recovery):** khi thao tác nhầm hoặc hệ thống lỗi, họ có nhận ra và sửa được không?
3. **Tốc độ (speed):** họ hoàn thành 4 việc trong bao lâu, bị vướng ở đâu?
4. **Tin cậy (trust):** họ có tin các số liệu và thao tác (xóa, đổi trạng thái) mà hệ thống hiển thị không?

## 3. Mục tiêu đo và nhiệm vụ (Objectives and tasks)

**Kịch bản gửi cho participant** (hướng mục tiêu, không chỉ từng bước):

> "Bạn là chủ một cửa hàng online nhỏ bán đồ điện tử. Sáng nay bạn mở trang quản trị của cửa hàng để làm vài việc. Hãy làm lần lượt các việc sau, vừa làm vừa nói ra điều bạn đang nghĩ."

| # | Nhiệm vụ (lời nói với participant) | Trạng thái đầu | Tiêu chí thành công | Chuẩn thời gian |
|---|---|---|---|---|
| T1 | "Bạn muốn biết cửa hàng đang kinh doanh ra sao. Hãy cho tôi biết **tổng doanh thu** và **tổng số đơn hàng**." | Đã đăng nhập, đang ở trang đầu | Đọc đúng hai con số trên màn hình | 1 phút |
| T2 | "Bạn vừa nhập một nhóm hàng mới là **Màn hình**. Hãy thêm nhóm hàng này vào cửa hàng." | Danh sách nhóm hàng chưa có 'Màn hình' | Dòng 'Màn hình' xuất hiện trong danh sách | 1 phút |
| T3 | "Một khách vừa đặt đơn **150.000 ₫**. Hãy tìm đơn đó, cho tôi biết nó đang ở trạng thái nào, rồi **xác nhận** đơn." | Có đơn 150.000 ₫ đang Chờ xác nhận | Đơn chuyển sang 'Đã xác nhận' | 2 phút |
| T4 | "Bạn muốn biết khách hàng có email **vana@example.com** đã đăng ký tài khoản chưa. Hãy kiểm tra." | Tài khoản tồn tại | Nói đúng 'đã có' và nêu được mã (ID) hoặc email | 1,5 phút |

Tổng thời gian thao tác dự kiến: khoảng 5,5 phút; cả phiên (có giới thiệu, SUS, phỏng vấn) khoảng 25 đến 30 phút.

**Kết quả của mỗi nhiệm vụ:** *Hoàn thành* (không trợ giúp), *Hoàn thành có trợ giúp*, *Không hoàn thành*.

## 4. Hồ sơ người dùng (User profile)

- **Đối tượng mục tiêu:** chủ hoặc nhân viên cửa hàng nhỏ cần quản lý đơn hàng, danh mục, khách hàng trên một trang quản trị.
- **Tiêu chí tuyển:** 7 người thật, **ngoài lớp HW03**, ưu tiên **không làm IT/kiểm thử**; đã từng bán hàng hoặc dùng phần mềm quản lý cơ bản (bảng tính, trang bán hàng).
- **Loại trừ:** sinh viên đang học HW03; người đã thấy trước ứng dụng EShop.
- **Pilot:** 1 người nằm ngoài 7 người chính.
- Thông tin liên hệ xác minh được (Zalo, email hoặc SĐT, che 4 số giữa), lưu ở `04_participants_TEMPLATE.md` (do người kiểm thử tự điền).

## 5. Phương pháp và thiết kế thử nghiệm (Method)

- **Moderated, in-person hoặc từ xa có chia sẻ màn hình**, một người một phiên, **7 phiên chính + 1 pilot**.
- **Think-aloud:** participant nói ra điều đang nghĩ khi làm.
- **Within-subject đơn giản:** mọi người làm cùng 4 nhiệm vụ theo thứ tự cố định T1 → T4 (luồng phụ thuộc nhau về logic).
- **Loại kiểm thử:** *assessment test* (slide trang 33): nhiệm vụ rõ, đo cả định lượng và định tính.
- **Quy trình một phiên:** (1) giới thiệu và xin phép quay (3 phút) → (2) làm 4 nhiệm vụ (khoảng 8 đến 12 phút, mỗi nhiệm vụ xong trả lời 1 câu SEQ) → (3) làm bảng SUS (3 phút) → (4) phỏng vấn probe (5 đến 8 phút).

## 6. Môi trường và thiết bị (Environment)

- Máy tính xách tay/để bàn, trình duyệt Chrome, màn hình tối thiểu 1366×768.
- **Admin:** http://localhost:5174 (frontend-admin), **backend:** http://localhost:3000. Tài khoản Admin đăng nhập sẵn trước khi participant ngồi vào; participant không phải đăng nhập.
- **Dữ liệu chuẩn cho mỗi phiên:** khởi động lại backend rồi chạy `python hw03/scripts/usability_seed.py` để mọi participant có cùng trạng thái ban đầu (xem mục 9 của file này).
- **Quay màn hình** bằng công cụ của hệ điều hành (Win+G) hoặc OBS, kèm âm thanh **khi participant đồng ý**.
- **Lưu ý SUT:** tài khoản Admin bị khóa 3 phút nếu sai mật khẩu 2 lần; đăng nhập sẵn và không để participant thao tác đăng nhập. Không khởi động lại backend giữa phiên (dữ liệu bị seed lại).

## 7. Vai trò của người điều phối (Test monitor role)

- Giải thích mục đích, nhấn mạnh **"đang kiểm thử sản phẩm, không phải kiểm thử bạn"**.
- **Quan sát trung lập:** không gợi ý, không giải thích giao diện, không phản ứng bằng nét mặt hay lời khen.
- Chỉ can thiệp khi participant **hoàn toàn bí quá 2 phút**, theo thang gợi ý ở `03_moderator_script_and_notes_template.md`, và ghi rõ là "có trợ giúp".
- Ghi chú có cấu trúc: điểm vướng, lỗi, do dự, lời bực bội (ghi nguyên văn).

## 8. Dữ liệu cần thu thập và cách đánh giá (Evaluation measures)

**Hiệu năng (khách quan):** thời gian mỗi nhiệm vụ; kết quả (hoàn thành / có trợ giúp / không); số lỗi (thao tác sai, chọn nhầm); số lần cần trợ giúp.
**Sở thích (chủ quan):** SEQ (1 đến 7) sau mỗi nhiệm vụ; **SUS** sau phiên; câu trả lời probe về rõ ràng, phục hồi lỗi, tốc độ, tin cậy.

**Phân tích:** điểm SUS từng người, trung bình, trung vị, độ lệch chuẩn; tỉ lệ hoàn thành theo nhiệm vụ; thời gian trung bình; nhóm pain point thành lỗi đơn lẻ và vấn đề hệ thống; xếp **mức độ = nghiêm trọng × xác suất** (slide trang 41):

| Mức nghiêm trọng | Điểm | Ví dụ |
|---|---|---|
| Blocker | 4 | Không thể hoàn thành nhiệm vụ |
| Major | 3 | Hoàn thành được nhưng mất nhiều thời gian hoặc phải trợ giúp |
| Minor | 2 | Gây khó chịu nhưng vẫn làm được |
| Cosmetic | 1 | Thẩm mỹ |

Xác suất = số participant gặp vấn đề / 7. Mức ưu tiên = điểm nghiêm trọng × xác suất.

## 9. Nội dung báo cáo (Report contents)

Mục tiêu và phương pháp; bảng 7 participant; kết quả định lượng (SUS, thời gian, hoàn thành); phát hiện định tính theo bốn chủ đề; bảng phát hiện xếp mức độ; khuyến nghị; bug thật báo lên GitHub kèm ảnh; hạn chế của nghiên cứu.

---

## Giả thuyết cần kiểm chứng (rút từ kết quả Task 1)

Đây là điều kiểm thử viên **quan tâm quan sát**, không nói cho participant biết.

| Nhiệm vụ | Giả thuyết | Liên hệ bug Task 1 |
|---|---|---|
| T1 | Participant tin con số doanh thu dù nó gấp đôi tổng các đơn Đã giao | BUG-08 |
| T2 | Thêm xong không có thông báo thành công, participant không chắc đã thêm được chưa | BUG-09 |
| T2 | Bấm nút nhiều lần vì không thấy phản hồi (tạo bản sao) | BUG-12 |
| T3 | Bấm Xác nhận/Hủy không có xác nhận gây lo lắng hoặc thao tác nhầm | BUG-04 |
| T3 | Hiểu sai nhãn trạng thái hoặc nút | BUG-22 |
| T4 | Bảng Người dùng không có cột Tên/ô tìm kiếm nên mất thời gian tìm | BUG-23 |
| Cả luồng | Làm mới trang (F5) quay về Dashboard làm participant lạc hướng | BUG-14 |

## Chuẩn bị dữ liệu chuẩn cho mỗi phiên

Dữ liệu seed mặc định không có đơn hàng, nên cần tạo cùng một bộ dữ liệu cho mọi participant:

1. Khởi động lại backend (`node backend/server.js`), việc này seed lại toàn bộ database.
2. Chạy `python hw03/scripts/usability_seed.py` (tạo 6 đơn gồm đơn 150.000 ₫ Chờ xác nhận cho T3, và tài khoản `vana@example.com` cho T4).
3. Đăng nhập Admin trước, để màn hình ở trang đầu (Dashboard).
