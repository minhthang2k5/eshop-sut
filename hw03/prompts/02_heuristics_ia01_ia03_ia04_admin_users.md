# Prompt 2 – Sinh mục checklist từ các nguyên tắc thiết kế (IA-01, IA-03, IA-04)

- **Mục đích:** Dùng 3 bộ nguyên tắc trong bài giảng (Nielsen 10, Norman 6, Shneiderman 8) để sinh mục kiểm tra cho 3 khía cạnh: **IA-01** (chuẩn UI chung), **IA-03** (điều hướng), **IA-04** (phản hồi/trạng thái). IA-02 (Forms) để cho Prompt 3–4.
- **Căn cứ lý thuyết:** slide GUI Testing, trang 6–9 ("checklist đến từ đâu": Nielsen 10 → Norman 6 → Shneiderman 8 → biến thành bảng review, chấm Yes/No/N/A kèm priority và severity).
- **Đầu vào:** bản mô tả màn hình ở Prompt 1 và kết quả kiểm kê của AI.
- **Tool AI dùng:** _(điền)_
- **Ngày giờ chạy:** _(điền)_

---

## Prompt (dán nguyên khối vào AI, trong cùng cuộc hội thoại với Prompt 1)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Hãy kiểm thử HỘP ĐEN: chỉ dựa vào bản mô tả dưới đây, KHÔNG đọc mã nguồn, KHÔNG suy đoán cách cài đặt bên trong.

## Màn hình: "Quản lý Người dùng" (tab "Người dùng" của Web Admin EShop, tiếng Việt)
- Thanh menu tối bên trái, tiêu đề "EShop Admin", các mục: Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng (đang chọn, chữ xanh), Đăng xuất (chữ đỏ).
- Vùng nội dung bên phải nền sáng, tiêu đề trang "Quản lý Người dùng".
- Bảng nền trắng, hàng tiêu đề nền xám, 6 cột: checkbox (có ở tiêu đề và mỗi dòng), ID, Email, Role, Số ĐT, Hành động.
- Dữ liệu hiện có: 2 người dùng (1 admin, 1 user). Cột Số ĐT đang trống ở cả hai dòng. Mỗi dòng có nút "Xóa" nền đỏ chữ trắng.
- KHÔNG có: ô tìm kiếm, bộ lọc, sắp xếp cột, phân trang, cột Tên, nút Sửa, nút Thêm, biểu tượng cạnh các mục menu.

## Nhiệm vụ
Hãy sinh các MỤC CHECKLIST GUI cho màn hình này. Ở bước này chỉ sinh cho 3 khía cạnh sau (KHÔNG sinh cho Forms):

- IA-01: Chuẩn giao diện chung (bố cục, font, màu, căn lề, chính tả, độ nhất quán, hình ảnh/biểu tượng, độ tương phản)
- IA-03: Điều hướng (menu, chuyển giữa các tab/trang, vị trí hiện tại, quay lại, thoát)
- IA-04: Phản hồi và trạng thái (loading, thông báo thành công/lỗi, xác nhận thao tác, trạng thái rỗng, trạng thái chọn/vô hiệu, thao tác không thể hoàn tác)

## Nguồn nguyên tắc bắt buộc dùng
Mỗi mục sinh ra phải bám vào ít nhất một nguyên tắc dưới đây và ghi rõ tên nguyên tắc đó:

Nielsen 10 heuristics:
1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

Norman 6 principles: Visibility, Feedback, Affordance, Mapping, Constraints, Consistency.

Shneiderman 8 Golden Rules: (1) Strive for consistency, (2) Enable shortcuts for frequent users, (3) Offer informative feedback, (4) Design dialogues to yield closure, (5) Offer simple error handling, (6) Permit easy reversal of actions, (7) Support internal locus of control, (8) Reduce short-term memory load.

