# -*- coding: utf-8 -*-
"""Gom các mục Failed của GUI Checklist thành bug và dựng báo cáo + thân GitHub Issue.

Chạy:  python hw03/scripts/bugs.py   (từ thư mục eshop-sut)
Đầu ra (hw03/bugs/):
  Bug_Report.md              - bảng tổng hợp và chi tiết từng bug (dán vào báo cáo chính)
  issues/BUG-xx.md           - nội dung từng GitHub Issue (tiêu đề ở dòng đầu, thân phía sau)
Kiểm tra: mọi mục Failed phải thuộc đúng một bug.
"""
import sys
from pathlib import Path

HW = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from execution_results import R  # noqa: E402

ENV = "Chromium (Claude desktop), Windows 11; Admin http://localhost:5174, Web http://localhost:5173, API http://localhost:3000; ngày 10/11/2026"
ADMIN = "Đăng nhập Admin (tài khoản admin trong dữ liệu mẫu) tại http://localhost:5174"

# id, severity, tiêu đề, màn hình, mục checklist, các bước, kỳ vọng, thực tế, ảnh (đã có hoặc cần chụp)
BUGS = [
 dict(id="BUG-01", sev="Critical", area="Admin: Đơn hàng", title="Địa chỉ giao hàng bị render thành HTML (nguy cơ XSS)",
      items=["ORD-011"],
      steps=["Đăng nhập tài khoản khách test, gọi POST /api/checkout với shipping_address = `<b>1 Le Loi</b> & \"Q1\"`.", ADMIN + ", mở tab Đơn hàng.", "Xem cột Địa chỉ của đơn vừa tạo."],
      expected="Địa chỉ hiển thị nguyên văn `<b>1 Le Loi</b> & \"Q1\"` (đặc tả FR-18: hiển thị an toàn, không render HTML).",
      actual="Chữ '1 Le Loi' hiển thị đậm; innerHTML của ô chứa thẻ `<b>`. Thẻ HTML do người dùng nhập được thực thi, có thể bị lợi dụng để chèn script.",
      shot="Cần chụp: bảng Đơn hàng có dòng địa chỉ in đậm, kèm DevTools > Elements hiện thẻ <b>."),
 dict(id="BUG-02", sev="Critical", area="Web: Home", title="Tìm kiếm lộ lỗi SQL thô khi nhập dấu nháy đơn",
      items=["GUI-081"],
      steps=["Mở http://localhost:5173.", "Gõ `o'` vào ô tìm kiếm rồi bấm Tìm."],
      expected="Không hiện lỗi kỹ thuật; trang trả kết quả hoặc thông báo thân thiện.",
      actual="Hiện khung đỏ 'Database Error – SQLITE_ERROR: unrecognized token'. Lộ chi tiết cơ sở dữ liệu và gợi ý có thể SQL injection. Dòng 'Hiển thị 5 sản phẩm' vẫn còn bên dưới.",
      shot="Đã có: evidence/ev_home_sql_error.jpg"),
 dict(id="BUG-03", sev="Major", area="Admin: Người dùng", title="Admin tự xóa được chính tài khoản đang đăng nhập",
      items=["GUI-047"],
      steps=[ADMIN + ", mở tab Người dùng.", "Bấm Xóa ở dòng admin@eshop.com."],
      expected="Hệ thống chặn và báo rõ; admin không thể tự xóa mình.",
      actual="Dòng admin bị xóa ngay, không xác nhận, không cảnh báo; sau đó admin không đăng nhập lại được.",
      shot="Cần chụp: trước và sau khi bấm Xóa ở dòng admin."),
 dict(id="BUG-04", sev="Major", area="Admin: Người dùng, Danh mục, Đơn hàng", title="Hành động không thể hoàn tác không có bước xác nhận",
      items=["GUI-043", "GUI-068", "GUI-073", "ORD-027"],
      steps=[ADMIN + ".", "Tab Người dùng: bấm Xóa ở một người dùng thử.", "Tab Danh mục: bấm Xóa ở một danh mục thử.", "Tab Đơn hàng: bấm Hủy ở đơn Chờ xác nhận; bấm Hoàn thành ở đơn Đang giao."],
      expected="Có hộp xác nhận nêu rõ đối tượng và cảnh báo không hoàn tác trước khi thực hiện.",
      actual="Các thao tác được thực hiện ngay lập tức, không có xác nhận (hàm confirm không được gọi).",
      shot="Cần chụp: dòng biến mất ngay sau khi bấm Xóa (không có hộp thoại)."),
 dict(id="BUG-05", sev="Major", area="Admin: Danh mục", title="Xóa được danh mục đang có sản phẩm, không cảnh báo",
      items=["GUI-069"],
      steps=[ADMIN + ", mở tab Danh mục.", "Bấm Xóa ở danh mục 'Laptop' (đang có sản phẩm MacBook Pro M3)."],
      expected="Hệ thống chặn việc xóa kèm thông báo nêu rõ danh mục đang có sản phẩm.",
      actual="Danh mục bị xóa thành công, không chặn, không cảnh báo; sản phẩm vẫn tham chiếu danh mục đã xóa.",
      shot="Cần chụp: bảng Danh mục trước và sau khi xóa 'Laptop'."),
 dict(id="BUG-06", sev="Major", area="Admin: Danh mục", title="Form Thêm danh mục không kiểm tra dữ liệu nhập",
      items=["GUI-054", "GUI-055", "GUI-056", "GUI-058", "GUI-059", "GUI-062"],
      steps=[ADMIN + ", mở tab Danh mục.", "Để trống ô rồi bấm Thêm mới; nhập toàn dấu cách; nhập tên trùng 'Laptop' và 'laptop'; nhập 300 chữ W; nhập '  Phụ kiện mới  '."],
      expected="Từ chối tên rỗng/toàn khoảng trắng/trùng tên kèm thông báo; có giới hạn độ dài; cắt khoảng trắng đầu cuối; trường bắt buộc có dấu *.",
      actual="Tất cả đều được lưu: dòng tên rỗng, dòng toàn dấu cách, bản sao 'Laptop', chuỗi 300 ký tự (làm bảng rộng 4631 px), tên giữ nguyên khoảng trắng thừa. Ô nhập không có dấu * hay thuộc tính required.",
      shot="Cần chụp: bảng Danh mục sau khi thêm các giá trị trên (thấy dòng rỗng và bản sao)."),
 dict(id="BUG-07", sev="Major", area="Admin: Đơn hàng", title="Đơn đã hủy vẫn có nút 'Đánh dấu Đã giao' (sai máy trạng thái FR-10)",
      items=["ORD-028"],
      steps=["Tạo một đơn rồi bấm Hủy ở tab Đơn hàng.", "Xem cột Hành động của đơn đã hủy."],
      expected="Đơn Đã hủy là trạng thái kết thúc, không có nút chuyển trạng thái (FR-10).",
      actual="Đơn Đã hủy hiện nút 'Đánh dấu Đã giao'.",
      shot="Cần chụp: dòng đơn 'Đã hủy' kèm nút 'Đánh dấu Đã giao'."),
 dict(id="BUG-08", sev="Major", area="Admin: Dashboard", title="Doanh thu trên Dashboard gấp đôi tổng các đơn Đã giao",
      items=["GUI-075"],
      steps=["Tạo một đơn 500,000 ₫ và đưa đến trạng thái Đã giao.", "Mở tab Dashboard."],
      expected="'Tổng doanh thu' bằng tổng tiền các đơn Đã giao (500,000 ₫).",
      actual="Dashboard hiện 1,000,000 ₫.",
      shot="Cần chụp: Dashboard và tab Đơn hàng cạnh nhau."),
 dict(id="BUG-09", sev="Major", area="Admin: Người dùng, Danh mục, Đơn hàng", title="Không có phản hồi thành công sau khi thêm, xóa hoặc đổi trạng thái",
      items=["GUI-044", "GUI-064", "GUI-065", "ORD-026"],
      steps=[ADMIN + ".", "Thêm một danh mục, xóa một người dùng thử, bấm Xác nhận ở một đơn.", "Với bảng 165 dòng, thêm một danh mục."],
      expected="Có thông báo thành công; dòng mới được cuộn tới hoặc làm nổi bật.",
      actual="Dữ liệu đổi nhưng không có thông báo nào. Với bảng dài, dòng mới nối ở cuối (khoảng 8937 px), người dùng không thấy gì xảy ra.",
      shot="Cần chụp: sau khi thêm, màn hình không có thông báo (đầu trang)."),
 dict(id="BUG-10", sev="Minor", area="Admin: Người dùng, Danh mục, Đơn hàng", title="Thông báo lỗi là alert kỹ thuật tiếng Anh ('Network Error')",
      items=["GUI-045", "GUI-067", "ORD-029"],
      steps=["Chặn request (DevTools > Network > Block request URL) DELETE users, POST categories hoặc PUT order status.", "Thực hiện thao tác tương ứng."],
      expected="Thông báo lỗi dễ hiểu bằng tiếng Việt, nêu nguyên nhân và cách xử lý.",
      actual="Hộp alert: 'Lỗi xóa: Network Error', 'Lỗi thêm DM: Network Error', 'Lỗi: Network Error'.",
      shot="Cần chụp: hộp alert lỗi."),
 dict(id="BUG-11", sev="Major", area="Admin: Người dùng, Đơn hàng", title="Không có chỉ báo đang tải và không thông báo khi tải dữ liệu lỗi",
      items=["GUI-041", "GUI-042", "ORD-031", "ORD-032"],
      steps=["DevTools > Network > Slow 3G (hoặc Block request URL */api/admin/users và */api/admin/orders).", "Tải lại trang Admin và mở tab Người dùng, Đơn hàng."],
      expected="Có chỉ báo đang tải; khi lỗi có thông báo và cách thử lại.",
      actual="Chỉ thấy hàng tiêu đề bảng, không có chỉ báo tải, không có thông báo lỗi (lỗi tải bị bỏ qua im lặng).",
      shot="Cần chụp: bảng chỉ có hàng tiêu đề khi mạng chậm hoặc bị chặn."),
 dict(id="BUG-12", sev="Major", area="Admin: Người dùng, Danh mục, Đơn hàng", title="Bấm hai lần liên tiếp gửi trùng yêu cầu",
      items=["GUI-046", "GUI-066", "ORD-030"],
      steps=["Mở DevTools > Network.", "Bấm Xóa (người dùng), Thêm mới (danh mục) hoặc Xác nhận (đơn) hai lần thật nhanh."],
      expected="Chỉ một yêu cầu được gửi; nút bị vô hiệu khi đang xử lý.",
      actual="Gửi 2 yêu cầu DELETE, 2 yêu cầu POST (tạo 2 danh mục) hoặc 2 yêu cầu PUT.",
      shot="Cần chụp: tab Network có hai request trùng."),
 dict(id="BUG-13", sev="Minor", area="Admin: Đơn hàng; Web: Home", title="Thiếu thông báo cho trạng thái rỗng / không có kết quả",
      items=["GUI-071", "GUI-080"],
      steps=["Backend vừa khởi động (0 đơn): mở tab Đơn hàng.", "Mở Web Home, tìm 'xyz123'."],
      expected="Hiện 'Chưa có đơn hàng' và 'Không tìm thấy sản phẩm phù hợp'.",
      actual="Tab Đơn hàng chỉ có hàng tiêu đề; Home chỉ hiện 'Kết quả tìm kiếm cho: xyz123' và vùng trống.",
      shot="Cần chụp: hai màn hình trên."),
 dict(id="BUG-14", sev="Major", area="Admin: toàn bộ", title="Admin không có URL theo tab: F5 về Dashboard, nút Back thoát ứng dụng",
      items=["GUI-009", "GUI-038", "GUI-039"],
      steps=[ADMIN + ", mở tab Danh mục.", "Nhấn F5.", "Chuyển qua vài tab rồi bấm Back của trình duyệt."],
      expected="F5 giữ nguyên tab; Back quay về tab trước; URL phản ánh trang hiện tại.",
      actual="URL luôn là '/'; F5 luôn về Dashboard; Back rời khỏi ứng dụng.",
      shot="Cần chụp: thanh URL '/' ở nhiều tab khác nhau."),
 dict(id="BUG-15", sev="Major", area="Admin: toàn bộ", title="Menu không dùng được bằng bàn phím; focus bị mất sau khi đổi trạng thái đơn",
      items=["GUI-008", "GUI-032", "GUI-036", "ORD-025"],
      steps=[ADMIN + ".", "Nhấn Tab từ đầu trang.", "Ctrl+click một mục menu.", "Ở tab Đơn hàng, Tab tới nút Xác nhận rồi Enter."],
      expected="Mục menu nhận focus và kích hoạt bằng Enter; là liên kết thật; focus nằm lại trong bảng sau khi đổi trạng thái.",
      actual="Mục menu là thẻ li không focus được, không phải liên kết; Tab nhảy thẳng vào checkbox; sau Enter focus rơi về body.",
      shot="Cần chụp: DevTools Elements hiện menu là thẻ li."),
 dict(id="BUG-16", sev="Minor", area="Admin: Người dùng", title="Checkbox chọn dòng và 'chọn tất cả' không có tác dụng",
      items=["GUI-024", "GUI-030", "GUI-048", "GUI-049"],
      steps=[ADMIN + ", mở tab Người dùng.", "Tick checkbox ở tiêu đề; tick một dòng."],
      expected="Checkbox tiêu đề chọn tất cả; dòng được chọn khác màu; có hành động hàng loạt; có trạng thái trung gian.",
      actual="Checkbox tiêu đề chỉ tick chính nó; dòng được chọn không đổi nền; không có hành động nào đi kèm; không có trạng thái trung gian.",
      shot="Đã có một phần: evidence/ev_users_table.jpg (bảng có checkbox không tác dụng)."),
 dict(id="BUG-17", sev="Minor", area="Admin và Web", title="Thiếu tên truy cập, nhãn và alt cho các thành phần",
      items=["GUI-023", "GUI-029", "GUI-052", "GUI-077", "GUI-078", "ORD-018"],
      steps=["Mở DevTools > Accessibility.", "Kiểm tra nút Xóa, checkbox, ô 'Tên danh mục mới', ô tìm kiếm Home, ảnh sản phẩm, nút Hủy."],
      expected="Mỗi thành phần có tên truy cập mô tả (ví dụ 'Xóa test@eshop.com', 'Hủy đơn #5'); ảnh có alt; ô nhập có nhãn.",
      actual="Nút chỉ có tên 'Xóa'/'Hủy'; checkbox không có nhãn; ô nhập chỉ có placeholder; cả 5 ảnh có alt rỗng.",
      shot="Cần chụp: DevTools Accessibility cho một nút Xóa."),
 dict(id="BUG-18", sev="Minor", area="Admin và Web", title="Vùng bấm quá nhỏ hoặc quá sát nhau",
      items=["GUI-028", "GUI-079", "ORD-020"],
      steps=["Đo bằng DevTools: checkbox, nút 'Thêm vào giỏ'/'Xem chi tiết' ở 375 px, khoảng cách giữa nút Xác nhận và Hủy."],
      expected="Vùng bấm tối thiểu 24×24 px (44 px trên cảm ứng); hai nút cách nhau tối thiểu 8 px.",
      actual="Checkbox 13×13 px; nút Home cao 36 px; hai nút trong ô Hành động cách nhau 4 px.",
      shot="Cần chụp: DevTools box model của checkbox."),
 dict(id="BUG-19", sev="Minor", area="Admin: Người dùng, Đơn hàng", title="Tương phản màu không đạt 4.5:1 ở nút hành động",
      items=["GUI-014", "ORD-004"],
      steps=["Đo tương phản chữ/nền bằng DevTools hoặc WebAIM Contrast Checker."],
      expected="Mọi cặp màu đạt tối thiểu 4.5:1.",
      actual="Nút Xóa 3.76:1; Xác nhận 4.47:1; Hủy 2.54:1; Giao hàng 3.68:1; Hoàn thành và Đánh dấu Đã giao 2.28:1.",
      shot="Cần chụp: bảng Đơn hàng kèm công cụ đo tương phản."),
 dict(id="BUG-20", sev="Major", area="Admin và Web", title="Bố cục vỡ ở màn hình hẹp (tablet, điện thoại, zoom 200%)",
      items=["GUI-002", "GUI-005", "GUI-006", "GUI-076", "ORD-013", "ORD-014"],
      steps=["Đặt độ rộng cửa sổ 375 px (hoặc 768 px, hoặc zoom 200%).", "Mở tab Người dùng, Đơn hàng của Admin và trang Home."],
      expected="Bảng nằm gọn; vùng nội dung chiếm ít nhất 70% chiều rộng; tiêu đề không bẻ quá 2 dòng; nhãn nút không bẻ nhiều dòng.",
      actual="Ở 375 px menu chiếm 256 px, vùng nội dung chỉ 119 px (32%), tiêu đề bẻ 4 dòng, bảng phải cuộn ngang, nút 'Đánh dấu Đã giao' cao 72 px; Home: tiêu đề rộng 80 px, bẻ 4 dòng. Ở 768 px bảng Người dùng rộng 813 px > 512 px.",
      shot="Đã có: evidence/ev_admin_375_users.jpg"),
 dict(id="BUG-21", sev="Minor", area="Admin và Web", title="Thuộc tính lang='en' và tiêu đề tab là tên kỹ thuật",
      items=["GUI-001", "GUI-021"],
      steps=["DevTools > Elements: xem thẻ html của Admin và Web.", "Xem tiêu đề tab trình duyệt."],
      expected="lang='vi'; tiêu đề tab mang tên sản phẩm (ví dụ 'EShop Admin').",
      actual="lang='en'; tiêu đề tab là 'frontend-admin' và 'frontend-web'.",
      shot="Cần chụp: tab trình duyệt và thẻ html."),
 dict(id="BUG-22", sev="Cosmetic", area="Admin và Web", title="Không nhất quán ngôn ngữ, định dạng và kiểu giao diện",
      items=["GUI-012", "GUI-018", "GUI-019", "GUI-050", "GUI-074", "ORD-001", "ORD-035"],
      steps=["So sánh nhãn, định dạng tiền, định dạng ID và nút giữa các tab và giữa Admin với Home."],
      expected="Cùng ngôn ngữ, đơn vị tiền, định dạng ID, kiểu nút; số tiền căn phải; tên nút khớp tên trạng thái đích.",
      actual="Trộn 'Role', 'Dashboard', '(Delivered)'; Admin dùng '₫', Home dùng 'VND'; ID '#1' ở Danh mục nhưng '1' ở Người dùng; 'Tên Danh Mục' khác 'Tên danh mục mới'; nút Xóa kích thước khác nhau và không đổi màu khi hover; số tiền căn trái; nút 'Hoàn thành' đưa đơn sang 'Đã giao'.",
      shot="Đã có một phần: evidence/ev_users_table.jpg"),
 dict(id="BUG-23", sev="Minor", area="Admin: Người dùng, Đơn hàng", title="Bảng thiếu thông tin và chức năng cần thiết",
      items=["GUI-017", "GUI-022", "ORD-008", "ORD-015", "ORD-024"],
      steps=["Mở tab Người dùng và tab Đơn hàng."],
      expected="Người dùng: có cột Tên, số điện thoại hiển thị, có ô tìm kiếm. Đơn hàng: có thời gian đặt, email người đặt, cách xem chi tiết đơn.",
      actual="Cột Số ĐT luôn trống; không có cột Tên, không có ô tìm kiếm; Đơn hàng không có ngày đặt, hai khách cùng tên 'Test User' không phân biệt được, không xem được chi tiết đơn. (Các ý về Đơn hàng là đề xuất cải tiến, đặc tả không nêu.)",
      shot="Đã có: evidence/ev_users_table.jpg"),
 dict(id="BUG-24", sev="Minor", area="Admin: Danh mục, Đơn hàng", title="Bảng dài không có phân trang và tiêu đề cột bị cuộn mất",
      items=["GUI-051", "ORD-012"],
      steps=["Tạo 165 danh mục (hoặc 34 đơn), cuộn bảng xuống cuối."],
      expected="Có phân trang hoặc tiêu đề cột luôn nhìn thấy khi cuộn.",
      actual="Không phân trang; tiêu đề cột cuộn ra ngoài màn hình (top −8063 px); trang cao 8970 px.",
      shot="Cần chụp: cuối bảng dài không còn thấy tiêu đề."),
 dict(id="BUG-25", sev="Minor", area="Admin: Đơn hàng, Dashboard", title="Dữ liệu Admin chỉ tải một lần, không cập nhật khi đổi tab",
      items=["ORD-033"],
      steps=[ADMIN + ", mở tab Đơn hàng.", "Dùng tài khoản khách đặt thêm một đơn (POST /api/checkout).", "Chuyển sang tab Dashboard rồi quay lại tab Đơn hàng (không F5)."],
      expected="Đơn mới xuất hiện khi mở lại tab (hoặc có nút làm mới).",
      actual="Số dòng không đổi (vẫn 34); phải F5 mới thấy đơn mới. Dashboard cũng giữ số liệu cũ (từng hiện 35 đơn sau khi dữ liệu đã được seed lại).",
      shot="Cần chụp: số dòng trước và sau khi quay lại tab."),
]

