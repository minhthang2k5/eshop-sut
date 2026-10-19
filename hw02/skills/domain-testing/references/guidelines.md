# Guidelines xác định Equivalence Class và chọn test

Nguồn tổng hợp: `S04_Domain Testing.pdf`, CSC13003 HCMUS, slide 3–23. Phần BVA dựa trên slide 24–27. Các diễn giải để xử lý spec mơ hồ được đánh dấu riêng; không coi ví dụ là yêu cầu của SUT khác.

## 1. Chia theo khoảng giá trị — slide 8

Với điều kiện `1 <= count <= 999`, tạo:

| EC | Miền | Trạng thái |
|---|---|---|
| EC1 | 1 <= count <= 999 | Valid |
| EC2 | count < 1 | Invalid |
| EC3 | count > 999 | Invalid |

Nêu miền nền trước: nếu count phải là số nguyên, ba khoảng trên chỉ áp dụng sau khi xác nhận kiểu. Thêm EC sai kiểu nếu giao diện cho phép cung cấp sai kiểu; không áp dụng phép so sánh số cho `"abc"`.

## 2. Chia theo tập rời rạc — slide 9

Nếu spec cho phép BUS, TRUCK, TAXI-CAB, PASSENGER, MOTOCYCLE và có lý do mỗi loại được xử lý khác nhau, tạo năm Valid EC, mỗi loại một EC, cộng một Invalid EC ngoài tập như TRAILER. Giữ nguyên tên token theo spec; không tự sửa token trong test.

Không áp dụng máy móc “mỗi giá trị một EC” cho tập rất lớn khi mọi giá trị có cùng quy tắc và không có căn cứ phân nhánh. Nêu căn cứ tách class.

## 3. Điều kiện “must be” — slide 10

“Ký tự đầu phải là chữ cái”: một Valid EC bắt đầu bằng chữ, một Invalid EC bắt đầu bằng ký tự không phải chữ. Chốt ASCII/Unicode nếu điều này ảnh hưởng kết quả. Khi chuỗi rỗng, ký tự đầu không tồn tại; xử lý theo điều kiện độ dài/thứ tự validation đã xác định, không giả vờ có ký tự đầu.

## 4. Tách class khi có căn cứ — slide 11

Ví dụ điều kiện “hai ký tự đầu là chữ” có Invalid EC tổng quát gồm `1b3`, `A23`, `123`. Nếu cần phát hiện code chỉ kiểm tra một vị trí, tách thành: chỉ vị trí 1 sai; chỉ vị trí 2 sai; cả hai sai. Đây là các phần của một điều kiện tổng hợp. Nếu đã mô hình hóa hai vị trí thành hai điều kiện riêng, test `123` là test hai lỗi, phải chuyển ra bộ Invalid cô lập.

Nhận diện EC là heuristic. Ghi lý do tách; không tự hứa một đại diện sẽ phát hiện mọi lỗi trong class. “Cùng expected result” của slide 5 cần đọc cùng ví dụ cộng: cùng cách xử lý/quy tắc tính tổng, còn giá trị SUM cụ thể vẫn phụ thuộc A, B.

## 5. Điều kiện riêng, class kết hợp và class Output

- Điều kiện riêng có thể cùng đúng: “alphanumeric”, “length 3–15”, “first two letters”. Đây là ba trục phân loại, không phải ba miền rời nhau của toàn bộ Input.
- Valid toàn bộ = giao của mọi điều kiện hợp lệ. Với Invalid cô lập, làm sai một điều kiện và giữ đúng các điều kiện còn lại.
- Khi chia một trục thành class, tránh overlap và nêu phần chưa được mô hình hóa. Ví dụ số nguyên chia thành dưới khoảng/trong khoảng/trên khoảng, còn “không nguyên” là trục kiểu hoặc class hợp nhất sau khi loại kiểu.
- Giữ Output riêng: phép cộng có EC9 “SUM = A+B” và EC10 “Invalid Input”. Valid/Invalid của Output chỉ là nhánh trả kết quả/chặn dữ liệu; phản hồi lỗi đúng không phải bug.
- Một Invalid test có thể phủ EC sai đầu vào và EC10 cùng lúc. Điều đó vẫn chỉ chứa một lỗi Input.

## 6. Chọn test — slide 21–23

