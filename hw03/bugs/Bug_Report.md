# Bug Report – GUI & Usability (EShop)

Môi trường: Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026.

Tổng **25 bug** gom từ **77 mục Failed** của GUI Checklist. Critical: 2, Major: 12, Minor: 10, Cosmetic: 1.

| Bug | Mức độ | Màn hình | Tiêu đề | Mục checklist | Ảnh |
|---|---|---|---|---|---|
| BUG-01 | Critical | Admin: Đơn hàng | Địa chỉ giao hàng bị render thành HTML (nguy cơ XSS) | ORD-011 | evidence/BUG-01_address_bold.png; evidence/BUG-01_orders_full.jpg |
| BUG-02 | Critical | Web: Home | Tìm kiếm lộ lỗi SQL thô khi nhập dấu nháy đơn | GUI-081 | evidence/BUG-02_sql_error.jpg |
| BUG-03 | Major | Admin: Người dùng | Admin tự xóa được chính tài khoản đang đăng nhập | GUI-047 | evidence/BUG-03_before_delete_admin.jpg; evidence/BUG-03_after_delete_admin.jpg |
| BUG-04 | Major | Admin: Người dùng, Danh mục, Đơn hàng | Hành động không thể hoàn tác không có bước xác nhận | GUI-043, GUI-068, GUI-073, ORD-027 | evidence/BUG-04_no_confirm.jpg |
| BUG-05 | Major | Admin: Danh mục | Xóa được danh mục đang có sản phẩm, không cảnh báo | GUI-069 | evidence/BUG-05_laptop_deleted.jpg |
| BUG-06 | Major | Admin: Danh mục | Form Thêm danh mục không kiểm tra dữ liệu nhập | GUI-054, GUI-055, GUI-056, GUI-058, GUI-059, GUI-062 | evidence/BUG-06_invalid_categories.jpg |
| BUG-07 | Major | Admin: Đơn hàng | Đơn đã hủy vẫn có nút 'Đánh dấu Đã giao' (sai máy trạng thái FR-10) | ORD-028 | evidence/BUG-07_cancelled_row.png |
| BUG-08 | Major | Admin: Dashboard | Doanh thu trên Dashboard gấp đôi tổng các đơn Đã giao | GUI-075 | evidence/BUG-08_dashboard.jpg; evidence/BUG-07_cancelled_row.png |
| BUG-09 | Major | Admin: Người dùng, Danh mục, Đơn hàng | Không có phản hồi thành công sau khi thêm, xóa hoặc đổi trạng thái | GUI-044, GUI-064, GUI-065, ORD-026 | evidence/BUG-06_invalid_categories.jpg |
| BUG-10 | Minor | Admin: Người dùng, Danh mục, Đơn hàng | Thông báo lỗi là alert kỹ thuật tiếng Anh ('Network Error') | GUI-045, GUI-067, ORD-029 | evidence/BUG-10_console_alerts.txt |
| BUG-11 | Major | Admin: Người dùng, Đơn hàng | Không có chỉ báo đang tải và không thông báo khi tải dữ liệu lỗi | GUI-041, GUI-042, ORD-031, ORD-032 | evidence/BUG-11_no_loading.jpg |
| BUG-12 | Major | Admin: Người dùng, Danh mục, Đơn hàng | Bấm hai lần liên tiếp gửi trùng yêu cầu | GUI-046, GUI-066, ORD-030 | evidence/BUG-12_double_submit.jpg |
| BUG-13 | Minor | Admin: Đơn hàng; Web: Home | Thiếu thông báo cho trạng thái rỗng / không có kết quả | GUI-071, GUI-080 | evidence/BUG-13_orders_empty.jpg; evidence/BUG-13_home_no_result.jpg |
| BUG-14 | Major | Admin: toàn bộ | Admin không có URL theo tab: F5 về Dashboard, nút Back thoát ứng dụng | GUI-009, GUI-038, GUI-039 | evidence/BUG-14_navigation_measure.txt |
| BUG-15 | Major | Admin: toàn bộ | Menu không dùng được bằng bàn phím; focus bị mất sau khi đổi trạng thái đơn | GUI-008, GUI-032, GUI-036, ORD-025 | evidence/BUG-15_tab_focus.jpg |
| BUG-16 | Minor | Admin: Người dùng | Checkbox chọn dòng và 'chọn tất cả' không có tác dụng | GUI-024, GUI-030, GUI-048, GUI-049 | evidence/BUG-16_select_all.jpg |
| BUG-17 | Minor | Admin và Web | Thiếu tên truy cập, nhãn và alt cho các thành phần | GUI-023, GUI-029, GUI-052, GUI-077, GUI-078, ORD-018 | evidence/BUG-17_accessibility_measure.txt |
| BUG-18 | Minor | Admin và Web | Vùng bấm quá nhỏ hoặc quá sát nhau | GUI-028, GUI-079, ORD-020 | evidence/BUG-18_target_size_measure.txt |
| BUG-19 | Minor | Admin: Người dùng, Đơn hàng | Tương phản màu không đạt 4.5:1 ở nút hành động | GUI-014, ORD-004 | evidence/BUG-19_contrast_measure.txt; evidence/BUG-01_orders_full.jpg |
| BUG-20 | Major | Admin và Web | Bố cục vỡ ở màn hình hẹp (tablet, điện thoại, zoom 200%) | GUI-002, GUI-005, GUI-006, GUI-076, ORD-013, ORD-014 | evidence/BUG-20_admin_375_users.jpg; evidence/BUG-20_orders_375.jpg; evidence/BUG-20_home_375.jpg |
| BUG-21 | Minor | Admin và Web | Thuộc tính lang='en' và tiêu đề tab là tên kỹ thuật | GUI-001, GUI-021 | evidence/BUG-21_lang_title_measure.txt |
| BUG-22 | Cosmetic | Admin và Web | Không nhất quán ngôn ngữ, định dạng và kiểu giao diện | GUI-012, GUI-018, GUI-019, GUI-050, GUI-074, ORD-001, ORD-035 | evidence/BUG-22_users_table.jpg; evidence/BUG-08_dashboard.jpg |
| BUG-23 | Minor | Admin: Người dùng, Đơn hàng | Bảng thiếu thông tin và chức năng cần thiết | GUI-017, GUI-022, ORD-008, ORD-015, ORD-024 | evidence/BUG-22_users_table.jpg; evidence/BUG-01_orders_full.jpg |
| BUG-24 | Minor | Admin: Danh mục, Đơn hàng | Bảng dài không có phân trang và tiêu đề cột bị cuộn mất | GUI-051, ORD-012 | evidence/BUG-24_long_table.jpg |
| BUG-25 | Minor | Admin: Đơn hàng, Dashboard | Dữ liệu Admin chỉ tải một lần, không cập nhật khi đổi tab | ORD-033 | evidence/BUG-25_stale_data_measure.txt |

