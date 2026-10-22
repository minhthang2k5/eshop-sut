# Baseline Test Report – eShop

> Kết luận: **PASS — baseline một lần đo**, run `baseline-20261022-110446-eGLTX1`. Đủ workload, 25/25 thresholds đạt; chưa đánh giá độ lặp lại giữa các lần chạy.

## 1. Metadata và mục tiêu

| Trường | Giá trị |
|---|---|
| Người thực hiện | Người dùng thực hiện test; chưa cung cấp tên |
| Ngày / giờ / múi giờ | 22/10/2026, khoảng 11:04:46–11:11:48, UTC+07:00 (Asia/Ho_Chi_Minh) |
| Run ID | `baseline-20261022-110446-eGLTX1` |
| Build / checksum source | Không được lưu kèm run; không suy ngược từ source hiện tại |
| Phiên bản k6 / Node.js / OS | Linux theo người thực hiện; phiên bản cụ thể không được lưu trong bộ kết quả |
| Script | [baseline.js](baseline.js) |
| URL SUT | Chạy local, server và k6 cùng máy; URL mặc định của script là `http://localhost:3000`, không có bản ghi biến môi trường để xác nhận override |
| Raw metrics | [metrics.json](output/baseline-20261022-110446-eGLTX1/metrics.json) |
| Summary | [summary.json](output/baseline-20261022-110446-eGLTX1/summary.json) |
| Execution log | [k6.log](output/baseline-20261022-110446-eGLTX1/k6.log) |
| Nguồn số liệu tài nguyên | Quan sát Linux Resources do người thực hiện cung cấp; không có log tài nguyên theo thời gian đính kèm |

Đo mốc hiệu năng ở tải bình thường 50 VUs, dùng đối chiếu các lần cập nhật code trong cùng điều kiện. Phạm vi: Search, Detail, Cart, Checkout theo API/payload của `smoke.js`; Login chạy lazy trong flow Cart/Checkout và có thống kê riêng. Login được tính vào latency/error rate tổng, bao gồm tổng steady nếu request bắt đầu trong steady. Không đánh giá giới hạn tải hoặc browser rendering.

## 2. Workload và load profile

Theo `4_ZipTool/Tool_Analysis_and_Theory.md`, mục 2.3–2.4:

| API nghiệp vụ | Xác suất mỗi iteration | Think time sau request |
|---|---:|---:|
| GET /api/products?search=iPhone | 55% | Uniform 1–3 s |
| GET /api/products/1 | 25% | Uniform 2–5 s |
| POST /api/cart | 14% | Uniform 1–3 s |
| POST /api/checkout | 6% | Uniform 3–6 s |

Closed workload, mỗi VU lặp: chọn ngẫu nhiên một API nghiệp vụ → lazy login nếu Cart/Checkout chưa có token → gửi request nghiệp vụ → check status/body → sleep. Tỷ lệ 55/25/14/6 là xác suất chọn **API nghiệp vụ**, không bao gồm Login và không phải tỷ lệ VUs; khi login lỗi, request nghiệp vụ được bỏ qua nên tỷ lệ request thực gửi có thể lệch; ghi nhận tỷ lệ thực tế mỗi lần chạy. Think time trung bình có trọng số là 2.525 s. RPS phụ thuộc cả thời gian phản hồi, không áp đặt arrival rate hoặc threshold RPS chưa có căn cứ.

| Giai đoạn | Thời gian tính từ lúc scenario bắt đầu | VUs | Tag |
|---|---|---|---|
| Ramp-up | [0, 60) s | 0 → 50 | `ramp_up` |
| Steady-state | [60, 360) s | 50 | `steady` |
| Ramp-down | [360, 420) s | 50 → 0 | `ramp_down` |

Tổng profile 7 phút, chưa tính thời gian khởi tạo và chờ iteration kết thúc. k6 có thể cho iteration đang chạy hoàn tất khi giảm VUs; thời lượng thực tế cần lấy từ log. Dùng grace period mặc định của executor k6 (30 s); ghi lại phiên bản k6 khi đối chiếu. Không dùng CLI override stages/duration cho lần đo chính thức vì cửa sổ steady trong script cố định.

