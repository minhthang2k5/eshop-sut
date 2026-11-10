# Prompt 7 – Mục theo nguyên tắc thiết kế (IA-01, IA-03, IA-04) – Admin: Đơn hàng

> Chạy bằng skill `gui-checklist` (bước 3).

- **Căn cứ lý thuyết:** slide GUI Testing, trang 6–9 (Nielsen 10, Norman 6, Shneiderman 8 → bảng review có Mandatory/Optional).
- **Tool AI dùng:** Claude Code (Claude Sonnet 5.5), ngày 2026-11-10.
- **Lưu ý:** phiên này đã đọc mã nguồn SUT trước đó; prompt yêu cầu chỉ dựa vào mô tả.
- **Ý đã phủ ở màn hình khác (không lặp):** khung chung của Admin (menu và Đăng xuất, nút Back, F5 giữ tab, `lang`, dark mode, RTL, zoom, responsive chung, tiêu đề tab), mục trạng thái rỗng, xác nhận khi Hủy, nút Đã hủy → Đã giao, doanh thu Dashboard đã nằm trong checklist hiện có (các mục GUI-070 đến GUI-075).

---

## Prompt (dán nguyên khối vào AI; tự chứa đủ ngữ cảnh)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Kiểm thử HỘP ĐEN: chỉ dựa vào mô tả dưới đây, KHÔNG đọc mã nguồn.

