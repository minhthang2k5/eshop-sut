# Prompt 4 – Form, validation và phản hồi (IA-02, IA-04) – Admin: Danh mục

- **Mục đích:** Phủ phần **form thật** mà màn hình Người dùng không có: ô nhập, validation, thông báo lỗi, phản hồi sau khi gửi. Đây là phần chính của **IA-02**, bổ sung thêm **IA-04** cho thao tác Thêm và Xóa danh mục.
- **Căn cứ lý thuyết:** slide GUI Testing, trang 11 (checklist Text Box), trang 13 (Button), trang 16 (validation: chữ/số, giới hạn ký tự, thông báo lỗi, "Golden rule": khi lỗi phải đưa focus về ô sai và làm nổi bật), trang 21 (lỗi dữ liệu thường gặp: bắt buộc không được kiểm tra, mặc định sai, dữ liệu trên màn hình cũ).
- **Nguồn mô tả:** quan sát trực tiếp trên SUT (trình duyệt tích hợp, đọc cấu trúc và văn bản trang) ngày 2026-11-10. Hình chụp màn hình lần này không dùng được do khung trình duyệt bị thu nhỏ, nên mô tả dựa trên cấu trúc trang và văn bản.
- **Tool AI dùng:** Claude Code (Claude Sonnet 5.5)
- **Ngày giờ chạy:** 2026-11-10 (giờ chính xác xem `AI_Audit_Log.md` do hook ghi)
- **Lưu ý:** phiên này đã đọc mã nguồn SUT trước đó; prompt yêu cầu chỉ dựa vào mô tả.

---

## Prompt (dán nguyên khối vào AI; prompt đã tự chứa đủ ngữ cảnh)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Hãy kiểm thử HỘP ĐEN: chỉ dựa vào bản mô tả dưới đây, KHÔNG đọc mã nguồn, KHÔNG suy đoán cách cài đặt bên trong.

