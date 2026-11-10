# Prompt 8 – Mục theo từng control (IA-01, IA-02) – Admin: Đơn hàng

> Chạy bằng skill `gui-checklist` (bước 4). Màn hình không có form nên bỏ bước 5.

- **Căn cứ lý thuyết:** slide GUI Testing, trang 10–15 (checklist theo control: Button, Grid, Image...).
- **Tool AI dùng:** Claude Code (Claude Sonnet 5.5), ngày 2026-11-10.
- **Lưu ý:** phiên này đã đọc mã nguồn SUT trước đó; prompt yêu cầu chỉ dựa vào mô tả.
- **IA-02 ở màn hình này mỏng:** không có ô nhập, nên IA-02 chỉ có nút hành động. Phần validation form đã được phủ ở tab Danh mục.

---

## Prompt (dán nguyên khối vào AI; tự chứa đủ ngữ cảnh)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Kiểm thử HỘP ĐEN: chỉ dựa vào mô tả dưới đây, KHÔNG đọc mã nguồn.

## Màn hình: "Quản lý Đơn hàng" (tab "Đơn hàng", Web Admin EShop, tiếng Việt)
- Bảng 6 cột: ID (#5...), Người đặt, Tổng tiền (150,000 ₫), Địa chỉ, Trạng thái (nhãn chữ có màu nền), Hành động (các nút nhỏ xếp dọc: Xác nhận, Hủy, Giao hàng, Hoàn thành, Đánh dấu Đã giao; nút Hủy màu xám).
- 5 đơn thử đủ 5 trạng thái. KHÔNG có: tìm kiếm, lọc, sắp xếp, phân trang, ô nhập liệu, ảnh, liên kết.
- Đặc tả: địa chỉ phải hiển thị an toàn (không render HTML).

## Các ý ĐÃ phủ ở bước trước (KHÔNG lặp)
Định dạng cột Tổng tiền; nhãn trạng thái (chữ, màu, tương phản); tương phản và màu nút; cỡ chữ và bo góc nút; căn lề bảng; địa chỉ dài; thứ tự dòng; thứ tự Tab trong bảng; xác nhận khi đổi trạng thái; bấm nút liên tiếp; lỗi đổi trạng thái.

## Nhiệm vụ
Áp dụng checklist THEO TỪNG CONTROL lên control có thật (Button, Grid/bảng) cho IA-01 và IA-02. Control không có thì ghi "Không áp dụng" kèm lý do.

Checklist cần áp dụng:
- Button: Tab tới theo thứ tự; Space/Enter kích hoạt; hover có hiệu ứng; nhãn có nghĩa, không mơ hồ; mọi nút cùng kích thước/hình dạng/font; vùng bấm đủ lớn (WCAG 2.5.8: tối thiểu 24×24 px).
- Grid: tiêu đề cột đầy đủ; hiển thị đúng số dòng; cuộn bằng phím/chuột; nhấp đúp dòng không gây hành vi bất ngờ; dòng được chọn khác biệt.

## Quy tắc
- Mỗi mục MỘT điểm kiểm tra, có Passed/Failed; kết quả mong đợi MỘT tiêu chí đo được; không viết sẵn kết luận.
- Nêu cách thực hiện cụ thể (chuỗi thử, công cụ, kích thước). Mục cần dữ liệu phải ghi cách tạo (POST /api/checkout bằng tài khoản khách); KHÔNG tắt backend.
- Không lặp danh sách ĐÃ phủ. Khoảng 8–10 mục.

## Định dạng
Bảng Markdown: | ID tạm | IA | Control | Nguồn checklist | Mục kiểm tra | Kết quả mong đợi | Ưu tiên (Mandatory/Optional) |
ID dạng O8-01... Sau bảng: control không áp dụng kèm lý do; khía cạnh còn chưa phủ. Trả lời tiếng Việt.
```

---

## Ghi log

### Output của AI

| ID tạm | IA | Control | Nguồn checklist | Mục kiểm tra | Kết quả mong đợi | Ưu tiên |
|---|---|---|---|---|---|---|
| O8-01 | IA-02 | Nút hành động | Button: Space/Enter kích hoạt | Nhấn Tab tới nút "Xác nhận" của đơn thử #5 rồi nhấn Enter; làm lại với một đơn thử khác bằng Space | Cả Enter và Space cho kết quả giống click chuột | Mandatory |
| O8-02 | IA-02 | Nút hành động | Button: hover có hiệu ứng | Rê chuột lên từng loại nút hành động | Con trỏ đổi thành bàn tay và màu nền nút thay đổi | Optional |
| O8-03 | IA-02 | Nút "Hủy" | Button: nhãn có nghĩa | Mở DevTools > Accessibility, chọn nút "Hủy" của hai đơn khác nhau, đọc Computed name | Tên truy cập nêu mã đơn (ví dụ "Hủy đơn #5"), phân biệt được nút của các đơn khác nhau | Optional |
| O8-04 | IA-02 | Nút hành động | Button: vùng bấm đủ lớn (WCAG 2.5.8) | Đo chiều cao và chiều rộng các nút bằng DevTools (box model) | Mọi nút có vùng bấm tối thiểu 24×24 px | Mandatory |
| O8-05 | IA-02 | Hai nút xếp dọc | Button: tránh bấm nhầm | Đo khoảng cách giữa nút "Xác nhận" và "Hủy" trong cùng một ô | Khoảng cách tối thiểu 8 px giữa hai nút | Optional |
| O8-06 | IA-01 | Bảng | Grid: hiển thị đúng số dòng | So số dòng trên bảng với kết quả GET /api/admin/orders | Số dòng bằng số đơn trả về | Mandatory |
| O8-07 | IA-01 | Cột Địa chỉ | Grid: ký tự đặc biệt hiển thị an toàn (FR-18) | Tạo đơn có địa chỉ `<b>1 Le Loi</b> & "Q1"` bằng POST /api/checkout rồi xem bảng | Địa chỉ hiển thị nguyên văn, không thành chữ đậm | Mandatory |
| O8-08 | IA-01 | Bảng | Grid: cuộn và tiêu đề cố định | Tạo 30 đơn thử bằng API, cuộn bảng xuống cuối | Tiêu đề cột luôn nhìn thấy khi cuộn | Optional |
| O8-09 | IA-01 | Dòng đơn hàng | Grid: nhấp đúp dòng | Nhấp đúp vào một dòng đơn hàng | Không có thay đổi dữ liệu hay điều hướng bất ngờ | Optional |
| O8-10 | IA-01 | Dòng đơn hàng | Grid: dòng được chọn khác biệt | Rê chuột và nhấp vào một dòng, quan sát nền dòng | Dòng đang rê chuột có nền khác dòng còn lại | Optional |

**Control không áp dụng:** text box, dropdown, checkbox, radio, ô ngày (không có ô nhập hay lựa chọn); hyperlink và image (không có liên kết hay ảnh).

**Khía cạnh còn chưa phủ:** accessibility sâu bằng trình đọc màn hình, vùng chạm 44 px trên cảm ứng, dark mode và responsive của riêng bảng này (đã có mục cho toàn Admin).

### Nhận xét của người kiểm thử
_(mục nào yếu hoặc trùng? có mục nào cần dữ liệu khó tạo?)_
