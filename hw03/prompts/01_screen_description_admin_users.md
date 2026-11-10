# Prompt 1 – Mô tả màn hình và kiểm kê thành phần (Admin: Người dùng)

- **Mục đích:** Cho AI biết chính xác màn hình cần kiểm thử, rồi yêu cầu AI **kiểm kê các thành phần có thể kiểm thử** (chưa sinh checklist). Đầu ra của prompt này là nền cho Prompt 2–5.
- **Căn cứ lý thuyết:** slide GUI Testing, trang 4 (GUI chia thành các thành phần: màu sắc, font, căn lề, chính tả, ô nhập, nút, link, biểu tượng, hình ảnh, video, bảng).
- **Nguồn mô tả:** quan sát trực tiếp trên SUT (Chrome pane, khung 800×554) ngày 2026-11-10.
- **Tool AI dùng:** Claude Code (Claude Sonnet 5.5)
- **Ngày giờ chạy:** 2026-11-10 (giờ chính xác xem mục tương ứng trong `AI_Audit_Log.md` do hook ghi)
- **Lưu ý:** AI chạy prompt này trong cùng phiên đã từng đọc code SUT; yêu cầu AI chỉ dựa vào mô tả trong prompt.

---

## Prompt (dán nguyên khối vào AI)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Tôi đang kiểm thử giao diện của hệ thống EShop, một ứng dụng thương mại điện tử demo (Web Admin chạy ở localhost, tiếng Việt). Việc của bạn ở bước này CHƯA phải là viết checklist, mà là hiểu đúng màn hình và kiểm kê các thành phần có thể kiểm thử.

## Màn hình cần kiểm thử
Màn hình "Quản lý Người dùng" (tab "Người dùng") trong Web Admin.

## Mô tả quan sát được (chỉ dựa vào đây, KHÔNG tự thêm tính năng)
Bố cục chung:
- Thanh menu tối bên trái, tiêu đề "EShop Admin", các mục theo thứ tự: Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng (đang được chọn, chữ màu xanh), Đăng xuất (chữ màu đỏ).
- Vùng nội dung bên phải nền sáng, tiêu đề trang "Quản lý Người dùng".

Bảng dữ liệu (nền trắng, hàng tiêu đề nền xám), gồm 6 cột:
1. Cột checkbox: có một ô ở hàng tiêu đề và một ô ở mỗi dòng dữ liệu.
2. ID: số nguyên (hiện có 1 và 2).
3. Email: admin@eshop.com và test@eshop.com.
4. Role: "admin" và "user".
5. Số ĐT: đang hiển thị trống ở cả hai dòng.
6. Hành động: mỗi dòng có một nút "Xóa" nền đỏ, chữ trắng.

Những gì KHÔNG có trên màn hình: ô tìm kiếm, bộ lọc, sắp xếp cột, phân trang, cột Tên, nút Sửa, nút Thêm người dùng, biểu tượng nào cạnh các mục menu.
Dữ liệu hiện có: 2 người dùng (1 admin, 1 user).

## Yêu cầu
1. Nhắc lại ngắn gọn bạn hiểu màn hình này làm gì và ai là người dùng.
2. Lập bảng kiểm kê các thành phần có thể kiểm thử, nhóm theo loại: tiêu đề/văn bản, bảng và cột, checkbox, nút, menu điều hướng, màu sắc, font/căn lề, trạng thái dữ liệu (rỗng, nhiều dòng, dữ liệu dài).
   Với mỗi thành phần: tên, vị trí, hành vi/trạng thái cần kiểm tra.
3. Liệt kê các điều bạn CHƯA CHẮC hoặc cần tôi xác nhận thêm (ví dụ: bấm Xóa có hộp xác nhận không, checkbox dùng để làm gì). Không tự suy diễn.
4. Chưa viết test case hay checklist ở bước này.

