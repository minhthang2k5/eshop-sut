# Review 34 mục AI sinh – Admin: Đơn hàng

Thống kê: Giữ: 26, Sửa: 2, Gộp: 1, Gộp vào: 1, Bỏ: 4.  
34 mục nháp → 29 mục AI trong checklist cuối (4 bỏ, 1 gộp vào mục khác).

| ID nháp | Nguồn AI | Mục (tóm tắt) | Quyết định | Lý do | ID mới |
|---|---|---|---|---|---|
| DO-001 | 07_heuristics_admin_orders – O7-01 | Cột Tổng tiền: Quan sát cột Tổng tiền ở cả 5 đơn thử | Giữ | Đo được, Pass/Fail rõ. | ORD-001 |
| DO-002 | 07_heuristics_admin_orders – O7-02 | Nhãn trạng thái: Quan sát 5 nhãn Chờ xác nhận, Đã xác nhận, Đang giao, Đã hủy, Đã giao | Giữ | Rõ ràng. Lưu ý: trùng ý với mục GUI-070 của checklist chính; khi gộp hai checklist chỉ giữ một mục. | ORD-002 |
| DO-003 | 07_heuristics_admin_orders – O7-03 | Nhãn trạng thái: Đo tương phản chữ/nền của từng nhãn trong 5 trạng thái bằng DevTools h… | Giữ | Đo được bằng công cụ, có ngưỡng 4.5:1. | ORD-003 |
| DO-004 | 07_heuristics_admin_orders – O7-04 | Nút hành động: Đo tương phản chữ trắng trên nền của các nút Xác nhận, Hủy, Giao hàng,… | Giữ | Đo được bằng công cụ, có ngưỡng 4.5:1. | ORD-004 |
| DO-005 | 07_heuristics_admin_orders – O7-05 | Nút hành động: So sánh cỡ chữ, chiều cao, bo góc của các nút hành động giữa các dòng … | Giữ | Đo được bằng DevTools. | ORD-005 |
| DO-006 | 07_heuristics_admin_orders – O7-06 | Màu nút: So sánh màu nút Hủy với các nút tiếp tục luồng (Xác nhận, Giao hàng, H… | Bỏ | Chủ quan: đặc tả không quy định màu nút Hủy; 'nút hủy phải đỏ' chỉ là quy ước chung nên không có tiêu chí Pass/Fail khách quan. | — |
| DO-007 | 07_heuristics_admin_orders – O7-07 | Căn lề bảng: Quan sát căn lề tiêu đề cột so với dữ liệu và cách xếp nút trong cột H… | Giữ | Quan sát trực tiếp, Pass/Fail rõ. | ORD-006 |
| DO-008 | 07_heuristics_admin_orders – O7-08 | Cột Địa chỉ: Tạo đơn có địa chỉ dài (khoảng 150 ký tự) bằng POST /api/checkout rồi … | Giữ | Có cách tạo dữ liệu (POST /api/checkout), tiêu chí rõ. | ORD-007 |
| DO-009 | 07_heuristics_admin_orders – O7-09 | Bảng đơn hàng: Xem các cột hiển thị cho một đơn | Sửa | Mục đòi hỏi tính năng mà đặc tả FR-18 không nêu; bỏ nhánh 'ghi nhận thiếu nếu không có' và gắn rõ là yêu cầu bổ sung để có một tiêu chí. | ORD-008 |
| DO-010 | 07_heuristics_admin_orders – O7-10 | Thứ tự dòng: Ghi thứ tự ID các dòng, đổi trạng thái một đơn rồi quan sát lại | Giữ | Rõ ràng. | ORD-009 |
| DO-011 | 08_per_control_admin_orders – O8-06 | Bảng: So số dòng trên bảng với kết quả GET /api/admin/orders | Giữ | Đối chiếu được với API. | ORD-010 |
| DO-012 | 08_per_control_admin_orders – O8-07 | Cột Địa chỉ: Tạo đơn có địa chỉ `<b>1 Le Loi</b> & "Q1"` bằng POST /api/checkout rồ… | Giữ | Có căn cứ trong đặc tả FR-18 (địa chỉ hiển thị an toàn, không render HTML). | ORD-011 |
| DO-013 | 08_per_control_admin_orders – O8-08 | Bảng: Tạo 30 đơn thử bằng API, cuộn bảng xuống cuối | Giữ | Cần tạo 30 đơn bằng API (làm được); tiêu chí rõ. | ORD-012 |
| DO-014 | 08_per_control_admin_orders – O8-09 | Dòng đơn hàng: Nhấp đúp vào một dòng đơn hàng | Bỏ | Yếu: đặc tả không quy định hành vi nhấp đúp; kết quả 'không có thay đổi bất ngờ' không có ngưỡng Pass/Fail. | — |
| DO-015 | 08_per_control_admin_orders – O8-10 | Dòng đơn hàng: Rê chuột và nhấp vào một dòng, quan sát nền dòng | Bỏ | Yếu: hiệu ứng hover dòng không thuộc đặc tả và giá trị thấp. | — |
| DO-016 | 08_per_control_admin_orders – O8-01 | Nút hành động: Nhấn Tab tới nút "Xác nhận" của đơn thử #5 rồi nhấn Enter; làm lại với… | Giữ | Rõ ràng; dùng đơn thử nên an toàn. | ORD-017 |
| DO-017 | 08_per_control_admin_orders – O8-02 | Nút hành động: Rê chuột lên từng loại nút hành động | Bỏ | Yếu: hiệu ứng hover nút không có tiêu chí khách quan, giá trị thấp so với các mục khác. | — |
| DO-018 | 08_per_control_admin_orders – O8-03 | Nút "Hủy": Mở DevTools > Accessibility, chọn nút "Hủy" của hai đơn khác nhau, đọc… | Giữ | Đo được bằng DevTools > Accessibility. | ORD-018 |
| DO-019 | 08_per_control_admin_orders – O8-04 | Nút hành động: Đo chiều cao và chiều rộng các nút bằng DevTools (box model) | Giữ | Đo được, có ngưỡng 24×24 px (WCAG 2.5.8). | ORD-019 |
| DO-020 | 08_per_control_admin_orders – O8-05 | Hai nút xếp dọc: Đo khoảng cách giữa nút "Xác nhận" và "Hủy" trong cùng một ô | Giữ | Đo được, có ngưỡng khoảng cách. | ORD-020 |
| DO-021 | 07_heuristics_admin_orders – O7-11 | Mục menu "Đơn hàng": Bấm "Đơn hàng" trên menu | Giữ | Rõ ràng. | ORD-021 |
| DO-022 | 07_heuristics_admin_orders – O7-12 | Sau khi đổi trạng thái: Bấm "Xác nhận" ở một đơn thử rồi quan sát tab đang hiển thị và vị trí … | Giữ | Rõ ràng. | ORD-022 |
| DO-023 | 07_heuristics_admin_orders – O7-13 | Nút hành động: Nhấn Tab liên tục trong bảng | Giữ | Rõ ràng. | ORD-023 |
| DO-024 | 07_heuristics_admin_orders – O7-14 | Chi tiết đơn: Tìm cách xem chi tiết một đơn (sản phẩm, số lượng) từ dòng đơn hàng | Sửa | Mục đòi hỏi tính năng mà đặc tả không nêu; bỏ nhánh 'ghi nhận thiếu nếu không có' và gắn rõ là yêu cầu bổ sung. | ORD-024 |
| DO-025 | 07_heuristics_admin_orders – O7-15 | Xác nhận đơn thành công: Bấm "Xác nhận" ở đơn Chờ xác nhận | Giữ | Rõ ràng. | ORD-026 |
| DO-026 | 07_heuristics_admin_orders – O7-16 | Chuyển sang Đã giao: Bấm "Hoàn thành" ở đơn Đang giao (dùng đơn thử) | Giữ | Rõ ràng. Lưu ý: liên quan mục GUI-073 (xác nhận khi Hủy) của checklist chính nhưng khác nút; không gộp. | ORD-027 |
| DO-027 | 07_heuristics_admin_orders – O7-17 | Đơn Đã giao: Quan sát cột Hành động của đơn Đã giao | Gộp | Gộp với DO-034: cả hai kiểm tra cột Hành động của từng trạng thái; mục 'Đã giao không còn nút' là một dòng của mục 'nút theo trạng thái'. Lưu ý: trùng ý với GUI-072 của checklist chính. | ORD-028 |
| DO-028 | 07_heuristics_admin_orders – O7-18 | Lỗi đổi trạng thái: DevTools > Network > Block request URL "*/api/admin/orders/*" rồi bấm … | Giữ | Cách giả lập bằng DevTools, không mất dữ liệu. | ORD-029 |
| DO-029 | 07_heuristics_admin_orders – O7-19 | Bấm nút liên tiếp: Mở DevTools > Network, bấm "Xác nhận" hai lần liên tiếp thật nhanh trê… | Giữ | Đo được số yêu cầu trong tab Network. | ORD-030 |
| DO-030 | 07_heuristics_admin_orders – O7-20 | Đang tải: DevTools > Network > Slow 3G rồi mở tab Đơn hàng | Giữ | Khả thi bằng DevTools > Slow 3G. | ORD-031 |
| DO-031 | 07_heuristics_admin_orders – O7-21 | Lỗi tải danh sách: DevTools > Block request URL "*/api/admin/orders", tải lại rồi mở tab … | Giữ | Cách giả lập bằng DevTools, không mất dữ liệu. | ORD-032 |
| DO-032 | 07_heuristics_admin_orders – O7-22 | Dữ liệu cập nhật: Tạo đơn mới bằng tài khoản khách (không F5 admin), bấm lại tab Đơn hàn… | Giữ | Cần tài khoản khách đặt đơn mới; làm được. | ORD-033 |
| DO-033 | 07_heuristics_admin_orders – O7-23 | Tổng số đơn: So "Tổng số đơn hàng" ở Dashboard với số dòng ở tab Đơn hàng | Giữ | Đối chiếu được hai con số. | ORD-034 |
| DO-034 | 07_heuristics_admin_orders – O7-24 | Nút theo trạng thái: Với từng trạng thái, ghi các nút hiển thị | Gộp vào DO-027 | Trùng ý với DO-027. | ORD-028 |
