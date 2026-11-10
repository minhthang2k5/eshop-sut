# Phân tích kết quả Usability (Task 2, Phase 3)

> Số liệu lấy từ `Usability_Sessions.xlsx` do người kiểm thử ghi nhận trong các phiên (P01 đến P07 là 7 phiên chính; P00 là pilot, **không tính** vào thống kê). Phân tích do Claude Code hỗ trợ, tính lại từ dữ liệu thô của từng sheet; người kiểm thử chịu trách nhiệm về tính đúng của dữ liệu đầu vào. Bản nháp ngày 2026-11-11.

## 1. Điểm SUS (7 phiên chính)

| Participant | P01 | P02 | P03 | P04 | P05 | P06 | P07 |
|---|---|---|---|---|---|---|---|
| SUS | 50,0 | 72,5 | 77,5 | 70,0 | 57,5 | 52,5 | 65,0 |

- **Trung bình 63,6**, trung vị 65,0, độ lệch chuẩn 10,5, thấp nhất 50,0, cao nhất 77,5. Pilot P00: 45,0 (không tính).
- **Dưới mốc ngành 68** (xếp "dưới trung bình", khoảng 51 đến 68). Hai người điểm cao nhất (P02, P03) là hai sinh viên khối công nghệ quen máy; ba người điểm thấp nhất (P01, P06, P05) là người lớn tuổi hoặc ít kinh nghiệm. Với 7 người, đây chỉ là xu hướng, không phải kết luận thống kê.

## 2. Kết quả theo nhiệm vụ

| Nhiệm vụ | Thời gian TB (khoảng) | Chuẩn | Hoàn thành không trợ giúp | Kể cả có trợ giúp | Tổng lỗi | Số lần trợ giúp | SEQ TB (1-7) |
|---|---|---|---|---|---|---|---|
| T1 Doanh thu, số đơn | 34 s (18 đến 55) | 60 s | 7/7 | 7/7 | 0 | 0 | 5,86 |
| T2 Thêm nhóm "Màn hình" | 70 s (35 đến 110) | 60 s | 6/7 | 7/7 | 4 | 1 | 4,57 |
| T3 Xác nhận đơn 150.000 ₫ | 129 s (70 đến 205) | 120 s | 4/7 | 7/7 | 8 | 3 | 4,00 |
| T4 Tìm vana@example.com | 147 s (48 đến 300) | 90 s | 4/7 | **6/7** | 8 | 4 | **3,71** |

- **T1 dễ nhất** nhưng đó chính là nhiệm vụ mà con số hiển thị **sai** (doanh thu gấp đôi); 5/7 người tin con số.
- **T4 khó nhất:** thời gian vượt chuẩn gần 60%, SEQ thấp nhất, và **1 người không hoàn thành** (kết luận sai "chưa có khách này" vì bảng chỉ có email).
- T2 và T3 vượt chuẩn nhẹ; lỗi chủ yếu là bấm nút nhiều lần và do dự khi bấm Xác nhận/Hủy.

## 3. Phát hiện xếp theo mức độ ưu tiên

Mức ưu tiên = mức nghiêm trọng (1 đến 4) × xác suất (số người gặp / 7). Mức nghiêm trọng do người kiểm thử đánh giá.

| Hạng | Phát hiện | NV | Nghiêm trọng | Số người gặp | Ưu tiên | Bug Task 1 liên quan |
|---|---|---|---|---|---|---|
| 1 | Xác nhận/Hủy/Xóa không hỏi lại; người dùng lo hoặc do dự | T3 | 3 | 6/7 | **2,57** | BUG-04 |
| 2 | Doanh thu Dashboard gấp đôi tổng đơn Đã giao nhưng người dùng vẫn tin | T1 | 3 | 5/7 | **2,14** | BUG-08, BUG-22 |
| 2 | Thêm danh mục xong không có thông báo thành công | T2 | 3 | 5/7 | **2,14** | BUG-09 |
| 4 | Danh sách người dùng chỉ có email, không có cột Tên và ô tìm kiếm | T4 | 3 | 4/7 | 1,71 | BUG-23 |
| 5 | F5 quay về Dashboard làm lạc hướng | Cả luồng | 3 | 3/7 | 1,29 | BUG-14 |
| 6 | Nhãn và định dạng không nhất quán (Delivered, Role, 150,000 và 150.000, Hoàn thành và Đã giao) | T3 | 2 | 4/7 | 1,14 | BUG-22 |
| 7 | Bấm "Thêm mới" nhiều lần vì không thấy phản hồi | T2 | 2 | 3/7 | 0,86 | BUG-12, BUG-11 |
| 8 | Đơn đã hủy vẫn có nút "Đánh dấu Đã giao" | T3 | 2 | 2/7 | 0,57 | BUG-07 |
| 8 | Không có chỉ báo đang tải | Cả luồng | 2 | 2/7 | 0,57 | BUG-11 |
| 8 | Chữ và nút nhỏ, khó đọc/khó bấm với người lớn tuổi | Cả luồng | 2 | 2/7 | 0,57 | BUG-18, BUG-19 (xem mục 5) |