Mức độ: Critical = ảnh hưởng bảo mật hoặc chặn luồng chính; Major = sai chức năng hoặc làm người dùng mất kiểm soát; Minor = khó dùng nhưng có cách khác; Cosmetic = thẩm mỹ.

## BUG-01: Địa chỉ giao hàng bị render thành HTML (nguy cơ XSS)

- **Mức độ:** Critical
- **Màn hình:** Admin: Đơn hàng
- **Mục checklist:** ORD-011

**Các bước tái hiện**

1. Đăng nhập tài khoản khách test, gọi POST /api/checkout với shipping_address = `<b>1 Le Loi</b> & "Q1"`.
2. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Đơn hàng.
3. Xem cột Địa chỉ của đơn vừa tạo.

**Kết quả mong đợi:** Địa chỉ hiển thị nguyên văn `<b>1 Le Loi</b> & "Q1"` (đặc tả FR-18: hiển thị an toàn, không render HTML).

**Kết quả thực tế:** Chữ '1 Le Loi' hiển thị đậm; innerHTML của ô chứa thẻ `<b>`. Thẻ HTML do người dùng nhập được thực thi, có thể bị lợi dụng để chèn script.

**Ảnh:** evidence/BUG-01_address_bold.png; evidence/BUG-01_orders_full.jpg

## BUG-02: Tìm kiếm lộ lỗi SQL thô khi nhập dấu nháy đơn

