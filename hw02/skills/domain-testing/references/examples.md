# Ví dụ hoàn chỉnh: EP và BVA

Mỗi ví dụ đi qua bốn bước: Input/Output, EC, chọn test và BVA; sau đó tự kiểm tra và ghi giả định. Đánh số EC độc lập trong từng ví dụ. Các bảng không biểu thị kết quả thực thi.

Nguồn: `S04_Domain Testing.pdf`, CSC13003 HCMUS. Ví dụ cộng dựa trên slide 4–7, 22–23, 27; các ví dụ còn lại lấy spec từ slide 12–20 rồi bổ sung phần chọn test và BVA. Dùng slide-errata.md để phân biệt nội dung gốc và phần sửa/bổ sung.

## A. Cộng hai số nguyên trong -99..99

### (1) Input/Output variables

| Biến | Input/Output | Kiểu | Ràng buộc |
|---|---|---|---|
| A | Input | integer hoặc raw input sai kiểu | -99 <= A <= 99 |
| B | Input | integer hoặc raw input sai kiểu | -99 <= B <= 99 |
| SUM | Output | integer | A+B khi cả hai Input Valid |
| Error | Output | phản hồi lỗi | Invalid Input nếu một Input Invalid |

### (2) Equivalence Classes

| STT | Input/Output | Equivalence Class | Valid/Invalid |
|---|---|---|---|
| EC1 | Input A | A nguyên, -99 <= A <= 99 | Valid |
| EC2 | Input A | A nguyên, A < -99 | Invalid |
| EC3 | Input A | A nguyên, A > 99 | Invalid |
| EC4 | Input A | A không phải số nguyên | Invalid |
| EC5 | Input B | B nguyên, -99 <= B <= 99 | Valid |
| EC6 | Input B | B nguyên, B < -99 | Invalid |
| EC7 | Input B | B nguyên, B > 99 | Invalid |
| EC8 | Input B | B không phải số nguyên | Invalid |
| EC9 | Output SUM | Trả SUM=A+B khi cả hai Valid | Valid |
| EC10 | Output Error | Trả Invalid Input khi có Input Invalid | Invalid |

### (3) Chọn test case

**Test cases providing coverage of partitions** — truy vết từng EC; TC được phép lặp ở bảng này.

| #TC | Partitions Tested | A | B | Expected Output |
|---|---|---|---|---|
| TC1 | EC1 | 10 | 9 | 19 |
| TC2 | EC2 | -102 | 9 | Invalid Input |
| TC3 | EC3 | 102 | 9 | Invalid Input |
| TC4 | EC4 | "Abc" | 9 | Invalid Input |
| TC1 | EC5 | 10 | 9 | 19 |
| TC5 | EC6 | 10 | -200 | Invalid Input |
| TC6 | EC7 | 10 | 200 | Invalid Input |
| TC7 | EC8 | 10 | 1.25 | Invalid Input |
| TC1 | EC9 | 10 | 9 | 19 |
| TC2 | EC10 | -102 | 9 | Invalid Input |

**Minimum set of test cases**

| #TC | Partitions Tested | A | B | Expected Output |
|---|---|---|---|---|
| TC1 | EC1, EC5, EC9 | 10 | 9 | 19 |
| TC2 | EC2, EC5, EC10 | -102 | 9 | Invalid Input |
| TC3 | EC3, EC5, EC10 | 102 | 9 | Invalid Input |
| TC4 | EC4, EC5, EC10 | "Abc" | 9 | Invalid Input |
| TC5 | EC1, EC6, EC10 | 10 | -200 | Invalid Input |
| TC6 | EC1, EC7, EC10 | 10 | 200 | Invalid Input |
| TC7 | EC1, EC8, EC10 | 10 | 1.25 | Invalid Input |

Sáu Invalid EC Input phải cô lập, cộng ít nhất một Valid test: tối thiểu bảy test trong mô hình này. EC10 không cộng thêm một lỗi Input.

### (4) Boundary Value Test Cases

LB=-99, UB=99, delta=1. Giữ B=9 khi thay A; giữ A=10 khi thay B. Điểm danh nghĩa (10,9) đã ở TC1. Chưa biết min/max UI nên không thêm cực trị UI. Hai partition Invalid mỗi biến được phủ tại ranh giới hữu hạn -100/100.

