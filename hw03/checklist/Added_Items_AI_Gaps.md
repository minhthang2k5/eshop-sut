# Mục bổ sung và lý do AI bỏ sót

Tổng 26 mục tự thêm; Chất lượng prompt: 6, Giới hạn của model: 9, Đặc thù giao diện: 11. Trong đó 18 mục đã xác nhận bằng cách chạy ứng dụng thật (10/11/2026).

| ID | Màn hình | IA | Mục bổ sung | Nguyên nhân AI bỏ sót | Giải thích | Quan sát thật |
|---|---|---|---|---|---|---|
| GUI-001 | Admin: Toàn trang | IA-01 | Thuộc tính ngôn ngữ trang | Giới hạn của model | AI không thấy mã HTML. Chạy thật: cả hai ứng dụng đều để lang="en" trong khi nội dung là tiếng Việt. | Có |
| GUI-002 | Admin: Toàn trang | IA-01 | Zoom 200% | Chất lượng prompt | Prompt không nhắc tới zoom; AI chỉ kiểm ở 1366 và 1920. | — |
| GUI-003 | Admin: Toàn trang | IA-01 | Dark mode | Chất lượng prompt | Prompt không nhắc tới dark mode. | Có |
| GUI-004 | Admin: Toàn trang | IA-01 | Bố cục RTL | Chất lượng prompt | Prompt không yêu cầu quốc tế hóa. Ưu tiên thấp vì sản phẩm chỉ phục vụ tiếng Việt, giữ ở mức Optional. | — |
| GUI-005 | Admin: Toàn trang | IA-01 | Responsive – tablet | Chất lượng prompt | Prompt chỉ cho độ rộng desktop (1366, 1920). | Có |
| GUI-006 | Admin: Toàn trang | IA-01 | Responsive – điện thoại | Giới hạn của model | Chỉ thấy khi chạy thật: menu trái cố định 256 px nên vùng nội dung chỉ còn ~119 px, tiêu đề "Quản lý Người dùng" xuống 4–5 dòng, bảng phải cuộn ngang. | Có |
| GUI-007 | Admin: Toàn trang | IA-02 | Trình đọc màn hình | Chất lượng prompt | Prompt không yêu cầu kiểm tra với trình đọc màn hình nên AI không sinh mục nào. | — |
| GUI-008 | Admin: Toàn trang | IA-03 | Thứ tự focus toàn trang | Giới hạn của model | AI chỉ đọc mô tả/ảnh chụp nên tưởng menu là liên kết. Chạy thật: các mục menu là thẻ <li> chỉ có onClick, không phải liên kết hay nút (không có thuộc tính tabindex) nên Tab bỏ qua toàn bộ menu. | Có |
| GUI-009 | Admin: Toàn trang | IA-03 | Giữ trạng thái khi F5 | Giới hạn của model | AI không biết ứng dụng lưu tab trong state React. Chạy thật: URL luôn là "/" ở mọi tab, F5 luôn quay về Dashboard. (Bổ sung cho mục nháp D-032 / AI-03-08 vốn chỉ xét tab Người dùng.) | Có |
| GUI-022 | Admin: Người dùng | IA-01 | Cột thông tin người dùng | Đặc thù giao diện | AI không biết luồng thật của nhóm là 'tìm khách hàng X'. Chạy thật: API trả về name nhưng bảng không hiển thị, không có ô tìm kiếm; cột Số ĐT luôn trống vì API không trả phone. | Có |
| GUI-050 | Admin: Danh mục | IA-01 | Định dạng cột ID và tiêu đề | Đặc thù giao diện | Prompt 4 chỉ yêu cầu form validation (IA-02/IA-04) nên tab Danh mục không có mục IA-01. Chạy thật: Danh mục hiện "#1", Người dùng hiện "1"; "Tên Danh Mục" và "Tên danh mục mới" viết hoa khác nhau. | Có |
| GUI-051 | Admin: Danh mục | IA-01 | Bảng hàng trăm dòng | Giới hạn của model | Chạy thật với 153 dòng: không phân trang, tiêu đề cột cuộn mất (position: static), trang dài ~9.400 px. Nhớ chạy `... clean` để dọn dữ liệu. | Có |
| GUI-063 | Admin: Danh mục | IA-03 | Thứ tự Tab trong trang | Đặc thù giao diện | Prompt 4 không bao gồm IA-03 (điều hướng) cho Danh mục. | — |
| GUI-064 | Admin: Danh mục | IA-03 | Vị trí dòng mới khi bảng dài | Giới hạn của model | Chỉ thấy khi chạy với dữ liệu thật: dòng mới nối vào cuối bảng ~9.000 px, ô nhập ở đầu trang, không có thông báo nên người dùng không biết đã thêm chưa. | Có |
| GUI-070 | Admin: Đơn hàng | IA-01 | Nhãn trạng thái đơn | Đặc thù giao diện | Màn hình Đơn hàng chưa được prompt nào phủ. | — |
| GUI-071 | Admin: Đơn hàng | IA-04 | Trạng thái rỗng | Đặc thù giao diện | Màn hình Đơn hàng chưa được prompt nào phủ. Chạy thật: seed không có đơn nên tab chỉ có hàng tiêu đề; đây là trạng thái rỗng có sẵn, thay cho mục nháp D-036/D-061 vốn cần giả lập nặng. | Có |
| GUI-072 | Admin: Đơn hàng | IA-04 | Hành động trên đơn đã hủy | Đặc thù giao diện | Đặc thù nghiệp vụ của màn hình: giao diện hiện nút "Đánh dấu Đã giao" cho đơn đã hủy (phát hiện khi đọc mã App.jsx). AI không có thông tin về luồng trạng thái này. | — |
| GUI-073 | Admin: Đơn hàng | IA-04 | Đổi trạng thái đơn | Đặc thù giao diện | Màn hình Đơn hàng chưa được prompt nào phủ. | — |
| GUI-074 | Admin: Dashboard | IA-01 | Nhãn và định dạng tiền | Đặc thù giao diện | Dashboard và Home chưa được prompt nào phủ. Chạy thật: Admin hiện "₫", Home hiện "30,000,000 VND" (dấu phẩy kiểu Anh). | Có |
| GUI-075 | Admin: Dashboard | IA-04 | Số liệu doanh thu | Giới hạn của model | Chỉ lộ ra khi có dữ liệu thật (phát hiện khi đọc mã App.jsx): công thức doanh thu nhân đôi total_amount, nên Dashboard sẽ gấp đôi tổng ở tab Đơn hàng. | — |
| GUI-076 | Web: Home | IA-01 | Responsive – điện thoại | Giới hạn của model | Chỉ thấy khi chạy thật: tiêu đề bị ô tìm kiếm ép còn ~80 px, xuống 4 dòng (cao 144 px). | Có |
| GUI-077 | Web: Home | IA-02 | Ảnh sản phẩm | Đặc thù giao diện | Home chưa được phủ. Chạy thật: cả 5 ảnh đều có alt="". | Có |
| GUI-078 | Web: Home | IA-02 | Ô tìm kiếm | Đặc thù giao diện | Home chưa được phủ. Chạy thật: ô tìm kiếm không có label, không có aria-label. | Có |
| GUI-079 | Web: Home | IA-02 | Vùng chạm trên điện thoại | Chất lượng prompt | Prompt không yêu cầu kiểm tra trên thiết bị cảm ứng. Chạy thật: nút cao 36 px. | Có |
| GUI-080 | Web: Home | IA-04 | Tìm kiếm không có kết quả | Đặc thù giao diện | Home chưa được phủ. Chạy thật: chỉ còn dòng "Kết quả tìm kiếm cho: xyz123", vùng sản phẩm trống, không có thông báo. | Có |
| GUI-081 | Web: Home | IA-04 | Thông báo lỗi tìm kiếm | Giới hạn của model | Chỉ thấy khi chạy thật: trang hiện khung đỏ "Database Error – SQLITE_ERROR: unrecognized token". | Có |