- **Mức độ:** Critical
- **Màn hình:** Web: Home
- **Mục checklist:** GUI-081

**Các bước tái hiện**

1. Mở http://localhost:5173.
2. Gõ `o'` vào ô tìm kiếm rồi bấm Tìm.

**Kết quả mong đợi:** Không hiện lỗi kỹ thuật; trang trả kết quả hoặc thông báo thân thiện.

**Kết quả thực tế:** Hiện khung đỏ 'Database Error – SQLITE_ERROR: unrecognized token'. Lộ chi tiết cơ sở dữ liệu và gợi ý có thể SQL injection. Dòng 'Hiển thị 5 sản phẩm' vẫn còn bên dưới.

**Ảnh:** evidence/BUG-02_sql_error.jpg

## BUG-03: Admin tự xóa được chính tài khoản đang đăng nhập

- **Mức độ:** Major
- **Màn hình:** Admin: Người dùng
- **Mục checklist:** GUI-047

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Người dùng.
2. Bấm Xóa ở dòng admin@eshop.com.

**Kết quả mong đợi:** Hệ thống chặn và báo rõ; admin không thể tự xóa mình.

**Kết quả thực tế:** Dòng admin bị xóa ngay, không xác nhận, không cảnh báo; sau đó admin không đăng nhập lại được.

**Ảnh:** evidence/BUG-03_before_delete_admin.jpg; evidence/BUG-03_after_delete_admin.jpg

## BUG-04: Hành động không thể hoàn tác không có bước xác nhận

- **Mức độ:** Major
- **Màn hình:** Admin: Người dùng, Danh mục, Đơn hàng
- **Mục checklist:** GUI-043, GUI-068, GUI-073, ORD-027

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174.
2. Tab Người dùng: bấm Xóa ở một người dùng thử.
3. Tab Danh mục: bấm Xóa ở một danh mục thử.
4. Tab Đơn hàng: bấm Hủy ở đơn Chờ xác nhận; bấm Hoàn thành ở đơn Đang giao.

**Kết quả mong đợi:** Có hộp xác nhận nêu rõ đối tượng và cảnh báo không hoàn tác trước khi thực hiện.

**Kết quả thực tế:** Các thao tác được thực hiện ngay lập tức, không có xác nhận (hàm confirm không được gọi).

**Ảnh:** evidence/BUG-04_no_confirm.jpg

## BUG-05: Xóa được danh mục đang có sản phẩm, không cảnh báo

- **Mức độ:** Major
- **Màn hình:** Admin: Danh mục
- **Mục checklist:** GUI-069

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Danh mục.
2. Bấm Xóa ở danh mục 'Laptop' (đang có sản phẩm MacBook Pro M3).

**Kết quả mong đợi:** Hệ thống chặn việc xóa kèm thông báo nêu rõ danh mục đang có sản phẩm.

**Kết quả thực tế:** Danh mục bị xóa thành công, không chặn, không cảnh báo; sản phẩm vẫn tham chiếu danh mục đã xóa.

**Ảnh:** evidence/BUG-05_laptop_deleted.jpg

## BUG-06: Form Thêm danh mục không kiểm tra dữ liệu nhập

- **Mức độ:** Major
- **Màn hình:** Admin: Danh mục
- **Mục checklist:** GUI-054, GUI-055, GUI-056, GUI-058, GUI-059, GUI-062

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Danh mục.
2. Để trống ô rồi bấm Thêm mới; nhập toàn dấu cách; nhập tên trùng 'Laptop' và 'laptop'; nhập 300 chữ W; nhập '  Phụ kiện mới  '.

**Kết quả mong đợi:** Từ chối tên rỗng/toàn khoảng trắng/trùng tên kèm thông báo; có giới hạn độ dài; cắt khoảng trắng đầu cuối; trường bắt buộc có dấu *.

**Kết quả thực tế:** Tất cả đều được lưu: dòng tên rỗng, dòng toàn dấu cách, bản sao 'Laptop', chuỗi 300 ký tự (làm bảng rộng 4631 px), tên giữ nguyên khoảng trắng thừa. Ô nhập không có dấu * hay thuộc tính required.

**Ảnh:** evidence/BUG-06_invalid_categories.jpg

