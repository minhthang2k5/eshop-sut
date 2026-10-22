# Sample scripts

- `chatgpt_script_good.js`: script mẫu đạt các rule tĩnh của rubric. Khi SUT đã seed và chạy, k6 smoke cũng phải pass.
- `claude_script_with_errors.js`: script cố ý dùng `/api/auth/login`, đọc `accessToken`, gửi token sai header, thiếu workload/data/thresholds để dashboard có evidence lỗi rõ ràng.

Khi tạo audit, upload `docs/localhost.har` cùng hai file này.
