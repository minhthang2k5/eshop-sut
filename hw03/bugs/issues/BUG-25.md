[BUG-25] Dữ liệu Admin chỉ tải một lần, không cập nhật khi đổi tab

**Mức độ:** Minor  
**Màn hình:** Admin: Đơn hàng, Dashboard  
**Mục checklist liên quan:** ORD-033  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Đơn hàng.
2. Dùng tài khoản khách đặt thêm một đơn (POST /api/checkout).
3. Chuyển sang tab Dashboard rồi quay lại tab Đơn hàng (không F5).

### Kết quả mong đợi
Đơn mới xuất hiện khi mở lại tab (hoặc có nút làm mới).

### Kết quả thực tế
Số dòng không đổi (vẫn 34); phải F5 mới thấy đơn mới. Dashboard cũng giữ số liệu cũ (từng hiện 35 đơn sau khi dữ liệu đã được seed lại).

### Ảnh
_(đính kèm ảnh)_  Cần chụp: số dòng trước và sau khi quay lại tab.
