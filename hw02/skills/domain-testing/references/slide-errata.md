# Lỗi và điểm cần diễn giải trong slide

Đã đối chiếu text và ảnh các trang liên quan của `S04_Domain Testing.pdf` (29 trang PDF; slide có nội dung đến 28). Số slide dưới đây trùng số trang PDF. Tách lỗi chắc chắn, điểm thiếu nhất quán và phần mở rộng do skill bổ sung.

| Slide | Quan sát | Cách xử lý |
|---|---|---|
| 24 | Dòng lỗi cuối ghi `25 >= INPUT`, chồng lên miền `10 <= INPUT < 25`. | Sửa thành `INPUT >= 25`. Ba miền là INPUT < 10, 10 <= INPUT < 25, INPUT >= 25. |
| 27, TC2 | A=-99, B=9 nhưng Expected Output=90. | Sửa thành **-90**. |
| 27, TC3 | A=-98, B=9 nhưng Expected Output=89. | Sửa thành **-89**. |
| 27, TC8 | A=10, B=-99 nhưng Expected Output=89. | Sửa thành **-89**. |
| 27, TC9 | A=10, B=-98 nhưng Expected Output=88. | Sửa thành **-88**. |
| 27, TC7 | A=-10 trong khi các test biên B khác giữ A=10. | Dùng A=10 cho nhất quán. **-10 vẫn là Valid**, nên không phải lỗi cô lập Invalid và không làm Expected Output “Invalid Input” sai. |
| 26 | Hình ghi `UB-1` cho cả điểm phía trong và điểm phía ngoài UB. | Điểm ngoài phía trên phải là **UB+1**; điểm trong là UB-1. |
| 26 | Có chín vị trí nhưng sáu giá trị sát biên và hai cực trị UI chỉ cộng thành tám. | Điểm 1 là đại diện Valid bên trong; sáu điểm sát biên là 2–7, cực trị UI là 8–9. Đây là tối đa điểm ứng viên; gộp trùng, không bịa cực trị UI. |

## Slide 12: “not an integer” kèm khoảng giá trị

Slide vừa chia theo kiểu (integer/not integer), vừa chia theo khoảng, rồi ghi các khoảng trong ngoặc sau “not an integer”. Không áp phép so sánh số cho mọi dữ liệu không nguyên.

- Với mô hình kết hợp, dùng: số nguyên 1..99 (Valid), số nguyên <=0 (Invalid), số nguyên >=100 (Invalid), không phải số nguyên (Invalid).
- Số thập phân hữu hạn như 1.5 có thể so sánh theo khoảng, nhưng vẫn vi phạm kiểu. Chuỗi `abc` không có vị trí số học trong ba khoảng này.
- Nếu tách theo hai trục kiểu/khoảng để bám cách trình bày ban đầu, nêu rõ các class có thể giao nhau và chỉ xét range khi giá trị có ý nghĩa số. Không đếm một test 1.5 là “hai Invalid” nếu toàn bộ mô hình đã gom nó vào class sai kiểu.
- Null, missing, boolean, whitespace và quy tắc chuyển chuỗi thành số phụ thuộc spec/interface; ghi giả định, không tự coi chúng là số nguyên.

## Slide 7, 22–23: giữ Output EC riêng

EC9 là nhánh SUM=A+B; EC10 là nhánh phản hồi lỗi. Dòng EC10 bị xuống dòng thành “EC1 / 0” trong bảng slide 7, nhưng là **EC10**, không phải EC1 và EC0.

Đánh dấu EC9 là Valid output branch, EC10 là Invalid-input response branch. Một test lỗi phủ EC2 và EC10 chỉ có một lỗi Input; không được đếm EC10 thành lỗi thứ hai. Giữ hai EC này trong bảng Complete set of partitions và bảng coverage.

## Slide 5: “cùng expected result” và kết quả tính toán

Đọc “giống nhau” theo quy tắc/hành vi xử lý như ví dụ cộng ở slide 7, 22–23, không gộp tất cả output vào một hằng số. Các input hợp lệ có thể cùng EC dù SUM khác nhau; oracle phải tính lại SUM của từng test.

## Slide 13: ví dụ chữ hoa chưa bao phủ hết phần bù

Invalid “ký tự đầu viết thường” chưa bao gồm ký tự đầu là số, dấu câu hoặc khoảng trắng. Dùng phần bù “không phải chữ hoa” trong miền ký tự đã xác định; có thể tách các class nhỏ hơn khi có rủi ro xử lý khác nhau. Xem chuỗi rỗng theo điều kiện độ dài, không đọc ký tự đầu không tồn tại.

## Slide 19: “first 2 characters are not letters”

Diễn giải Invalid là phủ định của “cả hai vị trí đều là chữ”: **ít nhất một vị trí không phải chữ**, chứ không chỉ trường hợp cả hai không phải chữ. Ví dụ `1b3`, `A23`, `123`. Nếu cần tách nhỏ, giữ rõ một điều kiện tổng hợp hay hai điều kiện vị trí độc lập để không vi phạm quy tắc chọn Invalid test.

## Phần bổ sung của skill, không phải bài giải có sẵn trên slide

- Slide 15–20 chỉ phân tích widget EC; ví dụ hoàn chỉnh gồm coverage, minimum set và BVA trong examples.md là phần skill xây dựng thêm.
- Các ví dụ số nguyên dương, chuỗi và tọa độ cũng được bổ sung bảng chọn test/BVA; các giả định được ghi riêng.
- ASCII, cách đếm ký tự, mô tả phản hồi từ chối và miền số nguyên của tọa độ trong ví dụ là giả định để minh họa, không phải yêu cầu được xác nhận từ slide.
- Không diễn giải “biên bắt cả hai lỗi” của slide 25 thành lời hứa BVA bắt mọi bug; kết luận chỉ áp dụng hai biến thể lỗi trong ví dụ mốc 25.