| #TC | Biến/điểm biên | Partitions Tested | A | B | Expected Output |
|---|---|---|---|---|---|
| BVA1 | A: LB-1 | EC2, EC5, EC10 | -100 | 9 | Invalid Input |
| BVA2 | A: LB | EC1, EC5, EC9 | -99 | 9 | -90 |
| BVA3 | A: LB+1 | EC1, EC5, EC9 | -98 | 9 | -89 |
| BVA4 | A: UB-1 | EC1, EC5, EC9 | 98 | 9 | 107 |
| BVA5 | A: UB | EC1, EC5, EC9 | 99 | 9 | 108 |
| BVA6 | A: UB+1 | EC3, EC5, EC10 | 100 | 9 | Invalid Input |
| BVA7 | B: LB-1 | EC1, EC6, EC10 | 10 | -100 | Invalid Input |
| BVA8 | B: LB | EC1, EC5, EC9 | 10 | -99 | -89 |
| BVA9 | B: LB+1 | EC1, EC5, EC9 | 10 | -98 | -88 |
| BVA10 | B: UB-1 | EC1, EC5, EC9 | 10 | 98 | 108 |
| BVA11 | B: UB | EC1, EC5, EC9 | 10 | 99 | 109 |
| BVA12 | B: UB+1 | EC1, EC7, EC10 | 10 | 100 | Invalid Input |

### (5) Checklist

- [x] EC1–EC10 được phủ, sáu test Invalid chỉ sai một Input, phép cộng đã tính lại.
- [x] Biên từng biến giữ biến còn lại Valid; lỗi Expected Output âm trên slide đã sửa.

### (6) Giả định và điểm yếu

Mô hình theo ví dụ slide: số nguyên, không chấp nhận 1.25; literal "Abc" là chuỗi nhập, không phải code. Cách xử lý chuỗi biểu diễn số, whitespace, missing và UI limits chưa có trong slide. Giới hạn SUM suy ra là -198..198; có thể bổ sung (-99,-99) và (99,99) để kiểm tra biên Output. Đây là hai test bổ sung Valid, không thay mười hai test thay từng biến. Một đại diện Valid không đảm bảo bắt lỗi đặc biệt tại 0 hoặc lỗi phép cộng giữa miền.

## B. Số nguyên dương nhỏ hơn 100

### (1) Input/Output variables

| Biến | Input/Output | Kiểu | Ràng buộc |
|---|---|---|---|
| x | Input | integer hoặc raw input sai kiểu | x nguyên và 0 < x < 100 |
| Result | Output | kết quả validation | Chấp nhận hoặc Từ chối |

### (2) Equivalence Classes

| STT | Input/Output | Equivalence Class | Valid/Invalid |
|---|---|---|---|
| EC1 | Input x | x nguyên, 1 <= x <= 99 | Valid |
| EC2 | Input x | x nguyên, x <= 0 | Invalid |
| EC3 | Input x | x nguyên, x >= 100 | Invalid |
| EC4 | Input x | x không phải số nguyên | Invalid |
| EC5 | Output Result | Chấp nhận | Valid |
| EC6 | Output Result | Từ chối | Invalid |

### (3) Chọn test case

**Test cases providing coverage of partitions**

| #TC | Partitions Tested | x | Expected Output |
|---|---|---|---|
| TC1 | EC1 | 50 | Chấp nhận |
| TC2 | EC2 | -5 | Từ chối |
| TC3 | EC3 | 120 | Từ chối |
| TC4 | EC4 | 1.5 | Từ chối |
| TC1 | EC5 | 50 | Chấp nhận |
| TC2 | EC6 | -5 | Từ chối |

**Minimum set of test cases**

| #TC | Partitions Tested | x | Expected Output |
|---|---|---|---|
| TC1 | EC1, EC5 | 50 | Chấp nhận |
| TC2 | EC2, EC6 | -5 | Từ chối |
| TC3 | EC3, EC6 | 120 | Từ chối |
| TC4 | EC4, EC6 | 1.5 | Từ chối |

Ba Invalid EC loại trừ nhau và một Valid EC: bốn test là tối thiểu trong mô hình hợp nhất này.

### (4) Boundary Value Test Cases

