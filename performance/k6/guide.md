# Lưu ý khi viết lại baseline và spike

Cập nhật: 02/11/2026. Đây là hướng dẫn cho lần viết lại tiếp theo, chưa phải xác nhận các thay đổi đã được triển khai. Tham chiếu: [baseline.js](baseline.js), [spike.js](spike.js), [analyzer](analyze/README.md), [fixture](data/README.md).

## 1. Chốt workload trước khi sửa code

Hai bài phục vụ mục tiêu khác nhau; cần giữ rõ ý nghĩa của từng bài và ghi lại mọi thay đổi workload khi so sánh kết quả cũ/mới.

| Nội dung | Baseline hiện tại | Spike hiện tại |
|---|---|---|
| Mục tiêu | Quan sát hiệu năng ổn định ở tải nền | Quan sát suy giảm và recovery sau tăng tải đột biến |
| Profile | 0 → 50 VU/60s; giữ 50 VU/300s; hạ về 0/60s | Bắt đầu 50 VU/30s; nhảy lên 1500 VU/60s; giảm về 50 VU/60s |
| Phase đánh giá | `steady` | `hold_50`, `hold_1500`, `recovery_1` |
| Mix Search/Detail/Cart/Checkout | 55/25/14/6 | 40/20/22/18 |
| Login | Lazy login, cache token riêng từng VU | Lazy login, cache token riêng từng VU |
| Phân account | Một account/VU, hiện yêu cầu 50 account | Chia vòng tròn trên 50 account; đỉnh có thể 30 VU/account |
| Dữ liệu nghiệp vụ | Keyword `iPhone`, sản phẩm ID 1 | Keyword `iPhone`, sản phẩm ID 1 |

Mỗi iteration chọn **một** nghiệp vụ; login là request bổ sung khi cần xác thực. Không chuyển thành chuỗi Search → Detail → Cart → Checkout mà vẫn mô tả là cùng workload.

Think time hiện tại: Search/Cart 1–3s, Detail 2–5s, Checkout 3–6s. Giữ sleep ở cả nhánh thành công, HTTP lỗi và login lỗi để pacing không thay đổi khi hệ thống suy giảm. Không đặt RPS mục tiêu mới nếu vẫn dùng mô hình tải theo VU.

Nếu muốn đổi sang fixture đa dạng, account theo iteration hoặc login mỗi thao tác như stress, cần ghi rõ đó là phiên bản workload mới. Đặc biệt, import thẳng `lib/workload.js` sẽ mang theo mix, chiến lược login, metric và profile stress.

## 2. Sửa tương thích fixture trước khi phát tải

- `data/test_accounts.csv` hiện có 10.000 account; baseline/spike đều đang chặn nếu số account khác 50. Chỉ chạy lại runner hiện tại sẽ dừng ở bước init với fixture này.
- Chọn rõ chính sách: dùng tập con 50 account đã seed, hay cho phép tập account lớn hơn và phân phối lại. Baseline có thể lấy 50 account khác nhau cho 50 VU; spike cần quyết định có tiếp tục chia sẻ account hay cấp đủ account riêng cho VU đỉnh.
- Kiểm tra header, trường bắt buộc, email duy nhất và đủ số account cho chính sách đã chọn. Dừng sớm nếu thiếu fixture; không âm thầm quay vòng account khi thiết kế yêu cầu mỗi VU một account.
- Parser CSV hiện tại dùng `split(',')` và từ chối quoting. Nếu chuẩn hóa parser, giữ cùng quy ước với seed: hỗ trợ dấu phẩy trong trường quoted, dấu nháy kép escape và BOM; không tự tuyên bố hỗ trợ CSV nhiều dòng nếu parser chưa xử lý.
- `lib/data.js` có kiểm tra manifest và giới hạn dữ liệu riêng của stress. Chỉ tái sử dụng sau khi đã xác nhận các ràng buộc đó phù hợp; đổi CSV phải cập nhật manifest bằng `node performance/k6/data/build-manifest.cjs`.
- Chọn sản phẩm và keyword thực sự tồn tại trong DB đã seed. Nếu chuyển sang phân bố nhiều sản phẩm/keyword, cập nhật cả expected response và mô tả workload.