## BUG-07: Đơn đã hủy vẫn có nút 'Đánh dấu Đã giao' (sai máy trạng thái FR-10)

- **Mức độ:** Major
- **Màn hình:** Admin: Đơn hàng
- **Mục checklist:** ORD-028

**Các bước tái hiện**

1. Tạo một đơn rồi bấm Hủy ở tab Đơn hàng.
2. Xem cột Hành động của đơn đã hủy.

**Kết quả mong đợi:** Đơn Đã hủy là trạng thái kết thúc, không có nút chuyển trạng thái (FR-10).

**Kết quả thực tế:** Đơn Đã hủy hiện nút 'Đánh dấu Đã giao'.

**Ảnh:** evidence/BUG-07_cancelled_row.png

## BUG-08: Doanh thu trên Dashboard gấp đôi tổng các đơn Đã giao

- **Mức độ:** Major
- **Màn hình:** Admin: Dashboard
- **Mục checklist:** GUI-075

**Các bước tái hiện**

1. Tạo một đơn 500,000 ₫ và đưa đến trạng thái Đã giao.
2. Mở tab Dashboard.

**Kết quả mong đợi:** 'Tổng doanh thu' bằng tổng tiền các đơn Đã giao (500,000 ₫).

**Kết quả thực tế:** Dashboard hiện 1,000,000 ₫.

**Ảnh:** evidence/BUG-08_dashboard.jpg; evidence/BUG-07_cancelled_row.png

## BUG-09: Không có phản hồi thành công sau khi thêm, xóa hoặc đổi trạng thái

- **Mức độ:** Major
- **Màn hình:** Admin: Người dùng, Danh mục, Đơn hàng
- **Mục checklist:** GUI-044, GUI-064, GUI-065, ORD-026

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174.
2. Thêm một danh mục, xóa một người dùng thử, bấm Xác nhận ở một đơn.
3. Với bảng 165 dòng, thêm một danh mục.

**Kết quả mong đợi:** Có thông báo thành công; dòng mới được cuộn tới hoặc làm nổi bật.

**Kết quả thực tế:** Dữ liệu đổi nhưng không có thông báo nào. Với bảng dài, dòng mới nối ở cuối (khoảng 8937 px), người dùng không thấy gì xảy ra.

**Ảnh:** evidence/BUG-06_invalid_categories.jpg

## BUG-10: Thông báo lỗi là alert kỹ thuật tiếng Anh ('Network Error')

- **Mức độ:** Minor
- **Màn hình:** Admin: Người dùng, Danh mục, Đơn hàng
- **Mục checklist:** GUI-045, GUI-067, ORD-029

**Các bước tái hiện**

1. Chặn request (DevTools > Network > Block request URL) DELETE users, POST categories hoặc PUT order status.
2. Thực hiện thao tác tương ứng.

**Kết quả mong đợi:** Thông báo lỗi dễ hiểu bằng tiếng Việt, nêu nguyên nhân và cách xử lý.

**Kết quả thực tế:** Hộp alert: 'Lỗi xóa: Network Error', 'Lỗi thêm DM: Network Error', 'Lỗi: Network Error'.

**Ảnh:** evidence/BUG-10_console_alerts.txt

## BUG-11: Không có chỉ báo đang tải và không thông báo khi tải dữ liệu lỗi

- **Mức độ:** Major
- **Màn hình:** Admin: Người dùng, Đơn hàng
- **Mục checklist:** GUI-041, GUI-042, ORD-031, ORD-032

**Các bước tái hiện**

1. DevTools > Network > Slow 3G (hoặc Block request URL */api/admin/users và */api/admin/orders).
2. Tải lại trang Admin và mở tab Người dùng, Đơn hàng.

**Kết quả mong đợi:** Có chỉ báo đang tải; khi lỗi có thông báo và cách thử lại.

**Kết quả thực tế:** Chỉ thấy hàng tiêu đề bảng, không có chỉ báo tải, không có thông báo lỗi (lỗi tải bị bỏ qua im lặng).

**Ảnh:** evidence/BUG-11_no_loading.jpg

## BUG-12: Bấm hai lần liên tiếp gửi trùng yêu cầu

