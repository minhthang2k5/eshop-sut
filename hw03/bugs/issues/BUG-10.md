[BUG-10] Thông báo lỗi là alert kỹ thuật tiếng Anh ('Network Error')

**Mức độ:** Minor  
**Màn hình:** Admin: Người dùng, Danh mục, Đơn hàng  
**Mục checklist liên quan:** GUI-045, GUI-067, ORD-029  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. Chặn request (DevTools > Network > Block request URL) DELETE users, POST categories hoặc PUT order status.
2. Thực hiện thao tác tương ứng.

### Kết quả mong đợi
Thông báo lỗi dễ hiểu bằng tiếng Việt, nêu nguyên nhân và cách xử lý.

### Kết quả thực tế
Hộp alert: 'Lỗi xóa: Network Error', 'Lỗi thêm DM: Network Error', 'Lỗi: Network Error'.

### Ảnh
_(đính kèm ảnh)_  Cần chụp: hộp alert lỗi.