Thứ tự chuẩn bị vẫn là **khởi động backend → đợi sẵn sàng → seed đúng DB → kiểm tra fixture → chạy tải**. Backend reset DB khi khởi động; seed trước khi khởi động có thể bị xóa. Khi so sánh gốc/tuned, giữ tương đương dữ liệu ban đầu, số order và trạng thái giỏ hàng.

## 3. Login, token và skipped

- Token giữ riêng trong trạng thái của từng VU. Với lazy login, chỉ login khi Cart/Checkout cần token; không chia sẻ token qua `setup()`.
- Login chỉ thành công khi status 200 và body có token dạng chuỗi không rỗng. Parse JSON lỗi phải thành một kết quả thất bại, không làm iteration văng lỗi ngoài kiểm soát.
- Login lỗi: ghi lỗi login, tăng skipped cho thao tác bị chặn, không gửi Cart/Checkout thiếu token, vẫn nghỉ think time.
- Với lazy login, khi API bảo vệ trả 401, xóa token để lần thao tác bảo vệ sau đăng nhập lại. Spike đã có nhánh này; baseline hiện chưa có. Không retry ngay request ghi vì checkout timeout có thể đã tạo order trên server.
- Lazy login có thể hoàn tất hết trong ramp-up. **Không yêu cầu `count>0` cho Login trong steady** rồi kết luận baseline FAIL chỉ vì không có login tại cửa sổ đó.

Phải chọn chính sách skipped cùng cách ghi nhận lỗi thao tác:

| Trạng thái | Chính sách |
|---|---|
| Baseline/spike hiện tại | Skipped vẫn là điều kiện FAIL: baseline toàn bài, spike từng phase |
| Stress hiện tại | Skipped chỉ để theo dõi; login lỗi đã tính vào `business_operations_failed` |
| Nếu muốn baseline/spike bỏ FAIL độc lập do skipped | Bổ sung metric lỗi thao tác trước; cập nhật threshold, analyzer và tài liệu cùng lúc |

Không chỉ xóa threshold skipped rồi coi các thao tác không gửi được là thành công. Nếu bổ sung metric nghiệp vụ, mỗi thao tác đã có kết quả phải được tính thành công/thất bại đúng một lần; login lỗi chặn Cart/Checkout là một thao tác thất bại. Iteration bị ngắt chưa có kết quả không mặc định là thành công. Theo dõi thêm số thao tác được chọn, HTTP nghiệp vụ thực gửi, skipped và thao tác hoàn tất để đối chiếu.

Khi tính tỷ lệ theo phase, cả mẫu thành công và thất bại phải có cùng bộ tag. Baseline hiện gọi `skippedRequests.add(0)` không tag nhưng nhánh lỗi có tag; cần thống nhất nếu muốn xuất metric skipped theo phase/endpoint.

## 4. Profile, phase và tag phải nhất quán

- Dùng một profile để sinh executor stages và phân loại phase. Baseline hiện có stages và mốc `60000`/`360000` khai báo riêng; viết lại cần tránh sửa một chỗ nhưng quên chỗ còn lại.
- Tính phase từ `exec.scenario.startTime`; không dùng lúc tiến trình k6 khởi động vì còn init/setup.
- Gắn `phase`, `endpoint`, `name` ổn định theo **lúc request bắt đầu**. Login và request nghiệp vụ có thể thuộc hai phase khác nhau; tính lại phase sau login.
- Nếu thêm metric thao tác, chọn rõ phase của thao tác, chẳng hạn lúc bắt đầu iteration; không trộn với phase lúc HTTP bắt đầu hoặc hoàn tất.
- Giữ tên endpoint nhất quán: `login`, `search`, `detail`, `cart`, `checkout`. Không đưa URL chứa ID/keyword/token vào tag `name`; dùng tên route ổn định như `GET /api/products/:id`.
- Spike có stage chuyển target `0s` (`burst`, `unload`): không coi đó là cửa sổ có thời lượng để tính RPS hoặc bắt buộc có request. Giữ chúng trong profile để mô tả chuyển tải.
- Phân biệt lịch target với VU thực tế; công việc đang chạy và grace có thể còn tiếp tục qua ranh giới phase. Ghi grace rõ ràng và không abort do threshold fail trước khi đo xong recovery.

Chuẩn hóa địa chỉ sau khi lấy giá trị môi trường:

```javascript
const BASE_URL = (__ENV.BASE_URL || 'http://localhost:3000').replace(/\/+$/, '');
```

