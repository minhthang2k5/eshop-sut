# Công cụ thu thập dữ liệu (Task 2, Phase 1)

> Gồm: **SUS** (thang chuẩn sau phiên), **SEQ** (sau mỗi nhiệm vụ), **câu hỏi probe** (bốn chủ đề bắt buộc), và các mẫu ghi chép. Bản nháp do Claude Code hỗ trợ soạn ngày 2026-11-11.

## 1. Vì sao dùng SUS

SUS (System Usability Scale, Brooke 1996) là thang 10 câu, 5 mức, được dùng rộng rãi, ngắn (3 phút), cho điểm 0 đến 100 và có mốc so sánh (trung bình ngành khoảng 68). Phù hợp với mẫu nhỏ (7 người) và đề cho phép dùng SUS trực tiếp. SEQ bổ sung đánh giá độ khó theo từng nhiệm vụ (slide Usability, trang 53 nhắc dùng "Likert + SEQ").

## 2. SUS – bản tiếng Việt (đưa cho participant sau phiên)

Hướng dẫn: *"Với mỗi câu, hãy khoanh một số từ 1 (Hoàn toàn không đồng ý) đến 5 (Hoàn toàn đồng ý) cho thấy bạn nghĩ gì về trang quản trị vừa dùng. Không có đáp án đúng hay sai."*

| # | Câu | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Tôi nghĩ rằng tôi sẽ muốn dùng trang quản trị này thường xuyên. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Tôi thấy trang quản trị này phức tạp không cần thiết. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Tôi thấy trang quản trị này dễ sử dụng. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Tôi nghĩ rằng tôi cần sự giúp đỡ của một người có kỹ thuật để dùng được trang này. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Tôi thấy các chức năng của trang này được kết hợp với nhau hợp lý. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Tôi thấy trang này có quá nhiều chỗ không nhất quán. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Tôi nghĩ hầu hết mọi người sẽ học cách dùng trang này rất nhanh. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Tôi thấy trang này rất rườm rà, khó dùng. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Tôi cảm thấy rất tự tin khi dùng trang này. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Tôi cần học rất nhiều thứ trước khi có thể bắt đầu dùng trang này. | ☐ | ☐ | ☐ | ☐ | ☐ |

(Các câu 1, 3, 5, 7, 9 là câu tích cực; 2, 4, 6, 8, 10 là câu tiêu cực. Không thay đổi thứ tự câu.)

### Cách tính điểm SUS

- Câu lẻ (1, 3, 5, 7, 9): đóng góp = **điểm − 1**.
- Câu chẵn (2, 4, 6, 8, 10): đóng góp = **5 − điểm**.
- **Điểm SUS = tổng 10 đóng góp × 2,5** (thang 0 đến 100).
- Mốc tham khảo: dưới 51 kém; 51 đến 68 dưới trung bình; 68 trung bình; 68 đến 80 tốt; trên 80 rất tốt.
- File tính tự động: `SUS_Scoring.xlsx` (sheet SUS).

## 3. SEQ – sau mỗi nhiệm vụ (Single Ease Question)

> "Nhìn chung, việc vừa rồi **dễ hay khó** với bạn?" Thang 1 (Rất khó) đến 7 (Rất dễ).

Hỏi ngay sau khi participant kết thúc từng nhiệm vụ T1 đến T4; ghi vào `SUS_Scoring.xlsx` (sheet Nhiệm vụ).

## 4. Câu hỏi probe (phỏng vấn cuối phiên)

Hỏi **trung lập**, câu hỏi mở, không gợi ý đáp án, hỏi vào chi tiết khi thấy participant vướng. Phủ **bốn chủ đề bắt buộc**:

### A. Rõ ràng (Clarity)
1. Hãy kể lại những gì bạn thấy trên màn hình đầu tiên. Có gì bạn không hiểu không?
2. Các con số và tên gọi trên trang (ví dụ doanh thu, trạng thái đơn, tên các nút) có rõ nghĩa với bạn không? Chỗ nào bạn phải đoán?
3. Khi bạn cần tìm chức năng, bạn đã nhìn vào đâu trước? Vì sao?
4. Có chỗ nào bạn tưởng một thứ nhưng hóa ra là thứ khác?

### B. Phục hồi lỗi (Error recovery)
5. Có lúc nào bạn làm nhầm hoặc nghĩ mình làm nhầm không? Chuyện gì xảy ra và bạn làm gì tiếp?
6. Sau khi làm xong một việc (thêm nhóm hàng, xác nhận đơn), làm sao bạn biết nó đã thành công?
7. Nếu bạn lỡ xóa nhầm một thứ, bạn mong trang này giúp gì cho bạn?

### C. Tốc độ (Speed)
8. Việc nào bạn thấy mất nhiều thời gian hơn bạn nghĩ? Điều gì làm nó chậm?
9. Có lúc nào bạn chờ và không biết trang đang làm gì không?
10. Bạn có phải làm lại hoặc quay lại bước nào không?

### D. Tin cậy (Trust)
11. Bạn có tin các con số trên trang tổng quan không? Vì sao?
12. Khi bấm các nút như Xác nhận, Hủy, Xóa, bạn có yên tâm không? Điều gì làm bạn lo?
13. Bạn có dám dùng trang này cho cửa hàng thật của bạn không? Điều gì khiến bạn ngần ngại?
14. Điều gì làm bạn tin hoặc không tin trang này?

### Câu kết
15. Nếu được thay đổi **một điều** để trang dễ dùng hơn, đó là điều gì?
16. Bạn muốn nói thêm gì không?

## 5. Mẫu bảng ghi nhận nhanh trong phiên

(Mẫu chi tiết ở `03_moderator_script_and_notes_template.md`.)

| Phiên | Nhiệm vụ | Bắt đầu | Kết thúc | Thời gian | Kết quả (H / HTG / K) | Số lỗi | Số lần trợ giúp | SEQ (1-7) | Ghi chú vướng mắc |
|---|---|---|---|---|---|---|---|---|---|

H = hoàn thành, HTG = hoàn thành có trợ giúp, K = không hoàn thành.

## 6. Biện minh lựa chọn công cụ

| Công cụ | Lý do chọn |
|---|---|
| SUS | Thang chuẩn, cho phép so với mốc ngành (68), ngắn, phù hợp 7 người |
| SEQ | Đo độ khó từng nhiệm vụ, giúp chỉ ra nhiệm vụ nào làm điểm SUS thấp |
| Think-aloud và probe | Giải thích "vì sao", cần cho phần phân tích định tính |
| Thời gian, tỉ lệ hoàn thành, lỗi | Số liệu khách quan (slide trang 37) |

Không dùng UEQ-S vì đề chỉ yêu cầu một thang chuẩn; SUS đủ và có mốc so sánh rõ.
