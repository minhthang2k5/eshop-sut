# -*- coding: utf-8 -*-
"""Dựng GUI Checklist cuối từ bản nháp AI (61 mục) + quyết định review + mục tự thêm.

Chạy:  python hw03/scripts/build_final_checklist.py   (từ thư mục eshop-sut)
Đầu ra (hw03/checklist/):
  GUI_Checklist_final.csv / .md   - checklist cuối, đánh lại ID
  AI_Review_Decisions.md          - quyết định giữ/sửa/tách/gộp/bỏ cho từng mục AI + lý do
  Added_Items_AI_Gaps.md          - bảng "Mục bổ sung và lý do AI bỏ sót" để đưa vào báo cáo
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CK = BASE / "checklist"
DRAFT = CK / "GUI_Checklist_draft.csv"

U, C, O, D, H, A = ("Admin: Người dùng", "Admin: Danh mục", "Admin: Đơn hàng",
                    "Admin: Dashboard", "Web: Home", "Admin: Toàn trang")
SCREEN_ORDER = [A, U, C, O, D, H]

# Ba nguyên nhân theo đề
PROMPT = "Chất lượng prompt"
MODEL = "Giới hạn của model"
SCREEN = "Đặc thù giao diện"

# --------------------------------------------------------------------------
# 1. Quyết định cho 61 mục AI.  action: Giữ | Sửa | Tách | Gộp | Bỏ | Gộp vào
#    "set": các cột cần ghi đè.  "split": danh sách các bản ghi đè khi tách.
# --------------------------------------------------------------------------
DEC = {
 "D-001": dict(a="Giữ", r="Đo được, Pass/Fail rõ."),
 "D-002": dict(a="Giữ", r="Rõ ràng, so sánh trực quan được."),
 "D-003": dict(a="Giữ", r="Có cơ sở thực tế: 'Role', 'Dashboard', '(Delivered)' trộn với nhãn tiếng Việt."),
 "D-004": dict(a="Sửa", r="Vế 'từ viết tắt dễ hiểu' mang tính cảm tính, không có ngưỡng Pass/Fail. Bỏ vế đó, chỉ giữ tiêu chí đếm được.",
                 set=dict(expected="0 lỗi chính tả, 0 lỗi hiển thị dấu tiếng Việt trên toàn màn hình")),
 "D-005": dict(a="Gộp", r="Gộp với D-006: cùng một phép đo tương phản, cùng công cụ, cùng ngưỡng 4.5:1. Bổ sung tên công cụ cụ thể để lặp lại được.",
                 set=dict(control="Tương phản màu chữ", check="Dùng DevTools (Inspect > Contrast) hoặc WebAIM Contrast Checker đo: chữ trắng trên nút \"Xóa\" đỏ (tab Người dùng, Danh mục); chữ xanh mục menu đang chọn và chữ đỏ \"Đăng xuất\" trên nền menu tối",
                          expected="Mọi cặp màu đạt tỉ lệ tương phản ≥ 4.5:1", basis="WCAG 1.4.3; Norman Visibility; Nielsen #8")),
 "D-006": dict(a="Gộp vào", into="D-005", r="Trùng phép đo với D-005 (AI-01-06 với AI-01-05)."),
 "D-007": dict(a="Giữ", r="Quan sát trực tiếp, Pass/Fail rõ."),
 "D-008": dict(a="Sửa", r="Không khả thi như AI viết: tab Người dùng không có chức năng tạo người dùng. Đổi bước sang tạo qua API /api/register; bỏ nhánh 'nếu bị cắt thì...' để có một tiêu chí.",
                 set=dict(check="Tạo người dùng có email ~60 ký tự qua API POST /api/register (Postman/curl), rồi mở tab Người dùng và quan sát cột Email",
                          expected="Email nằm gọn trong ô, không đè cột bên cạnh; đọc được đầy đủ email (xuống dòng, hoặc cắt bằng \"…\" kèm tooltip đầy đủ)")),
 "D-009": dict(a="Sửa", r="Làm rõ dữ liệu: seed không có số điện thoại nên mọi dòng đều trống; ghi rõ ký hiệu chấp nhận được để có Pass/Fail.",
                 set=dict(check="Xem cột \"Số ĐT\" ở mọi dòng (dữ liệu seed không có số điện thoại)",
                          expected="Ô không có dữ liệu hiển thị ký hiệu thống nhất (\"—\" hoặc \"Chưa cập nhật\"), không để ô trắng")),
 "D-010": dict(a="Giữ", r="Đo được bằng DevTools (kích thước, cỡ chữ)."),
 "D-011": dict(a="Sửa", r="Kết quả 'và/hoặc' cho phép Pass khi chỉ đạt một nửa; chốt cả hai dấu hiệu (con trỏ và màu nền).",
                 set=dict(expected="Khi rê chuột lên nút Xóa, con trỏ đổi thành bàn tay và màu nền nút thay đổi")),
 "D-012": dict(a="Sửa", r="Gộp hai tiêu chí khác bản chất (ngữ cảnh nhìn thấy và tên truy cập) dễ gây tranh cãi khi chấm. Giữ tiêu chí đo được: tên truy cập.",
                 set=dict(ia="IA-02", check="Mở DevTools > Accessibility, chọn nút \"Xóa\" ở một dòng, đọc Computed name",
                          expected="Tên truy cập chứa định danh người dùng (ví dụ \"Xóa test@eshop.com\"), không chỉ là \"Xóa\"")),
 "D-013": dict(a="Bỏ", r="Kết quả kiểu 'Nếu không sắp xếp thì...'. Màn hình không có tính năng sắp xếp, mục chỉ kiểm tra sự vắng mặt của một hành vi nên giá trị rất thấp; nhu cầu tìm/sắp xếp đã được phủ bởi mục tự thêm về ô tìm kiếm và bảng lớn."),
 "D-014": dict(a="Sửa", r="'Số người dùng thực tế' chưa nói lấy từ đâu; thêm nguồn đối chiếu để kiểm lại được.",
                 set=dict(check="Đếm số dòng trên bảng, đối chiếu với kết quả GET /api/admin/users (hoặc bảng users trong database.sqlite); tải lại trang 2 lần")),
 "D-015": dict(a="Giữ", r="Pass/Fail rõ (tiêu đề hiện tại là tên kỹ thuật)."),
 "D-016": dict(a="Sửa", r="C3-14 không có Pass/Fail rõ ('nếu là liên kết... nếu không...'). Chọn chuẩn: mục menu điều hướng phải là liên kết thật.",
                 set=dict(ia="IA-03", expected="Ctrl+click (hoặc chuột giữa) mở trang tương ứng trong tab mới, như một liên kết thật")),
 "D-017": dict(a="Giữ", r="Hành vi rõ, kiểm được ngay."),
 "D-018": dict(a="Giữ", r="Rõ ràng."),
 "D-019": dict(a="Giữ", r="Rõ ràng."),
 "D-020": dict(a="Giữ", r="Khác D-019 (thứ tự Tab, không phải phím Space) nên không gộp."),
 "D-021": dict(a="Tách", r="Một mục chứa hai phép đo độc lập (kích thước vùng bấm và tên truy cập); có thể đạt cái này trượt cái kia.",
                 split=[dict(check="Đo kích thước checkbox bằng DevTools (Computed / box model)",
                             expected="Vùng bấm tối thiểu 24×24 px (WCAG 2.5.8)"),
                        dict(check="Mở DevTools > Accessibility, chọn checkbox ở một dòng, đọc Computed name",
                             expected="Có tên truy cập mô tả mục đích (ví dụ \"Chọn người dùng test@eshop.com\")")]),
 "D-022": dict(a="Sửa", r="Kết quả 'trung gian hoặc bỏ chọn' cho phép hai đáp án. Chọn chuẩn phổ biến là trạng thái trung gian.",
                 set=dict(expected="Ô tiêu đề hiển thị trạng thái trung gian (dấu \"–\", indeterminate)")),
 "D-023": dict(a="Gộp", r="Gộp với D-024 (C3-07 + C3-08): cùng một thao tác bàn phím trên cùng nút, tách ra chỉ làm trùng bước.",
                 set=dict(check="Nhấn Tab tới nút \"Xóa\" của người dùng thử; nhấn Enter, làm lại với Space (dùng dữ liệu thử)",
                          expected="Nút nhận focus theo thứ tự hợp lý, có viền focus nhìn thấy; Enter và Space cho kết quả giống click chuột",
                          basis="Button: Tab đúng thứ tự, nhận focus; Space/Enter kích hoạt")),
 "D-024": dict(a="Gộp vào", into="D-023", r="Trùng ý với D-023 (C3-08 với C3-07)."),
 "D-025": dict(a="Giữ", r="Đếm được."),
 "D-026": dict(a="Giữ", r="Quan sát được."),
 "D-027": dict(a="Sửa", r="Kết quả 'và/hoặc' cho phép Pass khi chỉ đạt một nửa; chốt cả hai dấu hiệu (lưu ý mục Đăng xuất).",
                 set=dict(expected="Khi rê chuột qua mục menu, con trỏ đổi thành bàn tay và chữ hoặc nền mục menu đổi màu")),
 "D-028": dict(a="Gộp", r="Gộp với D-029 (AI-03-04 + AI-03-05): focus và kích hoạt bằng Enter là một chuỗi thao tác.",
                 set=dict(check="Nhấn Tab để đi qua các mục menu, tại mỗi mục nhấn Enter",
                          expected="Mỗi mục nhận focus, có viền focus nhìn thấy; Enter mở đúng tab", prio="Mandatory")),
 "D-029": dict(a="Gộp vào", into="D-028", r="Trùng ý với D-028 (AI-03-05 với AI-03-04)."),
 "D-030": dict(a="Giữ", r="Rõ ràng."),
 "D-031": dict(a="Giữ", r="Rõ ràng."),
 "D-032": dict(a="Giữ", r="Rõ ràng."),
 "D-033": dict(a="Sửa", r="Vế 'dễ tìm và tách biệt' là cảm tính. Thay bằng tiêu chí kiểm được (Back sau khi đăng xuất).",
                 set=dict(check="Bấm \"Đăng xuất\", sau đó bấm Back của trình duyệt",
                          expected="Về màn hình Admin Login; bấm Back không hiện lại dữ liệu quản trị")),
 "D-034": dict(a="Giữ", r="Khả thi: chỉ cần DevTools > Network > Slow 3G."),
 "D-035": dict(a="Sửa", r="Tắt backend rồi bật lại sẽ CHẠY LẠI SEED và xóa sạch dữ liệu (database.js drop table mỗi lần khởi động). Đổi sang chặn request bằng DevTools, nhẹ và không mất dữ liệu.",
                 set=dict(check="DevTools > Network > chuột phải request admin/users > Block request URL, rồi tải lại và mở tab Người dùng")),
 "D-036": dict(a="Bỏ", r="Giả lập quá nặng: muốn danh sách rỗng phải xóa cả tài khoản admin đang đăng nhập (tự khóa mình). Ý 'trạng thái rỗng' được kiểm ở tab Đơn hàng, nơi seed có sẵn 0 đơn (mục tự thêm)."),
 "D-037": dict(a="Gộp", r="Gộp với D-038: nội dung hộp xác nhận chỉ kiểm được khi hộp xác nhận tồn tại, tách ra thì D-038 luôn N/A khi D-037 trượt.",
                 set=dict(check="Bấm \"Xóa\" ở một người dùng thử nghiệm, đọc nội dung hộp xác nhận rồi bấm Hủy",
                          expected="Có hộp xác nhận nêu rõ người bị xóa (email/ID), cảnh báo không hoàn tác, có nút Hủy; bấm Hủy thì không xóa gì")),
 "D-038": dict(a="Gộp vào", into="D-037", r="Phụ thuộc vào D-037."),
 "D-039": dict(a="Giữ", r="Rõ ràng."),
 "D-040": dict(a="Sửa", r="Tương tự D-035: không tắt backend (mất dữ liệu khi bật lại). Dùng DevTools chặn request DELETE.",
                 set=dict(check="DevTools > Network > Block request URL \"*/api/admin/users/*\", rồi bấm Xóa ở người dùng thử")),
 "D-041": dict(a="Sửa", r="Kết quả 'đang xử lý hoặc chỉ gửi một yêu cầu' cho hai đáp án; chọn tiêu chí đo được: số yêu cầu trong tab Network.",
                 set=dict(check="Mở DevTools > Network, bấm \"Xóa\" hai lần liên tiếp thật nhanh trên cùng một dòng (người dùng thử)",
                          expected="Chỉ một yêu cầu DELETE được gửi đi")),
 "D-042": dict(a="Sửa", r="Bổ sung cách khôi phục cụ thể để mục an toàn khi thực thi; chốt kết quả là chặn xóa kèm thông báo (bỏ 'chặn hoặc cảnh báo').",
                 set=dict(check="Sao lưu backend/database.sqlite, thử xóa chính tài khoản admin@eshop.com, sau đó chép lại bản sao lưu (hoặc khởi động lại backend để seed lại)",
                          expected="Hệ thống chặn việc xóa kèm thông báo rõ; admin không thể tự xóa chính mình")),
 "D-043": dict(a="Tách", r="Kết quả có hai vế 'hoặc' độc lập (phản hồi trực quan và mục đích của checkbox). Tách thành hai mục có Pass/Fail riêng.",
                 split=[dict(check="Tick ô checkbox ở một dòng",
                             expected="Dòng được chọn có màu nền khác các dòng còn lại"),
                        dict(check="Tick vài checkbox, tìm hành động áp dụng cho các dòng đã chọn",
                             expected="Có hành động hàng loạt đi kèm (ví dụ nút \"Xóa đã chọn\"); checkbox không tồn tại vô nghĩa")]),
 "D-044": dict(a="Sửa", r="Kết quả 'nhãn cố định hoặc tên truy cập' cho hai đáp án; chốt tiêu chí nhìn thấy được: nhãn cố định, không chỉ placeholder.",
                 set=dict(expected="Ô có nhãn nhìn thấy cố định (không chỉ placeholder), vẫn đọc được sau khi gõ")),
 "D-045": dict(a="Giữ", r="Rõ ràng."),
 "D-046": dict(a="Sửa", r="Kết quả 'dấu hiệu rõ hoặc chú thích' mơ hồ; chốt dấu * theo checklist Text Box của bài giảng.",
                 set=dict(expected="Trường bắt buộc có dấu * (theo checklist Text Box)")),
 "D-047": dict(a="Gộp", r="Gộp với D-055 (C4-04 + C4-12): cùng thao tác 'để trống rồi bấm Thêm mới', chỉ khác điểm quan sát (thông báo và focus).",
                 set=dict(check="Để trống ô nhập rồi bấm \"Thêm mới\"; quan sát bảng, thông báo và vị trí focus",
                          expected="Không thêm danh mục; có thông báo lỗi rõ ràng gần ô nhập; focus quay về ô nhập và ô được làm nổi bật (viền đỏ)",
                          basis="Validation: trường bắt buộc bị bắt khi để trống; golden rule đưa focus về ô sai")),
 "D-048": dict(a="Giữ", r="Rõ ràng."),
 "D-049": dict(a="Sửa", r="C4-06: kết quả 'hoặc bị từ chối... hoặc được lưu...' khiến gần như luôn Pass. Chọn một kết quả.",
                 set=dict(expected="Được lưu và hiển thị nguyên văn `<b>test</b> & \"a\" 'b' $#+-` (không thành chữ đậm), bố cục bảng không vỡ")),
 "D-050": dict(a="Sửa", r="Kết quả có nhánh 'nếu chấp nhận thì...'. Chọn kỳ vọng cụ thể: có giới hạn độ dài.",
                 set=dict(expected="Ô nhập có giới hạn độ dài (ví dụ 100 ký tự) và báo rõ khi vượt; không lưu chuỗi 300 ký tự")),
 "D-051": dict(a="Giữ", r="Rõ ràng."),
 "D-052": dict(a="Giữ", r="Rõ ràng."),
 "D-053": dict(a="Giữ", r="Rõ ràng."),
 "D-054": dict(a="Sửa", r="Kết quả 'cắt hoặc từ chối' cho hai đáp án. Chọn hành vi chuẩn là cắt khoảng trắng.",
                 set=dict(expected="Khoảng trắng đầu/cuối được cắt; bảng hiển thị đúng \"Phụ kiện mới\"")),
 "D-055": dict(a="Gộp vào", into="D-047", r="Cùng thao tác với D-047 (C4-12 với C4-04)."),
 "D-056": dict(a="Giữ", r="Rõ ràng."),
 "D-057": dict(a="Sửa", r="Kết quả 'nút đang xử lý hoặc bị vô hiệu' cho hai đáp án; đo bằng số yêu cầu POST trong tab Network.",
                 set=dict(check="Mở DevTools > Network, nhập tên hợp lệ rồi bấm \"Thêm mới\" hai lần liên tiếp thật nhanh",
                          expected="Chỉ một yêu cầu POST được gửi và chỉ một danh mục mới được tạo (không có bản sao trong bảng)")),
 "D-058": dict(a="Sửa", r="Không tắt backend (khởi động lại sẽ seed lại DB). Dùng DevTools chặn request POST.",
                 set=dict(check="DevTools > Network > Block request URL \"*/api/categories\", nhập tên hợp lệ rồi bấm \"Thêm mới\"")),
 "D-059": dict(a="Giữ", r="Rõ ràng."),
 "D-060": dict(a="Sửa", r="Không cần tạo dữ liệu riêng: danh mục seed \"Laptop\" đã có sản phẩm. Ghi rõ sao lưu DB; chốt kết quả là chặn xóa kèm thông báo (bỏ 'chặn hoặc cảnh báo').",
                 set=dict(check="Sao lưu database.sqlite, bấm \"Xóa\" ở danh mục \"Laptop\" (đang có MacBook Pro M3), rồi khôi phục bản sao lưu",
                          expected="Hệ thống chặn việc xóa kèm thông báo nêu rõ danh mục đang có sản phẩm")),
 "D-061": dict(a="Bỏ", r="Giả lập nặng (phải xóa cả danh mục seed đang có sản phẩm) và trùng ý 'trạng thái rỗng' với mục tự thêm ở tab Đơn hàng, nơi trạng thái rỗng có sẵn."),
}

# --------------------------------------------------------------------------
# 2. Mục tự thêm.  obs=True: đã xác nhận bằng cách chạy thật (10/11/2026).
# --------------------------------------------------------------------------
NEW = [
 # --- Accessibility / toàn trang Admin
 dict(screen=A, ia="IA-03", control="Thứ tự focus toàn trang",
      check="Tải lại trang, nhấn Tab liên tục từ đầu trang qua menu trái tới hết nội dung tab Người dùng",
      expected="Mọi thành phần tương tác (mục menu, checkbox, nút) đều nhận focus theo thứ tự trái → phải, trên → dưới, có viền focus nhìn thấy",
      prio="Mandatory", basis="WCAG 2.4.3 Focus Order; Nielsen #7",
      why=MODEL, why_d="AI chỉ đọc mô tả/ảnh chụp nên tưởng menu là liên kết. Chạy thật: các mục menu là thẻ <li> chỉ có onClick, không phải liên kết hay nút (không có thuộc tính tabindex) nên Tab bỏ qua toàn bộ menu.", obs=True),
 dict(screen=A, ia="IA-02", control="Trình đọc màn hình",
      check="Bật NVDA (hoặc Windows Narrator), mở tab Người dùng, dùng phím H / D để duyệt tiêu đề và vùng (landmark)",
      expected="Trình đọc thông báo vùng điều hướng và vùng nội dung chính, đọc được tiêu đề \"Quản lý Người dùng\", đọc mục menu là liên kết/nút",
      prio="Optional", basis="WCAG 1.3.1 Info and Relationships; 4.1.2 Name, Role, Value",
      why=PROMPT, why_d="Prompt không yêu cầu kiểm tra với trình đọc màn hình nên AI không sinh mục nào.", obs=False),
 dict(screen=A, ia="IA-01", control="Thuộc tính ngôn ngữ trang",
      check="DevTools > Elements, xem thuộc tính lang của thẻ <html> (Admin và Web)",
      expected="lang=\"vi\" để trình đọc màn hình đọc tiếng Việt đúng giọng",
      prio="Optional", basis="WCAG 3.1.1 Language of Page",
      why=MODEL, why_d="AI không thấy mã HTML. Chạy thật: cả hai ứng dụng đều để lang=\"en\" trong khi nội dung là tiếng Việt.", obs=True),
 dict(screen=A, ia="IA-01", control="Zoom 200%",
      check="Ở cửa sổ 1280 px, nhấn Ctrl + + tới 200%, mở tab Người dùng và Danh mục",
      expected="Không mất nội dung và không mất chức năng; không phải cuộn ngang để đọc một dòng bảng",
      prio="Mandatory", basis="WCAG 1.4.4 Resize Text; 1.4.10 Reflow",
      why=PROMPT, why_d="Prompt không nhắc tới zoom; AI chỉ kiểm ở 1366 và 1920.", obs=False),
 dict(screen=A, ia="IA-01", control="Dark mode",
      check="Bật chế độ tối của hệ điều hành (hoặc DevTools > Rendering > prefers-color-scheme: dark), mở Admin",
      expected="Mọi vùng giao diện cùng một chế độ màu; không có vùng chữ đen trên nền tối hay chữ trắng trên nền trắng",
      prio="Optional", basis="WCAG 1.4.3 Contrast; Nielsen #4",
      why=PROMPT, why_d="Prompt không nhắc tới dark mode.", obs=True),
 dict(screen=A, ia="IA-01", control="Bố cục RTL",
      check="DevTools: thêm dir=\"rtl\" vào thẻ <html>, quan sát menu và bảng",
      expected="Menu và bảng đảo chiều gọn gàng, chữ không chồng lên nhau, nút không bị che",
      prio="Optional", basis="Internationalization; Nielsen #4",
      why=PROMPT, why_d="Prompt không yêu cầu quốc tế hóa. Ưu tiên thấp vì sản phẩm chỉ phục vụ tiếng Việt, giữ ở mức Optional.", obs=False),
 dict(screen=A, ia="IA-01", control="Responsive – tablet",
      check="DevTools Device Toolbar 768×1024, mở tab Người dùng, Danh mục, Đơn hàng",
      expected="Bảng nằm gọn trong vùng nội dung, không cột nào bị cắt, không cuộn ngang trang",
      prio="Mandatory", basis="Nielsen #8; Responsive design",
      why=PROMPT, why_d="Prompt chỉ cho độ rộng desktop (1366, 1920).", obs=True),
 dict(screen=A, ia="IA-01", control="Responsive – điện thoại",
      check="DevTools Device Toolbar 375×812, mở tab Người dùng",
      expected="Vùng nội dung chiếm ít nhất 70% chiều rộng màn hình (từ 262 px trở lên ở 375 px); tiêu đề trang không bị bẻ quá 2 dòng",
      prio="Mandatory", basis="Nielsen #8; Responsive design",
      why=MODEL, why_d="Chỉ thấy khi chạy thật: menu trái cố định 256 px nên vùng nội dung chỉ còn ~119 px, tiêu đề \"Quản lý Người dùng\" xuống 4–5 dòng, bảng phải cuộn ngang.", obs=True),
 dict(screen=A, ia="IA-03", control="Giữ trạng thái khi F5",
      check="Mở tab Danh mục, nhấn F5",
      expected="Sau khi tải lại vẫn ở tab Danh mục (không bị đưa về Dashboard)",
      prio="Mandatory", basis="Nielsen #3 User control and freedom",
      why=MODEL, why_d="AI không biết ứng dụng lưu tab trong state React. Chạy thật: URL luôn là \"/\" ở mọi tab, F5 luôn quay về Dashboard. (Bổ sung cho mục nháp D-032 / AI-03-08 vốn chỉ xét tab Người dùng.)", obs=True),
 # --- Người dùng
 dict(screen=U, ia="IA-01", control="Cột thông tin người dùng",
      check="Mở tab Người dùng, tìm khách hàng theo tên (ví dụ \"Test User\")",
      expected="Bảng có cột Tên và có ô tìm kiếm/lọc để tìm một người dùng nhanh",
      prio="Mandatory", basis="Nielsen #6 Recognition rather than recall; Nielsen #7",
      why=SCREEN, why_d="AI không biết luồng thật của nhóm là 'tìm khách hàng X'. Chạy thật: API trả về name nhưng bảng không hiển thị, không có ô tìm kiếm; cột Số ĐT luôn trống vì API không trả phone.", obs=True),
 # --- Danh mục: IA-01 và IA-03
 dict(screen=C, ia="IA-01", control="Định dạng cột ID và tiêu đề",
      check="So sánh cột ID và cách viết hoa tiêu đề cột giữa tab Danh mục và tab Người dùng",
      expected="Cùng định dạng ID (cùng có hoặc cùng không có dấu \"#\"); cách viết hoa tiêu đề nhất quán (\"Tên danh mục\" như placeholder)",
      prio="Optional", basis="Nielsen #4 Consistency and standards",
      why=SCREEN, why_d="Prompt 4 chỉ yêu cầu form validation (IA-02/IA-04) nên tab Danh mục không có mục IA-01. Chạy thật: Danh mục hiện \"#1\", Người dùng hiện \"1\"; \"Tên Danh Mục\" và \"Tên danh mục mới\" viết hoa khác nhau.", obs=True),
 dict(screen=C, ia="IA-03", control="Thứ tự Tab trong trang",
      check="Mở tab Danh mục, nhấn Tab từ đầu vùng nội dung",
      expected="Focus đi: ô nhập → nút Thêm mới → các nút Xóa theo thứ tự dòng",
      prio="Mandatory", basis="WCAG 2.4.3; Nielsen #7",
      why=SCREEN, why_d="Prompt 4 không bao gồm IA-03 (điều hướng) cho Danh mục.", obs=False),
 dict(screen=C, ia="IA-03", control="Vị trí dòng mới khi bảng dài",
      check="Chạy `node hw03/scripts/seed_bulk_categories.js add 150`, mở tab Danh mục, thêm danh mục \"Màn hình\"",
      expected="Có thông báo thành công nhìn thấy ngay, không phải cuộn xuống cuối bảng mới biết danh mục đã được thêm",
      prio="Mandatory", basis="Nielsen #1 Visibility of system status",
      why=MODEL, why_d="Chỉ thấy khi chạy với dữ liệu thật: dòng mới nối vào cuối bảng ~9.000 px, ô nhập ở đầu trang, không có thông báo nên người dùng không biết đã thêm chưa.", obs=True),
 # --- Dữ liệu lớn
 dict(screen=C, ia="IA-01", control="Bảng hàng trăm dòng",
      check="Sau khi seed 150 danh mục, cuộn bảng Danh mục xuống cuối",
      expected="Tiêu đề cột luôn nhìn thấy khi cuộn bảng và danh sách được chia trang",
      prio="Mandatory", basis="Nielsen #6; Nielsen #8",
      why=MODEL, why_d="Chạy thật với 153 dòng: không phân trang, tiêu đề cột cuộn mất (position: static), trang dài ~9.400 px. Nhớ chạy `... clean` để dọn dữ liệu.", obs=True),
 # --- Đơn hàng
 dict(screen=O, ia="IA-04", control="Trạng thái rỗng",
      check="Khởi động backend mới (seed có 0 đơn), mở tab Đơn hàng",
      expected="Có thông báo \"Chưa có đơn hàng\" thay vì chỉ còn hàng tiêu đề",
      prio="Mandatory", basis="Norman Feedback; Nielsen #1",
      why=SCREEN, why_d="Màn hình Đơn hàng chưa được prompt nào phủ. Chạy thật: seed không có đơn nên tab chỉ có hàng tiêu đề; đây là trạng thái rỗng có sẵn, thay cho mục nháp D-036/D-061 vốn cần giả lập nặng.", obs=True),
 dict(screen=O, ia="IA-01", control="Nhãn trạng thái đơn",
      check="Tạo đơn ở nhiều trạng thái (đặt hàng bằng tài khoản test@eshop.com, rồi đổi trạng thái), quan sát cột Trạng thái",
      expected="Năm trạng thái có chữ tiếng Việt và màu khác nhau; phân biệt được cả khi xem ảnh đen trắng (không chỉ dựa vào màu)",
      prio="Optional", basis="WCAG 1.4.1 Use of Color; Nielsen #4",
      why=SCREEN, why_d="Màn hình Đơn hàng chưa được prompt nào phủ.", obs=False),
 dict(screen=O, ia="IA-04", control="Hành động trên đơn đã hủy",
      check="Với một đơn ở trạng thái \"Đã hủy\", xem cột Hành động",
      expected="Đơn đã hủy không còn nút chuyển sang \"Đã giao\"",
      prio="Mandatory", basis="Nielsen #5 Error prevention; Norman Constraints",
      why=SCREEN, why_d="Đặc thù nghiệp vụ của màn hình: giao diện hiện nút \"Đánh dấu Đã giao\" cho đơn đã hủy (phát hiện khi đọc mã App.jsx). AI không có thông tin về luồng trạng thái này.", obs=False),
 dict(screen=O, ia="IA-04", control="Đổi trạng thái đơn",
      check="Bấm \"Hủy\" ở một đơn \"Chờ xác nhận\"",
      expected="Có hộp xác nhận trước khi hủy; sau khi hủy có thông báo thành công và nhãn trạng thái đổi ngay",
      prio="Mandatory", basis="Nielsen #5; Shneiderman #3, #4",
      why=SCREEN, why_d="Màn hình Đơn hàng chưa được prompt nào phủ.", obs=False),
 # --- Dashboard
 dict(screen=D, ia="IA-04", control="Số liệu doanh thu",
      check="Ghi tổng tiền các đơn \"Đã giao\" ở tab Đơn hàng, so với \"Tổng doanh thu\" ở Dashboard",
      expected="Hai con số bằng nhau",
      prio="Mandatory", basis="Nielsen #1; Norman Feedback",
      why=MODEL, why_d="Chỉ lộ ra khi có dữ liệu thật (phát hiện khi đọc mã App.jsx): công thức doanh thu nhân đôi total_amount, nên Dashboard sẽ gấp đôi tổng ở tab Đơn hàng.", obs=False),
 dict(screen=D, ia="IA-01", control="Nhãn và định dạng tiền",
      check="So sánh nhãn và cách hiển thị tiền ở Dashboard, Đơn hàng (Admin) và Home (Web)",
      expected="Cùng ngôn ngữ (không có \"(Delivered)\"), cùng đơn vị (₫ hoặc VND) và cùng dấu phân cách hàng nghìn",
      prio="Optional", basis="Nielsen #4 Consistency; Nielsen #2",
      why=SCREEN, why_d="Dashboard và Home chưa được prompt nào phủ. Chạy thật: Admin hiện \"₫\", Home hiện \"30,000,000 VND\" (dấu phẩy kiểu Anh).", obs=True),
 # --- Home
 dict(screen=H, ia="IA-04", control="Tìm kiếm không có kết quả",
      check="Gõ \"xyz123\" vào ô tìm kiếm, bấm \"Tìm\"",
      expected="Có thông báo rõ \"Không tìm thấy sản phẩm phù hợp\" kèm gợi ý",
      prio="Mandatory", basis="Nielsen #1; Nielsen #9",
      why=SCREEN, why_d="Home chưa được phủ. Chạy thật: chỉ còn dòng \"Kết quả tìm kiếm cho: xyz123\", vùng sản phẩm trống, không có thông báo.", obs=True),
 dict(screen=H, ia="IA-04", control="Thông báo lỗi tìm kiếm",
      check="Gõ \"o'\" (có dấu nháy đơn) rồi bấm \"Tìm\"",
      expected="Không hiện lỗi kỹ thuật (SQLITE_ERROR, stack trace) dù nhập ký tự đặc biệt",
      prio="Mandatory", basis="Nielsen #9; Shneiderman #5",
      why=MODEL, why_d="Chỉ thấy khi chạy thật: trang hiện khung đỏ \"Database Error – SQLITE_ERROR: unrecognized token\".", obs=True),
 dict(screen=H, ia="IA-02", control="Ảnh sản phẩm",
      check="DevTools > Accessibility, kiểm tra thuộc tính alt của ảnh sản phẩm",
      expected="Mỗi ảnh có alt mô tả (ví dụ tên sản phẩm)",
      prio="Optional", basis="WCAG 1.1.1 Non-text Content",
      why=SCREEN, why_d="Home chưa được phủ. Chạy thật: cả 5 ảnh đều có alt=\"\".", obs=True),
 dict(screen=H, ia="IA-02", control="Ô tìm kiếm",
      check="DevTools > Accessibility, chọn ô \"Tìm kiếm...\", đọc Computed name",
      expected="Có nhãn truy cập (label hoặc aria-label), không chỉ dựa vào placeholder",
      prio="Optional", basis="WCAG 3.3.2 Labels or Instructions",
      why=SCREEN, why_d="Home chưa được phủ. Chạy thật: ô tìm kiếm không có label, không có aria-label.", obs=True),
 dict(screen=H, ia="IA-01", control="Responsive – điện thoại",
      check="DevTools Device Toolbar 375×812, mở trang Home",
      expected="Tiêu đề \"Danh sách sản phẩm\" và ô tìm kiếm xếp chồng theo chiều dọc; tiêu đề không bị bẻ quá 2 dòng",
      prio="Mandatory", basis="Nielsen #8; Responsive design",
      why=MODEL, why_d="Chỉ thấy khi chạy thật: tiêu đề bị ô tìm kiếm ép còn ~80 px, xuống 4 dòng (cao 144 px).", obs=True),
 dict(screen=H, ia="IA-02", control="Vùng chạm trên điện thoại",
      check="Ở 375×812, đo chiều cao nút \"Thêm vào giỏ\" và \"Xem chi tiết\"",
      expected="Vùng chạm tối thiểu 44×44 px",
      prio="Optional", basis="WCAG 2.5.5 Target Size; Apple HIG",
      why=PROMPT, why_d="Prompt không yêu cầu kiểm tra trên thiết bị cảm ứng. Chạy thật: nút cao 36 px.", obs=True),
]

# --------------------------------------------------------------------------
def load_draft():
    with open(DRAFT, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    out = []
    for r in rows[1:]:
        out.append(dict(draft_id=r[0], screen=r[1], ia=r[2], control=r[3], check=r[4], expected=r[5],
                        prio=r[6], origin=r[7], basis=r[8]))
    return out


def main():
    draft = load_draft()
    assert len(draft) == 61, len(draft)
    assert set(DEC) == {d["draft_id"] for d in draft}

    items = []
    for d in draft:
        dec = DEC[d["draft_id"]]
        a = dec["a"]
        sub = d["origin"].replace("AI – ", "")
        if a in ("Bỏ", "Gộp vào"):
            continue
        if a == "Tách":
            for k, s in enumerate(dec["split"], 1):
                it = {**d, **s}
                it.update(source=f"AI (đã tách {k}/{len(dec['split'])})", draft_ref=f"{d['draft_id']} ({sub})")
                items.append(it)
            continue
        it = {**d, **dec.get("set", {})}
        if a == "Giữ":
            it["source"] = "AI"
            it["draft_ref"] = f"{d['draft_id']} ({sub})"
        elif a == "Sửa":
            it["source"] = "AI (đã sửa)"
            it["draft_ref"] = f"{d['draft_id']} ({sub})"
        elif a == "Gộp":
            other = [k for k, v in DEC.items() if v.get("into") == d["draft_id"]][0]
            osub = [x for x in draft if x["draft_id"] == other][0]["origin"].replace("AI – ", "")
            it["source"] = "AI (đã sửa – gộp)"
            it["draft_ref"] = f"{d['draft_id']} ({sub}) + {other} ({osub})"
        items.append(it)

    for n in NEW:
        items.append(dict(n, draft_ref="—", source="Tự thêm – quan sát thật" if n["obs"] else "Tự thêm",
                          why_full=f"{n['why']}: {n['why_d']}"))

    order = {s: i for i, s in enumerate(SCREEN_ORDER)}
    items = [it for _, it in sorted(enumerate(items), key=lambda t: (order[t[1]["screen"]], t[1]["ia"], t[0]))]
    for i, it in enumerate(items, 1):
        it["id"] = f"GUI-{i:03d}"

    headers = ["ID", "Màn hình", "IA", "Control / Thành phần", "Mục kiểm tra", "Kết quả mong đợi", "Ưu tiên",
               "Nguồn mục", "ID nháp (truy vết)", "Nguyên tắc / checklist nguồn", "Vì sao AI bỏ sót",
               "Kết quả (Passed/Failed)", "Notes", "Screenshot"]

    def row(it):
        return [it["id"], it["screen"], it["ia"], it["control"], it["check"], it["expected"], it["prio"],
                it["source"], it["draft_ref"], it["basis"], it.get("why_full", ""), "", "", ""]

    with open(CK / "GUI_Checklist_final.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for it in items:
            w.writerow(row(it))

    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    n_ai = sum(1 for it in items if it["source"].startswith("AI"))
    n_new = len(items) - n_ai
    from collections import Counter
    by_screen = Counter(it["screen"] for it in items)
    by_ia = Counter(it["ia"] for it in items)
    md = ["# GUI Checklist – bản cuối", "",
          f"Tổng số mục: **{len(items)}** (từ AI: {n_ai}; tự thêm: {n_new}). "
          "Cột Kết quả, Notes, Screenshot để trống, điền khi thực thi.", "",
          "Phân bố theo màn hình: " + ", ".join(f"{s}: {by_screen[s]}" for s in SCREEN_ORDER) + ".  ",
          "Phân bố theo IA: " + ", ".join(f"{k}: {by_ia[k]}" for k in sorted(by_ia)) + ".", "",
          "Quy ước cột *Nguồn mục*: `AI` giữ nguyên; `AI (đã sửa)` có chỉnh nội dung; `AI (đã sửa – gộp)` gộp hai mục nháp; "
          "`AI (đã tách k/n)` tách từ một mục nháp; `Tự thêm` do nhóm bổ sung; `Tự thêm – quan sát thật` đã xác nhận khi chạy ứng dụng.", "",
          "Chi tiết quyết định review: [AI_Review_Decisions.md](AI_Review_Decisions.md). "
          "Cách chạy lại dự án: [HOW_TO_RUN.md](HOW_TO_RUN.md).", "",
          "| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for it in items:
        md.append("| " + " | ".join(esc(c) for c in row(it)) + " |")
    (CK / "GUI_Checklist_final.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---- Bảng quyết định review
    new_id = {}
    for it in items:
        for ref in it["draft_ref"].split(" + "):
            did = ref.split(" ")[0]
            if did.startswith("D-"):
                new_id.setdefault(did, []).append(it["id"])
    cnt = Counter(DEC[d["draft_id"]]["a"] for d in draft)
    rv = ["# Review 61 mục AI sinh", "",
          "Thống kê: " + ", ".join(f"{k}: {cnt[k]}" for k in ["Giữ", "Sửa", "Tách", "Gộp", "Gộp vào", "Bỏ"]) + ".  ",
          f"61 mục nháp → {n_ai} mục AI trong checklist cuối ({cnt['Bỏ']} bỏ, {cnt['Gộp vào']} bị gộp vào mục khác, {cnt['Tách']} được tách đôi).", "",
          "| ID nháp | Nguồn AI | Mục (tóm tắt) | Quyết định | Lý do | ID mới |", "|---|---|---|---|---|---|"]
    for d in draft:
        dec = DEC[d["draft_id"]]
        a = dec["a"] + (f" {dec['into']}" if dec.get("into") else "")
        rv.append(f"| {d['draft_id']} | {esc(d['origin'].replace('AI – ', ''))} | {esc(d['control'])}: {esc(d['check'][:70])}"
                  f"{'…' if len(d['check']) > 70 else ''} | {a} | {esc(dec['r'])} | {', '.join(new_id.get(d['draft_id'], ['—']))} |")
    (CK / "AI_Review_Decisions.md").write_text("\n".join(rv) + "\n", encoding="utf-8")

    # ---- Bảng mục bổ sung cho báo cáo
    added = [it for it in items if it["source"].startswith("Tự thêm")]
    wc = Counter(it["why"] for it in added)
    ad = ["# Mục bổ sung và lý do AI bỏ sót", "",
          f"Tổng {len(added)} mục tự thêm; "
          + ", ".join(f"{k}: {wc[k]}" for k in [PROMPT, MODEL, SCREEN])
          + f". Trong đó {sum(1 for it in added if it['obs'])} mục đã xác nhận bằng cách chạy ứng dụng thật (10/11/2026).", "",
          "| ID | Màn hình | IA | Mục bổ sung | Nguyên nhân AI bỏ sót | Giải thích | Quan sát thật |",
          "|---|---|---|---|---|---|---|"]
    for it in added:
        ad.append(f"| {it['id']} | {it['screen']} | {it['ia']} | {esc(it['control'])} | {it['why']} | {esc(it['why_d'])} | {'Có' if it['obs'] else '—'} |")
    ad += ["", "## Nhận xét nhanh (cơ sở cho phần AI Critique)", "",
           "- **Giới hạn của model** là nhóm giá trị nhất: các lỗi như menu không nhận Tab, F5 về Dashboard, lỗi SQL thô khi tìm kiếm, "
           "bố cục vỡ ở 375 px chỉ lộ ra khi chạy thật; AI làm việc trên mô tả màn hình nên tưởng menu là liên kết chuẩn.",
           "- **Chất lượng prompt**: các prompt chỉ khoanh vùng desktop 1366/1920 và ba IA, nên dark mode, zoom, trình đọc màn hình, "
           "thiết bị cảm ứng bị bỏ qua hoàn toàn. Đây là lỗi của người viết prompt, không phải của model.",
           "- **Đặc thù giao diện**: Đơn hàng, Dashboard, Home chưa từng được đưa vào prompt; tab Danh mục chỉ được hỏi về validation "
           "nên thiếu IA-01 và IA-03.",
           f"- Về chất lượng mục AI: {cnt['Sửa']} mục cần sửa, {cnt['Tách']} mục phải tách, {cnt['Gộp vào']} mục trùng ý phải gộp; nhiều mục sửa vì kết quả mong đợi kiểu \"hoặc… hoặc…\"/\"nếu… thì…\" hoặc cảm tính, "
           "3 mục cần đổi cách giả lập vì AI không biết khởi động lại backend sẽ seed lại toàn bộ DB."]
    (CK / "Added_Items_AI_Gaps.md").write_text("\n".join(ad) + "\n", encoding="utf-8")

    print(f"Final: {len(items)} mục (AI {n_ai}, tự thêm {n_new})")
    print("Theo màn hình:", dict(by_screen))
    print("Theo IA:", dict(by_ia))
    print("Quyết định:", dict(cnt))
    print("Lý do bỏ sót:", dict(wc))


if __name__ == "__main__":
    main()