## Nhận xét nhanh (cơ sở cho phần AI Critique)

- **Giới hạn của model** là nhóm giá trị nhất: các lỗi như menu không nhận Tab, F5 về Dashboard, lỗi SQL thô khi tìm kiếm, bố cục vỡ ở 375 px chỉ lộ ra khi chạy thật; AI làm việc trên mô tả màn hình nên tưởng menu là liên kết chuẩn.
- **Chất lượng prompt**: các prompt chỉ khoanh vùng desktop 1366/1920 và ba IA, nên dark mode, zoom, trình đọc màn hình, thiết bị cảm ứng bị bỏ qua hoàn toàn. Đây là lỗi của người viết prompt, không phải của model.
- **Đặc thù giao diện**: Đơn hàng, Dashboard, Home chưa từng được đưa vào prompt; tab Danh mục chỉ được hỏi về validation nên thiếu IA-01 và IA-03.
- Về chất lượng mục AI: 22 mục cần sửa, 2 mục phải tách, 5 mục trùng ý phải gộp; nhiều mục sửa vì kết quả mong đợi kiểu "hoặc… hoặc…"/"nếu… thì…" hoặc cảm tính, 3 mục cần đổi cách giả lập vì AI không biết khởi động lại backend sẽ seed lại toàn bộ DB.
