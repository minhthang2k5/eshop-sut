# AI k6 Script Audit

Ứng dụng nội bộ để audit hai k6 script do AI sinh ra theo rubric chuẩn 10 tiêu chí của EShop. Ứng dụng không thay thế baseline, stress hoặc spike test; nó chỉ chạy smoke test nhỏ để chứng minh script hoạt động cơ bản.

## Chạy ứng dụng

Từ thư mục `test-web-performance`:

```powershell
npm run install:all
npm run dev:server
```

Ở cửa sổ khác:

```powershell
npm run dev:frontend
```

Mở `http://localhost:5175`. Khởi động SUT API trước ở `http://localhost:3000`.

## Đầu vào và đầu ra

- Upload: một HAR đã redacted và hai file `.js` bất kỳ, hiển thị Script 1 / Script 2 cùng tên file. Hai artifact thực tế trong samples là Gemini và Claude.
- Rubric: server dùng cấu hình máy đọc `server/src/rubric.js`, được đối chiếu với tài liệu chuẩn `../docs/rubric_audit.md`; không yêu cầu upload rubric.
- Smoke profile: 1 VU, 1 iteration, timeout 45 giây.
- Đầu ra: audit dashboard, evidence theo từng tiêu chí, và `rubric_scorecard.md` tải từ dashboard.

## Độ chính xác của bộ đánh giá

Source được parse bằng Acorn, không thực thi bằng Node. Bộ chấm nhận diện correlation qua JSON.parse/hàm hỗ trợ, header có hoặc không có dấu nháy, xác suất qua hằng số và hàm random dữ liệu. Comment không được tính làm evidence. Mẫu chưa nhận diện được được đánh dấu cần đối chiếu source; phân tích tĩnh hỗ trợ các cấu trúc phổ biến, chưa chứng minh ngữ nghĩa đúng cho mọi JavaScript.

Smoke đọc cả summary-export dạng phẳng và handleSummary dạng nested. Chỉ pass khi có request/check thực thi, đủ metric, không có check/request lỗi, timeout hoặc lỗi runtime được ghi nhận. Smoke 1 iteration chỉ xác nhận nhánh đã chạy.

Chạy `npm --prefix server test` từ thư mục test-web-performance. Audit cũ giữ nguyên evidence/điểm đã lưu; tạo audit mới để áp dụng bộ chấm mới, không tự sửa điểm lịch sử hoặc điểm người chấm đã duyệt.

## An toàn khi chạy script

Backend chỉ gọi k6 bằng file vừa upload, luôn ép 1 VU/1 iteration, chỉ cho SUT URL nằm trong allowlist (mặc định `http://localhost:3000`), và từ chối import HTTP không phải k6 hoặc chuỗi URL ngoài allowlist. Đây là công cụ chạy trong môi trường học tập/local; không upload script không tin cậy lên server công khai.

## Cấu hình

Có thể tạo `server/.env`:

```text
PORT=4000
SUT_BASE_URL=http://localhost:3000
K6_BINARY=k6
```

Frontend proxy `/api` sang `http://localhost:4000`.

## AI review bằng ChatGPT (tùy chọn)

Menu tài khoản ở đầu trang hỗ trợ đăng nhập và đăng xuất ChatGPT. Đăng xuất xóa phiên kết nối của ứng dụng trên máy; không đăng xuất tài khoản khỏi website ChatGPT và không xóa audit. Audit đang xem và các chỉnh điểm được khôi phục sau khi quay lại từ đăng nhập (trong cùng tab, khi trình duyệt cho phép session storage). Đầu vào dùng nhãn Script 1 / Script 2 và hiển thị tên file; tên field upload và tên file lưu nội bộ được giữ để tương thích với audit cũ.

Không cần API key để chạy audit, chấm điểm, chỉnh điểm hay tải scorecard. Sau khi audit xong, chọn **Bỏ qua AI review** để giữ nguyên kết quả rule engine + k6, hoặc chọn **Continue with ChatGPT** rồi cấp quyền dùng ChatGPT plan. Credentials OAuth được lưu cục bộ trong `server/data/chatgpt-auth/` (đã bị Git ignore), không được gửi vào Git.

AI chỉ nhận source script, rubric và evidence k6 để giải thích/rà soát thêm. AI không thay đổi điểm tự động; điểm luôn do rule engine, k6 và reviewer quyết định. Luồng này chỉ hoạt động khi tài khoản được ChatGPT cấp quyền `chatgpt.tokens.use.direct`; nếu không, cứ bỏ qua AI review và dùng đầy đủ phần audit còn lại.

## D7 — Luna đề xuất threshold và correlation

Dashboard có mục **Gợi ý hiệu năng**. Luna 5.6 reasoning medium tự phân tích source và smoke evidence để đề xuất threshold và correlation cho từng script. Prompt cố định cấu trúc JSON, không cố định con số hoặc flow. Backend kiểm tra dữ liệu rồi lưu kết quả; frontend dựng hai bảng từ JSON. Threshold có lý do, evidence và cách kiểm chứng; correlation có nguồn lấy dữ liệu, nơi truyền vào, hiện trạng và cách sửa. Trường confidence được lưu trong JSON nhưng không hiện nhãn độ tin cậy trên giao diện. Điểm rubric không thay đổi.

Chưa kết nối ChatGPT thì D7 hiển thị trạng thái chưa có đề xuất. Smoke 1 iteration không đủ làm baseline; Luna được phép để expression null khi thiếu dữ liệu. Kết quả cũ dùng template cố định cần tạo lại; không được gắn nhãn là đề xuất Luna. Output mới được xuất thành bảng trong scorecard. Prompt để tự tạo bản ghi D7 bằng ChatGPT nằm ở [`../docs/d7_luna_prompt.md`](../docs/d7_luna_prompt.md).

`server/.env` chỉ cần cấu hình local:

```text
PORT=4000
SUT_BASE_URL=http://localhost:3000
K6_BINARY=k6
FRONTEND_ORIGIN=http://localhost:5175
```
