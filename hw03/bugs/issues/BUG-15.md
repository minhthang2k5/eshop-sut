[BUG-15] Menu không dùng được bằng bàn phím; focus bị mất sau khi đổi trạng thái đơn

**Mức độ:** Major  
**Màn hình:** Admin: toàn bộ  
**Mục checklist liên quan:** GUI-008, GUI-032, GUI-036, ORD-025  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174.
2. Nhấn Tab từ đầu trang.
3. Ctrl+click một mục menu.
4. Ở tab Đơn hàng, Tab tới nút Xác nhận rồi Enter.

### Kết quả mong đợi
Mục menu nhận focus và kích hoạt bằng Enter; là liên kết thật; focus nằm lại trong bảng sau khi đổi trạng thái.

### Kết quả thực tế
Mục menu là thẻ li không focus được, không phải liên kết; Tab nhảy thẳng vào checkbox; sau Enter focus rơi về body.

### Ảnh
_(đính kèm ảnh)_  Cần chụp: DevTools Elements hiện menu là thẻ li.