CSV `data/test_accounts.csv` được đọc bằng `SharedArray`: yêu cầu đúng 50 email duy nhất, header `email,password,name,role`, bốn cột không rỗng và không dùng quoting (đúng định dạng fixture hiện tại). Dữ liệu sai sẽ dừng ở init trước khi phát tải. VU ID 1–50 lần lượt dùng dòng tài khoản 1–50; không chia sẻ tài khoản/token giữa VUs. Tài khoản phải tồn tại trong DB; script không tự đăng ký.

Mỗi VU giữ `authToken` riêng qua các iteration. Search/Detail không login; lần đầu chọn Cart hoặc Checkout sẽ gọi `POST /api/login` nếu chưa có token. Thành công thì cache token; thất bại thì ghi checks/HTTP error, tăng `business_requests_skipped`, bỏ request cần token và vẫn sleep theo nhánh đã chọn. Lần sau chọn Cart/Checkout sẽ thử login lại. Không tự refresh token đã có; JWT của backend hiện không đặt expiry.

Login có tag `endpoint:login` và phase tại thời điểm bắt đầu request. Request nghiệp vụ tính lại phase sau Login để không bị gán sai khi đi qua mốc 60/360 s. Login toàn test có thống kê và thresholds riêng; Login steady chỉ là thống kê (có thể không có mẫu nếu tất cả đã login trong ramp-up). Không có mẫu thì ghi N/A, không coi latency/error bằng 0.

Giữ dataset giống smoke: keyword iPhone, sản phẩm ID 1, giá 30,000,000, số lượng 1. Đây là workload cố định trên 50 tài khoản và một sản phẩm, có thể ưu tiên cache; không đại diện phân bố toàn catalog. Backend hiện checkout không đọc/xóa giỏ hàng, nên checkout được gọi độc lập để giữ đúng tỷ lệ API. Giỏ hàng tách theo user/VU và tăng trong RAM; mỗi checkout thêm một order SQLite. Khi đối chiếu lần sau, cần giữ dữ liệu tương đương và khởi động lại backend để xóa cart. Snapshot DB và số orders ban đầu của run này chưa được lưu; không khẳng định trạng thái dữ liệu đã được đóng băng.

## 3. Threshold và điều kiện chạy

| Chỉ số | Ngưỡng tự động | Căn cứ |
|---|---|---|
| Login toàn test | p95 < 500 ms, HTTP lỗi < 1%, checks ≥ 99%, count > 0 | Cùng SLO; theo dõi xác thực riêng |
| Business requests bị bỏ qua do login lỗi | 0 | Tránh kết luận đạt khi workload bị thiếu |
| Steady HTTP p95 | < 500 ms | SLO trong tài liệu mục 2.2 |
| Steady HTTP error rate | < 1% | SLO trong tài liệu mục 2.2 |
| Steady checks pass rate | ≥ 99% | Status + body, mục 2.7 |
| Steady số request | > 0 tổng và từng API nghiệp vụ | Chống thiếu mẫu/không chạy đủ cửa sổ |

Ba ngưỡng hiệu năng/check áp dụng cả tổng steady (gồm Login phát sinh trong steady) và **từng API nghiệp vụ**, tránh Search che khuất Checkout. HTTP thành công phải là status 200; body sai vẫn làm checks thất bại dù HTTP thành công. p90/p99 được ghi nhận, chưa có SLO riêng. Threshold `count>0` chỉ kiểm tra có mẫu, không chứng minh cỡ mẫu đủ tin cậy.

CPU/RAM/DB I/O là số liệu quan sát bên ngoài k6; chưa có NFR tài nguyên nên không tự đặt ngưỡng PASS/FAIL. Không diễn giải checks failure rate thành HTTP error rate (mỗi request có hai checks).

**Entry thực tế:** lần chạy trước bị lỗi do quên `seed.js` (người thực hiện xác nhận). Run hiện tại ghi nhận 50/50 Login thành công, đủ Cart/Checkout và checks đúng dữ liệu. Không có log smoke hoặc snapshot DB kèm run để xác minh riêng các bước này.

**Exit áp dụng:** một lần đo theo phạm vi đã thống nhất; đủ cửa sổ steady 5 phút với 50 VUs, có mẫu cả bốn API, thresholds đạt và có metrics/summary/log. Không yêu cầu ba lần chạy; độ lặp lại chưa được đánh giá. Tài nguyên toàn máy được ghi nhận thủ công, không dùng làm threshold tự động.

## 4. Môi trường và cách chạy

