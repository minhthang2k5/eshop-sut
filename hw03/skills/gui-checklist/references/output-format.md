# Định dạng đầu ra

## Bảng checklist cuối (`GUI_Checklist_final.csv` và `.md`)

Cột: ID | Màn hình | IA | Control / Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên | Nguồn mục | ID nháp (truy vết) | Nguyên tắc / checklist nguồn | Vì sao AI bỏ sót | Kết quả (Passed/Failed) | Notes | Screenshot

- Cột Kết quả, Notes, Screenshot để trống cho tới khi thực thi. Screenshot chỉ cho mục Failed.
- CSV lưu UTF-8 có BOM để Excel mở đúng tiếng Việt; khi nộp nên xuất thêm `.xlsx`.

### Quy ước ID
- ID nháp (bản gộp từ AI): `D-001`, `D-002`... (tiền tố khác ID cuối để khỏi nhầm).
- ID cuối: `GUI-001`... đánh lại sau khi review, theo màn hình rồi theo IA.

### Quy ước cột "Nguồn mục"
`AI` giữ nguyên; `AI (đã sửa)` có chỉnh nội dung; `AI (đã sửa – gộp)` gộp hai mục nháp; `AI (đã tách k/n)` tách từ một mục nháp; `Tự thêm` do người kiểm thử bổ sung; `Tự thêm – quan sát thật` đã xác nhận khi chạy ứng dụng.

## Bảng quyết định review (`AI_Review_Decisions.md`)

| ID nháp | Nguồn AI | Mục (tóm tắt) | Quyết định (Giữ/Sửa/Tách/Gộp/Gộp vào/Bỏ) | Lý do | ID mới |
|---|---|---|---|---|---|

Kèm thống kê: số mục theo quyết định và tổng số mục AI trong checklist cuối.

## Bảng mục bổ sung (`Added_Items_AI_Gaps.md`)

| ID | Màn hình | IA | Mục bổ sung | Nguyên nhân AI bỏ sót (3 nhóm) | Giải thích | Quan sát thật |
|---|---|---|---|---|---|---|

Kèm nhận xét ngắn làm cơ sở cho phần AI Critique.

## Nhật ký prompt (`prompts/NN_*.md`)

Mỗi prompt một file: mục đích, căn cứ lý thuyết, tool AI, ngày giờ, khối prompt nguyên văn, output nguyên văn, nhận xét của người kiểm thử.

## Hướng dẫn chuẩn bị chạy (`HOW_TO_RUN.md`)

Cách khởi động ứng dụng, tài khoản test, ba điểm cần biết trước khi test (ví dụ DB seed lại khi khởi động, khóa tài khoản, URL không theo tab), bảng chuẩn bị dữ liệu cho từng nhóm mục.

## Mẫu bug report (GitHub Issue) cho mục Failed

```
Tiêu đề: [GUI-xxx] <mô tả ngắn lỗi>
Màn hình: <tên>   IA: <IA-0x>   Mức độ: <Blocker/Major/Minor/Cosmetic>
Môi trường: <trình duyệt, hệ điều hành, kích thước, URL localhost>
Các bước tái hiện:
1. ...
Kết quả mong đợi: ...
Kết quả thực tế: ...
Tần suất: <x/y lần>
Ảnh chụp: (đính kèm)
```