## Màn hình: "Quản lý Đơn hàng" (tab "Đơn hàng", Web Admin EShop, tiếng Việt)
- Menu tối bên trái (Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng, Đăng xuất); vùng nội dung nền sáng, tiêu đề "Quản lý Đơn hàng".
- Bảng 6 cột: ID (#5, #4...), Người đặt, Tổng tiền (150,000 ₫...), Địa chỉ, Trạng thái (nhãn chữ có màu nền), Hành động (các nút nhỏ xếp dọc).
- Có 5 đơn thử, ID giảm dần, đủ 5 trạng thái: Chờ xác nhận (nút Xác nhận, Hủy), Đã xác nhận (Giao hàng, Hủy), Đang giao (Hoàn thành), Đã hủy (Đánh dấu Đã giao), Đã giao (không nút).
- KHÔNG có: tìm kiếm, lọc, sắp xếp, phân trang, cột ngày đặt, email người đặt, nút xem chi tiết, ô nhập liệu.
- Đặc tả: pending → confirmed → shipping → delivered; pending và confirmed có thể canceled; delivered và canceled là trạng thái kết thúc; địa chỉ phải hiển thị an toàn (không render HTML).

## Các ý ĐÃ phủ ở màn hình khác (KHÔNG lặp)
Menu và Đăng xuất; nút Back; F5 giữ tab; lang; dark mode; RTL; zoom; responsive chung; tiêu đề tab; trạng thái rỗng; xác nhận khi Hủy đơn; đơn đã hủy có nút Đã giao; số liệu doanh thu Dashboard; nhãn tiền ₫ so với VND.

## Nhiệm vụ
Sinh MỤC CHECKLIST cho IA-01 (chuẩn UI chung), IA-03 (điều hướng), IA-04 (phản hồi/trạng thái) CHỈ cho màn hình này. Mỗi mục bám ít nhất một nguyên tắc: Nielsen 10 (Visibility of system status, Match system and real world, User control and freedom, Consistency and standards, Error prevention, Recognition rather than recall, Flexibility and efficiency, Aesthetic and minimalist design, Help recognize/diagnose/recover from errors, Help and documentation), Norman 6 (Visibility, Feedback, Affordance, Mapping, Constraints, Consistency), Shneiderman 8, hoặc WCAG.

## Quy tắc
- Mỗi mục MỘT điểm kiểm tra, thực hiện được vài phút, có Passed/Failed.
- Kết quả mong đợi có MỘT tiêu chí đo được; tránh "hoặc", "nếu... thì", "dễ hiểu" không ngưỡng. KHÔNG viết sẵn kết luận Passed/Failed.
- Nêu cách thực hiện cụ thể (chuỗi thử, công cụ, ngưỡng). Mục cần giả lập phải ghi cách giả lập; ưu tiên chặn request bằng DevTools, KHÔNG tắt backend (khởi động lại sẽ seed lại dữ liệu).
- Không bịa tính năng. Với thứ không có, chỉ sinh mục nếu việc thiếu nó là vấn đề đáng kiểm tra và ghi rõ "đặc tả không nêu".
- IA-01 khoảng 8–10 mục, IA-03 khoảng 4–6, IA-04 khoảng 8–10.

## Định dạng
Bảng Markdown: | ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên (Mandatory/Optional) |
ID dạng O7-01, O7-02... Cuối bảng: nêu khía cạnh còn CHƯA phủ.
Trả lời tiếng Việt.
```

---

## Ghi log

### Output của AI

| ID tạm | IA | Nguyên tắc nguồn | Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| O7-01 | IA-01 | Nielsen #4 Consistency and standards | Cột Tổng tiền | Quan sát cột Tổng tiền ở cả 5 đơn thử | Mọi dòng cùng định dạng: dấu phân cách hàng nghìn và ký hiệu ₫; số thẳng hàng theo chữ số (căn phải) | Mandatory |
| O7-02 | IA-01 | Norman Visibility; WCAG 1.4.1 Use of Color | Nhãn trạng thái | Quan sát 5 nhãn Chờ xác nhận, Đã xác nhận, Đang giao, Đã hủy, Đã giao | Mỗi trạng thái có chữ riêng và màu nền riêng; vẫn phân biệt được khi xem ở thang xám nhờ chữ | Mandatory |
| O7-03 | IA-01 | WCAG 1.4.3 Contrast; Nielsen #8 | Nhãn trạng thái | Đo tương phản chữ/nền của từng nhãn trong 5 trạng thái bằng DevTools hoặc WebAIM Contrast Checker | Mọi nhãn đạt tỉ lệ tương phản ≥ 4.5:1 | Mandatory |
| O7-04 | IA-01 | WCAG 1.4.3 Contrast | Nút hành động | Đo tương phản chữ trắng trên nền của các nút Xác nhận, Hủy, Giao hàng, Hoàn thành, Đánh dấu Đã giao | Mọi nút đạt tỉ lệ ≥ 4.5:1 | Mandatory |
| O7-05 | IA-01 | Shneiderman #1; Norman Consistency | Nút hành động | So sánh cỡ chữ, chiều cao, bo góc của các nút hành động giữa các dòng (DevTools) | Mọi nút cùng cỡ chữ, bo góc và chiều cao | Optional |
| O7-06 | IA-01 | Norman Affordance; slide Button (màu thể hiện ý nghĩa) | Màu nút | So sánh màu nút Hủy với các nút tiếp tục luồng (Xác nhận, Giao hàng, Hoàn thành) | Nút hủy dùng màu cảnh báo (đỏ), khác màu các nút tiếp tục luồng | Optional |
| O7-07 | IA-01 | Nielsen #8 Aesthetic and minimalist design | Căn lề bảng | Quan sát căn lề tiêu đề cột so với dữ liệu và cách xếp nút trong cột Hành động | Tiêu đề và dữ liệu cùng cột thẳng hàng; các nút trong cột Hành động xếp đều, không lệch | Mandatory |
| O7-08 | IA-01 | Nielsen #8 | Cột Địa chỉ | Tạo đơn có địa chỉ dài (khoảng 150 ký tự) bằng POST /api/checkout rồi quan sát cột Địa chỉ | Địa chỉ xuống dòng trong ô, không tràn khỏi bảng, không đè cột bên cạnh | Mandatory |
| O7-09 | IA-01 | Nielsen #6 Recognition rather than recall | Bảng đơn hàng | Xem các cột hiển thị cho một đơn | Có cột thời gian đặt hàng để phân biệt đơn mới và cũ (đặc tả không nêu; ghi nhận thiếu nếu không có) | Optional |
| O7-10 | IA-01 | Nielsen #4 Consistency | Thứ tự dòng | Ghi thứ tự ID các dòng, đổi trạng thái một đơn rồi quan sát lại | Thứ tự dòng không đổi sau khi đổi trạng thái | Mandatory |
| O7-11 | IA-03 | Nielsen #1 Visibility of system status | Mục menu "Đơn hàng" | Bấm "Đơn hàng" trên menu | Mục menu được nổi bật và trang có tiêu đề "Quản lý Đơn hàng" | Mandatory |
| O7-12 | IA-03 | Nielsen #3 User control and freedom; Nielsen #7 | Sau khi đổi trạng thái | Bấm "Xác nhận" ở một đơn thử rồi quan sát tab đang hiển thị và vị trí cuộn | Vẫn ở tab Đơn hàng, vị trí cuộn không nhảy về đầu bảng | Mandatory |
| O7-13 | IA-03 | WCAG 2.4.3 Focus Order; Nielsen #7 | Nút hành động | Nhấn Tab liên tục trong bảng | Focus đi qua các nút theo thứ tự trên xuống dưới; mỗi nút có viền focus nhìn thấy | Mandatory |
| O7-14 | IA-03 | Nielsen #7 Flexibility; Shneiderman #8 | Chi tiết đơn | Tìm cách xem chi tiết một đơn (sản phẩm, số lượng) từ dòng đơn hàng | Có cách mở chi tiết đơn từ dòng đó (đặc tả không nêu; ghi nhận thiếu nếu không có) | Optional |
| O7-15 | IA-04 | Nielsen #1; Shneiderman #3 Informative feedback | Xác nhận đơn thành công | Bấm "Xác nhận" ở đơn Chờ xác nhận | Có thông báo thành công; nhãn đổi thành "Đã xác nhận" và nút đổi sang Giao hàng, Hủy ngay không cần tải lại | Mandatory |
| O7-16 | IA-04 | Nielsen #5 Error prevention; Shneiderman #6 | Chuyển sang Đã giao | Bấm "Hoàn thành" ở đơn Đang giao (dùng đơn thử) | Có bước xác nhận trước khi chuyển sang trạng thái kết thúc không hoàn tác | Mandatory |
| O7-17 | IA-04 | Shneiderman #4 Closure; FR-10 | Đơn Đã giao | Quan sát cột Hành động của đơn Đã giao | Đơn Đã giao không có nút chuyển trạng thái (trạng thái kết thúc theo FR-10) | Mandatory |
| O7-18 | IA-04 | Nielsen #9; Shneiderman #5 | Lỗi đổi trạng thái | DevTools > Network > Block request URL "*/api/admin/orders/*" rồi bấm "Xác nhận" | Có thông báo lỗi dễ hiểu; nhãn trạng thái không đổi sai | Mandatory |
| O7-19 | IA-04 | Nielsen #5; Norman Constraints | Bấm nút liên tiếp | Mở DevTools > Network, bấm "Xác nhận" hai lần liên tiếp thật nhanh trên cùng một đơn | Chỉ một yêu cầu PUT được gửi; đơn chỉ chuyển một bước | Mandatory |
| O7-20 | IA-04 | Nielsen #1 | Đang tải | DevTools > Network > Slow 3G rồi mở tab Đơn hàng | Có chỉ báo đang tải; không hiện bảng chỉ có hàng tiêu đề gây hiểu nhầm là chưa có đơn | Mandatory |
| O7-21 | IA-04 | Nielsen #9 | Lỗi tải danh sách | DevTools > Block request URL "*/api/admin/orders", tải lại rồi mở tab Đơn hàng | Có thông báo lỗi tải dễ hiểu | Mandatory |
| O7-22 | IA-04 | Nielsen #1 | Dữ liệu cập nhật | Tạo đơn mới bằng tài khoản khách (không F5 admin), bấm lại tab Đơn hàng | Đơn mới xuất hiện khi mở lại tab | Optional |
| O7-23 | IA-04 | Nielsen #4; Norman Feedback | Tổng số đơn | So "Tổng số đơn hàng" ở Dashboard với số dòng ở tab Đơn hàng | Hai con số bằng nhau | Mandatory |
| O7-24 | IA-04 | Nielsen #5 Error prevention; FR-10 | Nút theo trạng thái | Với từng trạng thái, ghi các nút hiển thị | Chờ xác nhận: Xác nhận, Hủy; Đã xác nhận: Giao hàng, Hủy; Đang giao: Hoàn thành; Đã hủy và Đã giao: không có nút chuyển trạng thái | Mandatory |

**Khía cạnh chưa phủ:** accessibility sâu (tên truy cập của nút, trình đọc màn hình), vùng chạm trên cảm ứng, bảng nhiều đơn (cuộn, tiêu đề cố định), ký tự đặc biệt trong địa chỉ (đưa sang prompt theo control).

### Nhận xét của người kiểm thử
_(mục nào tốt, mục nào mơ hồ hoặc trùng ý với màn hình khác?)_