**Nhận xét phân loại:** cả mười phát hiện đều lặp lại ở ít nhất 2 người nên được coi là vấn đề thiết kế, không phải lỗi đơn lẻ; ba vấn đề cuối (2/7) nên xem là bằng chứng yếu hơn.

## 4. Đối chiếu giả thuyết (kế hoạch, `01_test_plan.md`)

| Giả thuyết | Quan sát được ở | Kết luận |
|---|---|---|
| T1: tin con số doanh thu sai | 5/7 | **Được xác nhận**; chỉ 2 người (P03, P04) tự phát hiện lệch |
| T2: không chắc đã thêm được | 5/7 | Xác nhận |
| T2: bấm nhiều lần | 3/7 | Xác nhận một phần |
| T3: lo lắng khi bấm không có xác nhận | 6/7 | **Xác nhận mạnh nhất** |
| T3: hiểu sai nhãn trạng thái | 4/7 | Xác nhận một phần |
| T4: mất thời gian vì không có tìm kiếm | 4/7 | Xác nhận; hai người dùng Ctrl+F của trình duyệt để vượt qua |
| Cả luồng: F5 làm lạc hướng | 3/7 | Xác nhận một phần |

## 5. Kết nối với bug đã báo (Task 1)

Toàn bộ 10 phát hiện trùng với bug đã đăng (xem `bugs/GitHub_Issues.md`), nên **kết quả usability củng cố mức độ nghiêm trọng** của chúng bằng dữ liệu người dùng thật:
- BUG-04 (không xác nhận) và BUG-09 (không phản hồi thành công) là hai vấn đề người dùng cảm nhận rõ nhất.
- BUG-08 (doanh thu gấp đôi) nguy hiểm vì **đa số người dùng không nhận ra**, đây là lỗi niềm tin.
- **Một điểm chưa có trong 25 bug:** cỡ chữ nhỏ (nút hành động 12 px). Bug BUG-18 chỉ nêu vùng bấm, BUG-19 chỉ nêu tương phản. Đề xuất bổ sung một bug riêng (`bugs/issues/BUG-26.md`, đã đăng thành issue #46).

## 6. Khuyến nghị theo thứ tự ưu tiên

1. Thêm hộp xác nhận trước Xác nhận, Hủy, Xóa; nêu rõ đối tượng và cảnh báo không hoàn tác (BUG-04).
2. Sửa công thức doanh thu và Việt hóa nhãn "Delivered" (BUG-08).
3. Hiện thông báo thành công và làm nổi dòng mới sau mỗi thao tác (BUG-09).
4. Thêm cột Tên và ô tìm kiếm ở danh sách người dùng (BUG-23).
5. Dùng URL theo tab để F5 giữ nguyên vị trí (BUG-14).
6. Thống nhất định dạng tiền và tên trạng thái (BUG-22); tăng cỡ chữ và vùng bấm.

## 7. Hạn chế của nghiên cứu

- **Mẫu nhỏ (7 người)** và không ngẫu nhiên: tuyển từ người thân và bạn bè, nên điểm SUS và tỉ lệ chỉ mang tính định hướng.
- **Hồ sơ không đồng đều:** 3/7 chưa có kinh nghiệm bán hàng; 2/7 là sinh viên trường kỹ thuật, quen máy hơn đối tượng mục tiêu (chủ shop nhỏ).
- **Hình thức không đồng nhất:** 3 phiên tại chỗ, 4 phiên từ xa; ở phiên từ xa độ trễ điều khiển có thể làm tăng thời gian và số lần bấm lặp, gây nhiễu cho phát hiện "không có chỉ báo tải".
- **Không có video** (theo ghi nhận của người kiểm thử); bằng chứng là ghi chú quan sát, phiếu SUS và câu trả lời probe.
- **Mức nghiêm trọng do một người đánh giá**, chưa có người thứ hai kiểm chứng chéo.
- Người điều phối quen biết participant có thể ảnh hưởng cách họ trả lời (đặc biệt phần tin cậy).