Đổi khoảng mở (0,100) thành LB=1, UB=99 trên số nguyên. delta=1, nominal=50 đã có trong EP; UI limits chưa biết. Sai kiểu không có thứ tự, tiếp tục dùng TC4; có thể thêm "abc" khi có căn cứ parser xử lý khác.

| #TC | Biến/điểm biên | Partitions Tested | x | Expected Output |
|---|---|---|---|---|
| BVA1 | LB-1 | EC2, EC6 | 0 | Từ chối |
| BVA2 | LB | EC1, EC5 | 1 | Chấp nhận |
| BVA3 | LB+1 | EC1, EC5 | 2 | Chấp nhận |
| BVA4 | UB-1 | EC1, EC5 | 98 | Chấp nhận |
| BVA5 | UB | EC1, EC5 | 99 | Chấp nhận |
| BVA6 | UB+1 | EC3, EC6 | 100 | Từ chối |

### (5) Checklist

- [x] EC1–EC6 đều phủ; 1.5 chỉ ở EC sai kiểu, không bị gán thêm range Invalid.
- [x] Mốc 0 và 100 bị loại; 1 và 99 được nhận.

### (6) Giả định và điểm yếu

“Chấp nhận/Từ chối” mô tả hành vi validation, không phải chuỗi UI được slide xác nhận. Không gán khoảng cho "abc". Việc parse "1.0", chuỗi rỗng, null hoặc trim cần spec bổ sung. EP/BVA không kiểm tra đầy đủ mọi cách parse dữ liệu.

## C. Chuỗi dài đúng 7 ký tự, ký tự đầu viết hoa

### (1) Input/Output variables

| Biến | Input/Output | Kiểu | Ràng buộc |
|---|---|---|---|
| s | Input | chuỗi ASCII trong ví dụ này | length=7; ký tự đầu thuộc A–Z |
| Result | Output | kết quả validation | Chấp nhận hoặc Từ chối |

### (2) Equivalence Classes

| STT | Input/Output | Equivalence Class | Valid/Invalid |
|---|---|---|---|
| EC1 | Input length(s) | length=7 | Valid |
| EC2 | Input length(s) | length<7 | Invalid |
| EC3 | Input length(s) | length>7 | Invalid |
| EC4 | Input first(s), s không rỗng | ký tự đầu là A–Z | Valid |
| EC5 | Input first(s), s không rỗng | ký tự đầu không là A–Z | Invalid |
| EC6 | Output Result | Chấp nhận | Valid |
| EC7 | Output Result | Từ chối | Invalid |

### (3) Chọn test case

**Test cases providing coverage of partitions**

| #TC | Partitions Tested | s | Expected Output |
|---|---|---|---|
| TC1 | EC1 | "Abcdefg" | Chấp nhận |
| TC2 | EC2 | "Abcdef" | Từ chối |
| TC3 | EC3 | "Abcdefgh" | Từ chối |
| TC1 | EC4 | "Abcdefg" | Chấp nhận |
| TC4 | EC5 | "abcdefg" | Từ chối |
| TC1 | EC6 | "Abcdefg" | Chấp nhận |
| TC2 | EC7 | "Abcdef" | Từ chối |

**Minimum set of test cases**

| #TC | Partitions Tested | s | Expected Output |
|---|---|---|---|
| TC1 | EC1, EC4, EC6 | "Abcdefg" | Chấp nhận |
| TC2 | EC2, EC4, EC7 | "Abcdef" | Từ chối |
| TC3 | EC3, EC4, EC7 | "Abcdefgh" | Từ chối |
| TC4 | EC1, EC5, EC7 | "abcdefg" | Từ chối |

Ba Invalid EC có thể cô lập và một Valid test: bốn test. Nếu có lý do lowercase/digit/space xử lý khác nhau, tách EC5 và bổ sung "1bcdefg", " bcdefg"; mỗi chuỗi vẫn dài 7 và chỉ sai điều kiện chữ hoa.

### (4) Boundary Value Test Cases

Với length, LB=UB=7, delta=1: gộp thành ba độ dài 6,7,8. Dùng ký tự đầu A ở mọi test; không tự coi A/Z là biên theo thứ tự ký tự vì spec không quy định. Không biết cực trị UI.

