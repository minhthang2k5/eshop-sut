[BUG-06] Form Thêm danh mục không kiểm tra dữ liệu nhập

**Mức độ:** Major  
**Màn hình:** Admin: Danh mục  
**Mục checklist liên quan:** GUI-054, GUI-055, GUI-056, GUI-058, GUI-059, GUI-062  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Danh mục.
2. Để trống ô rồi bấm Thêm mới; nhập toàn dấu cách; nhập tên trùng 'Laptop' và 'laptop'; nhập 300 chữ W; nhập '  Phụ kiện mới  '.

### Kết quả mong đợi
Từ chối tên rỗng/toàn khoảng trắng/trùng tên kèm thông báo; có giới hạn độ dài; cắt khoảng trắng đầu cuối; trường bắt buộc có dấu *.

### Kết quả thực tế
Tất cả đều được lưu: dòng tên rỗng, dòng toàn dấu cách, bản sao 'Laptop', chuỗi 300 ký tự (làm bảng rộng 4631 px), tên giữ nguyên khoảng trắng thừa. Ô nhập không có dấu * hay thuộc tính required.

### Ảnh
_(đính kèm ảnh)_  Cần chụp: bảng Danh mục sau khi thêm các giá trị trên (thấy dòng rỗng và bản sao).