## Quy tắc
- Chỉ kiểm tra những gì có trên màn hình theo mô tả. Với tính năng không có (ví dụ tìm kiếm, phân trang), chỉ sinh mục nếu việc THIẾU nó là một vấn đề đáng kiểm tra, và ghi rõ như vậy.
- Mỗi mục là MỘT điểm kiểm tra rõ ràng, thực hiện được trong vài phút, có kết quả Passed/Failed. Không gộp nhiều ý vào một mục. Không lặp ý.
- Mục có thể phản ánh một hành vi cần kiểm tra bằng thao tác thật (ví dụ: bấm Xóa), hãy viết thành mục kiểm tra, không đoán kết quả.
- Mỗi IA sinh khoảng 8–10 mục.
- Cột "Kết quả mong đợi" chỉ mô tả CHUẨN tham chiếu mà giao diện nên đạt, KHÔNG viết sẵn kết luận Passed/Failed và KHÔNG viết "nếu không thì Failed".
- Mục so sánh với tab khác chỉ để kiểm tra tính nhất quán, không kiểm tra chức năng của tab đó.
- Mục cần giả lập điều kiện đặc biệt (mạng chậm, tắt backend, dữ liệu rỗng) phải ghi rõ cách giả lập trong cột "Mục kiểm tra".

## Định dạng đầu ra
Một bảng Markdown cho mỗi IA, với các cột:
| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Mức ưu tiên (Mandatory/Optional) |

ID tạm dạng AI-01-01, AI-03-01, AI-04-01.