| #TC | Biến/điểm biên | Partitions Tested | s | Expected Output |
|---|---|---|---|---|
| BVA1 | length=6: LB-1, UB-1 | EC2, EC4, EC7 | "Abcdef" | Từ chối |
| BVA2 | length=7: LB, UB | EC1, EC4, EC6 | "Abcdefg" | Chấp nhận |
| BVA3 | length=8: LB+1, UB+1 | EC3, EC4, EC7 | "Abcdefgh" | Từ chối |

### (5) Checklist

- [x] EC1–EC7 phủ đủ; độ dài và nội dung chỉ sai một điều kiện trong mỗi Invalid test chính.
- [x] BVA không tạo sáu dòng trùng khi LB=UB.

### (6) Giả định và điểm yếu

ASCII, không trim và không giới hạn sáu ký tự còn lại ngoài điều kiện length; đây là giả định minh họa. Output chỉ mô tả validation. Empty string thuộc EC2 nhưng first(s) không xác định: thêm test robustness riêng, Expected Output=Từ chối do độ dài; không tuyên bố EC4 Valid. Unicode/whitespace/missing cần spec. Cách chia này có thể bỏ sót xử lý đặc biệt từng nhóm ký tự.

## D. Điểm (X,Y): 3<=X<=7 và 5<=Y<=9

### (1) Input/Output variables

| Biến | Input/Output | Kiểu | Ràng buộc |
|---|---|---|---|
| X | Input | integer, giả định ví dụ | 3 <= X <= 7 |
| Y | Input | integer, giả định ví dụ | 5 <= Y <= 9 |
| Result | Output | kết quả validation | Chấp nhận điểm hoặc Từ chối |

### (2) Equivalence Classes

| STT | Input/Output | Equivalence Class | Valid/Invalid |
|---|---|---|---|
| EC1 | Input X | 3 <= X <= 7 | Valid |
| EC2 | Input X | X < 3 | Invalid |
| EC3 | Input X | X > 7 | Invalid |
| EC4 | Input Y | 5 <= Y <= 9 | Valid |
| EC5 | Input Y | Y < 5 | Invalid |
| EC6 | Input Y | Y > 9 | Invalid |
| EC7 | Output Result | Chấp nhận điểm | Valid |
| EC8 | Output Result | Từ chối | Invalid |

### (3) Chọn test case

**Test cases providing coverage of partitions**

| #TC | Partitions Tested | X | Y | Expected Output |
|---|---|---|---|---|
| TC1 | EC1 | 5 | 7 | Chấp nhận điểm |
| TC2 | EC2 | 1 | 7 | Từ chối |
| TC3 | EC3 | 10 | 7 | Từ chối |
| TC1 | EC4 | 5 | 7 | Chấp nhận điểm |
| TC4 | EC5 | 5 | 2 | Từ chối |
| TC5 | EC6 | 5 | 12 | Từ chối |
| TC1 | EC7 | 5 | 7 | Chấp nhận điểm |
| TC2 | EC8 | 1 | 7 | Từ chối |

**Minimum set of test cases**

| #TC | Partitions Tested | X | Y | Expected Output |
|---|---|---|---|---|
| TC1 | EC1, EC4, EC7 | 5 | 7 | Chấp nhận điểm |
| TC2 | EC2, EC4, EC8 | 1 | 7 | Từ chối |
| TC3 | EC3, EC4, EC8 | 10 | 7 | Từ chối |
| TC4 | EC1, EC5, EC8 | 5 | 2 | Từ chối |
| TC5 | EC1, EC6, EC8 | 5 | 12 | Từ chối |

Bốn Invalid EC cô lập và một Valid test: năm test trong miền integer đã giả định.

### (4) Boundary Value Test Cases

X: LB=3, UB=7; Y: LB=5, UB=9; delta=1. Nominal=(5,7) đã ở TC1. Min/max UI chưa được cho.

