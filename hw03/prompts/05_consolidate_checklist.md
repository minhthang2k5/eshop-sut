# Prompt 5 – Gộp và định dạng thành bảng checklist thống nhất

- **Mục đích:** Gộp kết quả của Prompt 2 (Lần 2), 3 và 4 thành **một bảng checklist duy nhất** với ID thống nhất, sẵn sàng để thực thi (Passed/Failed). Bước này chỉ gộp và định dạng, **không thêm mục mới**; việc review và bổ sung mục AI bỏ sót là Bước 4.
- **Căn cứ lý thuyết:** slide GUI Testing, trang 9 (biến nguyên tắc thành bảng review chấm Yes/No/N/A kèm priority và severity, Mandatory/Optional).
- **Tool dùng:** Claude Code (Claude Sonnet 5.5), ngày 2026-11-10 (giờ chính xác xem `AI_Audit_Log.md`).
- **Cách thực hiện:** thay vì để AI chép lại 61 dòng (dễ sai sót khi chép tay), Claude Code viết và chạy một script Python đọc trực tiếp các bảng trong file Prompt 2, 3, 4, gộp, đánh lại ID và xuất file. Script lưu tại `scripts/merge_checklist.py` (xem mục cuối).
- **Lưu ý:** Prompt 2 chỉ lấy **Lần 2**; Lần 1 (AI mất bối cảnh, tự đọc mã nguồn) giữ lại làm bằng chứng nhưng không đưa vào checklist.

---

## Prompt (yêu cầu giao cho AI)

```text
Hãy gộp ba bảng checklist GUI (Prompt 2 Lần 2, Prompt 3, Prompt 4) thành MỘT bảng duy nhất. Chỉ gộp và định dạng; KHÔNG thêm, sửa nội dung hay bỏ mục nào.

Yêu cầu:
1. Đánh lại ID thống nhất dạng D-001, D-002, ... theo thứ tự: màn hình (Admin: Người dùng trước, Admin: Danh mục sau), trong mỗi màn hình theo IA-01, IA-02, IA-03, IA-04.
2. Cột của bảng: ID | Màn hình | IA | Control / Thành phần | Mục kiểm tra | Kết quả mong đợi | Ưu tiên | Nguồn mục | Nguyên tắc / checklist nguồn | Kết quả (Passed/Failed) | Notes | Screenshot.
3. Cột "Nguồn mục" ghi rõ mục do AI sinh, từ prompt nào và ID gốc (ví dụ "AI – Prompt 3 – C3-07") để về sau phân biệt với mục do người kiểm thử tự thêm.
4. Cột Kết quả, Notes, Screenshot để trống.
5. Xuất cả Markdown và CSV (UTF-8 có BOM để mở bằng Excel).
6. Báo cáo: tổng số mục, số mục theo màn hình, theo IA, theo mức ưu tiên, và các mục có thể trùng ý (chỉ nêu, không tự xóa).
```

---

## Kết quả

- File Markdown: `../checklist/GUI_Checklist_draft.md`
- File CSV (mở bằng Excel): `../checklist/GUI_Checklist_draft.csv`

### Thống kê

| Chỉ tiêu | Giá trị |
|---|---|
| Tổng số mục | **61** |
| Theo màn hình | Admin: Người dùng 43; Admin: Danh mục 18 |
| Theo IA | IA-01: 16; IA-02: 20; IA-03: 9; IA-04: 16 |
| Theo ưu tiên | Mandatory 45; Optional 16 |
| Theo prompt nguồn | Prompt 2 (Lần 2): 29; Prompt 3: 14; Prompt 4: 18 |

Phân bố theo màn hình và IA:

| Màn hình | IA-01 | IA-02 | IA-03 | IA-04 |
|---|---|---|---|---|
| Admin: Người dùng | 16 | 8 | 9 | 10 |
| Admin: Danh mục | 0 | 12 | 0 | 6 |

### Mục có thể trùng ý (chỉ nêu, chưa xóa – để quyết định ở Bước 4)
- AI-03-04 (Tab trên menu) và AI-03-05 (Enter trên menu): cùng nhóm bàn phím trên menu.
- C3-07 (Tab tới nút Xóa) và C3-08 (Enter/Space trên nút Xóa): cùng nhóm bàn phím trên nút Xóa.
- AI-01-05 và AI-01-06: cùng là đo tương phản, khác phần tử (nút Xóa và menu).
- C4-04 (để trống) và C4-05 (chỉ khoảng trắng); C4-13 (thêm thành công) và C4-14 (bấm Thêm hai lần).
- AI-04-10 (checkbox dòng phản hồi) và nhóm C3-01 đến C3-06 (checkbox): cùng control, khác góc nhìn.
- Không có cặp nào trùng hoàn toàn nên chưa loại mục nào ở bước này.

### Nhận xét của người kiểm thử
_(bảng đã đủ sạch để thực thi chưa? có mục nào cần tách, gộp hay đổi ID? IA nào đang mỏng: IA-03 chỉ có 9 mục và chỉ ở màn hình Người dùng, IA-01 chưa có ở màn hình Danh mục)_
