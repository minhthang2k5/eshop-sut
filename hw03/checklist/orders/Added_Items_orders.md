# Mục bổ sung và lý do AI bỏ sót – Admin: Đơn hàng

Tổng 6 mục tự thêm; Chất lượng prompt: 2, Giới hạn của model: 3, Đặc thù giao diện: 1. 2 mục đã thấy hiện tượng khi chạy thật (10/11/2026); các mục còn lại cần xác nhận khi thực thi.

| ID | IA | Mục bổ sung | Nguyên nhân AI bỏ sót | Giải thích | Quan sát thật |
|---|---|---|---|---|---|
| ORD-013 | IA-01 | Bố cục điện thoại | Chất lượng prompt | Prompt chỉ mô tả bảng ở độ rộng desktop. Chạy thật ở 375 px: menu trái chiếm 256 px nên vùng nội dung chỉ còn 119 px, bảng rộng 413 px và nội dung rộng 445 px nên phải cuộn ngang. | Có |
| ORD-014 | IA-01 | Nhãn nút ở độ rộng hẹp | Giới hạn của model | Chỉ lộ ra khi chạy thật: ở 375 px mọi nút chỉ rộng 47 px; nút "Đánh dấu Đã giao" bị bẻ thành nhiều dòng cao 72 px, nút "Hủy" cao 24 px. | Có |
| ORD-015 | IA-01 | Phân biệt người đặt | Đặc thù giao diện | Cột Người đặt chỉ hiển thị tên; với dữ liệu mẫu toàn "Test User" AI không thấy được rủi ro trùng tên. Cần tạo dữ liệu trùng để xác nhận. | — |
| ORD-016 | IA-01 | Cột Tổng tiền | Chất lượng prompt | Prompt chỉ yêu cầu thử địa chỉ dài, không yêu cầu thử số tiền rất lớn. | — |
| ORD-025 | IA-03 | Focus sau khi đổi trạng thái | Giới hạn của model | Chỉ lộ ra khi thao tác bằng bàn phím trên giao diện thật: nút bị thay bằng nút khác sau khi đổi trạng thái nên focus có thể mất. | — |
| ORD-035 | IA-04 | Tên nút so với trạng thái đích | Giới hạn của model | Mô tả liệt kê tên nút và tên trạng thái rời nhau nên AI không nối được nút nào dẫn tới trạng thái nào; nút "Hoàn thành" đưa đơn sang "Đã giao" (theo đặc tả FR-10). Cần bấm để xác nhận. | — |
