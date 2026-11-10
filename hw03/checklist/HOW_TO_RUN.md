# Cách chạy lại dự án để thực thi GUI Checklist

Các file trong thư mục này:

| File | Nội dung |
|---|---|
| `GUI_Checklist_final.md` / `.csv` | Checklist cuối, 81 mục (55 từ AI, 26 tự thêm). Cột Kết quả, Notes, Screenshot để trống |
| `AI_Review_Decisions.md` | Quyết định giữ / sửa / tách / gộp / bỏ cho từng mục trong 61 mục AI, có lý do và ID mới |
| `Added_Items_AI_Gaps.md` | Bảng "Mục bổ sung và lý do AI bỏ sót" để đưa vào báo cáo, kèm nhận xét cho phần AI Critique |
| `GUI_Checklist_draft.*` | Bản nháp AI gốc (giữ nguyên để truy vết) |

Nếu muốn đổi một quyết định hoặc một mục, sửa `hw03/scripts/build_final_checklist.py` (biến `DEC` và `NEW`) rồi dựng lại:

```bash
python hw03/scripts/build_final_checklist.py
```

## 1. Khởi động (3 terminal, đứng ở thư mục `eshop-sut`)

```bash
node backend/server.js
```

```bash
npm --prefix frontend-admin run dev
```

```bash
npm --prefix frontend-web run dev
```

- Backend: http://localhost:3000. Admin: cổng Vite in ra (thường là http://localhost:5174). Web: http://localhost:5173.
- Lần đầu chạy `frontend-web` cần `npm install` trong thư mục đó.
- Tài khoản admin (từ seed trong `backend/database.js`): `admin@eshop.com` / `Admin123!`. Tài khoản khách: `test@eshop.com` / `Test1234!`.

## 2. Ba điểm cần biết trước khi test

1. **Mỗi lần khởi động backend, toàn bộ DB bị xóa và seed lại** (`database.js` chạy `DROP TABLE` khi được nạp). Vì vậy:
   - Không tắt/bật backend để giả lập lỗi mạng (các mục nháp D-035, D-040, D-058 đã được sửa sang chặn request bằng DevTools).
   - Muốn reset dữ liệu sạch sau khi test thì chỉ cần khởi động lại backend.
   - Nếu đang có dữ liệu cần giữ, chép `backend/database.sqlite` ra chỗ khác trước.
   - Chạy hai backend cùng lúc cũng gây seed lại (tiến trình thứ hai không mở được cổng 3000 nhưng vẫn kịp reset DB).
2. **Khóa tài khoản rất nhanh**: mỗi lần sai mật khẩu bị cộng 2, đủ 3 thì khóa 3 phút, nên chỉ cần 2 lần nhập sai. Mở khóa:
   ```bash
   node hw03/scripts/unlock_admin.js
   ```
3. **Không có URL theo tab**: Admin luôn ở `/`, F5 quay về Dashboard. Sau mỗi lần tải lại cần bấm lại tab đang test.

## 3. Chuẩn bị dữ liệu cho từng nhóm mục

| Nhóm mục | Cách chuẩn bị |
|---|---|
| Lỗi tải / lỗi xóa / lỗi thêm | DevTools > Network > chuột phải request > **Block request URL**, xong thì bỏ chặn |
| Mạng chậm | DevTools > Network > Throttling **Slow 3G** |
| Email dài | `POST http://localhost:3000/api/register` với body `{"name":"Long","email":"<60 ký tự>@example.com","password":"Test1234!"}` |
| Bảng hàng trăm dòng | `node hw03/scripts/seed_bulk_categories.js add 150`, test xong chạy `node hw03/scripts/seed_bulk_categories.js clean` |
| Xóa danh mục có sản phẩm | Dùng danh mục seed "Laptop" (đang có MacBook Pro M3); khởi động lại backend để khôi phục |
| Đơn hàng nhiều trạng thái, doanh thu | Đăng nhập Web bằng `test@eshop.com`, thêm sản phẩm vào giỏ, Checkout; vào Admin > Đơn hàng để đổi trạng thái |
| Trạng thái rỗng | Backend vừa khởi động: tab Đơn hàng có sẵn 0 đơn |
| Responsive | DevTools > Device Toolbar: 375×812 (điện thoại), 768×1024 (tablet) |
| Dark mode | DevTools > More tools > Rendering > `prefers-color-scheme: dark` |
| RTL | DevTools > Elements, thêm `dir="rtl"` vào thẻ `<html>` |
| Zoom | Ctrl + + tới 200% ở cửa sổ 1280 px |
| Tương phản, tên truy cập | DevTools > Elements > Accessibility pane (Computed name), hoặc tiện ích axe DevTools |
| Trình đọc màn hình | NVDA (miễn phí) hoặc Windows Narrator (Ctrl + Win + Enter) |

## 4. Ghi kết quả

Mở `GUI_Checklist_final.csv` bằng Excel/Google Sheets, điền cột **Kết quả (Passed/Failed)**, **Notes** và đường dẫn ảnh ở **Screenshot**. Các mục có nguồn "Tự thêm – quan sát thật" đã được thử sơ bộ ngày 10/11/2026 (chi tiết ở cột "Vì sao AI bỏ sót"), nhưng vẫn cần chạy lại và chụp ảnh làm bằng chứng.
