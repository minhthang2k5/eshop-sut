---
name: domain-testing
description: Thiết kế test case từ spec bằng Domain Testing, Equivalence Partitioning, Boundary Value Analysis (phân vùng tương đương, giá trị biên) theo slide S04 CSC13003 HCMUS. Dùng khi cần xác định Input/Output, Equivalence Class Valid/Invalid, chọn bộ test phủ partition và phân tích LB/UB. Không dùng làm skill chính cho viết code test tự động, chạy test, sửa bug hoặc white-box testing.
---

# Domain Testing theo S04

Thiết kế test từ đặc tả theo bốn bước dưới đây. Viết tiếng Việt, giữ thuật ngữ English và chỉ rõ căn cứ từ spec. Không tuyên bố đã chạy test khi chỉ thiết kế.

## Chuẩn bị và tài liệu tham chiếu

- Đọc spec được cung cấp; không suy ra hành vi mong đợi chỉ từ code hiện tại.
- Đọc [slide-errata.md](references/slide-errata.md) trước khi dùng ví dụ, bảng hoặc công thức trong slide.
- Đọc [guidelines.md](references/guidelines.md) khi chia EC, xử lý điều kiện phụ thuộc, biên mở hoặc kiểu dữ liệu.
- Đọc phần tương ứng trong [examples.md](references/examples.md) khi cần mẫu chọn test, bảng phủ và BVA; các ví dụ đã có đủ bốn bước.
- Nếu thiếu quy tắc quyết định Valid/Invalid hoặc Expected Output, hỏi phần thiếu; vẫn phân tích phần đã rõ. Ghi giả định ở mục (6), không biến giả định thành yêu cầu thật.
- Không tự đặt thông báo lỗi, giới hạn UI, tập ký tự, quy tắc trim hoặc độ chính xác số. Dùng kết quả mô tả theo spec; đánh dấu điều chưa xác định.

## Bước 1. Xác định Input & Output

Liệt kê từng biến, kiểu/đơn vị, miền biểu diễn, ràng buộc, quan hệ giữa biến và nguồn trong spec. Liệt kê cả kết quả thành công lẫn phản hồi lỗi; tách Output khỏi Input. Chốt ý nghĩa độ dài ký tự và bước biểu diễn trước khi tính biên nếu chúng ảnh hưởng kết quả.

## Bước 2. Xác định Equivalence Class

- Chia EC cho từng Input và Output; đánh số EC1, EC2... duy nhất trong một đặc tả, ghi Valid/Invalid.
- Áp dụng định nghĩa slide: cùng EC nếu kết quả mong đợi giống nhau. Với kết quả tính toán, hiểu là cùng quy tắc/hành vi mong đợi, không bắt buộc cùng con số; vẫn tính Expected Output cho từng test.
- Với khoảng: một Valid và hai Invalid; với tập giá trị được xử lý khác nhau: một Valid mỗi giá trị và một Invalid ngoài tập; với “must be”: một Valid và một Invalid.
- Tách nhỏ khi có căn cứ xử lý khác nhau; nhận diện EC là heuristic. Phân biệt điều kiện riêng với tổ hợp điều kiện; không tạo giao nhau giả do so sánh chuỗi với số.
- Giữ các EC Output riêng như EC9 (SUM) và EC10 (Error) trong ví dụ cộng; EC Output lỗi là phản hồi đúng cho Input Invalid, không phải một lỗi đầu vào bổ sung.

## Bước 3. Chọn test case

- Chọn ít nhất một test cho mỗi EC khả thi, kể cả EC Output. Ghi rõ EC không thể đạt và nguyên nhân nếu có.
- Gộp các Valid EC vào ít test nhất có thể; giữ bảng truy vết từ EC đến test.
- Mỗi Invalid test chỉ vi phạm đúng MỘT điều kiện Input; các Input/điều kiện còn lại dùng giá trị Valid bình thường. Một biến có thể mang nhiều điều kiện, nên phải kiểm tra từng điều kiện, không chỉ đếm số biến sai.
- Nếu ràng buộc phụ thuộc khiến không thể cô lập, nêu rõ và tách test bổ sung; không tuyên bố test nhiều lỗi tuân thủ quy tắc một Invalid. Xem guidelines.md.
- Tạo cả bảng “Test cases providing coverage of partitions” và “Minimum set of test cases”. Gộp test trùng toàn bộ Input/Expected Output, giữ mọi EC đã phủ.
- Hiểu “Minimum” là bộ rút gọn theo cách gộp của slide; chỉ khẳng định tối thiểu tuyệt đối khi chứng minh được.
- Tính Expected Output độc lập cho từng test; không dùng kết quả chạy làm oracle.

