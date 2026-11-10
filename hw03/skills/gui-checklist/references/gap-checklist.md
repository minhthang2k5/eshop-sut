# Mục AI hay bỏ sót và nguyên nhân

Dùng ở bước 7 của quy trình. Với mỗi mục bổ sung, chọn **đúng một** nguyên nhân và viết giải thích cụ thể cho màn hình đang làm (không viết chung chung).

## Ba nhóm nguyên nhân (theo đề)

| Nhóm | Khi nào chọn | Ví dụ |
|---|---|---|
| **Chất lượng prompt** | Prompt không yêu cầu hoặc không nhắc tới nên AI không sinh | dark mode, zoom 200%, trình đọc màn hình, thiết bị cảm ứng, chỉ khoanh vùng độ rộng desktop |
| **Giới hạn của model** | AI không thể biết khi chỉ làm việc trên mô tả; chỉ lộ ra khi chạy thật | menu không phải liên kết nên Tab bỏ qua, F5 về trang đầu, lỗi kỹ thuật thô khi nhập ký tự đặc biệt, bố cục vỡ ở 375 px, bảng hàng trăm dòng |
| **Đặc thù giao diện** | Màn hình có điểm riêng hoặc chưa từng được đưa vào prompt | màn hình chưa được phủ, nghiệp vụ riêng, luồng thật của nhóm |

## Danh sách khía cạnh cần rà soát

**Truy cập (accessibility)**: thuộc tính `lang` của trang; tên truy cập (accessible name) của nút, ô, checkbox; alt của ảnh; thứ tự focus toàn trang và viền focus; trình đọc màn hình (NVDA/Narrator) và landmark; tương phản (WCAG 1.4.3, 4.5:1); không chỉ dùng màu để truyền ý (WCAG 1.4.1); vùng chạm tối thiểu (24 px WCAG 2.5.8; 44 px trên cảm ứng).

**Hiển thị**: dark mode (`prefers-color-scheme`); RTL (`dir="rtl"`); zoom 200% (reflow); responsive tablet 768 và điện thoại 375; in ấn nếu liên quan; định dạng tiền, ngày, số nhất quán giữa các màn hình; tiêu đề tab và favicon.

**Điều hướng nâng cao**: URL theo trang; F5 giữ vị trí; Back/Forward; Ctrl+click mở tab mới; phiên hết hạn.

**Dữ liệu và trạng thái**: bảng hàng trăm dòng (phân trang, tiêu đề cố định, vị trí dòng mới); dữ liệu dài/ký tự đặc biệt; trạng thái rỗng thật; lỗi kỹ thuật lộ ra người dùng; thông báo lỗi bằng `alert` so với thông báo gắn với ô; hành động hủy diệt thiếu xác nhận; thao tác lặp (bấm hai lần).

**Quan sát khi chạy thật**: mở màn hình, thử như người dùng thật, ghi lại điều AI không thể biết. Đây là nhóm mục giá trị nhất; gắn nhãn "đã xác nhận khi chạy" và ghi ngày.

## Đánh dấu độ chắc chắn của mỗi mục bổ sung

- **Đã xác nhận khi chạy**: đã thấy hiện tượng trên ứng dụng thật.
- **Suy ra, chưa xác nhận**: xuất phát từ đọc mã nguồn hoặc suy luận; phải chạy thật trước khi kết luận Failed.
