# Prompt 6 – Mô tả màn hình và kiểm kê thành phần (Admin: Đơn hàng)

> Chạy bằng skill `gui-checklist` (bước 1–2) trên màn hình mới. Đánh số tiếp theo chuỗi prompt 01–05.

- **Mục đích:** Cho AI biết chính xác màn hình cần kiểm thử và kiểm kê thành phần (chưa sinh checklist).
- **Căn cứ lý thuyết:** slide GUI Testing, trang 4 (các thành phần có thể kiểm thử của GUI).
- **Nguồn mô tả:** quan sát trực tiếp trên SUT (trình duyệt tích hợp, đọc cấu trúc trang và văn bản) ngày 2026-11-10, sau khi chuẩn bị 5 đơn thử đủ 5 trạng thái.
- **Tool AI dùng:** Claude Code (Claude Sonnet 5.5)
- **Ngày giờ chạy:** 2026-11-10 (giờ chính xác xem `AI_Audit_Log.md`)
- **Lưu ý:** phiên này đã đọc mã nguồn SUT trước đó; prompt yêu cầu chỉ dựa vào mô tả.

## Chuẩn bị dữ liệu (để màn hình hiện đủ trạng thái)

Seed mặc định không có đơn nào nên tab chỉ có hàng tiêu đề. Dữ liệu thử được tạo bằng API (tài khoản khách `test@eshop.com`, đăng nhập admin để đổi trạng thái): 5 đơn có trạng thái `pending`, `confirmed`, `shipping`, `canceled`, `delivered`. Backend chặn nhảy thẳng từ `pending` sang `shipping` hoặc `delivered` (trả 400), nên phải đi từng bước theo FR-10. Dữ liệu này mất khi khởi động lại backend.

---

## Prompt (dán nguyên khối vào AI)

```text
Bạn là chuyên gia kiểm thử giao diện (GUI testing). Hãy kiểm thử HỘP ĐEN: chỉ dựa vào bản mô tả dưới đây, KHÔNG đọc mã nguồn, KHÔNG suy đoán cách cài đặt bên trong.

## Màn hình: "Quản lý Đơn hàng" (tab "Đơn hàng" của Web Admin EShop, tiếng Việt)
- Cùng khung với các tab khác: menu tối bên trái (Dashboard, Danh mục, Sản phẩm, Mã Giảm Giá, Đơn hàng, Người dùng, Đăng xuất), vùng nội dung bên phải nền sáng.
- Tiêu đề trang "Quản lý Đơn hàng".
- Một bảng nền trắng, hàng tiêu đề nền xám, 6 cột: ID (dạng #5, #4...), Người đặt, Tổng tiền, Địa chỉ, Trạng thái, Hành động.
- Dữ liệu hiện có: 5 đơn, đều của "Test User", sắp từ ID lớn xuống nhỏ:
  #5: 150,000 ₫, "3 Hai Ba Trung, Q1, TP.HCM", Chờ xác nhận, nút: Xác nhận, Hủy.
  #4: 2,000,000 ₫, "99 CMT8, Q3, TP.HCM", Đã xác nhận, nút: Giao hàng, Hủy.
  #3: 300,000 ₫, "7 Tran Hung Dao, Q5, TP.HCM", Đang giao, nút: Hoàn thành.
  #2: 1,250,000 ₫, "45 Nguyen Hue, Q1, TP.HCM", Đã hủy, nút: Đánh dấu Đã giao.
  #1: 500,000 ₫, "12 Le Loi, Q1, TP.HCM", Đã giao, không có nút.
- Trạng thái hiển thị bằng nhãn chữ có màu nền; các nút hành động nhỏ, xếp dọc trong ô (nút Hủy màu xám).
- KHÔNG có: ô tìm kiếm, bộ lọc theo trạng thái, sắp xếp cột, phân trang, cột ngày đặt hàng, cột email người đặt, nút xem chi tiết đơn, nút xuất file, ô nhập liệu nào.
- Nguyên tắc nghiệp vụ liên quan (đặc tả FR-10, FR-18): trạng thái pending → confirmed → shipping → delivered; pending và confirmed có thể chuyển sang canceled; delivered và canceled là trạng thái kết thúc, không chuyển sang trạng thái nào khác; địa chỉ phải hiển thị an toàn (không render HTML).

## Yêu cầu
1. Nhắc lại ngắn gọn bạn hiểu màn hình làm gì và ai dùng.
2. Lập bảng kiểm kê các thành phần có thể kiểm thử, nhóm theo loại (văn bản/tiêu đề, bảng và cột, nhãn trạng thái, nút hành động, màu sắc, căn lề, trạng thái dữ liệu: rỗng, nhiều dòng, dữ liệu dài). Với mỗi thành phần: tên, vị trí, hành vi/trạng thái cần kiểm tra.
3. Liệt kê các điều CHƯA CHẮC cần xác nhận khi thao tác thật. Không tự suy diễn.
4. Chưa viết checklist ở bước này.

Trả lời bằng tiếng Việt, dùng bảng Markdown.
```