| #TC | Biến/điểm biên | Partitions Tested | X | Y | Expected Output |
|---|---|---|---|---|---|
| BVA1 | X: LB-1 | EC2, EC4, EC8 | 2 | 7 | Từ chối |
| BVA2 | X: LB | EC1, EC4, EC7 | 3 | 7 | Chấp nhận điểm |
| BVA3 | X: LB+1 | EC1, EC4, EC7 | 4 | 7 | Chấp nhận điểm |
| BVA4 | X: UB-1 | EC1, EC4, EC7 | 6 | 7 | Chấp nhận điểm |
| BVA5 | X: UB | EC1, EC4, EC7 | 7 | 7 | Chấp nhận điểm |
| BVA6 | X: UB+1 | EC3, EC4, EC8 | 8 | 7 | Từ chối |
| BVA7 | Y: LB-1 | EC1, EC5, EC8 | 5 | 4 | Từ chối |
| BVA8 | Y: LB | EC1, EC4, EC7 | 5 | 5 | Chấp nhận điểm |
| BVA9 | Y: LB+1 | EC1, EC4, EC7 | 5 | 6 | Chấp nhận điểm |
| BVA10 | Y: UB-1 | EC1, EC4, EC7 | 5 | 8 | Chấp nhận điểm |
| BVA11 | Y: UB | EC1, EC4, EC7 | 5 | 9 | Chấp nhận điểm |
| BVA12 | Y: UB+1 | EC1, EC6, EC8 | 5 | 10 | Từ chối |

### (5) Checklist

- [x] EC1–EC8 phủ đủ; mỗi Invalid test chỉ sai một biến.
- [x] Giữ Y=7 khi thay X, giữ X=5 khi thay Y; bốn phía của miền được xét.

### (6) Giả định và điểm yếu

Slide chỉ cho bất đẳng thức, không xác nhận kiểu integer. Bảng trên giả định integer đã được nhập có kiểu; nếu nhận số thực, cần xác định delta rồi làm lại BVA. Nếu interface nhận raw text, bổ sung EC sai kiểu cho từng biến và test cô lập. Output chỉ là mô tả validation. Các test góc và quan hệ đặc biệt giữa X,Y có thể bổ sung khi spec/rủi ro yêu cầu; không thay bộ thay từng biến.

## E. Widget identifier: 3–15 alphanumeric, hai ký tự đầu là chữ

### (1) Input/Output variables

| Biến | Input/Output | Kiểu | Ràng buộc |
|---|---|---|---|
| id | Input | chuỗi ASCII trong ví dụ | alphanumeric; 3 <= length <= 15; hai ký tự đầu là chữ A–Z/a–z |
| Result | Output | kết quả validation | Chấp nhận identifier hoặc Từ chối |

### (2) Equivalence Classes

Giữ EC1–EC7 theo ba điều kiện slide 17–19; thêm Output EC8–EC9. Với EC6/EC7, đánh giá hai ký tự đầu khi length>=2.

| STT | Input/Output | Equivalence Class | Valid/Invalid |
|---|---|---|---|
| EC1 | Input id/content | tất cả ký tự thuộc A–Z/a–z/0–9 | Valid |
| EC2 | Input id/content | có ít nhất một ký tự ngoài tập alphanumeric | Invalid |
| EC3 | Input length(id) | 3 <= length <= 15 | Valid |
| EC4 | Input length(id) | length < 3 | Invalid |
| EC5 | Input length(id) | length > 15 | Invalid |
| EC6 | Input prefix(id), length>=2 | hai ký tự đầu đều là chữ | Valid |
| EC7 | Input prefix(id), length>=2 | ít nhất một trong hai ký tự đầu không là chữ | Invalid |
| EC8 | Output Result | Chấp nhận identifier | Valid |
| EC9 | Output Result | Từ chối | Invalid |

### (3) Chọn test case

**Test cases providing coverage of partitions**

| #TC | Partitions Tested | id | Expected Output |
|---|---|---|---|
| TC1 | EC1 | "Ab123" | Chấp nhận identifier |
| TC2 | EC2 | "Ab#12" | Từ chối |
| TC1 | EC3 | "Ab123" | Chấp nhận identifier |
| TC3 | EC4 | "Ab" | Từ chối |
| TC4 | EC5 | "Ab12345678901234" | Từ chối |
| TC1 | EC6 | "Ab123" | Chấp nhận identifier |
| TC5 | EC7 | "1b234" | Từ chối |
| TC1 | EC8 | "Ab123" | Chấp nhận identifier |
| TC2 | EC9 | "Ab#12" | Từ chối |

**Minimum set of test cases**