Trả lời bằng tiếng Việt, dùng bảng Markdown.
```

---

## Ghi log (điền sau khi chạy)

### Output của AI

**1. Hiểu về màn hình**
Đây là trang quản trị người dùng trong Web Admin của EShop. Người dùng là quản trị viên (chủ shop/nhân viên vận hành) cần xem danh sách tài khoản (ID, email, vai trò, số điện thoại) và xóa tài khoản khi cần. Màn hình đóng vai trò xem và xóa, không có thêm hoặc sửa.

**2. Kiểm kê thành phần có thể kiểm thử**

| Nhóm | Thành phần | Vị trí | Hành vi / trạng thái cần kiểm tra |
|---|---|---|---|
| Tiêu đề, văn bản | "EShop Admin" | Đầu thanh menu trái | Đúng chính tả, font đậm, căn lề |
| | "Quản lý Người dùng" | Đầu vùng nội dung | Đúng chính tả và dấu tiếng Việt, cỡ chữ phân cấp so với bảng |
| | Tiêu đề cột: ID, Email, Role, Số ĐT, Hành động | Hàng tiêu đề bảng | Ngôn ngữ nhất quán (có cột Việt, có cột Anh: "Role" so với "Số ĐT"), căn lề với dữ liệu |
| Bảng và cột | Bảng 6 cột | Vùng nội dung | Độ rộng cột, căn lề, đường kẻ, màu nền tiêu đề so với thân bảng, tràn ngang khi cửa sổ hẹp |
| | Cột ID, Email, Role | Bảng | Hiển thị đủ dữ liệu, không bị cắt, email dài có xuống dòng hay bị tràn |
| | Cột Số ĐT | Bảng | Đang trống: kiểm tra cách hiển thị giá trị rỗng (có ký hiệu thay thế hay không) |
| Checkbox | Checkbox hàng tiêu đề | Cột đầu tiên | Trạng thái mặc định, có chọn tất cả không, nhãn truy cập (accessible name) |
| | Checkbox từng dòng | Cột đầu tiên | Bật/tắt bằng chuột và Space, kích thước vùng bấm, trạng thái focus |
| Nút | Nút "Xóa" (đỏ, chữ trắng) | Cột Hành động, mỗi dòng | Hiển thị, hover/focus, kích thước đồng nhất, độ tương phản chữ trắng trên nền đỏ, kích hoạt bằng bàn phím, phản hồi sau khi bấm |
| Điều hướng | Menu: Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng, Đăng xuất | Thanh trái | Mục đang chọn được làm nổi bật, thứ tự, hover, vào được bằng Tab, Đăng xuất màu đỏ có cần xác nhận không |
| Màu sắc | Nền menu tối, vùng nội dung sáng, chữ xanh (mục chọn), chữ đỏ (Đăng xuất), nút đỏ | Toàn trang | Độ tương phản, không dùng màu làm tín hiệu duy nhất (ví dụ phân biệt mục chọn chỉ bằng màu) |
| Font, căn lề | Cỡ chữ, độ đậm, khoảng cách dòng | Toàn trang | Nhất quán giữa menu, tiêu đề và bảng |
| Trạng thái dữ liệu | Rỗng (0 người dùng) | Bảng | Có thông báo "chưa có dữ liệu" hay chỉ hiển thị bảng trống |
| | Nhiều dòng (hàng chục, hàng trăm) | Bảng | Cuộn, hiệu năng, giữ tiêu đề cột; hiện không có phân trang |
| | Dữ liệu dài (email dài, tên vai trò lạ) | Bảng | Cắt, tràn hoặc xuống dòng |
| | Đang tải / lỗi tải | Trang | Có chỉ báo tải hoặc thông báo lỗi hay không |

**3. Điều chưa chắc, cần bạn xác nhận**
1. Bấm "Xóa" có hộp xác nhận không, và sau khi xóa có thông báo thành công/thất bại không?
2. Checkbox ở các dòng dùng để làm gì (xóa hàng loạt, chọn tất cả)? Hiện không thấy nút nào đi kèm.
3. Cột "Số ĐT" trống là vì dữ liệu chưa có hay vì lỗi hiển thị?
4. Có thể xóa chính tài khoản đang đăng nhập (admin) không, và giao diện có cảnh báo gì không?
5. Menu Dashboard, Danh mục… khi chọn có đổi địa chỉ URL không (nút Back của trình duyệt có hoạt động không)?
6. Bảng có thay đổi khi thu nhỏ cửa sổ hoặc trên màn hình nhỏ không (responsive)?
7. Có hỗ trợ bàn phím, đọc màn hình (accessibility) và chế độ tối không? Mô tả không nói đến.
8. Cột "Role" hiển thị giá trị thô ("admin", "user"), có cần nhãn tiếng Việt không?

Chưa viết test case hay checklist ở bước này.

### Nhận xét nhanh của người kiểm thử
**Điểm tốt**
- AI hiểu đúng bố cục và mục đích của màn hình (xem và xóa người dùng), nhắc lại chính xác 6 cột, thanh menu và dữ liệu hiện có.
- AI không bịa thêm tính năng ngoài phần mô tả, kể cả khi prompt chỉ liệt kê những thứ "không có" (tìm kiếm, phân trang, nút Sửa/Thêm).
- Bảng kiểm kê chia theo nhóm thành phần như slide GUI Testing, và chủ động đưa ra 8 điểm cần xác nhận. Một số điểm có giá trị thật, ví dụ nhận ra cột "Role" (tiếng Anh) và "Số ĐT" (tiếng Việt) không đồng nhất ngôn ngữ, và hỏi về việc xóa chính tài khoản admin đang đăng nhập.

**Hạn chế**
- Phần kiểm kê còn chung chung. Responsive, accessibility, chế độ tối chỉ xuất hiện như câu hỏi, không thành mục kiểm tra cụ thể.
- AI không thể biết hành vi động (bấm Xóa xảy ra gì, checkbox làm gì, nút Back), nên 8 điểm "chưa chắc" vẫn phải tự kiểm tra trên màn hình thật. Cột "Số ĐT" trống cũng chưa thể kết luận là lỗi hay thiếu dữ liệu.
- AI không phát hiện được lỗi chỉ lộ ra khi chạy thật vì nó chỉ làm việc trên mô tả chữ do tôi cung cấp.

