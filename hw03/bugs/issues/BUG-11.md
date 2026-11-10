[BUG-11] Không có chỉ báo đang tải và không thông báo khi tải dữ liệu lỗi

**Mức độ:** Major  
**Màn hình:** Admin: Người dùng, Đơn hàng  
**Mục checklist liên quan:** GUI-041, GUI-042, ORD-031, ORD-032  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. DevTools > Network > Slow 3G (hoặc Block request URL */api/admin/users và */api/admin/orders).
2. Tải lại trang Admin và mở tab Người dùng, Đơn hàng.

### Kết quả mong đợi
Có chỉ báo đang tải; khi lỗi có thông báo và cách thử lại.

### Kết quả thực tế
Chỉ thấy hàng tiêu đề bảng, không có chỉ báo tải, không có thông báo lỗi (lỗi tải bị bỏ qua im lặng).

### Ảnh
_(đính kèm ảnh)_  Cần chụp: bảng chỉ có hàng tiêu đề khi mạng chậm hoặc bị chặn.