| #TC | Partitions Tested | id | Expected Output |
|---|---|---|---|
| TC1 | EC1, EC3, EC6, EC8 | "Ab123" | Chấp nhận identifier |
| TC2 | EC2, EC3, EC6, EC9 | "Ab#12" | Từ chối |
| TC3 | EC1, EC4, EC6, EC9 | "Ab" | Từ chối |
| TC4 | EC1, EC5, EC6, EC9 | "Ab12345678901234" | Từ chối |
| TC5 | EC1, EC3, EC7, EC9 | "1b234" | Từ chối |

Kiểm tra cô lập: TC2 dài 5, hai ký tự đầu là chữ; TC3 dài 2 nhưng vẫn có đủ hai chữ; TC4 dài 16 nhưng content/prefix Valid; TC5 dài 5, alphanumeric, chỉ sai prefix. Bốn Invalid EC và một Valid test: tối thiểu năm test trong mô hình gộp EC7.

**Bổ sung theo guideline tách nhỏ EC7** để tránh bỏ sót code chỉ kiểm tra một vị trí:

| #TC | Partitions Tested | id | Expected Output |
|---|---|---|---|
| EXTRA1 | EC1, EC3, EC7 (chỉ vị trí 2 sai), EC9 | "A1234" | Từ chối |
| EXTRA2 | EC1, EC3, EC7 (cả hai vị trí sai), EC9 | "12345" | Từ chối |

TC5 đã phủ chỉ vị trí 1 sai. Nếu chính thức tách EC7 thành ba class con, cập nhật bảng EC/coverage và bộ chính thành bảy test; không tiếp tục gọi năm test là đủ cho mô hình đã tách. Trong mô hình hiện tại prefix là một điều kiện tổng hợp; nếu tách thành hai điều kiện vị trí độc lập, EXTRA2 phải được ghi là test kết hợp nhiều lỗi.

### (4) Boundary Value Test Cases

BVA theo length: LB=3, UB=15, delta=1, nominal length=5 đã có TC1. Giữ hai ký tự đầu là `Ab`, phần còn lại là chữ/số. Không có min/max UI được xác nhận. Content/prefix là điều kiện categorical, tiếp tục dùng EP.

| #TC | Biến/điểm biên | Partitions Tested | id | Expected Output |
|---|---|---|---|---|
| BVA1 | length=2, LB-1 | EC1, EC4, EC6, EC9 | "Ab" | Từ chối |
| BVA2 | length=3, LB | EC1, EC3, EC6, EC8 | "Ab1" | Chấp nhận identifier |
| BVA3 | length=4, LB+1 | EC1, EC3, EC6, EC8 | "Ab12" | Chấp nhận identifier |
| BVA4 | length=14, UB-1 | EC1, EC3, EC6, EC8 | "Ab123456789012" | Chấp nhận identifier |
| BVA5 | length=15, UB | EC1, EC3, EC6, EC8 | "Ab1234567890123" | Chấp nhận identifier |
| BVA6 | length=16, UB+1 | EC1, EC5, EC6, EC9 | "Ab12345678901234" | Từ chối |

### (5) Checklist

- [x] EC1–EC9 đều phủ, Output không bị bỏ quên.
- [x] Mỗi Invalid test chính chỉ sai một điều kiện; các độ dài 2/3/4/14/15/16 được kiểm tra cụ thể.
- [x] EC7 dùng “ít nhất một vị trí sai”; test bổ sung làm rõ phần mở rộng so với slide.

### (6) Giả định và điểm yếu

ASCII, không trim, không có quy tắc uniqueness được bổ sung; Result chỉ mô tả validation, không khẳng định đã ghi database. Nếu spec có uniqueness hoặc trạng thái DB, thêm điều kiện/EC và precondition tương ứng.

Empty string và chuỗi `"A"` là robustness bổ sung: sai độ dài và thiếu ký tự để đánh giá prefix; ghi prefix không xác định/không áp dụng theo spec. Không trộn chúng vào bộ một Invalid rồi khẳng định prefix Valid. Whitespace/Unicode/kiểu dữ liệu thô cần spec. Những lỗi riêng ở ký tự giữa chuỗi hoặc thứ tự validation có thể vẫn nằm ngoài mô hình hiện tại.