SEV = {"Critical": 1, "Major": 2, "Minor": 3, "Cosmetic": 4}

# Bằng chứng cho từng bug (file trong hw03/evidence). Ảnh chụp trên giao diện thật ngày 10/11/2026;
# .txt là số đo/nhật ký khi bằng chứng không biểu diễn được bằng ảnh.
EVIDENCE = {
 "BUG-01": ["BUG-01_address_bold.png", "BUG-01_orders_full.jpg"],
 "BUG-02": ["BUG-02_sql_error.jpg"],
 "BUG-03": ["BUG-03_before_delete_admin.jpg", "BUG-03_after_delete_admin.jpg"],
 "BUG-04": ["BUG-04_no_confirm.jpg"],
 "BUG-05": ["BUG-05_laptop_deleted.jpg"],
 "BUG-06": ["BUG-06_invalid_categories.jpg"],
 "BUG-07": ["BUG-07_cancelled_row.png"],
 "BUG-08": ["BUG-08_dashboard.jpg", "BUG-07_cancelled_row.png"],
 "BUG-09": ["BUG-06_invalid_categories.jpg"],
 "BUG-10": ["BUG-10_console_alerts.txt"],
 "BUG-11": ["BUG-11_no_loading.jpg"],
 "BUG-12": ["BUG-12_double_submit.jpg"],
 "BUG-13": ["BUG-13_orders_empty.jpg", "BUG-13_home_no_result.jpg"],
 "BUG-14": ["BUG-14_devtools_url_history.png", "BUG-14_navigation_measure.txt"],
 "BUG-15": ["BUG-15_tab_focus.jpg"],
 "BUG-16": ["BUG-16_select_all.jpg"],
 "BUG-17": ["BUG-17_devtools_accessibility.png", "BUG-17_accessibility_measure.txt"],
 "BUG-18": ["BUG-18_devtools_boxmodel.png", "BUG-18_target_size_measure.txt"],
 "BUG-19": ["BUG-19_devtools_contrast.png", "BUG-19_contrast_measure.txt", "BUG-01_orders_full.jpg"],
 "BUG-20": ["BUG-20_admin_375_users.jpg", "BUG-20_orders_375.jpg", "BUG-20_home_375.jpg"],
 "BUG-21": ["BUG-21_devtools_elements_lang.png", "BUG-21_devtools_console.png", "BUG-21_lang_title_measure.txt"],
 "BUG-22": ["BUG-22_users_table.jpg", "BUG-08_dashboard.jpg"],
 "BUG-23": ["BUG-22_users_table.jpg", "BUG-01_orders_full.jpg"],
 "BUG-24": ["BUG-24_long_table.jpg"],
 "BUG-25": ["BUG-25_devtools_stale_rows.png", "BUG-25_stale_data_measure.txt"],
}
REPO = "minhthang2k5/eshop-sut"
BRANCH = "HW3_THMTHANG"


