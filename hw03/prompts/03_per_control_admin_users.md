# Prompt 3 – Checklist theo từng control (IA-01 và IA-02) – Admin: Người dùng

- **Mục đích:** Bổ sung các mục kiểm tra **chi tiết theo từng control** (checkbox, nút, bảng/grid, link menu), phủ IA-02 (Forms/điều khiển nhập liệu) và phần chi tiết của IA-01. Prompt 2 đã phủ nguyên tắc thiết kế nên Prompt 3 phải **không lặp** các ý đó.
- **Căn cứ lý thuyết:** slide GUI Testing, trang 10–15 (Waghmare 2009): "Test every control" – checklist riêng cho Button, Checkbox, Radio, Hyperlink, Image, Grid.
- **Lưu ý về IA-02 trên màn hình này:** Tab "Người dùng" **không có ô nhập liệu hay form** (chỉ có checkbox và nút Xóa). Vì vậy IA-02 ở đây chỉ phủ được checkbox và nút; phần form thật (text box, validation) sẽ lấy ở màn hình **Admin: Danh mục** (có ô "Tên danh mục mới" và nút "Thêm mới"), do đó Prompt 4 sẽ nhắm vào đó.
- **Tool AI dùng:** Claude Code (Claude Sonnet 5.5)
- **Ngày giờ chạy:** 2026-11-10 (giờ chính xác xem `AI_Audit_Log.md` do hook ghi)
- **Lưu ý:** phiên này đã đọc mã nguồn SUT trước đó; prompt yêu cầu chỉ dựa vào mô tả.

---

## Prompt (dán nguyên khối vào AI; prompt đã tự chứa đủ ngữ cảnh)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Hãy kiểm thử HỘP ĐEN: chỉ dựa vào bản mô tả dưới đây, KHÔNG đọc mã nguồn, KHÔNG suy đoán cách cài đặt bên trong.

## Màn hình: "Quản lý Người dùng" (tab "Người dùng" của Web Admin EShop, tiếng Việt)
- Thanh menu tối bên trái, tiêu đề "EShop Admin", các mục: Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng (đang chọn, chữ xanh), Đăng xuất (chữ đỏ).
- Vùng nội dung bên phải nền sáng, tiêu đề trang "Quản lý Người dùng".
- Bảng nền trắng, hàng tiêu đề nền xám, 6 cột: checkbox (có ở tiêu đề và mỗi dòng), ID, Email, Role, Số ĐT, Hành động.
- Dữ liệu hiện có: 2 người dùng (1 admin, 1 user). Cột Số ĐT đang trống ở cả hai dòng. Mỗi dòng có nút "Xóa" nền đỏ chữ trắng.
- KHÔNG có: ô tìm kiếm, bộ lọc, sắp xếp cột, phân trang, cột Tên, nút Sửa, nút Thêm, biểu tượng cạnh các mục menu, ô nhập liệu nào.

## Các ý ĐÃ được phủ ở bước trước (KHÔNG lặp lại)
Bố cục 1366/1920; phân cấp chữ; ngôn ngữ nhãn Anh–Việt; chính tả và dấu tiếng Việt; tương phản nút Xóa và menu; căn lề bảng; dữ liệu dài; ô Số ĐT trống; nhất quán nút Xóa giữa các dòng; số mục và nổi bật mục menu đang chọn; hover menu; Tab và Enter trên menu; nhãn menu khớp tiêu đề; nút Back; F5; Đăng xuất; trạng thái đang tải, lỗi tải, rỗng; xác nhận và nội dung xác nhận khi xóa; thông báo xóa thành công/thất bại; bấm Xóa hai lần; xóa tài khoản đang đăng nhập; checkbox dòng có phản hồi.

## Nhiệm vụ
Áp dụng checklist THEO TỪNG CONTROL dưới đây lên các control có thật trên màn hình, sinh mục kiểm tra cho IA-01 (chuẩn UI chung) và IA-02 (form/điều khiển nhập liệu). Chỉ dùng control có trên màn hình; control không có thì ghi "Không áp dụng" kèm lý do.

### Checklist control cần áp dụng (từ bài giảng)
Button: bật/tắt đúng trạng thái; Tab tới được theo thứ tự; hover có hiệu ứng và tooltip; nhãn có nghĩa, không viết tắt khó hiểu; Space/Enter kích hoạt khi đang focus; tất cả nút cùng kích thước, hình dạng, font; màu thể hiện ý nghĩa (đỏ = hành động hủy diệt); hành động không hoàn tác phải có xác nhận Có/Không; click đơn, đúp, nhiều lần đều xử lý đúng.
Checkbox: có thể bật/tắt; trạng thái mặc định đúng; nhãn phù hợp; Tab chuyển tuần tự giữa các checkbox; chuột, Space đều đổi trạng thái; bấm vào chữ nhãn cũng đổi trạng thái; căn lề và kích thước vùng bấm hợp lý.
Hyperlink / mục điều hướng: kiểu hiển thị nhất quán; mở bằng click và Enter; Ctrl+click mở tab mới (nếu là link); Tab đi tới được; dẫn đúng trang.
Grid/bảng: có tiêu đề cột và tiêu đề bảng; click tiêu đề có sắp xếp (nếu có) kèm biểu tượng; cuộn bằng chuột/phím/nút; thao tác trên dòng (double-click) đúng; hiển thị đúng số dòng; dòng được chọn khác biệt.
Image/Biểu tượng: không mờ, không vỡ, đúng kích thước, căn lề đúng (kiểm tra favicon và biểu tượng nếu có).

