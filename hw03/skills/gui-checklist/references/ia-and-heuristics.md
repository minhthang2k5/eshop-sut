# Khía cạnh giao diện (IA) và nguyên tắc thiết kế

Nguồn: slide GUI Testing (Part 1, trang 6–9) và định nghĩa IA của đề HW03.

## Bốn khía cạnh giao diện (IA)

| IA | Tên | Câu hỏi nó trả lời |
|---|---|---|
| IA-01 | Chuẩn UI chung | Giao diện có nhất quán, dễ đọc, đúng chuẩn không? (font, màu, căn lề, chính tả, tương phản, ảnh/biểu tượng) |
| IA-02 | Form | Ô nhập liệu và điều khiển có dùng được, rõ ràng, kiểm soát đầu vào không? (nhãn, ràng buộc, validation, bàn phím) |
| IA-03 | Điều hướng | Người dùng có đi lại giữa các màn hình dễ dàng không? (menu, vị trí hiện tại, Back, F5, thoát) |
| IA-04 | Phản hồi / trạng thái | Hệ thống có cho biết chuyện gì đang xảy ra không? (loading, thành công/lỗi, xác nhận, trạng thái rỗng) |

### Quy ước phân loại khi chồng nhau (giữ nhất quán trong cả bảng)

- Quy tắc, nhãn, thông báo lỗi **gắn với một ô nhập** → IA-02.
- Phản hồi của hệ thống **sau khi gửi hoặc thao tác** (thành công, thất bại, xác nhận, rỗng) → IA-04.
- Thao tác bàn phím trên menu → IA-03; trên ô nhập hoặc nút của form → IA-02.
- Vùng chạm, tên truy cập của control → IA-02; tương phản và hiển thị → IA-01.

## Nielsen 10 heuristics

1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

## Norman 6 principles

Visibility ("Tôi có thấy nó không?"), Feedback ("Nó đang làm gì?"), Affordance ("Dùng nó thế nào?"), Mapping, Constraints ("Vì sao tôi không làm được?"), Consistency.

## Shneiderman 8 Golden Rules

1. Strive for consistency
2. Enable frequent users to use shortcuts
3. Offer informative feedback
4. Design dialogues to yield closure
5. Offer simple error handling
6. Permit easy reversal of actions
7. Support internal locus of control
8. Reduce short-term memory load

## Đầu vào tốt của một GUI checklist (slide trang 9)

Yêu cầu và đặc tả UI; Nielsen 10, Norman 6, Shneiderman 8; hướng dẫn nền tảng và WCAG; checklist theo từng control. Chấm từng mục Yes/No/N/A kèm priority (Mandatory/Optional) và severity.