def ev_url(name):
    return f"https://github.com/{REPO}/blob/{BRANCH}/hw03/evidence/{name}?raw=true"


def ev_md(files):
    lines = []
    for f in files:
        if f.lower().endswith((".jpg", ".png")):
            lines.append(f"![{f}]({ev_url(f)})")
        else:
            lines.append(f"[{f}](https://github.com/{REPO}/blob/{BRANCH}/hw03/evidence/{f})")
    return "\n\n".join(lines)


def main():
    failed = {k for k, v in R.items() if v[0] == "Failed"}
    assigned = [i for b in BUGS for i in b["items"]]
    dup = {i for i in assigned if assigned.count(i) > 1}
    extra = set(assigned) - failed
    missing = failed - set(assigned)
    # GUI-070/072 là mục trùng, không thực thi; BUG-07 ghi nhận qua ORD-028
    assert not dup, f"mục thuộc nhiều bug: {dup}"
    assert not extra, f"mục không Failed nhưng có trong bug: {extra}"
    assert not missing, f"mục Failed chưa thuộc bug nào: {sorted(missing)}"

    assert set(EVIDENCE) == {b["id"] for b in BUGS}, "thiếu bằng chứng cho bug"
    for b in BUGS:
        for f in EVIDENCE[b["id"]]:
            assert (HW / "evidence" / f).exists(), f"thiếu file {f}"
        b["shot"] = "; ".join("evidence/" + f for f in EVIDENCE[b["id"]])

    out = HW / "bugs"; (out / "issues").mkdir(parents=True, exist_ok=True)
    from collections import Counter
    cs = Counter(b["sev"] for b in BUGS)
    md = ["# Bug Report – GUI & Usability (EShop)", "",
          f"Môi trường: {ENV}.", "",
          f"Tổng **{len(BUGS)} bug** gom từ **{len(failed)} mục Failed** của GUI Checklist. "
          + ", ".join(f"{k}: {cs[k]}" for k in SEV if cs[k]) + ".", "",
          "| Bug | Mức độ | Màn hình | Tiêu đề | Mục checklist | Ảnh |", "|---|---|---|---|---|---|"]
    for b in BUGS:
        md.append(f"| {b['id']} | {b['sev']} | {b['area']} | {b['title']} | {', '.join(b['items'])} | {b['shot']} |")
    md += ["", "Mức độ: Critical = ảnh hưởng bảo mật hoặc chặn luồng chính; Major = sai chức năng hoặc làm người dùng mất kiểm soát; Minor = khó dùng nhưng có cách khác; Cosmetic = thẩm mỹ.", ""]
    for b in BUGS:
        md += [f"## {b['id']}: {b['title']}", "", f"- **Mức độ:** {b['sev']}", f"- **Màn hình:** {b['area']}", f"- **Mục checklist:** {', '.join(b['items'])}", "",
               "**Các bước tái hiện**", ""] + [f"{n}. {s}" for n, s in enumerate(b["steps"], 1)] + ["",
               f"**Kết quả mong đợi:** {b['expected']}", "", f"**Kết quả thực tế:** {b['actual']}", "", f"**Ảnh:** {b['shot']}", ""]
        body = [f"**Mức độ:** {b['sev']}  \n**Màn hình:** {b['area']}  \n**Mục checklist liên quan:** {', '.join(b['items'])}  \n**Môi trường:** {ENV}", "",
                "### Các bước tái hiện"] + [f"{n}. {s}" for n, s in enumerate(b["steps"], 1)] + ["", "### Kết quả mong đợi", b["expected"], "",
                "### Kết quả thực tế", b["actual"], "", "### Ảnh / bằng chứng", ev_md(EVIDENCE[b["id"]]), ""]
        (out / "issues" / f"{b['id']}.md").write_text(f"[{b['id']}] {b['title']}\n\n" + "\n".join(body), encoding="utf-8")
    (out / "Bug_Report.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{len(BUGS)} bug, {len(failed)} mục Failed đều được phân bổ đúng một lần.", dict(cs))
    print("Mục trùng ý (không thực thi):", "GUI-070 → ORD-002; GUI-072 → ORD-028 (BUG-07)")


if __name__ == "__main__":
    main()
