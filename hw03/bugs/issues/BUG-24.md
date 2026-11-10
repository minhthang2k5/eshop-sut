[BUG-24] Bảng dài không có phân trang và tiêu đề cột bị cuộn mất

**Mức độ:** Minor  
**Màn hình:** Admin: Danh mục, Đơn hàng  
**Mục checklist liên quan:** GUI-051, ORD-012  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. Tạo 165 danh mục (hoặc 34 đơn), cuộn bảng xuống cuối.

### Kết quả mong đợi
Có phân trang hoặc tiêu đề cột luôn nhìn thấy khi cuộn.

### Kết quả thực tế
Không phân trang; tiêu đề cột cuộn ra ngoài màn hình (top −8063 px); trang cao 8970 px.

### Ảnh
_(đính kèm ảnh)_  Cần chụp: cuối bảng dài không còn thấy tiêu đề.
