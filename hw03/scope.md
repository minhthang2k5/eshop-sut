# HW03 – Phạm vi (Scope Selection)

## 1. Màn hình chính cho GUI Checklist (Task 1)

| # | Màn hình | Giao diện | Vai trò |
|---|---|---|---|
| 1 | Admin: Users | Web Admin (`frontend-admin`, tab `users`) | Màn hình chính (FR-19) |
| 2 | Admin: Categories | Web Admin (tab `categories`) | Bổ sung |
| 3 | Admin: Orders | Web Admin (tab `orders`) | Bổ sung |
| 4 | Admin: Dashboard | Web Admin (tab `dashboard`) | Bổ sung |
| 5 | Web Home (danh sách, tìm kiếm sản phẩm) | Web (`frontend-web`, `Home.jsx`) | Phụ |

## 2. Luồng Usability (Task 2)

Luồng quản trị trên Admin:
**Xem Dashboard → tạo danh mục mới (Categories) → kiểm tra trạng thái một đơn hàng (Orders) → tìm một người dùng (Users).**

- Vai participant: chủ cửa hàng online nhỏ / nhân viên vận hành.
- Tài khoản Admin do người kiểm thử cấp sẵn, participant không phải đăng nhập.
- Scenario (hướng mục tiêu): "Bạn là chủ một cửa hàng online nhỏ. Hôm nay bạn muốn nắm tình hình kinh doanh, thêm một nhóm hàng mới tên 'Phụ kiện', xem đơn hàng gần nhất đang ở trạng thái nào, và tìm xem khách hàng X đã đăng ký chưa."

## 3. Không đụng vào (dành cho thành viên khác trong nhóm)

- Web: Profile, Product Detail, Cart, Checkout, Login, Register, Forgot Password
- Admin: tab Products, tab Coupons, màn hình đăng nhập Admin
- Mobile: toàn bộ
- Mã `SAVE10` và nội dung về coupon

## 4. Nền tảng cho Task 3

Chrome, Firefox, Safari (hoặc Android Chrome) – không dùng Mobile/Expo.

## 5. Lý do chọn luồng Admin

Luồng và checklist cùng nằm trên nhóm màn hình Admin nên kết quả usability bổ sung trực tiếp cho checklist. Luồng khác hoàn toàn luồng khách mua hàng của thành viên khác trong nhóm.
