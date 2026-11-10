---
name: gui-checklist
description: Thiết kế GUI checklist (IA-01 chuẩn UI chung, IA-02 form, IA-03 điều hướng, IA-04 phản hồi/trạng thái) cho một màn hình web theo từng bước của bài giảng GUI Testing (nguyên tắc Nielsen/Norman/Shneiderman, checklist theo control, validation), có cổng review của người kiểm thử và bước bổ sung mục AI hay bỏ sót. Dùng khi người dùng muốn lập hoặc mở rộng checklist giao diện cho một màn hình/tab mới, chuẩn bị bảng Passed/Failed, hoặc làm HW03 GUI & Usability. Không dùng để chạy test tự động, sửa bug, hay thiết kế test case chức năng.
---

# GUI Checklist theo từng bước

Lập checklist giao diện cho MỘT màn hình mỗi lần chạy. Viết tiếng Việt, giữ thuật ngữ English. Đây là kiểm thử **hộp đen**: chỉ dựa vào những gì quan sát được trên giao diện và mô tả đặc tả, không dựa vào mã nguồn để kết luận.

Không bao giờ nộp kết quả thô của AI. Quy trình có một **cổng review bắt buộc** (bước 6): người kiểm thử quyết định từng mục; AI không tự quyết thay.

## Tài liệu tham chiếu (đọc khi cần)

- [ia-and-heuristics.md](references/ia-and-heuristics.md): định nghĩa IA-01..04, quy ước phân loại IA, Nielsen 10, Norman 6, Shneiderman 8.
- [control-checklists.md](references/control-checklists.md): checklist theo từng control (Text box, Dropdown, Button, Checkbox/Radio, Hyperlink, Image, Grid, List, Date, Validation).
- [gap-checklist.md](references/gap-checklist.md): các khía cạnh AI hay bỏ sót và ba nhóm nguyên nhân.
- [output-format.md](references/output-format.md): cột bảng, quy ước ID, mẫu bảng review và bảng mục bổ sung, mẫu bug report.
- [item-quality-rules.md](references/item-quality-rules.md): quy tắc viết một mục checklist tốt.

## Đầu vào cần có

Hỏi người dùng nếu thiếu: (a) tên màn hình và cách mở nó (URL, vai trò, tài khoản test lấy từ file seed của dự án); (b) màn hình/luồng đã có thành viên khác nhận (đọc `scope.md` nếu có); (c) thư mục lưu kết quả (mặc định `checklist/` và `prompts/` cạnh `scope.md`).

## Quy trình

1. **Kiểm tra phạm vi.** Đọc scope của nhóm. Không lập mục cho màn hình đã giao cho người khác; mục so sánh với tab khác chỉ để kiểm tra nhất quán.
2. **Quan sát màn hình thật.** Mở màn hình bằng trình duyệt có sẵn (đọc cấu trúc trang, văn bản, chụp ảnh nếu có). Viết bản mô tả hộp đen: bố cục, từng control, dữ liệu hiện có, và danh sách **những gì KHÔNG có** (tìm kiếm, phân trang, nút Sửa...). Lưu thành file prompt 01 kèm tool, ngày giờ.
3. **Sinh mục theo nguyên tắc (IA-01, IA-03, IA-04).** Dùng Nielsen/Norman/Shneiderman trong `ia-and-heuristics.md`. Mỗi mục ghi nguyên tắc nguồn. Mỗi IA khoảng 8–10 mục. Prompt phải tự chứa mô tả màn hình và quy tắc ở `item-quality-rules.md`.
4. **Sinh mục theo control (IA-01, IA-02).** Chỉ áp dụng checklist của control có thật trên màn hình; liệt kê control "không áp dụng" kèm lý do. Truyền vào prompt danh sách ý đã phủ ở bước 3 để không lặp.
5. **Màn hình có form: sinh mục validation (IA-02, IA-04).** Áp dụng Text box và Validation, gồm golden rule (lỗi thì đưa focus về ô sai). Nếu màn hình không có form, ghi rõ IA-02 mỏng và đề xuất màn hình khác bù, không ép sinh mục.
6. **Gộp và CHỜ REVIEW của người kiểm thử.**
   - Gộp các bảng bằng `scripts/merge_checklist.py` (đọc trực tiếp các bảng, đánh ID nháp `D-001...`, không chép tay).
   - Nêu các cặp có thể trùng ý, mục có kết quả mong đợi mơ hồ (nhiều "hoặc", "nếu"), mục cần giả lập nặng hoặc có thể làm mất dữ liệu.
   - Dừng lại và yêu cầu người dùng quyết định từng mục: Giữ / Sửa / Tách / Gộp / Bỏ, kèm lý do. Chỉ đề xuất, không tự áp dụng.
7. **Quét mục AI bỏ sót.** Dùng `gap-checklist.md`, ưu tiên điều người dùng quan sát được khi chạy thật. Mỗi mục bổ sung phải có cột "Vì sao AI bỏ sót" thuộc một trong ba nhóm: Chất lượng prompt / Giới hạn của model / Đặc thù giao diện. Đánh dấu mục nào đã được xác nhận khi chạy thật và mục nào chỉ suy ra (ví dụ từ đọc code).
8. **Xuất kết quả** theo `output-format.md`: bảng cuối (csv/md) có các cột Kết quả, Notes, Screenshot để trống; bảng quyết định review; bảng mục bổ sung và lý do; hướng dẫn chuẩn bị dữ liệu/giả lập. Ghi lại mọi prompt và tool đã dùng để làm AI Audit Report.

## Quy tắc không được vi phạm

- Không tuyên bố Passed/Failed, đã chạy test hay đã tìm thấy bug khi chưa thực thi. Kết quả mong đợi chỉ là chuẩn tham chiếu.
- Không tự đặt thông báo lỗi, giới hạn hay quy tắc mà đặc tả không nêu; nếu thiếu thì ghi câu hỏi.
- Không kết luận lỗi chỉ từ đọc mã nguồn. Nếu một mục xuất phát từ mã nguồn, gắn nhãn "suy ra từ code, cần xác nhận khi chạy".
- Không dùng thao tác có thể làm mất dữ liệu (xóa tài khoản đang đăng nhập, tắt rồi bật lại backend nếu nó seed lại DB) khi chưa nêu cách sao lưu và khôi phục.
- Không tự quyết định giữ/bỏ mục thay người kiểm thử; không chép lại nội dung của người khác trong nhóm.
- Không đưa mật khẩu hay token thật vào kết quả; dùng tài khoản test từ file seed của dự án.

## Giai đoạn thực thi (sau khi checklist được người dùng duyệt)

Chạy từng mục, ghi Passed/Failed vào bảng, ghi Notes ngắn cho mỗi mục Failed, chụp ảnh chỉ cho mục Failed, rồi lập bug report theo mẫu trong `output-format.md`. Chỉ báo bug khi đã tái hiện được ít nhất hai lần.