## Quy tắc
- Mỗi mục là MỘT điểm kiểm tra, thực hiện được trong vài phút, có kết quả Passed/Failed.
- Cột "Kết quả mong đợi" chỉ nêu chuẩn tham chiếu, KHÔNG viết sẵn kết luận Passed/Failed.
- Mục cần giả lập điều kiện (mạng chậm, tắt backend, dữ liệu rỗng) phải ghi rõ cách giả lập.
- Không lặp các ý ở danh sách "ĐÃ phủ". Nếu muốn kiểm tra sâu hơn một ý đã phủ, nêu rõ điểm khác biệt.
- Khoảng 10–14 mục.

## Định dạng đầu ra
Một bảng Markdown:
| ID tạm | IA | Control | Nguồn checklist | Mục kiểm tra | Kết quả mong đợi | Mức ưu tiên (Mandatory/Optional) |

ID tạm dạng C3-01, C3-02, ...

Sau bảng:
1. Liệt kê các control trong checklist mà bạn xếp "Không áp dụng" kèm lý do.
2. Nêu các khía cạnh GUI mà bạn nghĩ vẫn CHƯA phủ.

Trả lời bằng tiếng Việt.
```

---

## Ghi log (điền sau khi chạy)

### Output của AI

| ID tạm | IA | Control | Nguồn checklist | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| C3-01 | IA-02 | Checkbox (tiêu đề) | Checkbox: bật/tắt đúng | Tick ô checkbox ở hàng tiêu đề | Tất cả checkbox dòng được chọn; bỏ tick ô tiêu đề thì bỏ chọn tất cả | Mandatory |
| C3-02 | IA-02 | Checkbox | Checkbox: trạng thái mặc định đúng | Mở lại trang (F5) rồi quan sát mọi checkbox | Tất cả checkbox ở trạng thái bỏ chọn khi vừa tải | Mandatory |
| C3-03 | IA-02 | Checkbox | Checkbox: Space đổi trạng thái | Dùng Tab để focus một checkbox rồi nhấn Space | Trạng thái chọn đổi như khi click chuột | Mandatory |
| C3-04 | IA-02 | Checkbox | Checkbox: Tab tuần tự | Nhấn Tab liên tiếp từ checkbox tiêu đề xuống các dòng | Focus đi lần lượt từ trên xuống dưới, mỗi checkbox một lần, không bỏ sót | Mandatory |
| C3-05 | IA-02 | Checkbox | Checkbox: căn lề và vùng bấm hợp lý | Đo kích thước vùng bấm của checkbox; kiểm tra tên truy cập bằng công cụ accessibility | Vùng bấm tối thiểu khoảng 24×24 px; có tên truy cập mô tả mục đích (ví dụ "Chọn người dùng X") | Optional |
| C3-06 | IA-02 | Checkbox (tiêu đề) | Checkbox: trạng thái đúng theo nhóm | Chọn một dòng (không chọn tất cả) rồi xem ô tiêu đề | Ô tiêu đề thể hiện trạng thái trung gian hoặc bỏ chọn nhất quán, không hiện "đã chọn tất cả" | Optional |
| C3-07 | IA-02 | Nút "Xóa" | Button: Tab đúng thứ tự, nhận focus | Nhấn Tab liên tiếp để tới nút Xóa | Nút Xóa nhận focus theo thứ tự hợp lý, có dấu hiệu focus nhìn thấy được | Mandatory |
| C3-08 | IA-02 | Nút "Xóa" | Button: Space/Enter kích hoạt | Focus nút Xóa của người dùng thử rồi nhấn Enter; làm lại với Space (dùng dữ liệu thử) | Cả hai phím cho kết quả giống click chuột | Mandatory |
| C3-09 | IA-01 | Nút "Xóa" | Button: hover có hiệu ứng | Rê chuột lên nút Xóa | Con trỏ đổi và/hoặc nút đổi màu để báo nút bấm được | Optional |
| C3-10 | IA-01 | Nút "Xóa" | Button: nhãn có nghĩa | Xem nhãn "Xóa" khi bảng có nhiều dòng; kiểm tra tên truy cập của nút | Đối tượng bị xóa xác định được từ ngữ cảnh dòng; tên truy cập nêu rõ người dùng (ví dụ "Xóa người dùng X") | Optional |
| C3-11 | IA-01 | Bảng/Grid (tiêu đề cột) | Grid: click tiêu đề cột sắp xếp | Click lên tiêu đề các cột và rê chuột lên đó | Nếu không sắp xếp thì tiêu đề không có dấu hiệu bấm được, và không có phản ứng bất ngờ | Optional |
| C3-12 | IA-01 | Bảng/Grid (dữ liệu) | Grid: hiển thị đúng số dòng | So sánh số dòng trên bảng với số người dùng thực tế; tải lại trang | Số dòng khớp dữ liệu; thứ tự các dòng ổn định giữa các lần tải | Mandatory |
| C3-13 | IA-01 | Favicon và tiêu đề tab | Image: không mờ, đúng kích thước | Quan sát favicon và tiêu đề tab trình duyệt | Favicon rõ nét; tiêu đề tab mang tên sản phẩm/màn hình, không phải tên kỹ thuật | Optional |
| C3-14 | IA-01 | Mục menu | Hyperlink: Ctrl+click, đúng trang | Ctrl+click (hoặc chuột giữa) lên một mục menu | Hành vi theo chuẩn: nếu là liên kết thì mở tab mới đúng trang; nếu không phải liên kết thì không gây lỗi | Optional |

**Control không áp dụng (kèm lý do)**
- Text box, dropdown/combo box, radio button, date field: màn hình không có ô nhập liệu, danh sách chọn hay trường ngày.
- Image nội dung: màn hình không có ảnh; chỉ còn favicon.
- Hyperlink văn bản: không có liên kết dạng chữ trong vùng nội dung; chỉ có mục menu (đã xét ở C3-14).
- Nút Duyệt/Browse, nút Lưu/Hủy: không có.

**Khía cạnh GUI vẫn chưa phủ**
- IA-02 thật sự (form, validation, thông báo lỗi trường nhập): màn hình này không có ô nhập; cần màn hình khác (ví dụ Danh mục).
- Responsive (tablet, điện thoại, thu phóng 150–200%), dark mode, RTL.
- Accessibility sâu: đọc bằng trình đọc màn hình, thứ tự focus trên cả trang, tương phản ở chế độ tối.
- Dữ liệu lớn: bảng hàng trăm dòng, cuộn, tiêu đề cố định.
- Sắp xếp, tìm kiếm, phân trang (tính năng không có).

### Nhận xét sau khi chạy (ghi bởi người chạy prompt)
- AI xử lý đúng việc màn hình không có form: chỉ áp dụng checklist cho checkbox, nút, bảng, favicon, menu, và ghi "không áp dụng" cho text box, dropdown, radio, date.
- 14 mục, không có mục nào lặp Prompt 2. Phần IA-02 mỏng như dự kiến (8 mục, toàn bộ là checkbox và nút).
- Vài mục khá yếu hoặc khó có kết quả Pass/Fail rõ: C3-09 (hover), C3-13 (favicon), C3-14 (Ctrl+click vào mục không rõ có phải link không).

### Nhận xét của người kiểm thử
**Điểm tốt**
- AI xử lý đúng việc màn hình Admin Users không có form: chỉ áp dụng checklist cho các control thật sự có (checkbox, nút Xóa, bảng, favicon, menu) và ghi rõ "không áp dụng" cho text box, dropdown, radio, date field cùng lý do.
- 14 mục không lặp các ý đã phủ ở Prompt 2 (tôi đã liệt kê sẵn trong prompt). Mỗi mục ghi rõ nguồn từ checklist theo control của slide, ví dụ "Checkbox: Space đổi trạng thái", "Button: Space/Enter kích hoạt".
- Một số mục có giá trị mà Prompt 2 chưa có: checkbox tiêu đề chọn tất cả (C3-01, vốn bị thiếu ở Prompt 2), trạng thái trung gian của checkbox (C3-06), thứ tự Tab (C3-04), vùng bấm và tên truy cập (C3-05, C3-10).

**Hạn chế**
- IA-02 trên màn hình này chỉ có 8 mục, toàn bộ là checkbox và nút. Không có kiểm tra nhập liệu hay validation vì màn hình không có ô nhập. Đây là giới hạn của màn hình, không phải lỗi của AI, nhưng nó cho thấy IA-02 phải được bù ở màn hình khác (Danh mục).
- Một số mục yếu hoặc khó có kết quả Pass/Fail rõ: C3-09 (hover chỉ là hiệu ứng nhỏ), C3-13 (favicon), C3-14 (Ctrl+click vào mục menu mà chưa biết có phải liên kết). Kết quả mong đợi của C3-14 viết theo kiểu "nếu... thì..." nên chưa xác định.
- Một số mục chồng nhẹ với Prompt 2: C3-07 và C3-08 đụng tới bàn phím như AI-03-04 và AI-03-05, C3-10 chạm vào ngữ cảnh nút Xóa đã có ở AI-04-04.
- AI vẫn chưa phủ accessibility sâu, responsive, dark mode, RTL; nó tự nêu những điểm này trong phần "chưa phủ".