- **Mức độ:** Major
- **Màn hình:** Admin: Người dùng, Danh mục, Đơn hàng
- **Mục checklist:** GUI-046, GUI-066, ORD-030

**Các bước tái hiện**

1. Mở DevTools > Network.
2. Bấm Xóa (người dùng), Thêm mới (danh mục) hoặc Xác nhận (đơn) hai lần thật nhanh.

**Kết quả mong đợi:** Chỉ một yêu cầu được gửi; nút bị vô hiệu khi đang xử lý.

**Kết quả thực tế:** Gửi 2 yêu cầu DELETE, 2 yêu cầu POST (tạo 2 danh mục) hoặc 2 yêu cầu PUT.

**Ảnh:** evidence/BUG-12_double_submit.jpg

## BUG-13: Thiếu thông báo cho trạng thái rỗng / không có kết quả

- **Mức độ:** Minor
- **Màn hình:** Admin: Đơn hàng; Web: Home
- **Mục checklist:** GUI-071, GUI-080

**Các bước tái hiện**

1. Backend vừa khởi động (0 đơn): mở tab Đơn hàng.
2. Mở Web Home, tìm 'xyz123'.

**Kết quả mong đợi:** Hiện 'Chưa có đơn hàng' và 'Không tìm thấy sản phẩm phù hợp'.

**Kết quả thực tế:** Tab Đơn hàng chỉ có hàng tiêu đề; Home chỉ hiện 'Kết quả tìm kiếm cho: xyz123' và vùng trống.

**Ảnh:** evidence/BUG-13_orders_empty.jpg; evidence/BUG-13_home_no_result.jpg

## BUG-14: Admin không có URL theo tab: F5 về Dashboard, nút Back thoát ứng dụng

- **Mức độ:** Major
- **Màn hình:** Admin: toàn bộ
- **Mục checklist:** GUI-009, GUI-038, GUI-039

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Danh mục.
2. Nhấn F5.
3. Chuyển qua vài tab rồi bấm Back của trình duyệt.

**Kết quả mong đợi:** F5 giữ nguyên tab; Back quay về tab trước; URL phản ánh trang hiện tại.

**Kết quả thực tế:** URL luôn là '/'; F5 luôn về Dashboard; Back rời khỏi ứng dụng.

**Ảnh:** evidence/BUG-14_navigation_measure.txt

## BUG-15: Menu không dùng được bằng bàn phím; focus bị mất sau khi đổi trạng thái đơn

- **Mức độ:** Major
- **Màn hình:** Admin: toàn bộ
- **Mục checklist:** GUI-008, GUI-032, GUI-036, ORD-025

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174.
2. Nhấn Tab từ đầu trang.
3. Ctrl+click một mục menu.
4. Ở tab Đơn hàng, Tab tới nút Xác nhận rồi Enter.

**Kết quả mong đợi:** Mục menu nhận focus và kích hoạt bằng Enter; là liên kết thật; focus nằm lại trong bảng sau khi đổi trạng thái.

**Kết quả thực tế:** Mục menu là thẻ li không focus được, không phải liên kết; Tab nhảy thẳng vào checkbox; sau Enter focus rơi về body.

**Ảnh:** evidence/BUG-15_tab_focus.jpg

## BUG-16: Checkbox chọn dòng và 'chọn tất cả' không có tác dụng

- **Mức độ:** Minor
- **Màn hình:** Admin: Người dùng
- **Mục checklist:** GUI-024, GUI-030, GUI-048, GUI-049

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Người dùng.
2. Tick checkbox ở tiêu đề; tick một dòng.

**Kết quả mong đợi:** Checkbox tiêu đề chọn tất cả; dòng được chọn khác màu; có hành động hàng loạt; có trạng thái trung gian.

**Kết quả thực tế:** Checkbox tiêu đề chỉ tick chính nó; dòng được chọn không đổi nền; không có hành động nào đi kèm; không có trạng thái trung gian.

**Ảnh:** evidence/BUG-16_select_all.jpg

## BUG-17: Thiếu tên truy cập, nhãn và alt cho các thành phần

- **Mức độ:** Minor
- **Màn hình:** Admin và Web
- **Mục checklist:** GUI-023, GUI-029, GUI-052, GUI-077, GUI-078, ORD-018