## Màn hình: "Quản lý Danh mục" (tab "Danh mục" của Web Admin EShop, tiếng Việt)
- Cùng bố cục với các tab khác: menu tối bên trái (Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng, Đăng xuất), vùng nội dung bên phải nền sáng.
- Tiêu đề trang "Quản lý Danh mục".
- Một form nằm ngang gồm: một ô nhập văn bản một dòng có placeholder "Tên danh mục mới" (không thấy nhãn riêng), và một nút "Thêm mới" nền xanh.
- Bảng nền trắng, hàng tiêu đề nền xám, 3 cột: ID (hiển thị dạng #1, #2...), Tên Danh Mục, Hành động.
- Dữ liệu hiện có: 3 danh mục: #1 Điện thoại, #2 Laptop, #3 Phụ kiện. Mỗi dòng có nút "Xóa" nền đỏ chữ trắng.
- KHÔNG có: nút Sửa, ô tìm kiếm, phân trang, đánh dấu trường bắt buộc (dấu *), dropdown, checkbox, radio, ô ngày, ô số.

## Các ý ĐÃ được phủ ở bước trước ở tab Người dùng (không lặp lại, trừ khi áp dụng khác biệt cho màn hình này)
Bố cục 1366/1920; chính tả; tương phản nút Xóa; căn lề bảng; menu và nút Back/F5/Đăng xuất; trạng thái đang tải và lỗi tải; checkbox; nút Xóa nhận focus.

## Nhiệm vụ
Sinh mục checklist cho:
- IA-02 (Form): ô nhập, nhãn, ràng buộc, validation, thông báo lỗi, bàn phím.
- IA-04 (Phản hồi/trạng thái): kết quả của thao tác Thêm mới và Xóa.

### Checklist cần áp dụng (từ bài giảng)
Text box: nhãn đúng; đánh dấu trường bắt buộc; con trỏ nhấp nháy khi focus; độ rộng đúng và dừng ở giới hạn (thử với nhiều chữ "W"); từ chối chuỗi chỉ gồm khoảng trắng; thử số, ký tự đặc biệt (1 $ # + -), chữ và số; căn lề nhất quán với các phần tử xung quanh; hiện thanh cuộn hoặc cắt hợp lý khi nội dung vượt quá ô.
Validation: mọi quy tắc sai đều có thông báo hợp lý và người dùng phải sửa mới đi tiếp; trường bắt buộc phải bị bắt khi để trống; giới hạn ký tự bằng giới hạn cột dữ liệu và có thông báo khi chạm giới hạn; trường tùy chọn để trống không báo lỗi; thử mọi trường với ký tự đặc biệt. Golden rule: khi báo lỗi, đưa focus về ô sai và làm nổi bật ô đó.
Button: nhãn có nghĩa; Enter/Space kích hoạt; hành động không hoàn tác phải có xác nhận; bấm nhiều lần xử lý đúng; trạng thái bật/tắt phản ánh đúng.

## Quy tắc
- Mỗi mục là MỘT điểm kiểm tra, thực hiện được trong vài phút, có kết quả Passed/Failed.
- Cột "Kết quả mong đợi" chỉ nêu chuẩn tham chiếu, KHÔNG viết sẵn kết luận Passed/Failed.
- Mục cần giả lập điều kiện (tắt backend, dữ liệu rỗng) phải nêu rõ cách giả lập.
- Quy ước phân loại: quy tắc và thông báo lỗi gắn với ô nhập → IA-02; phản hồi hệ thống sau khi gửi hoặc xóa (thành công, thất bại, xác nhận, trạng thái rỗng) → IA-04.
- Khoảng 14–18 mục.

## Định dạng đầu ra
Một bảng Markdown:
| ID tạm | IA | Control | Nguồn checklist | Mục kiểm tra | Kết quả mong đợi | Mức ưu tiên (Mandatory/Optional) |

ID tạm dạng C4-01, C4-02, ...

Sau bảng:
1. Liệt kê control không áp dụng kèm lý do.
2. Nêu các khía cạnh GUI vẫn CHƯA phủ.

Trả lời bằng tiếng Việt.
```

---

## Ghi log

### Output của AI

| ID tạm | IA | Control | Nguồn checklist | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| C4-01 | IA-02 | Ô nhập "Tên danh mục mới" | Text box: nhãn đúng | Click vào ô, gõ một ký tự rồi quan sát; so với yêu cầu có nhãn nhìn thấy được | Ô có nhãn nhìn thấy cố định hoặc tên truy cập rõ; người dùng vẫn biết ô dùng để nhập gì sau khi placeholder biến mất | Mandatory |
| C4-02 | IA-02 | Ô nhập | Text box: con trỏ nhấp nháy, trạng thái ban đầu | Mở tab Danh mục, click vào ô nhập | Ô ban đầu trống, hiển thị placeholder; khi focus có con trỏ nhấp nháy và viền focus nhìn thấy được | Mandatory |
| C4-03 | IA-02 | Ô nhập | Text box: đánh dấu trường bắt buộc | Quan sát ô nhập và vùng form | Trường bắt buộc có dấu hiệu rõ (ví dụ dấu *) hoặc chú thích | Mandatory |
| C4-04 | IA-02 | Ô nhập + nút "Thêm mới" | Validation: trường bắt buộc bị bắt khi để trống | Để trống ô nhập rồi bấm "Thêm mới" | Không thêm danh mục; có thông báo lỗi rõ ràng, gần ô nhập, dễ hiểu | Mandatory |
| C4-05 | IA-02 | Ô nhập | Text box: từ chối chuỗi chỉ gồm khoảng trắng | Nhập chỉ vài dấu cách rồi bấm "Thêm mới" | Bị từ chối như trường hợp để trống, có thông báo | Mandatory |
| C4-06 | IA-02 | Ô nhập | Validation: ký tự đặc biệt | Nhập `<b>test</b> & "a" 'b' $#+-` rồi bấm "Thêm mới" | Hoặc bị từ chối kèm thông báo, hoặc được lưu và hiển thị nguyên văn (không bị biến thành định dạng) mà không làm vỡ bố cục | Mandatory |
| C4-07 | IA-02 | Ô nhập | Text box: độ rộng, dừng ở giới hạn | Nhập chuỗi rất dài (ví dụ 300 chữ "W") rồi bấm "Thêm mới" | Có giới hạn độ dài kèm thông báo khi chạm giới hạn; nếu chấp nhận thì bảng hiển thị không bị tràn hay đè cột | Mandatory |
| C4-08 | IA-02 | Ô nhập | Validation: thông báo cho mọi quy tắc sai | Nhập tên đã có (ví dụ "Laptop", rồi "laptop" viết thường) và bấm "Thêm mới" | Có thông báo rõ rằng tên trùng, không tạo bản sao ngầm | Mandatory |
| C4-09 | IA-02 | Ô nhập | Text box: chữ, số, ký tự lạ | Nhập tên có dấu tiếng Việt và ký tự khác (ví dụ "Điện thoại di động 2025", "Tai nghe 🎧") | Lưu và hiển thị đúng, không lỗi font hoặc mất dấu | Optional |
| C4-10 | IA-02 | Ô nhập + form | Button: Enter kích hoạt | Gõ tên hợp lệ trong ô nhập rồi nhấn Enter | Form được gửi như khi bấm "Thêm mới" | Mandatory |
| C4-11 | IA-02 | Ô nhập | Validation: khoảng trắng đầu/cuối | Nhập " Phụ kiện mới  " (có dấu cách đầu và cuối) rồi bấm "Thêm mới" | Khoảng trắng thừa được cắt hoặc bị từ chối; tên lưu không lệch do dấu cách | Optional |
| C4-12 | IA-02 | Ô nhập | Validation: golden rule (đưa focus về ô sai) | Gây lỗi (để trống) rồi bấm "Thêm mới" và quan sát focus | Focus quay về ô nhập và ô được làm nổi bật (viền đỏ hoặc tương đương) | Mandatory |
| C4-13 | IA-04 | Nút "Thêm mới" | Button: kết quả hành động | Nhập tên hợp lệ ("Màn hình") rồi bấm "Thêm mới" | Có phản hồi thành công; ô nhập được xóa; dòng mới xuất hiện trong bảng ngay không cần tải lại trang | Mandatory |
| C4-14 | IA-04 | Nút "Thêm mới" | Button: bấm nhiều lần xử lý đúng | Nhập tên hợp lệ rồi bấm "Thêm mới" hai lần liên tiếp thật nhanh | Chỉ tạo một danh mục; nút chuyển trạng thái đang xử lý hoặc bị vô hiệu | Mandatory |
| C4-15 | IA-04 | Nút "Thêm mới" | Validation: lỗi hệ thống | Tắt backend rồi nhập tên hợp lệ và bấm "Thêm mới" | Có thông báo lỗi dễ hiểu; nội dung đã nhập không bị mất | Mandatory |
| C4-16 | IA-04 | Nút "Xóa" | Button: hành động không hoàn tác phải có xác nhận | Bấm "Xóa" ở một danh mục thử nghiệm | Có bước xác nhận nêu rõ danh mục sẽ bị xóa và có lựa chọn Hủy; chưa xóa khi chưa xác nhận | Mandatory |
| C4-17 | IA-04 | Nút "Xóa" | Validation: ràng buộc dữ liệu | Xóa một danh mục đang có sản phẩm thuộc về nó (dùng dữ liệu thử) | Hệ thống chặn hoặc cảnh báo bằng lời dễ hiểu; không để lại sản phẩm mồ côi mà không báo | Mandatory |
| C4-18 | IA-04 | Bảng danh mục | Trạng thái rỗng | Xóa hết danh mục thử nghiệm (hoặc dùng cơ sở dữ liệu trống) | Có thông báo "chưa có danh mục" thay vì chỉ còn hàng tiêu đề | Optional |

**Control không áp dụng (kèm lý do)**
- Dropdown, radio, checkbox, ô ngày, ô số: màn hình không có các control này.
- Validation số (giá trị biên, âm, 0): không có trường số.
- Nút Sửa/Lưu/Hủy: không có chức năng sửa.

**Khía cạnh GUI vẫn chưa phủ**
- Responsive: form nằm ngang có xuống dòng gọn khi cửa sổ hẹp không.
- Accessibility: nhãn truy cập cho ô nhập, thứ tự focus, tương phản ở chế độ tối.
- Dark mode, RTL.
- Danh sách rất dài (hàng trăm danh mục): cuộn, hiệu năng.
- Sắp xếp và tìm kiếm danh mục (không có).
- Thông báo lỗi bằng cửa sổ chặn (alert) so với thông báo gắn với ô: chuẩn nên dùng cái nào chưa có tiêu chí rõ.

### Nhận xét của người kiểm thử
**Điểm tốt**
- Prompt 4 bù đúng phần IA-02 mà màn hình Người dùng không có: 12 mục về ô nhập "Tên danh mục mới" (nhãn, trường bắt buộc, để trống, chỉ khoảng trắng, ký tự đặc biệt, chuỗi quá dài, tên trùng, dấu tiếng Việt, khoảng trắng đầu/cuối, phím Enter, đưa focus về ô sai). Phần lớn bám sát checklist Text Box và Validation ở trang 11 và 16 của slide, kể cả "golden rule" (C4-12).
- Việc AI tách IA-02 (quy tắc và lỗi gắn với ô nhập) khỏi IA-04 (phản hồi sau khi gửi hoặc xóa) theo quy ước tôi nêu trong prompt giúp phân loại rõ, ít chồng chéo.
- Nhiều mục có cách thực hiện cụ thể, dùng được ngay (chuỗi thử `<b>test</b> & "a" 'b' $#+-`, 300 chữ "W", tên trùng "Laptop"/"laptop", tắt backend để gây lỗi hệ thống).
- AI xử lý đúng control không áp dụng: không sinh mục về dropdown, radio, ô số, ô ngày, không có nút Sửa.

**Hạn chế**
- Chưa có mục kiểm tra chi tiết kích thước/độ rộng ô nhập và việc xử lý khi nội dung vượt quá ô, ngoài C4-07.
- Một số cặp mục gần nhau và có thể bị coi là lặp ý: C4-04 và C4-05 (để trống và chỉ khoảng trắng), C4-13 và C4-14 (cùng nút Thêm mới).
- C4-06 có kết quả mong đợi theo kiểu "hoặc... hoặc...", nên khi chạy khó kết luận Passed/Failed rõ ràng.
- Mục C4-17 (xóa danh mục đang có sản phẩm) cần dữ liệu thử có ràng buộc; C4-15 và C4-18 cần giả lập (tắt backend, xóa hết danh mục), nên tốn công thực hiện và có thể làm hỏng dữ liệu mẫu.
- AI vẫn chưa phủ responsive của form nằm ngang, accessibility (nhãn truy cập, thứ tự focus), dark mode, RTL; nó tự nêu những điểm này ở phần "chưa phủ".