Baseline hiện chỉ `.replace()` trên chuỗi mặc định do vị trí dấu ngoặc; URL môi trường có dấu `/` cuối chưa được chuẩn hóa.

## 5. Checks và threshold

Giữ checks cho cả status và body; HTTP thành công không đồng nghĩa nghiệp vụ đúng. Với SUT hiện tại:

- Status thành công là 200.
- Search kiểm tra cấu trúc/kết quả theo keyword đã chọn; Detail kiểm tra đúng sản phẩm.
- Cart kiểm tra thông báo `Added to cart`; Checkout kiểm tra `orderId` là số nguyên dương.
- Checkout tạo order độc lập với giỏ và không xóa giỏ; không gán thêm giả định “checkout thành công nghĩa là cart đã rỗng”.

Giữ `http.expectedStatuses(200)` nếu hợp đồng API chưa đổi; timeout hiện tại là 10s. Giữ `summaryTrendStats` gồm avg, median, p95, p99 để analyzer có dữ liệu cần thiết.

Đối chiếu phạm vi threshold trước khi viết lại:

| Phạm vi | Baseline | Spike |
|---|---|---|
| p95 <500ms, HTTP lỗi <1%, checks ≥99%, request count >0 | Tổng steady và từng API nghiệp vụ trong steady | Tổng và từng API nghiệp vụ trong mỗi hold/recovery |
| Login | Có SLO riêng toàn bài | Chỉ thống kê toàn bài, hiện chưa có SLO riêng |
| Skipped | Count =0 toàn bài | Count =0 từng phase |

Không tự thêm SLO Login cho spike hoặc chuyển Login baseline sang steady mà không cập nhật thiết kế. Khi cần thống kê không có threshold, có thể khai báo submetric với danh sách threshold rỗng như code hiện tại; thiếu mẫu hiển thị N/A.

Checks failure rate và HTTP error rate có mẫu số khác nhau; hiện mỗi request có hai checks. Không coi chúng là cùng một metric. Percentile dùng đúng summary của cửa sổ; không cộng hoặc lấy trung bình percentile giữa endpoint/phase.

## 6. Đồng bộ với analyzer và báo cáo

Khi đổi phase, thời lượng, target VU, metric hoặc threshold, cập nhật mục tương ứng trong [analyze/profiles.json](analyze/profiles.json):

- `profile`: tên phase, số giây, target; tên phase phải duy nhất.
- `assess_phases`: phase có thời lượng dương và thực sự cần đánh giá.
- `rules`: tên metric, statistic, toán tử, giới hạn, scope `phase`/`global`, endpoint.
- `description`: đúng chính sách login/skipped thực thi.

Analyzer và script k6 hiện dùng hai cấu hình riêng; sửa script không tự cập nhật analyzer. Giữ tag/submetric cần thiết được xuất trong `summary.json`. Analyzer không đọc raw `metrics.json` để bù các metric thiếu và không tự suy ra lỗi thao tác từ HTTP error rate.

Đánh giá dữ liệu đã lưu từ `eshop-sut`:

```bash
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type baseline
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type spike
```

Mặc định xuất `analysis/report.md`, `analysis/report.html` và CSV trong run. Báo cáo dùng bảng tổng quan, bảng phase/điều kiện và các biểu đồ VU, p95, CPU/RAM khi đủ dữ liệu.

Khi dùng `--report-dir`, tên báo cáo theo loại test và nội dung được tạo lại toàn bộ. Tránh xuất analyzer thẳng vào thư mục run baseline: runner baseline đã có dashboard k6 tên `baseline_report.html`, trùng tên HTML mà analyzer dùng với `--report-dir`. Dùng thư mục `analysis/` mặc định hoặc thư mục đích riêng.

## 7. Runner, timeline và CPU/RAM nếu bổ sung

Runner baseline/spike hiện chỉ lưu summary, raw metrics và log; baseline có thêm dashboard k6. Chưa có bước thu CPU/RAM theo cửa sổ run hoặc tự gọi analyzer. Nếu mở rộng:

1. Tạo thư mục riêng cho mỗi run; lưu đúng summary/log/timeline và chỉ phần mẫu tài nguyên thuộc run đó. Bộ thu backend đã có trong [telemetry/](telemetry/README.md), không cần viết lại collector.
2. Ghi mốc epoch milliseconds: `before_start_ms`, `k6_start_ms`, `scenario_start_ms`, `k6_end_ms`, `after_end_ms`; lưu `profile` thực tế và `interrupted`. Thời gian phải đúng thứ tự. Nếu thu trước/sau như stress, giữ backend đến khi thu xong.
3. Ưu tiên lưu `scenario_start_ms`/`profile` trực tiếp trong `measurement-timeline.json`. Fallback log của analyzer hiện chỉ nhận marker `STRESS_TIMELINE`; marker mới tên `BASELINE_TIMELINE` hoặc `SPIKE_TIMELINE` sẽ chưa được nhận nếu không cập nhật parser.
4. Gọi analyzer sau khi có summary/timeline, kể cả khi k6 kết thúc với threshold fail. Với `set -e`/`pipefail`, hook đặt ngay sau pipeline k6 có thể không được chạy khi k6 trả 99; cần quản lý mã thoát hoặc trap hoàn tất tương tự runner stress.
5. Giữ mã thoát k6: analyzer thành công không được biến kết quả k6 fail thành exit 0. Khi Ctrl-C, dừng k6, đánh dấu run bị ngắt và không khẳng định đã đủ toàn bộ lịch tải.
6. Khi telemetry bị tắt/không tìm thấy, vẫn tạo báo cáo HTTP. Không tạo mẫu CPU/RAM bằng 0 để lấp dữ liệu thiếu.

RPS phase = request count / thời lượng cửa sổ quan sát. Nếu chỉ có profile danh định, ghi rõ cơ sở `nominal`; không dùng `rate` submetric vốn chia cho thời gian toàn bài. Thiếu timeline không tự suy ra timestamp từ tên thư mục. PASS trên metric với độ đầy đủ UNKNOWN chưa chứng minh đã chạy đủ lịch.

Recovery đạt chỉ phản ánh cửa sổ quan sát, không xác định chính xác giây hồi phục. CPU 100% = một core; RAM = RSS (MiB). CPU/RAM không có SLO riêng trong cấu hình hiện tại và chưa đủ để kết luận nút thắt hoặc memory leak.

## 8. Lưu dữ liệu và tiêu chí kiểm tra sau khi viết lại

Git ignore hiện bao phủ `output/telemetry/`, `node-cpu-ram.jsonl`, `node-cpu-ram.csv`, `cpu-ram-phases.csv`, `cpu-ram-before-during-after.csv`; `k6.log` và `metrics.json` cũng được ignore riêng. Các file vẫn tồn tại trên máy. Muốn chuyển bằng chứng đo sang máy khác, lưu riêng mẫu JSONL của run, timeline và log nếu cần khôi phục profile; CSV có thể tạo lại. Summary k6 không chứa mẫu CPU/RAM.

Trước khi chạy tải đầy đủ, đối chiếu:

- Fixture 10.000 account không còn bị chặn vì điều kiện đúng 50; chính sách phân account đã được kiểm tra với VU nền/đỉnh.
- Login trả body sai, timeout hoặc 401 được tính đúng; không retry write; nhánh lỗi vẫn sleep.
- Request đi qua ranh giới phase được gắn tag tại lúc bắt đầu; global/phase của login và skipped đúng thiết kế.
- Metric bắt buộc thiếu hoặc window count=0 không tạo PASS giả; các vi phạm vẫn được giữ khi run bị ngắt.
- Summary đủ p95/p99 và submetric để analyzer đánh giá; cấu hình analyzer khớp script.
- Nếu sửa runner, kiểm tra cả exit 0, exit 99, Ctrl-C và telemetry tắt; không ghi đè dashboard hoặc artifact run khác.

Chạy kiểm thử đối chiếu hiện có từ `eshop-sut`:

```bash
python3 -m unittest discover -s performance/k6/analyze -v
bash -n performance/k6/run-baseline.sh
bash -n performance/k6/run-spike.sh
```

Kiểm thử có Node.js kiểm tra profile/threshold khớp cấu hình analyzer; không chứng minh workload runtime, fixture hay HTTP thực tế đã đúng. Nếu đổi cấu trúc khởi tạo JS/metric, cập nhật phần giả lập của kiểm thử tương ứng và xác minh các nhánh thực thi bằng kiểm tra tập trung trước khi đo tải đầy đủ.