**Các bước tái hiện**

1. Mở DevTools > Accessibility.
2. Kiểm tra nút Xóa, checkbox, ô 'Tên danh mục mới', ô tìm kiếm Home, ảnh sản phẩm, nút Hủy.

**Kết quả mong đợi:** Mỗi thành phần có tên truy cập mô tả (ví dụ 'Xóa test@eshop.com', 'Hủy đơn #5'); ảnh có alt; ô nhập có nhãn.

**Kết quả thực tế:** Nút chỉ có tên 'Xóa'/'Hủy'; checkbox không có nhãn; ô nhập chỉ có placeholder; cả 5 ảnh có alt rỗng.

**Ảnh:** evidence/BUG-17_accessibility_measure.txt

## BUG-18: Vùng bấm quá nhỏ hoặc quá sát nhau

- **Mức độ:** Minor
- **Màn hình:** Admin và Web
- **Mục checklist:** GUI-028, GUI-079, ORD-020

**Các bước tái hiện**

1. Đo bằng DevTools: checkbox, nút 'Thêm vào giỏ'/'Xem chi tiết' ở 375 px, khoảng cách giữa nút Xác nhận và Hủy.

**Kết quả mong đợi:** Vùng bấm tối thiểu 24×24 px (44 px trên cảm ứng); hai nút cách nhau tối thiểu 8 px.

**Kết quả thực tế:** Checkbox 13×13 px; nút Home cao 36 px; hai nút trong ô Hành động cách nhau 4 px.

**Ảnh:** evidence/BUG-18_target_size_measure.txt

## BUG-19: Tương phản màu không đạt 4.5:1 ở nút hành động

- **Mức độ:** Minor
- **Màn hình:** Admin: Người dùng, Đơn hàng
- **Mục checklist:** GUI-014, ORD-004

**Các bước tái hiện**

1. Đo tương phản chữ/nền bằng DevTools hoặc WebAIM Contrast Checker.

**Kết quả mong đợi:** Mọi cặp màu đạt tối thiểu 4.5:1.

**Kết quả thực tế:** Nút Xóa 3.76:1; Xác nhận 4.47:1; Hủy 2.54:1; Giao hàng 3.68:1; Hoàn thành và Đánh dấu Đã giao 2.28:1.

**Ảnh:** evidence/BUG-19_contrast_measure.txt; evidence/BUG-01_orders_full.jpg

## BUG-20: Bố cục vỡ ở màn hình hẹp (tablet, điện thoại, zoom 200%)

- **Mức độ:** Major
- **Màn hình:** Admin và Web
- **Mục checklist:** GUI-002, GUI-005, GUI-006, GUI-076, ORD-013, ORD-014

**Các bước tái hiện**

1. Đặt độ rộng cửa sổ 375 px (hoặc 768 px, hoặc zoom 200%).
2. Mở tab Người dùng, Đơn hàng của Admin và trang Home.

**Kết quả mong đợi:** Bảng nằm gọn; vùng nội dung chiếm ít nhất 70% chiều rộng; tiêu đề không bẻ quá 2 dòng; nhãn nút không bẻ nhiều dòng.

**Kết quả thực tế:** Ở 375 px menu chiếm 256 px, vùng nội dung chỉ 119 px (32%), tiêu đề bẻ 4 dòng, bảng phải cuộn ngang, nút 'Đánh dấu Đã giao' cao 72 px; Home: tiêu đề rộng 80 px, bẻ 4 dòng. Ở 768 px bảng Người dùng rộng 813 px > 512 px.

**Ảnh:** evidence/BUG-20_admin_375_users.jpg; evidence/BUG-20_orders_375.jpg; evidence/BUG-20_home_375.jpg

## BUG-21: Thuộc tính lang='en' và tiêu đề tab là tên kỹ thuật

- **Mức độ:** Minor
- **Màn hình:** Admin và Web
- **Mục checklist:** GUI-001, GUI-021

**Các bước tái hiện**

1. DevTools > Elements: xem thẻ html của Admin và Web.
2. Xem tiêu đề tab trình duyệt.