---

## Ghi log

### Output của AI

**1. Hiểu về màn hình.** Đây là trang quản trị đơn hàng toàn hệ thống: quản trị viên xem mọi đơn và đưa đơn đi qua các trạng thái (xác nhận, giao, hoàn thành, hủy). Người dùng là chủ shop hoặc nhân viên vận hành.

**2. Kiểm kê thành phần**

| Nhóm | Thành phần | Vị trí | Hành vi/trạng thái cần kiểm tra |
|---|---|---|---|
| Văn bản | Tiêu đề "Quản lý Đơn hàng" | Đầu vùng nội dung | Chính tả, dấu tiếng Việt, phân cấp so với tiêu đề cột |
| Bảng/cột | 6 cột ID, Người đặt, Tổng tiền, Địa chỉ, Trạng thái, Hành động | Vùng nội dung | Căn lề, độ rộng, đủ cột cần thiết, thứ tự dòng |
| | Cột ID dạng "#n" | Bảng | Nhất quán định dạng với các tab khác |
| | Cột Tổng tiền | Bảng | Dấu phân cách hàng nghìn, ký hiệu ₫, căn lề số |
| | Cột Địa chỉ | Bảng | Địa chỉ dài, ký tự đặc biệt, hiển thị an toàn |
| Nhãn trạng thái | 5 nhãn: Chờ xác nhận, Đã xác nhận, Đang giao, Đã hủy, Đã giao | Cột Trạng thái | Chữ và màu phân biệt, tương phản, không chỉ dựa vào màu |
| Nút hành động | Xác nhận, Hủy, Giao hàng, Hoàn thành, Đánh dấu Đã giao | Cột Hành động | Nút nào xuất hiện ở trạng thái nào, kích thước, vùng chạm, khoảng cách giữa hai nút, màu theo ý nghĩa, focus bàn phím |
| Điều hướng | Mục menu "Đơn hàng" | Menu trái | Nổi bật khi đang chọn; giữ tab sau khi đổi trạng thái |
| Màu sắc | Nền xám tiêu đề, nhãn trạng thái, nút | Toàn bảng | Tương phản, ý nghĩa màu |
| Trạng thái dữ liệu | Rỗng, đang tải, lỗi tải | Bảng | Có thông báo phù hợp hay chỉ còn hàng tiêu đề |
| | Nhiều đơn (hàng chục) | Bảng | Cuộn, tiêu đề cố định, không phân trang |
| Phản hồi | Sau khi bấm nút hành động | Cột Trạng thái, Hành động | Nhãn đổi, nút đổi, thông báo, xác nhận, lỗi |

**3. Điều chưa chắc**
1. Bấm "Hủy" hoặc "Hoàn thành" có hộp xác nhận không?
2. Sau khi đổi trạng thái có thông báo thành công không, hay chỉ nhãn đổi?
3. Đơn "Đã hủy" đang có nút "Đánh dấu Đã giao", điều này có phù hợp với FR-10 (trạng thái kết thúc) không?
4. Địa chỉ chứa ký tự `< > &` có hiển thị nguyên văn không?
5. Khi có đơn mới tạo từ phía khách, danh sách có tự cập nhật không?
6. Bảng có phản ứng ra sao khi có hàng chục đơn và khi cửa sổ hẹp?
7. Có cách xem chi tiết đơn (sản phẩm, ngày đặt) không?
8. Nút bấm hai lần nhanh có gửi hai yêu cầu không?

### Nhận xét của người kiểm thử
_(AI hiểu đúng chưa? có bịa không? điểm chưa chắc nào đáng kiểm tra nhất?)_
