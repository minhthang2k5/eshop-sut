# Checklist theo từng control

Nguồn: slide GUI Testing (Part 1, trang 10–16, Waghmare 2009). Chỉ áp dụng cho control **có thật** trên màn hình; control không có thì ghi "Không áp dụng" kèm lý do.

## Text box
- Bật/tắt đúng đặc tả; khi tắt thì xám, không có con trỏ, không sửa được.
- Giá trị ban đầu đúng (trống hoặc điền sẵn); con trỏ nhấp nháy khi focus.
- Trường bắt buộc có dấu * đỏ.
- Dừng ở độ rộng tối đa (thử nhiều chữ "W"); độ rộng đúng đặc tả.
- Từ chối chuỗi chỉ gồm khoảng trắng; thử khoảng trắng kèm ký tự.
- Thử số, ký tự đặc biệt (1 $ # + -), chữ và số.
- Có mặt nạ định dạng khi cần (ví dụ SSN); từ chối giá trị quá ngắn.
- Nhãn đúng; căn lề nhất quán với phần tử xung quanh.
- Có thanh cuộn hoặc cắt hợp lý khi nội dung vượt quá ô.
- Nhấp đúp chọn tất cả; con trỏ đổi khi rê qua ô sửa được.

## Dropdown / Combo box
- Có mũi tên; giá trị mặc định hoặc trống; trường bắt buộc có nhận giá trị trống không.
- Từ chối giá trị ngoài danh sách; danh sách không rỗng; có thanh cuộn khi dài.
- Gõ chữ cái đầu chọn được mục; danh sách sắp xếp; tên không bị cắt.
- Mục đã chọn hiện ở đầu khi mở lại.
- Combo sửa được: nhập chữ/ký tự đặc biệt; giá trị gõ trùng giá trị danh sách không bị coi là khác.
- Dropdown thuần: không gõ tự do; Alt+Xuống mở danh sách.

## Button
- Bật/tắt đúng; Tab tới theo thứ tự; ảnh đổi khi click.
- Click đơn, đúp, nhiều lần xử lý đúng.
- Hover có hiệu ứng và tooltip.
- Một nút mặc định kích hoạt bằng Enter; Hủy bằng Esc.
- Nhãn có nghĩa, không viết tắt khó hiểu; "…" nếu mở màn hình khác.
- Alt + chữ gạch chân kích hoạt; Space kích hoạt khi đang focus; không trùng phím nóng.
- Hành động không hoàn tác phải có xác nhận Có/Không.
- Mọi nút cùng kích thước, hình dạng, font; màu thể hiện ý nghĩa (xanh = đi tiếp, đỏ = hủy diệt).

## Checkbox
- Bật/tắt; mặc định đúng; nhãn phù hợp.
- Tab chuyển tuần tự; chuột, Space, Enter, Alt+chữ đều đổi trạng thái; bấm vào chữ nhãn cũng đổi.
- Sự kiện đúng khi đổi; căn lề đúng; vùng bấm đủ lớn.

## Radio / Option group
- Mặc định đúng; chỉ chọn được MỘT mục trong nhóm.
- Phím mũi tên đổi lựa chọn trong nhóm; chuột, Space, Enter, Alt+chữ đổi lựa chọn.
- Xử lý giá trị trống từ CSDL cho tập cố định.

## Hyperlink / mục điều hướng
- Màu chuẩn, gạch chân đủ mọi ký tự; mở bằng click, Enter, Ctrl+click.
- Tab đi tới được; dẫn đúng trang; không bị chết.

## Image / biểu tượng
- Không mờ, đúng kích thước, không vỡ, căn lề đúng; có thuộc tính alt khi là ảnh nội dung.

## Grid / bảng
- Có tiêu đề cột và tiêu đề bảng; click tiêu đề sắp xếp tăng/giảm kèm biểu tượng (nếu có).
- Cuộn bằng phím, chuột, nút; nhấp đúp dòng kích hoạt đúng sự kiện.
- Hiển thị đúng số dòng; dòng được chọn khác biệt; trạng thái rỗng.

## List box
- Chọn đơn bằng chuột/mũi tên; gõ chữ nhảy tới mục khớp; nhấp đúp = chọn và mở; thanh cuộn khi cần.

## Date field
- Năm nhuận; từ chối tháng 00/13, ngày 00/32, 30/2; đổi thế kỷ; đúng định dạng nhập.

## Validation đầu vào (nơi nhiều lỗi GUI nhất)
- Số: thấp nhất, cao nhất, vừa trong miền, ngoài miền hai phía; rỗng ở đầu và cuối; dấu + và −; không chia cho 0; quyết định có cho số âm và số 0 không.
- Chữ: rỗng và không rỗng; ký tự và ký hiệu không hợp lệ; ký tự hợp lệ.
- Mọi quy tắc sai đều có thông báo hợp lý và người dùng phải sửa mới đi tiếp.
- Trường bắt buộc khi cột CSDL NOT NULL; có dấu *.
- Giới hạn ký tự bằng kích thước cột CSDL và có thông báo "giới hạn N ký tự".
- Trường tùy chọn để trống thì không báo lỗi; thử mọi trường với ký tự đặc biệt.
- **Golden rule:** khi báo lỗi, đưa focus về ô sai và làm nổi bật nó, kể cả khi người dùng bấm OK mà chưa rời ô.

## Lỗi GUI thường gặp (trang 21, để gợi ý mục bổ sung)
Lỗi validation; giá trị mặc định sai; trường bắt buộc không được kiểm tra; truy vấn lấy sai trường hoặc nhiều dòng; dữ liệu trên màn hình cũ; sai modal; trạng thái control và menu lệch với trạng thái dữ liệu.
