# HW02 — Phạm vi tính năng đã chọn (bản nháp để sinh viên rà soát)

## Bốn lựa chọn

| Pool | Phần việc đã chọn | Căn cứ đặc tả | Phạm vi kiểm thử ban đầu |
|---|---|---|---|
| A | FR-05 — Xem danh sách và tìm kiếm sản phẩm | `../README.md`, FR-05 | Danh sách sản phẩm trên Web, tìm theo tên, trạng thái tải/rỗng, cách hiển thị thông tin sản phẩm và từ khóa. |
| B | FR-07 — Giỏ hàng | `../README.md`, FR-07 | Hiển thị sản phẩm, điều chỉnh số lượng, cộng dồn khi thêm cùng sản phẩm, tính thành tiền/tổng tiền, xác nhận xóa, tiếp tục mua sắm và giỏ rỗng. |
| C | FR-19 — Quản lý người dùng (Admin) | `../README.md`, FR-19 | Xem danh sách người dùng mà không lộ mật khẩu; xóa người dùng khác; không cho xóa chính tài khoản Admin đang đăng nhập. Dùng FR-12 làm điều kiện truy cập cần kiểm tra khi thiết lập test. |
| D | FR-20 — Mobile: Xem sản phẩm | `../README.md`, FR-20; ảnh người dùng cung cấp | Danh sách sản phẩm, tìm kiếm theo tên và xem trang chi tiết trên Mobile, theo lựa chọn đã xác nhận của sinh viên. |

## Đầu vào và kết quả cần phân tích tiếp

| Phần việc | Đầu vào/trạng thái chính | Kết quả mong đợi cần đối chiếu |
|---|---|---|
| FR-05 | Tập sản phẩm, từ khóa tìm kiếm, trạng thái tải dữ liệu | Danh sách phù hợp, thông tin thẻ sản phẩm, trạng thái loading/empty, từ khóa hiển thị an toàn. |
| FR-07 | Sản phẩm và số lượng trong giỏ; thao tác thêm, tăng/giảm, xóa | Dòng giỏ hàng và thành tiền/tổng tiền chính xác; xác nhận trước khi xóa; giao diện giỏ rỗng. |
| FR-19 | Tài khoản Admin đang đăng nhập, người dùng mục tiêu, thao tác xem/xóa | Danh sách không chứa mật khẩu; không thể tự xóa tài khoản đang dùng. |
| FR-20 / Xem sản phẩm | Danh sách sản phẩm, từ khóa tìm kiếm, sản phẩm được chọn | Danh sách và kết quả tìm kiếm phù hợp; thông tin chi tiết sản phẩm hiển thị trên Mobile. |

## Điểm cần xác nhận trước khi lập bộ test hoàn chỉnh

1. Các thành viên trong nhóm không chọn trùng phần việc; đề yêu cầu mỗi sinh viên chọn một tính năng ở mỗi pool.
2. Pool D trong đề không tách mã FR cho từng chức năng Mobile. Ghi phần đã chọn là **FR-20 / Mobile — Xem sản phẩm**; xác nhận với nhóm hoặc TA nếu có quy tắc phân chia cụ thể.
3. FR-20 chỉ nêu tên “Xem sản phẩm”; sinh viên đã xác nhận phạm vi gồm danh sách, tìm kiếm và trang chi tiết. Khi thiết kế test Mobile, chỉ mượn quy tắc nghiệp vụ tương ứng của FR-05/FR-06 nếu chúng áp dụng cho cả hai nền tảng; không tự áp các yêu cầu riêng của Web như thẻ HTML `<h1>` lên Mobile.
4. Chưa gán mốc biên số lượng/độ dài tùy ý nếu đặc tả không định nghĩa. Các trường hợp BVA phải có biên thực sự hoặc nêu rõ điểm chưa xác định.
5. Trước khi chạy Mobile trên thiết bị/máy ảo, kiểm tra `API_URL` trong `../frontend-mobile/App.js`: mã nguồn hiện đặt IP LAN `192.168.10.13`. Điều chỉnh kết nối cho đúng môi trường chạy và ghi lại cấu hình dùng khi test; lỗi kết nối do sai IP chưa đủ để kết luận là bug chức năng.

**Trạng thái:** Đây là bản xác định phạm vi; chưa phải bộ test case, kết quả thực thi hay bug đã xác nhận. Sinh viên cần rà soát và chỉnh lại theo phân công cuối cùng của nhóm.