| Thành phần | Cấu hình / bằng chứng |
|---|---|
| App và load generator | Node.js backend và k6 chạy chung một máy Linux; RAM toàn máy 7.39 GB, Swap 8.59 GB |
| CPU / phần cứng | Chưa ghi nhận model CPU, số core hoặc cấu hình phần cứng chi tiết |
| Database | SQLite embedded trong backend; chưa ghi nhận version, journal mode, kích thước, snapshot và số orders ban đầu |
| Dataset sử dụng | 50 tài khoản từ CSV, thao tác trên sản phẩm ID 1; không suy ra tổng catalog chỉ có một sản phẩm |
| Kịch bản | Local execution, một scenario, tối đa 50 VUs, ba stages, profile 7 phút |
| Grace period | Log ghi `gracefulRampDown: 30s`, `gracefulStop: 30s` |
| Monitoring | Linux Resources, quan sát cấp toàn máy; chưa tách Node.js/SQLite/k6 |

Lệnh tái chạy từ thư mục gốc repository sau khi chuẩn bị tài khoản/dữ liệu:

```bash
bash sut/eshop-sut/test/run-baseline.sh
```

Runner lưu raw metrics, summary và log trong thư mục riêng dưới `test/output/`. Báo cáo này chỉ phân tích run đã có, không chạy lại hoặc thay đổi dữ liệu. Smoke dùng tài khoản hard-code nên không thay thế việc kiểm tra 50 tài khoản CSV.

**Quy tắc xử lý:** số liệu baseline lấy từ tag `phase:steady`; p50 là `med`, thời gian phản hồi tính bằng ms. RPS steady = count / **300 s**, không lấy trường `rate` trong summary (được chuẩn hóa theo thời lượng cả run). Tổng steady gồm Login; mix nghiệp vụ lấy mẫu số là 5919 request Search/Detail/Cart/Checkout, loại sáu Login. TPS theo từng API bằng RPS API, không phải TPS của hành trình mua hàng hoàn chỉnh.

Tag phase được chốt ngay trước từng request; request hoàn tất qua ranh giới stage vẫn giữ phase lúc bắt đầu. Timestamp trong raw JSON là thời điểm phát mẫu, không phải mốc chính xác bắt đầu scenario. Cửa sổ steady là [60,360) s từ scenario start, khoảng 11:05:46–11:10:46 UTC+07:00; mẫu HTTP steady đầu/cuối được ghi lúc **11:05:46.249 / 11:10:46.232**. Không dùng khoảng cách hai mẫu này làm mẫu số RPS.

## 5. Kết quả đo và phân tích

### 5.1 Tổng quan steady-state

| Chỉ số | Giá trị |
|---|---|
| Cửa sổ đo | [60,360) s, 300 giây; khoảng 11:05:46–11:10:46 UTC+07:00 |
| VUs steady | 50; log duy trì 50/50 VUs trong steady |
| Tổng request, gồm Login | 5925 |
| Throughput tổng steady | **19.750 requests/s** |
| Request nghiệp vụ / throughput nghiệp vụ | 5919 / **19.730 requests/s** |
| Latency avg / p50 | 2.516 / 2.034 ms |
| Latency p90 / p95 / p99 / max | **3.082 / 8.122 / 14.546 / 18.441 ms** |
| HTTP error rate | **0% (0/5925)**; tất cả trả status 200 |
| Checks pass rate | **100% (11850/11850)** |
| Request timeout | 0 ghi nhận trong run |
| Business requests bị bỏ qua | 0 toàn run |
| Iterations bị ngắt | 0 toàn run theo log |

Quy ước: số thập phân dùng dấu chấm; số đếm không dùng dấu phân cách hàng nghìn.

### 5.2 Chi tiết API trong steady-state