1. Đánh ID EC ổn định. Chọn đại diện có oracle rõ ràng cho từng EC.
2. Lập bảng **Test cases providing coverage of partitions**: cho thấy từng EC được test nào phủ. Có thể lặp cùng một test trên nhiều dòng truy vết.
3. Lập **Minimum set of test cases**: gộp các dòng cùng Input và Expected Output; gom Valid EC tối đa; mỗi dòng Invalid chỉ vi phạm một điều kiện Input.
4. Kiểm tra Output EC cũng được phủ, kể cả nhánh lỗi.
5. Nêu cơ sở tối thiểu: nếu có k điều kiện/EC Invalid cần cô lập và ít nhất một Valid test, cần tối thiểu k+1 test, khi từng Invalid có thể cô lập và một Valid test phủ đủ mọi Valid EC. Nếu có các Valid EC loại trừ nhau, cần nhiều Valid test hơn.

Ví dụ cộng: một Valid test phủ EC1, EC5, EC9; sáu test cô lập EC2, EC3, EC4, EC6, EC7, EC8 đồng thời phủ EC10. Bộ bảy test đạt tối thiểu trong mô hình đó.

## 7. Ràng buộc phụ thuộc: không ép “một lỗi” bất khả thi

Ví dụ widget length=2 dùng `Ab`: sai độ dài nhưng vẫn alphanumeric và hai ký tự đầu là chữ, nên cô lập được lỗi length. Với length=0 hoặc 1, điều kiện “hai ký tự đầu là chữ” không thể được đánh giá đầy đủ.

- Nếu spec định nghĩa short-circuit theo độ dài, ghi điều kiện ký tự là không áp dụng sau khi kiểm tra độ dài thất bại.
- Nếu không có quy định, đưa chuỗi rỗng/length=1 vào test robustness riêng, ghi phụ thuộc và Expected Output chỉ đến mức spec cho biết. Không ghi rằng mọi điều kiện khác đều Valid.
- Không loại bỏ EC quan trọng chỉ vì không thể cô lập; ghi rõ giới hạn của mô hình và hỏi spec khi cần.

## 8. BVA — slide 24–27

Với miền số nguyên hữu hạn `[LB,UB]`, lấy `{LB-1, LB, LB+1, UB-1, UB, UB+1}`. Thêm một giá trị Valid danh nghĩa (thường đã có trong EP) và hai cực trị UI đã được xác nhận: tối đa chín điểm ứng viên của hình slide 26. Gộp giá trị trùng và giữ đủ nhãn biên được phủ.

- `[7,7]` chỉ cho ba điểm biên khác nhau: 6, 7, 8. Không sinh sáu dòng trùng.
- `(0,100)` trên số nguyên đổi thành `[1,99]`; test 0, 1, 2, 98, 99, 100.
- Với số thập phân cố định hai chữ số, delta=0.01; ghi theo spec. Không mặc định ±1 hoặc “số thực kế tiếp” nếu không biết biểu diễn.
- Với invalid partition không bị chặn về một phía, chỉ xét ranh giới hữu hạn liên quan; không đặt infinity thành dữ liệu test và không tự tạo min/max UI.
- Với tập unordered hoặc sai kiểu, dùng EP; không gán LB/UB tùy ý. Với chuỗi, BVA áp dụng cho độ dài; quy tắc chữ/alphanumeric vẫn dùng EP nếu spec không định nghĩa thứ tự ký tự.
- Khi một test biên nằm ngoài Valid partition, gắn EC Invalid thực tế. Giữ các biến khác và các điều kiện nội dung Valid.
- Giới hạn “chín” nói về mẫu điểm của một partition trong slide, không phải trần số test của cả chức năng hay lệnh bỏ các EC khác. Nếu phân tích nhiều ràng buộc cần nhiều test, giữ chúng và giải thích.

## 9. Phạm vi và oracle

Đặc tả quyết định đúng/sai; chương trình thực tế là đối tượng kiểm thử. Không sửa Expected Output để khớp bug của SUT. Spec thiếu thông báo lỗi thì ghi “từ chối dữ liệu/không thực hiện tác vụ” thay vì bịa chuỗi lỗi. Các ví dụ trong examples.md có giả định minh họa riêng.

Domain Testing không đảm bảo phát hiện lỗi giữa miền hoặc các tổ hợp đặc biệt, và miền thực tế có thể chưa biết chắc (slide 28). Bổ sung kỹ thuật khác theo rủi ro, không biến việc đó thành yêu cầu của slide.