## Bước 4. Boundary Value Analysis

- Với partition có thứ tự, xác định LB/UB hữu hạn và tính bao hàm. Dùng LB-1, LB, LB+1, UB-1, UB, UB+1 cho miền số nguyên hoặc độ dài.
- Với biên mở trên số nguyên, đổi sang giá trị được nhận đầu/cuối trước; ví dụ 0 < x < 100 có LB=1, UB=99. Với số thập phân dùng ±delta theo độ chính xác; chưa biết delta thì hỏi/ghi chưa xác định.
- Giữ các biến khác tại giá trị Valid danh nghĩa; với độ dài chuỗi, giữ đúng các quy tắc nội dung. Tách test nhiều lỗi nếu cấu trúc dữ liệu không cho phép cô lập.
- Kết hợp một điểm Valid danh nghĩa với sáu điểm biên và min/max UI khi đã biết: tối đa chín điểm ứng viên trong mẫu slide. Tái sử dụng điểm danh nghĩa của EP; gộp điểm trùng, bỏ điểm không thể biểu diễn có giải thích.
- Với partition không có thứ tự, ghi BVA không áp dụng cho chính điều kiện đó. Với miền vô hạn không đặt LB/UB là ±vô cực hoặc tự bịa giới hạn UI. Các partition kề nhau có thể dùng chung test tại ranh giới.
- Giải thích ngắn: sai dấu bất đẳng thức dễ lộ ngay tại biên; gõ nhầm mốc cũng có thể bị phát hiện ở biên. Điểm xa biên như 53 có thể bỏ sót cả hai lỗi trong ví dụ mốc 25 ở slide 24–25; đây không phải bảo đảm cho mọi loại lỗi.

## Đầu ra Markdown theo đúng thứ tự

### (1) Input/Output variables

| Biến | Input/Output | Kiểu/đơn vị | Ràng buộc và nguồn spec |
|---|---|---|---|

### (2) Equivalence Classes

| STT | Input/Output | Equivalence Class | Valid/Invalid |
|---|---|---|---|

### (3) Chọn test case

Tạo hai bảng mang tên **Test cases providing coverage of partitions** và **Minimum set of test cases**. Trong bảng phủ, chỉ rõ từng EC và test đại diện; trong bảng Minimum, mỗi tổ hợp dữ liệu chỉ có một dòng.

| #TC | Partitions Tested | Các Input (mỗi biến một cột) | Expected Output |
|---|---|---|---|

### (4) Boundary Value Test Cases

Nêu LB/UB, delta, giá trị danh nghĩa và nguồn giới hạn UI. Dùng một dòng cho mỗi tổ hợp Input cụ thể; ghi EC thực sự chứa điểm test, kể cả EC phía ngoài partition đang xét.

| #TC | Biến/điểm biên | Partitions Tested | Các Input (mỗi biến một cột) | Expected Output |
|---|---|---|---|---|

### (5) Checklist tự kiểm tra

- [ ] Mọi EC khả thi, cả Input và Output, được phủ; EC chưa phủ có lý do.
- [ ] Mỗi Invalid test trong bộ chính chỉ vi phạm một điều kiện Input.
- [ ] Các biến còn lại Valid danh nghĩa; test phụ thuộc/robustness được tách rõ.
- [ ] Expected Output tính đúng, không sao chép lỗi dấu/số học từ slide.
- [ ] Biên mở/đóng, delta, điểm trùng và giới hạn UI được xử lý rõ.
- [ ] Không gán Passed/Failed hoặc bug đã xác nhận khi chưa thực thi.

### (6) Giả định và điểm yếu cần nhắc

Ghi giả định hoặc câu hỏi còn thiếu: số thập phân, chuỗi rỗng, whitespace/trim, số âm, Unicode, thứ tự validation và giới hạn UI. Ghi “Không có” nếu spec đã rõ, không tự thêm quy tắc. Nhắc Domain Testing có thể bỏ sót lỗi ngoài biên/trường hợp đặc biệt và miền thực tế có thể chưa biết chắc; đề xuất thêm kỹ thuật phù hợp như decision table hoặc state transition nếu cần.

Chỉ khi người dùng yêu cầu lưu kết quả, ghi sáu mục trên vào `domain-testing-output.md` tại thư mục làm việc, hoặc đường dẫn họ chỉ định. Không ghi đè báo cáo có nội dung không liên quan.
