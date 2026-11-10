[BUG-21] Thuộc tính lang='en' và tiêu đề tab là tên kỹ thuật

**Mức độ:** Minor  
**Màn hình:** Admin và Web  
**Mục checklist liên quan:** GUI-001, GUI-021  
**Môi trường:** Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026

### Các bước tái hiện
1. DevTools > Elements: xem thẻ html của Admin và Web.
2. Xem tiêu đề tab trình duyệt.

### Kết quả mong đợi
lang='vi'; tiêu đề tab mang tên sản phẩm (ví dụ 'EShop Admin').

### Kết quả thực tế
lang='en'; tiêu đề tab là 'frontend-admin' và 'frontend-web'.

### Ảnh / bằng chứng
[BUG-21_lang_title_measure.txt](https://github.com/minhthang2k5/eshop-sut/blob/HW3_THMTHANG/hw03/evidence/BUG-21_lang_title_measure.txt)
