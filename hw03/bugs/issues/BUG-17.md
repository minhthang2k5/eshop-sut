[BUG-17] Thiếu tên truy cập, nhãn và alt cho các thành phần

**Mức độ:** Minor  
**Màn hình:** Admin và Web  
**Mục checklist liên quan:** GUI-023, GUI-029, GUI-052, GUI-077, GUI-078, ORD-018  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. Mở DevTools > Accessibility.
2. Kiểm tra nút Xóa, checkbox, ô 'Tên danh mục mới', ô tìm kiếm Home, ảnh sản phẩm, nút Hủy.

### Kết quả mong đợi
Mỗi thành phần có tên truy cập mô tả (ví dụ 'Xóa test@eshop.com', 'Hủy đơn #5'); ảnh có alt; ô nhập có nhãn.

### Kết quả thực tế
Nút chỉ có tên 'Xóa'/'Hủy'; checkbox không có nhãn; ô nhập chỉ có placeholder; cả 5 ảnh có alt rỗng.

### Ảnh
_(đính kèm ảnh)_  Cần chụp: DevTools Accessibility cho một nút Xóa.
