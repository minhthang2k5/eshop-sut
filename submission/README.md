# Bộ báo cáo seminar Performance Testing

Mở [báo cáo chính](Bao_cao_seminar_Performance_Testing.md) bằng VS Code Markdown Preview hoặc trình xem Markdown hỗ trợ bảng và Mermaid.

## Cách bổ sung của nhóm

- Lê Nguyễn Quốc Thái (A, MSSV 23120352) điền chương 4, bài tập 1 và bổ sung minh chứng thực nghiệm của mình vào bảng đóng góp khi cần.
- Võ Hữu Thắng (B, MSSV 23120355) điền chương 5, bài tập 2 và bổ sung minh chứng thực nghiệm của mình vào bảng đóng góp khi cần.
- Lê Nguyễn Quốc Thái và Võ Hữu Thắng cùng hoàn thiện bảng so sánh thực nghiệm, kết luận chung và thông tin nhóm ở đầu báo cáo.
- Phần Trịnh Hồ Minh Thắng (C, MSSV 23120354) đã có nội dung chương 6, bài tập 3, ảnh và dữ liệu minh chứng. Giữ nguyên liên kết evidence khi chỉnh sửa hoặc di chuyển báo cáo.

Chương 2 giải thích các khái niệm bằng ví dụ EShop: loại test, SUT/contract, script k6, VU/iteration, workload/think-time, metric/phân vị, check/threshold, HAR, data driven/correlation, phân tích source/runtime, tuning/hồi quy và evidence/AI. Chương 7 chỉ điền bài tập 3 về quy trình web audit; bài tập 1–2 để trống cho hai thành viên phụ trách.

Mục 8.2 có phân công cả ba thành viên theo tuần 1–3 và mã Jira; phần Trịnh Hồ Minh Thắng được chia theo đầu vào/rubric → web audit → evaluator/AI/test/báo cáo. Ba ảnh phân công dùng nguyên bản trong `Split_task/`, kèm nguồn và checksum riêng. Trạng thái Jira được đối chiếu ngày 23/10/2026; các tuần là mốc kế hoạch, không phải lịch sử ngày tạo/hoàn thành task.

## Nội dung thư mục

```text
submission/
  Bao_cao_seminar_Performance_Testing.md
  README.md
  Split_task/
    sprint_1.png
    sprint_2.png
    sprint_3.png
    README.md
    SHA256SUMS.txt
  evidence/
    01-upload.png ... 08-regression-tests.png
    09-ai-review-result.png
    10-ai-threshold-results-part-1.png
    11-ai-threshold-correlation-results.png
    12-ai-correlation-results.png
    audit-results.json
    rubric_scorecard.md
    script-1-summary.json
    script-2-summary.json
    script-1-k6.log
    script-2-k6.log
    luna-d7-output.json
    evaluation-tests.txt
    har-api-manifest.json
    ai_prompt_template.txt
    d7_luna_prompt.md
    SHA256SUMS.txt
    scripts/
      gemini_script_real.js
      claude_scipt_real.js
```

## Truy vết số liệu

- Audit minh chứng ở mục 6.5–6.8: `AUD-20261023-E85CDC`, 09:50:07 ngày 23/10/2026, UTC+7.
- Output Luna đã lưu: `AUD-20261023-CD3D6B`, 08:57:54 cùng ngày. Báo cáo trình bày output này theo đúng evidence của lần chạy đó, không ghép vào metric của audit mới.
- Bốn ảnh `09-ai-review-result.png` đến `12-ai-correlation-results.png` do Trịnh Hồ Minh Thắng cung cấp sau khi chạy AI, chèn tại mục 6.9.1. Ảnh hiển thị p95 khoảng 86,7 ms và 1,21 ms, không có audit ID/thời điểm chạy; giữ riêng với hai audit nêu trên. Nội dung chồng lặp giữa các ảnh là phần tiếp theo của bảng, không phải nhiều lần chạy.
- Hai script và rubric dùng cho audit mới được giữ trong evidence. Log k6 được thay phần đường dẫn máy bằng `<PROJECT_ROOT>`; summary vẫn giữ số liệu gốc.
- Thư mục không chứa profile OAuth, `.env`, token phiên hoặc HAR nguyên bản. Manifest HAR chỉ giữ method/path/status.
- `SHA256SUMS.txt` hỗ trợ kiểm tra tính toàn vẹn của file evidence; không bao gồm chính file hash.

Các link `../docs/` và `../api_specification.md` trong báo cáo trỏ tới tài liệu trong repository. Khi gửi riêng submission, có thể đọc phần của Trịnh Hồ Minh Thắng và evidence độc lập; gửi kèm repository để truy cập toàn bộ source và các tài liệu nền.