Trả lời bằng tiếng Việt. Cuối cùng, nêu ngắn gọn các khía cạnh GUI mà bạn nghĩ mình CHƯA phủ trong bảng.
```

---

## Ghi log (điền sau khi chạy)

### Output của AI – Lần 1 (prompt gốc, AI mất bối cảnh Prompt 1)

> Ghi chú: AI báo không thấy bản mô tả và bảng kiểm kê của Prompt 1 trong cuộc hội thoại, nên tự đọc mã nguồn `frontend-admin/src/App.jsx` làm căn cứ. Đây là chạy khác bối cảnh dự kiến (xem nhận xét).

Tôi chưa thấy bản mô tả màn hình và bảng kiểm kê ở bước trước trong cuộc trò chuyện này, nên tôi sẽ tìm trong thư mục dự án.

Tôi không thấy bản mô tả màn hình và bảng kiểm kê ở bước trước trong cuộc trò chuyện này. Vì vậy tôi lấy màn hình thật làm căn cứ, từ mã nguồn tại [App.jsx](eshop-sut/frontend-admin/src/App.jsx) (tab `users`, dòng 879–918, cùng sidebar). Nếu bản mô tả của bạn khác mã nguồn, hãy báo tôi để chỉnh lại.

Các mục dưới đây là điểm cần kiểm tra bằng thao tác thật. Cột "Kết quả mong đợi" là chuẩn tham chiếu, không phải kết quả tôi đoán.

## IA-01: Chuẩn giao diện chung

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Mức ưu tiên |
|---|---|---|---|---|---|---|
| AI-01-01 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Bố cục tổng thể (sidebar + vùng nội dung) | Mở tab "Người dùng" ở độ rộng 1366 và 1920; quan sát bố cục | Sidebar bên trái và vùng nội dung bên phải không chồng lấn. Bảng nằm gọn trong vùng nội dung, không có thanh cuộn ngang ngoài ý muốn | Mandatory |
| AI-01-02 | IA-01 | Nielsen #4 Consistency and standards; Shneiderman #1 | Tiêu đề trang "Quản lý Người dùng" | So sánh tiêu đề với các trang Danh mục, Sản phẩm, Mã giảm giá, Đơn hàng (cỡ chữ, độ đậm, khoảng cách tới nội dung) | Tiêu đề cùng kiểu và cùng khoảng cách ở mọi trang quản lý | Mandatory |
| AI-01-03 | IA-01 | Nielsen #4 Consistency and standards; Norman Consistency | Nút "Xóa" trong bảng | So sánh nút Xóa ở tab Người dùng với nút Xóa ở Danh mục, Sản phẩm, Mã giảm giá (màu, kích thước, cỡ chữ, bo góc) | Mọi nút Xóa có cùng màu, kích thước và cỡ chữ | Mandatory |
| AI-01-04 | IA-01 | Nielsen #4 Consistency and standards | Nhãn tiêu đề cột và menu | Đối chiếu ngôn ngữ của các nhãn "Email", "Role", "Số ĐT", "Hành động" và "Dashboard" với phần còn lại của giao diện | Cùng một ngôn ngữ cho các nhãn cùng loại. Không trộn Anh–Việt tuỳ tiện | Mandatory |
| AI-01-05 | IA-01 | Nielsen #2 Match between system and real world | Chính tả, dấu tiếng Việt | Đọc toàn bộ chữ trên màn hình; kiểm tra dấu, ký tự "₫" và từ viết tắt "ĐT" | Không lỗi chính tả hay lỗi hiển thị font. Từ viết tắt dễ hiểu với admin | Mandatory |
| AI-01-06 | IA-01 | Norman Visibility; Nielsen #8 | Độ tương phản chữ/nền | Kiểm tra tương phản: chữ trắng trên nút đỏ, chữ xanh của mục menu đang chọn trên nền xám đậm, chữ trong tiêu đề bảng xám | Chữ đọc rõ, tỉ lệ tương phản đạt tối thiểu 4.5:1 cho chữ thường | Mandatory |
| AI-01-07 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Căn lề và khoảng cách trong bảng | Quan sát căn lề tiêu đề cột so với dữ liệu, padding ô, đường kẻ giữa các dòng | Tiêu đề và dữ liệu cùng cột thẳng hàng. Padding đồng đều. Các dòng phân tách rõ | Mandatory |
| AI-01-08 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Ô dữ liệu dài (Email, Số ĐT) | Dữ liệu có email rất dài (khoảng 60 ký tự); quan sát ô Email | Nội dung không tràn khỏi bảng và không đè lên cột bên cạnh. Nếu bị cắt thì có dấu "…" và xem được đầy đủ | Optional |
| AI-01-09 | IA-01 | Nielsen #4 Consistency and standards | Giá trị trống của cột "Số ĐT" | Xem dòng có Số ĐT rỗng; so với cột "Địa chỉ" ở tab Đơn hàng (hiển thị "Chưa cập nhật") | Ô rỗng được hiển thị thống nhất, ví dụ "—" hoặc "Chưa cập nhật", không để trống không giải thích | Optional |
| AI-01-10 | IA-01 | Norman Consistency; Nielsen #4 | Giá trị cột "Role", icon, tab trình duyệt | Quan sát cách hiển thị "Role" (chữ thuần hay badge) so với badge "Trạng thái" ở tab Đơn hàng. Xem tiêu đề tab trình duyệt và favicon | Cách hiển thị giá trị phân loại thống nhất giữa các bảng. Tiêu đề tab mang tên sản phẩm (EShop Admin) thay vì tên kỹ thuật | Optional |

## IA-03: Điều hướng

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Mức ưu tiên |
|---|---|---|---|---|---|---|
| AI-03-01 | IA-03 | Norman Visibility; Nielsen #6 Recognition rather than recall | Menu sidebar | Ở tab Người dùng, đếm các mục menu hiển thị | Đủ 7 mục (Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng, Đăng xuất), luôn thấy mà không phải cuộn | Mandatory |
| AI-03-02 | IA-03 | Nielsen #1 Visibility of system status | Mục menu "Người dùng" (vị trí hiện tại) | Chuyển lần lượt qua từng tab; quan sát mục menu được làm nổi bật | Chỉ mục của tab đang mở được nổi bật. Phân biệt rõ với các mục còn lại | Mandatory |
| AI-03-03 | IA-03 | Norman Affordance | Mục menu | Rê chuột qua từng mục menu; quan sát con trỏ và hiệu ứng | Con trỏ đổi thành bàn tay. Có hiệu ứng hover cho thấy mục bấm được | Mandatory |
| AI-03-04 | IA-03 | Nielsen #7 Flexibility and efficiency of use; Shneiderman #2 | Mục menu (bàn phím) | Dùng phím Tab/Enter để đi qua menu và mở tab "Người dùng" | Từng mục menu nhận được focus (có viền focus nhìn thấy được) và kích hoạt được bằng Enter | Optional |
| AI-03-05 | IA-03 | Norman Mapping; Nielsen #2 | Nhãn menu so với tiêu đề trang | Bấm "Người dùng" rồi đối chiếu với tiêu đề "Quản lý Người dùng" | Nhãn menu khớp rõ ràng với tiêu đề trang đích | Optional |
| AI-03-06 | IA-03 | Nielsen #3 User control and freedom | Nút Back của trình duyệt | Ở tab Người dùng sau khi đã đi qua vài tab, bấm Back của trình duyệt | Quay về tab trước đó trong ứng dụng, không thoát khỏi ứng dụng admin ngoài ý muốn | Mandatory |
| AI-03-07 | IA-03 | Nielsen #1 Visibility of system status; Nielsen #7 | Địa chỉ (URL) và việc tải lại trang | Ở tab Người dùng, nhấn F5; quan sát URL trước và sau | Sau khi tải lại vẫn ở tab Người dùng. URL phản ánh trang hiện tại, dùng được để đánh dấu hoặc chia sẻ | Mandatory |
| AI-03-08 | IA-03 | Nielsen #3 User control and freedom | Mục "Đăng xuất" | Bấm "Đăng xuất" | Quay về màn hình đăng nhập và không còn thấy dữ liệu quản trị. Mục này tách biệt khỏi nhóm menu chính và dễ tìm | Mandatory |
| AI-03-09 | IA-03 | Nielsen #5 Error prevention | Mục "Đăng xuất" (bấm nhầm) | Bấm "Đăng xuất" khi đang làm việc; xem có bước xác nhận không | Có xác nhận, hoặc việc đăng xuất ngoài ý muốn được chấp nhận và dễ khắc phục. Ghi nhận hành vi thực tế | Optional |
| AI-03-10 | IA-03 | Nielsen #3 User control and freedom; Nielsen #9 | Phiên đăng nhập hết hạn | Đang ở tab Người dùng, làm token hết hạn hoặc sai rồi tải lại dữ liệu | Quay về trang đăng nhập kèm thông báo "phiên hết hạn", không đột ngột bị đẩy ra | Optional |

## IA-04: Phản hồi và trạng thái

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Mức ưu tiên |
|---|---|---|---|---|---|---|
| AI-04-01 | IA-04 | Nielsen #1 Visibility of system status; Shneiderman #3 | Bảng người dùng (đang tải) | Giả lập mạng chậm (Slow 3G), mở tab Người dùng | Có chỉ báo đang tải (spinner hoặc "Đang tải…"), không hiện bảng trống gây hiểu nhầm | Mandatory |
| AI-04-02 | IA-04 | Nielsen #9 Help users recognize, diagnose, and recover from errors | Bảng người dùng (lỗi tải dữ liệu) | Tắt backend rồi mở hoặc tải lại tab Người dùng | Có thông báo lỗi tải dữ liệu dễ hiểu kèm cách thử lại, không im lặng hiển thị bảng rỗng | Mandatory |
| AI-04-03 | IA-04 | Nielsen #1; Norman Feedback | Bảng người dùng (trạng thái rỗng) | Cho API trả về danh sách rỗng; quan sát bảng | Có thông báo "Chưa có người dùng", không chỉ còn hàng tiêu đề | Mandatory |
| AI-04-04 | IA-04 | Nielsen #5 Error prevention; Shneiderman #4 Design dialogues to yield closure | Nút "Xóa" (xác nhận) | Bấm "Xóa" trên một người dùng thử nghiệm | Có hộp xác nhận trước khi xóa. Chưa có dữ liệu nào bị xóa tại thời điểm này | Mandatory |
| AI-04-05 | IA-04 | Shneiderman #6 Permit easy reversal of actions; Nielsen #3 | Hộp xác nhận xóa (nội dung) | Đọc nội dung hộp xác nhận | Nêu rõ người dùng bị xóa (email/ID) và cảnh báo hành động không hoàn tác. Có nút Hủy và nút Đồng ý | Mandatory |
| AI-04-06 | IA-04 | Nielsen #1; Shneiderman #3 Offer informative feedback | Kết quả xóa thành công | Xác nhận xóa một người dùng thử nghiệm | Có thông báo thành công (toast hoặc tương đương). Dòng biến mất khỏi bảng mà không cần tải lại trang | Mandatory |
| AI-04-07 | IA-04 | Nielsen #9; Shneiderman #5 Offer simple error handling | Kết quả xóa thất bại | Xóa người dùng khi backend lỗi hoặc người dùng có dữ liệu ràng buộc (đơn hàng); xem thông báo | Thông báo lỗi nêu nguyên nhân bằng ngôn ngữ dễ hiểu và gợi ý cách xử lý. Không hiện mã lỗi kỹ thuật thô | Mandatory |
| AI-04-08 | IA-04 | Nielsen #5; Norman Constraints | Nút "Xóa" khi đang xử lý | Bấm "Xóa" nhanh hai lần liên tiếp (hoặc khi mạng chậm) | Nút chuyển sang trạng thái đang xử lý/vô hiệu hóa. Chỉ gửi một yêu cầu xóa | Mandatory |
| AI-04-09 | IA-04 | Nielsen #5 Error prevention; Norman Constraints | Nút "Xóa" của tài khoản đang đăng nhập | Thử xóa chính tài khoản admin đang đăng nhập | Hệ thống chặn (nút vô hiệu hóa hoặc có cảnh báo). Không để admin tự khóa mình ra khỏi hệ thống | Mandatory |
| AI-04-10 | IA-04 | Norman Feedback; Norman Affordance | Checkbox chọn dòng / chọn tất cả | Tick ô checkbox ở tiêu đề và ở từng dòng | Trạng thái chọn thể hiện rõ: dòng được chọn khác biệt, ô tiêu đề chọn được tất cả, có chỉ báo số dòng đã chọn và hành động đi kèm. Nếu checkbox không làm gì thì ghi Failed (gây hiểu nhầm) | Mandatory |

## Điểm nghi vấn trong mã nguồn, cần xác nhận bằng thao tác thật

- Nút Xóa gọi API ngay, chưa thấy hộp xác nhận.
- Các thông báo hiện dùng `alert` với thông điệp lỗi thô.
- Chưa thấy trạng thái loading hay trạng thái rỗng.
- Hàm tải dữ liệu bỏ qua im lặng mọi lỗi trừ 401/403.
- Checkbox có vẻ chưa gắn hành động nào.
- Điều hướng dùng state, không dùng router, nên F5 và Back có thể không đúng như mong đợi.
- Nút Xóa ở tab Người dùng dùng `px-3 py-1` và không có `text-sm`, khác nút ở các tab khác.
- Tiêu đề tab trình duyệt là `frontend-admin`.

## Khía cạnh GUI chưa phủ trong bảng

- **Forms:** đã loại theo yêu cầu. Màn hình đăng nhập cũng chưa kiểm.
- **Tính năng thiếu:** chưa có mục riêng cho tìm kiếm, lọc, sắp xếp, phân trang, sửa người dùng và xem chi tiết. Danh sách dài mà thiếu các tính năng này là vấn đề đáng kiểm tra (Nielsen #7).
- **Responsive:** màn hình nhỏ như tablet và điện thoại, thu phóng 150–200%.
- **Khả năng truy cập:** trình đọc màn hình, nhãn `aria` cho checkbox, thứ tự focus chi tiết.
- **Trợ giúp:** tooltip hoặc hướng dẫn, ví dụ ý nghĩa của Role (Nielsen #10).
- **Hiệu năng cảm nhận và dữ liệu lớn:** hàng trăm người dùng, cuộn bảng, tiêu đề bảng cố định.
- **Tương thích trình duyệt:** Chrome, Firefox, Edge.
- **Định dạng dữ liệu:** số điện thoại, ID, hiển thị Role không phân biệt hoa thường.
- **Chế độ tối và in ấn:** chưa kiểm.

### Output của AI – Lần 2 (prompt đã chỉnh: mô tả nằm ngay trong prompt, kiểm thử hộp đen)

- **Tool:** Claude Code (Claude Sonnet 5.5), chạy ngày 2026-11-10.
- **Lưu ý:** phiên này đã đọc mã nguồn trước đó. Output dưới đây chỉ dựa vào mô tả trong prompt, nhưng không thể loại trừ hoàn toàn ảnh hưởng của kiến thức đã có.

## IA-01: Chuẩn giao diện chung

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| AI-01-01 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Bố cục tổng thể | Mở tab "Người dùng" ở độ rộng 1366 và 1920 | Menu trái và vùng nội dung không chồng lấn; bảng nằm gọn trong vùng nội dung, không có cuộn ngang ngoài ý muốn | Mandatory |
| AI-01-02 | IA-01 | Norman Visibility; Shneiderman #1 Consistency | Phân cấp chữ | So sánh cỡ chữ, độ đậm của tiêu đề "Quản lý Người dùng", tiêu đề cột và nội dung bảng | Tiêu đề trang nổi bật hơn tiêu đề cột; tiêu đề cột phân biệt được với dữ liệu | Mandatory |
| AI-01-03 | IA-01 | Nielsen #4 Consistency and standards | Ngôn ngữ nhãn | Đọc các nhãn "Email", "Role", "Số ĐT", "Hành động" và tên các mục menu | Các nhãn cùng loại dùng cùng một ngôn ngữ, không trộn Anh–Việt tùy tiện | Mandatory |
| AI-01-04 | IA-01 | Nielsen #2 Match between system and real world | Chính tả, dấu tiếng Việt | Đọc toàn bộ chữ trên màn hình, kiểm tra dấu và từ viết tắt "ĐT" | Không sai chính tả, không lỗi hiển thị dấu; từ viết tắt dễ hiểu | Mandatory |
| AI-01-05 | IA-01 | Norman Visibility; Nielsen #8 | Tương phản nút "Xóa" | Đo tương phản chữ trắng trên nền đỏ của nút Xóa (công cụ đo tương phản) | Tỉ lệ tương phản ≥ 4.5:1 cho chữ thường | Mandatory |
| AI-01-06 | IA-01 | Norman Visibility; Nielsen #8 | Tương phản menu | Đo tương phản chữ xanh của mục đang chọn và chữ đỏ "Đăng xuất" trên nền menu tối | Tỉ lệ tương phản ≥ 4.5:1 | Mandatory |
| AI-01-07 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Căn lề bảng | Quan sát tiêu đề cột so với dữ liệu cùng cột | Tiêu đề và dữ liệu thẳng hàng nhất quán | Mandatory |
| AI-01-08 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Dữ liệu dài | Tạo người dùng có email rất dài (khoảng 60 ký tự) và quan sát cột Email | Nội dung không tràn khỏi bảng, không đè cột bên cạnh; nếu bị cắt thì có dấu "…" | Optional |
| AI-01-09 | IA-01 | Nielsen #4; Nielsen #6 Recognition rather than recall | Ô Số ĐT trống | Xem dòng người dùng chưa có số điện thoại | Ô trống được thể hiện có chủ đích (ví dụ "—", "Chưa cập nhật"), không để người dùng tự đoán | Optional |
| AI-01-10 | IA-01 | Shneiderman #1 Consistency; Norman Consistency | Nút "Xóa" | So sánh màu, kích thước, bo góc, cỡ chữ của các nút "Xóa" giữa các dòng và với nút "Xóa" ở tab Danh mục | Các nút Xóa cùng màu, kích thước, kiểu chữ | Optional |

## IA-03: Điều hướng

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| AI-03-01 | IA-03 | Norman Visibility; Nielsen #6 | Menu trái | Đếm các mục menu khi ở tab Người dùng | Đủ 7 mục (Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng, Đăng xuất), luôn thấy không cần cuộn | Mandatory |
| AI-03-02 | IA-03 | Nielsen #1 Visibility of system status | Mục đang chọn | Lần lượt mở từng tab, quan sát mục menu được nổi bật | Chỉ mục của tab đang mở được nổi bật, phân biệt rõ với các mục khác | Mandatory |
| AI-03-03 | IA-03 | Norman Affordance | Hover menu | Rê chuột qua từng mục menu | Con trỏ đổi thành bàn tay và/hoặc có hiệu ứng hover cho thấy mục bấm được | Mandatory |
| AI-03-04 | IA-03 | Nielsen #7 Flexibility; Shneiderman #2 | Bàn phím | Nhấn Tab để di chuyển qua các mục menu | Mỗi mục nhận focus và có viền/dấu hiệu focus nhìn thấy được | Optional |
| AI-03-05 | IA-03 | Nielsen #7; Norman Affordance | Kích hoạt bằng bàn phím | Khi mục menu đang focus, nhấn Enter | Mục được kích hoạt và mở đúng tab | Optional |
| AI-03-06 | IA-03 | Norman Mapping; Nielsen #2 | Nhãn menu so với trang | Bấm "Người dùng" và đối chiếu với tiêu đề trang đích | Nhãn menu khớp rõ với tiêu đề "Quản lý Người dùng" | Optional |
| AI-03-07 | IA-03 | Nielsen #3 User control and freedom | Nút Back trình duyệt | Chuyển qua vài tab rồi bấm Back của trình duyệt | Quay về tab trước đó trong ứng dụng, không thoát khỏi ứng dụng ngoài ý muốn | Mandatory |
| AI-03-08 | IA-03 | Nielsen #1; Nielsen #7 | Tải lại trang | Đang ở tab Người dùng, nhấn F5 và quan sát địa chỉ URL trước/sau | Sau khi tải lại vẫn ở tab Người dùng; URL phản ánh trang hiện tại | Mandatory |
| AI-03-09 | IA-03 | Nielsen #3 User control and freedom | Đăng xuất | Bấm "Đăng xuất" | Quay về màn hình đăng nhập, không còn thấy dữ liệu quản trị; mục Đăng xuất dễ tìm và tách biệt khỏi nhóm menu chính | Mandatory |

## IA-04: Phản hồi và trạng thái

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| AI-04-01 | IA-04 | Nielsen #1 Visibility of system status; Shneiderman #3 | Đang tải | Giả lập mạng chậm (Slow 3G trong DevTools) rồi mở tab Người dùng | Có chỉ báo đang tải, không hiện bảng trống gây hiểu nhầm | Mandatory |
| AI-04-02 | IA-04 | Nielsen #9 Recognize, diagnose, recover from errors | Lỗi tải dữ liệu | Tắt backend rồi tải lại tab Người dùng | Có thông báo lỗi dễ hiểu và cách thử lại, không im lặng hiện bảng rỗng | Mandatory |
| AI-04-03 | IA-04 | Norman Feedback; Nielsen #1 | Trạng thái rỗng | Giả lập danh sách người dùng rỗng (xóa hết người dùng thử hoặc dùng DB trống) | Có thông báo "chưa có dữ liệu", không chỉ còn hàng tiêu đề | Mandatory |
| AI-04-04 | IA-04 | Nielsen #5 Error prevention; Shneiderman #4 | Xác nhận khi xóa | Bấm "Xóa" ở một người dùng thử nghiệm | Có bước xác nhận trước khi xóa; chưa có dữ liệu nào bị xóa tại thời điểm này | Mandatory |
| AI-04-05 | IA-04 | Shneiderman #6 Easy reversal; Nielsen #3 | Nội dung xác nhận | Đọc nội dung hộp xác nhận xóa | Nêu rõ người bị xóa (email/ID), cảnh báo không hoàn tác, có lựa chọn Hủy | Mandatory |
| AI-04-06 | IA-04 | Shneiderman #3 Informative feedback | Xóa thành công | Xác nhận xóa một người dùng thử nghiệm | Có thông báo thành công; dòng biến mất khỏi bảng mà không cần tải lại trang | Mandatory |
| AI-04-07 | IA-04 | Nielsen #9; Shneiderman #5 Simple error handling | Xóa thất bại | Tắt backend sau khi đã mở trang rồi bấm Xóa và xác nhận | Có thông báo lỗi nêu nguyên nhân bằng ngôn ngữ dễ hiểu, không lộ mã lỗi hay nội dung kỹ thuật thô | Mandatory |
| AI-04-08 | IA-04 | Nielsen #5; Norman Constraints | Bấm Xóa liên tiếp | Bấm "Xóa" hai lần liên tiếp thật nhanh trên cùng một dòng | Nút chuyển sang trạng thái đang xử lý hoặc chỉ gửi một yêu cầu | Mandatory |
| AI-04-09 | IA-04 | Nielsen #5 Error prevention; Norman Constraints | Xóa tài khoản đang đăng nhập | Thử xóa chính tài khoản admin đang đăng nhập (dùng bản sao dữ liệu để thử) | Hệ thống chặn hoặc cảnh báo rõ; không để admin tự khóa mình khỏi hệ thống | Mandatory |
| AI-04-10 | IA-04 | Norman Feedback; Norman Affordance | Checkbox dòng | Tick ô checkbox ở một dòng | Trạng thái chọn thể hiện rõ (ô được đánh dấu, dòng có thể khác biệt về màu); nếu checkbox không có hành động đi kèm thì có chỉ dẫn rõ vì sao tồn tại | Mandatory |

## Khía cạnh GUI chưa phủ trong 29 mục trên
- **Forms:** đã loại theo yêu cầu, thuộc Prompt 3–4.
- **Checkbox tiêu đề (chọn tất cả):** mới có checkbox dòng, chưa có mục riêng cho ô ở tiêu đề.
- **Responsive:** tablet, điện thoại, thu phóng 150–200%.
- **Accessibility:** trình đọc màn hình, nhãn cho checkbox, thứ tự focus đầy đủ, tương phản chế độ tối.
- **Dark mode, RTL, in ấn.**
- **Tính năng thiếu:** tìm kiếm, lọc, sắp xếp, phân trang khi danh sách dài (Nielsen #7).
- **Dữ liệu lớn:** hàng trăm người dùng, cuộn bảng, tiêu đề cố định.
- **Trợ giúp:** ý nghĩa của cột Role (Nielsen #10), tooltip.
- **Tương thích trình duyệt** (thuộc Task 3).

### Thay đổi so với Lần 1 (người kiểm thử ghi)
- Prompt có mô tả màn hình và quy tắc kiểm thử hộp đen, nên AI không phải đọc mã nguồn.
- Mỗi mục kiểm tra một điểm; checkbox tách khỏi mục khác; mục cần giả lập đều nêu cách giả lập.
- Cột "Kết quả mong đợi" không còn chứa kết luận Passed/Failed.
- Không còn các mục so sánh sâu với tab Sản phẩm, Mã giảm giá, Đơn hàng.
- 29 mục (10 + 9 + 10) thay vì 30.

### Nhận xét của người kiểm thử
- Em đưa mô tả màn hình vào thẳng prompt, thêm yêu cầu kiểm thử hộp đen và ba quy tắc: không viết sẵn Passed/Failed, mục so sánh tab khác chỉ để kiểm tra nhất quán, mục cần giả lập phải nêu cách giả lập. AI sinh 29 mục (10 + 9 + 10), mỗi mục một điểm kiểm tra và đều có cách thực hiện cụ thể.
- Hạn chế còn lại: AI vẫn thiếu checkbox tiêu đề ("chọn tất cả") vì gộp checkbox vào một mục; vài mục như AI-03-04 và AI-03-05 hơi chồng nhau; AI-01-09 và AI-01-10 nhẹ so với các mục còn lại.
- Phần AI tự nêu "chưa phủ" (responsive, accessibility, dark mode, RTL, trợ giúp, dữ liệu lớn) rất khớp với những gì bài giảng và đề bài nói AI hay bỏ sót, nên tôi sẽ dùng chính danh sách này để bổ sung ở Bước 4.