| API | Count | Mix nghiệp vụ (%) | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | RPS | HTTP lỗi (%) | Checks đạt (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Search | 3247 | 54.857 | 2.003 | 2.810 | 3.071 | 4.808 | 10.823 | 0 | 100 |
| Detail | 1480 | 25.004 | 1.972 | 2.788 | 3.031 | 4.440 | 4.933 | 0 | 100 |
| Cart | 843 | 14.242 | 1.867 | 2.594 | 2.770 | 5.721 | 2.810 | 0 | 100 |
| Checkout | 349 | 5.896 | 11.516 | 15.368 | 16.006 | 16.681 | 1.163 | 0 | 100 |
| Login | 6 | N/A | 2.461 | 3.413 | 3.600 | 3.750 | 0.020 | 0 | 100 |

Mix thực tế là **54.857 / 25.004 / 14.242 / 5.896%**, sát mục tiêu 55/25/14/6%; độ lệch lớn nhất khoảng **0.242 điểm phần trăm**. Sai lệch nhỏ phù hợp cơ chế chọn nhánh ngẫu nhiên. Tổng các tỷ lệ làm tròn có thể lệch 0.001%.

**Login toàn test:** 50 request thành công, trong đó 44 ở ramp-up và 6 ở steady, không có ở ramp-down. Avg **3.230 ms**, p50 **2.931 ms**, p90 **4.320 ms**, p95 **4.820 ms**, p99 **13.751 ms**, max **21.519 ms**; HTTP lỗi 0%, checks 100% (100/100). Count này phù hợp cơ chế lazy login một lần cho mỗi VU. Percentile Login steady chỉ dựa trên sáu mẫu, cần đọc cùng cỡ mẫu; không thay số này cho thống kê Login toàn run.

### 5.3 Toàn run và phân loại lỗi

| Chỉ số toàn run (gồm ramp-up/down) | Giá trị |
|---|---|
| Thời lượng thực thi | Khoảng 7 phút 02.2 giây theo log |
| HTTP requests / iterations hoàn tất | 7187 / 7137; chênh lệch 50 là Login bổ sung |
| HTTP throughput toàn run | 17.023 requests/s; không dùng thay RPS steady |
| Latency avg / p50 / p90 / p95 / p99 / max (ms) | 2.539 / 2.068 / 3.107 / 8.122 / 14.843 / 21.519 |
| HTTP lỗi / checks đạt | 0/7187; 14374/14374 checks đạt |
| Network received / sent | 3042704 / 1227833 bytes |

| Loại lỗi | Steady | Toàn run | Bằng chứng |
|---|---:|---:|---|
| HTTP 4xx | 0/5925 | 0/7187 | Raw HTTP request status đều 200 |
| HTTP 5xx | 0/5925 | 0/7187 | Raw HTTP request status đều 200 |
| Lỗi transport/timeout | 0/5925 | 0/7187 | Không có HTTP request lỗi |
| Check status/body không đạt | 0/11850 checks | 0/14374 checks | Checks đạt 100% |
| Request nghiệp vụ bỏ qua do Login lỗi | 0 | 0 | `business_requests_skipped` |

### 5.4 Tài nguyên máy dùng chung

Nguồn: người thực hiện quan sát Linux Resources. Đây là khoảng quan sát, **không phải avg/max được tính từ chuỗi thời gian**, không phải RSS của backend hoặc k6.

| Phạm vi | Chỉ số | Kết quả được cung cấp |
|---|---|---|
| Toàn máy: server + k6 + hệ điều hành/tác vụ khác | CPU | 4–7% |
| Toàn máy | Memory | 3.20 GB / 7.39 GB, khoảng 43%; dao động 43–45% |
| Toàn máy | Swap | 2.03 GB / 8.59 GB, khoảng 24%, không đổi |
| Trước / trong / sau test | Memory và Swap | Duy trì ổn định theo quan sát người thực hiện |
| Node.js + SQLite riêng | CPU / RSS | Không thu thập riêng |
| k6 riêng | CPU / RSS | Không thu thập riêng |
| SQLite riêng | CPU / RAM | N/A: embedded trong Node.js, chưa có profiler để quy thuộc |
| Hệ thống / DB | Disk I/O, swap-in/out, GC, event-loop lag | Không thu thập |

Quan sát chưa cho thấy CPU hoặc RAM toàn máy bị bão hòa ở mức tải này. Swap đã chiếm 24% và không tăng; không thể suy ra không có swap I/O vì chưa đo swap-in/out. RAM ổn định trong bài test ngắn không đủ chứng minh không có memory leak. Do k6 và server cùng máy, số liệu này không tách được chi phí của từng thành phần hoặc đại diện mạng production.

### 5.5 Nhận xét hiệu năng

Checkout chậm hơn các API khác: p95 **16.006 ms**, so với Search **3.071 ms**, Detail **3.031 ms**, Cart **2.770 ms**. Backend Checkout thực hiện ghi order vào SQLite nên có thêm công việc so với thao tác đọc/cart trong RAM; đây là giải thích khả dĩ theo luồng xử lý, **chưa phải kết luận bottleneck DB** vì chưa có profiling/I/O. Tất cả API đều cách xa ngưỡng 500 ms; p95 Checkout chỉ khoảng 3.2% ngưỡng này.

p95 tổng là 8.122 ms, thấp hơn p95 Checkout do Checkout chỉ chiếm khoảng 5.9% request nghiệp vụ; cần giữ bảng per-API khi so sánh regression. Không có lỗi, iteration bị ngắt hoặc bằng chứng bão hòa trong lần đo. Kết quả chỉ xác nhận workload đã thử, không xác định tải tối đa hệ thống.

## 6. Baseline tham chiếu một lần đo

Theo phạm vi đã thống nhất, chọn run **`baseline-20261022-110446-eGLTX1`** làm baseline hiện tại. Không yêu cầu ba lần chạy, không tính mean/std dev/CV giữa các run từ một mẫu. Các chỉ số tham chiếu tổng steady là **p90 3.082 ms, p95 8.122 ms, p99 14.546 ms, RPS 19.750, HTTP lỗi 0%**; bảng mục 5.2 là reference theo API.

Khi đối chiếu code mới, giữ 50 VUs, stages 1m/5m/1m, think time và mix, 50 tài khoản, sản phẩm/keyword, trạng thái DB/cart, cấu hình máy và cách chạy chung máy tương đương. Dùng cùng cách lọc `phase:steady` và mẫu số 300 s. Build/snapshot/version chưa được lưu ở run này làm giảm khả năng tái lập chính xác; cần lưu các thông tin đó ở lần đo sau. Độ lặp lại và độ biến thiên tự nhiên giữa các run **chưa được xác minh**.

Quy tắc cảnh báo regression đề xuất (chưa phải SLO đã duyệt): p90/p95 tăng >10% hoặc RPS giảm >10% trong điều kiện tương đương; vẫn kiểm tra SLO tuyệt đối độc lập. Không coi biến động một lần đo là bằng chứng chắc chắn do thay đổi code. Error reference bằng 0 thì so sánh chênh lệch điểm phần trăm, không chia cho 0.

**Sự cố chuẩn bị dữ liệu trước đó:** run `baseline-20261022-104957-BIQXTW` có 1372 Login trả 401 và không gửi Cart/Checkout; người thực hiện xác nhận quên chạy `seed.js`. Run lỗi bị loại khỏi reference và không được dùng để tính mức cải thiện hiệu năng so với run hiện tại, vì workload thực thi khác nhau.

## 7. Đối chiếu và kết luận

| Tiêu chí | Kết quả | Đánh giá |
|---|---|---|
| Steady 50 VUs × 5 phút, có mẫu bốn API | Đủ cửa sổ; Search 3247, Detail 1480, Cart 843, Checkout 349 | PASS |
| p95 tổng steady <500 ms | 8.122 ms | PASS |
| p95 từng API nghiệp vụ <500 ms | Cao nhất Checkout 16.006 ms | PASS |
| HTTP lỗi tổng steady và từng API <1% | Tất cả 0% | PASS |
| Checks tổng steady và từng API ≥99% | Tất cả 100% | PASS |
| Login toàn test đạt ngưỡng | 50 mẫu; p95 4.820 ms, lỗi 0%, checks 100% | PASS |
| Không bỏ request nghiệp vụ | 0 | PASS |
| Tất cả thresholds cấu hình | 25/25 đạt theo summary và log | PASS |
| Một lần đo, lưu đủ metrics/summary/log | Có đủ ba tệp nguồn; 7137 iterations hoàn tất, 0 bị ngắt | PASS |
| Tài nguyên | CPU 4–7%, RAM 43–45%, Swap 24% ổn định; quan sát toàn máy | Ghi nhận, không có threshold tài nguyên |
| Độ lặp lại / tài nguyên từng tiến trình | Chưa đo | Ngoài phạm vi lần đo này |

**Kết luận: PASS cho baseline một lần đo đã thống nhất.** Workload nghiệp vụ được thực thi đầy đủ, các SLO cấu hình đều đạt và tài nguyên toàn máy không có dấu hiệu tăng bất thường theo quan sát được cung cấp. Sử dụng số liệu steady và từng API làm mốc cho lần đối chiếu tiếp theo; giữ các giới hạn về một lần đo, môi trường chạy chung máy, tài liệu môi trường chưa đầy đủ và monitoring thủ công khi diễn giải kết quả.