**Kết quả mong đợi:** lang='vi'; tiêu đề tab mang tên sản phẩm (ví dụ 'EShop Admin').

**Kết quả thực tế:** lang='en'; tiêu đề tab là 'frontend-admin' và 'frontend-web'.

**Ảnh:** evidence/BUG-21_lang_title_measure.txt

## BUG-22: Không nhất quán ngôn ngữ, định dạng và kiểu giao diện

- **Mức độ:** Cosmetic
- **Màn hình:** Admin và Web
- **Mục checklist:** GUI-012, GUI-018, GUI-019, GUI-050, GUI-074, ORD-001, ORD-035

**Các bước tái hiện**

1. So sánh nhãn, định dạng tiền, định dạng ID và nút giữa các tab và giữa Admin với Home.

**Kết quả mong đợi:** Cùng ngôn ngữ, đơn vị tiền, định dạng ID, kiểu nút; số tiền căn phải; tên nút khớp tên trạng thái đích.

**Kết quả thực tế:** Trộn 'Role', 'Dashboard', '(Delivered)'; Admin dùng '₫', Home dùng 'VND'; ID '#1' ở Danh mục nhưng '1' ở Người dùng; 'Tên Danh Mục' khác 'Tên danh mục mới'; nút Xóa kích thước khác nhau và không đổi màu khi hover; số tiền căn trái; nút 'Hoàn thành' đưa đơn sang 'Đã giao'.

**Ảnh:** evidence/BUG-22_users_table.jpg; evidence/BUG-08_dashboard.jpg

## BUG-23: Bảng thiếu thông tin và chức năng cần thiết

- **Mức độ:** Minor
- **Màn hình:** Admin: Người dùng, Đơn hàng
- **Mục checklist:** GUI-017, GUI-022, ORD-008, ORD-015, ORD-024

**Các bước tái hiện**

1. Mở tab Người dùng và tab Đơn hàng.

**Kết quả mong đợi:** Người dùng: có cột Tên, số điện thoại hiển thị, có ô tìm kiếm. Đơn hàng: có thời gian đặt, email người đặt, cách xem chi tiết đơn.

**Kết quả thực tế:** Cột Số ĐT luôn trống; không có cột Tên, không có ô tìm kiếm; Đơn hàng không có ngày đặt, hai khách cùng tên 'Test User' không phân biệt được, không xem được chi tiết đơn. (Các ý về Đơn hàng là đề xuất cải tiến, đặc tả không nêu.)

**Ảnh:** evidence/BUG-22_users_table.jpg; evidence/BUG-01_orders_full.jpg

## BUG-24: Bảng dài không có phân trang và tiêu đề cột bị cuộn mất

- **Mức độ:** Minor
- **Màn hình:** Admin: Danh mục, Đơn hàng
- **Mục checklist:** GUI-051, ORD-012

**Các bước tái hiện**

1. Tạo 165 danh mục (hoặc 34 đơn), cuộn bảng xuống cuối.

**Kết quả mong đợi:** Có phân trang hoặc tiêu đề cột luôn nhìn thấy khi cuộn.

**Kết quả thực tế:** Không phân trang; tiêu đề cột cuộn ra ngoài màn hình (top −8063 px); trang cao 8970 px.

**Ảnh:** evidence/BUG-24_long_table.jpg

## BUG-25: Dữ liệu Admin chỉ tải một lần, không cập nhật khi đổi tab

- **Mức độ:** Minor
- **Màn hình:** Admin: Đơn hàng, Dashboard
- **Mục checklist:** ORD-033

**Các bước tái hiện**

1. Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174, mở tab Đơn hàng.
2. Dùng tài khoản khách đặt thêm một đơn (POST /api/checkout).
3. Chuyển sang tab Dashboard rồi quay lại tab Đơn hàng (không F5).

**Kết quả mong đợi:** Đơn mới xuất hiện khi mở lại tab (hoặc có nút làm mới).

**Kết quả thực tế:** Số dòng không đổi (vẫn 34); phải F5 mới thấy đơn mới. Dashboard cũng giữ số liệu cũ (từng hiện 35 đơn sau khi dữ liệu đã được seed lại).

**Ảnh:** evidence/BUG-25_stale_data_measure.txt
