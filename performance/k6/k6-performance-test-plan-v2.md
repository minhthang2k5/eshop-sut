# Kế hoạch k6 v2 — Black Friday / Flash Sale

Ngày lập: 31/10/2026. Trạng thái: **kế hoạch triển khai, chưa thay đổi script hoặc chạy tải**.

## 1. Mục tiêu và phạm vi đã xác nhận

1. Xác định vùng tải còn đáp ứng SLO và vùng bắt đầu suy giảm trong điều kiện thử nghiệm.
2. So sánh backend gốc và tuned bằng cùng workload, dữ liệu, cấu hình đo và phần cứng.
3. Kiểm chứng việc `userCarts` giữ dữ liệu lâu dài, đối chiếu với diễn biến bộ nhớ và hiệu năng.

Quyết định đã chốt qua phỏng vấn:

- Seed trong khoảng 10.000–50.000 user và 100–500 product; người thực hiện bổ sung dữ liệu seed.
- Stress/spike dùng 10–15 keyword với trọng số khác nhau.
- **Kịch bản chính giữ random thao tác Search/Detail/Cart/Checkout = 40/20/22/18**: mỗi iteration chọn một thao tác nghiệp vụ độc lập. Quyết định này thay thế phương án chuỗi phiên 60/25/15 trước đó; không triển khai chuỗi phiên trong phạm vi hiện tại.
- Stress giữ mỗi bậc 120 giây.
- Ưu tiên một máy chạy cả server và k6; đo riêng Node, k6 và toàn máy.
- Soak khoảng một giờ mỗi backend, gồm thời gian quan sát sau khi ngừng tạo iteration.
- Chỉ thêm đo lường để kiểm chứng vấn đề; **không sửa cơ chế giỏ hàng, không bổ sung tuning backend**.

Các tỷ lệ và cấu hình ghi “đề xuất” bên dưới là mặc định để triển khai thử, chưa phải dữ liệu hành vi Black Friday thực tế hay cam kết từ người dùng.

## 2. Hiện trạng đã đối chiếu mã nguồn

| Thành phần | Hiện trạng và hệ quả |
|---|---|
| `stress.js`, `spike.js` | Bắt buộc đúng 50 account; account chọn theo VU, token giữ suốt VU. Mỗi iteration chọn một API theo xác suất 40/20/22/18. |
| Search/detail/cart | Search cố định `iPhone`; detail/cart cố định ID 1. Chưa có correlation sản phẩm giữa các bước. |
| Stress | 11 bậc 500–2800 VU, ramp 30s + hold 60s, recovery 50 VU trong 60s. |
| Spike | 50 VU/30s → 1500 VU/60s → 50 VU/60s; có grace khi hạ tải. |
| Seed | `data/seed.js` đọc CSV account và ghi SQLite sau khi backend khởi động. Cả hai backend reset bảng khi start; mỗi bên có CSV product riêng, hiện có 5 sản phẩm. |
| Login | Đọc user theo email, đồng thời phát lệnh UPDATE trạng thái login. Tần suất login phụ thuộc chính sách luân phiên account; tăng login làm thay đổi cả tải đọc và ghi DB. |
| Detail | ID chẵn có `price` dạng chuỗi; ID không tồn tại có thể trả 200 với `{}`. Không thể chỉ check HTTP 200. |
| Cart/checkout | Cart `push(req.body)` vào mảng trong `userCarts`; checkout chỉ thêm order, không đọc/xóa giỏ. Mỗi POST cart thành công thêm item; checkout độc lập không dọn item đã có. |
| Tuned | WAL và index tên product đã có; giữ nguyên cấu hình tối ưu hiện hữu. |
| Soak/evidence | Chưa có script soak; report 05 là template. Báo cáo cũ không có chuỗi telemetry đồng bộ đủ để quy nguyên nhân. |

Không dùng kết quả v1 làm đối chứng định lượng trực tiếp cho v2: workload, login, số dữ liệu và thời lượng đã đổi. Phải chạy lại cả hai backend với v2.

## 3. Cấu hình đề xuất cho đợt đầu

| Tham số | Mặc định đề xuất | Quy tắc |
|---|---|---|
| Dataset chính | 10.000 account, 200 product | Cùng snapshot logic ở cả hai backend. 50.000/500 là cấu hình mở rộng riêng, không thay giữa một cặp đo. |
| Thao tác — đã chốt | Search 40%, Detail 20%, Cart 22%, Checkout 18% | Xác suất chọn thao tác mỗi iteration; login bổ sung nằm ngoài tỷ lệ. |
| Search | 12 keyword; 3 hot/4 warm/5 tail | Trọng số cụ thể ở mục 5; tổng 100%. |
| Request timeout | 10s | Không retry write tự động. |
| Think time | Search 1–3s, Detail 2–5s, Cart 1–3s, Checkout 3–6s | Giữ pacing hiện tại: sleep cuối mỗi iteration, kể cả lỗi; không thêm khoảng nghỉ thứ hai. |
| Grace | 60s | Ghi iteration bị ngắt; thời gian grace không mặc nhiên là thời gian idle. |
| Telemetry | 1 mẫu/giây | Cùng cấu hình cho cả hai backend; kiểm tra overhead bằng pilot. |
| Lặp | Stress/spike 3 lần mỗi backend; soak 1 lần mỗi backend trước | Nếu không đủ thời gian, ghi số lần thực tế và hạn chế; soak bất thường cần chạy xác minh. |

Đóng băng cấu hình sau pilot, trước khi thu bộ evidence chính thức. Không chạy toàn bộ tổ hợp dataset nếu chưa có nhu cầu so sánh kích thước dữ liệu.

## 4. Kiến trúc và luồng workload

Giữ kiến trúc hiện có: k6 → Express routes → SQLite hoặc `userCarts` trong bộ nhớ. Tách helper k6 dùng chung cho dữ liệu, thao tác, profile và metrics; telemetry chỉ quan sát và ghi file, không thay nghiệp vụ.

### 4.1 Một iteration chọn một thao tác nghiệp vụ

| Khoảng random `r` trong [0, 1) | Thao tác | Xác suất |
|---|---|---|
| `r < 0.40` | Search | 40% |
| `0.40 <= r < 0.60` | Detail | 20% |
| `0.60 <= r < 0.82` | Cart | 22% |
| `0.82 <= r` | Checkout | 18% |

Không bắt buộc Search trước Detail/Cart hoặc Cart trước Checkout. Với 1.000 iteration, kỳ vọng chọn khoảng 400 Search, 200 Detail, 220 Cart, 180 Checkout; số thực tế dao động do ngẫu nhiên. Ghi cả số thao tác được chọn và số request thực sự gửi vì login lỗi có thể chặn Cart/Checkout.

Login là request bổ sung, không nằm trong mix 40/20/22/18. Không gọi thêm search/detail để chuẩn bị Cart vì sẽ làm đổi mix. Trọng số keyword ở mục 5 chỉ áp dụng bên trong 40% thao tác Search, không thay thế mix API.

### 4.2 Phân phối account và login — đề xuất điều chỉnh theo workload mới

Mục tiêu dùng nhiều account vẫn giữ nguyên, nhưng khái niệm “đổi sau mỗi phiên” không còn áp dụng khi bỏ chuỗi phiên. **Đề xuất đổi account theo iteration**, chưa coi đây là chính sách xác thực người dùng đã chốt:

```js
import exec from 'k6/execution';
const userIndex = exec.scenario.iterationInTest % accounts.length;
```

- Dùng một scenario cho mỗi bài. Trong iteration chọn thao tác; chỉ login nếu là Cart/Checkout, dùng đúng account được phân bổ và token cục bộ của iteration đó. Không dùng token cũ của VU cho account mới.
- Đề xuất không cache token xuyên iteration để tránh state/cache lớn ở máy k6. Với 1.000 iteration đúng tỷ lệ và không lỗi, có 400 login bổ sung: tổng 1.400 request, trong đó Search/Detail/Cart/Checkout vẫn là 400/200/220/180. Đây là hệ quả của chính sách đề xuất, không phải đặc tính bắt buộc của mix random.
- Login theo mỗi thao tác bảo vệ khác login một lần mỗi VU ở v1; phải ghi rõ trong manifest và áp dụng giống nhau cho gốc/tuned. Nếu chọn chính sách khác trước triển khai, cập nhật ví dụ tải login và coverage tương ứng.
- Account của Search/Detail chỉ là phân bổ phía client, server chưa nhận danh tính. Báo riêng account được phân bổ và account login thành công duy nhất; không khẳng định tất cả tài khoản seed đã được dùng trên server.
- Áp dụng một tiến trình k6 cục bộ. Hết tập account thì quay vòng; không cam kết độc quyền khi iteration cũ chưa kết thúc.
- Ghi số iteration bắt đầu/kết thúc/bị ngắt, thao tác thành công/thất bại và request bị bỏ qua do login lỗi. Không dùng số VU làm số khách duy nhất.
- Không dùng user ID/email/iteration ID làm metric tags. Nếu cần unique coverage, ghi audit tối giản gồm chỉ số account và loại sự kiện, khử trùng lặp sau chạy; không ghi password/token. Đo overhead trong pilot.
- Không tăng tải soak chỉ để sử dụng hết account; báo độ phủ thực tế.

### 4.3 Dữ liệu cho thao tác độc lập và xử lý lỗi

1. Search: chọn keyword có trọng số, URL-encode; check mảng và tập ID kỳ vọng từ manifest seed.
2. Detail: chọn ID từ manifest sản phẩm, gọi đúng một request; check ID, tên và giá hợp lệ. Chuẩn hóa giá dạng chuỗi thành số hữu hạn, dương khi kiểm tra.
3. Cart: đề xuất chọn product từ manifest đã đối chiếu seed, gửi ID/name/price và quantity = 1; không gọi Detail trước. Checkout dùng total_amount và địa chỉ fixture hợp lệ, không phụ thuộc giỏ hoặc thao tác trước đó. Đề xuất chọn product đều trong manifest cho Detail/Cart; ghi chính sách này để không nhầm với trọng số search.
4. Search/detail lỗi chỉ làm thất bại thao tác hiện tại; iteration sau vẫn chọn thao tác mới. Login lỗi thì bỏ qua Cart/Checkout đã chọn, tăng counter skipped và sleep theo thao tác đó.
5. Không retry write hoặc login trong cùng iteration. Timeout checkout là kết quả chưa rõ phía server; không gửi lại để tránh tạo order trùng. 401 được ghi lỗi, không lấy token account khác thay thế.

Đây là workload hỗn hợp API dưới tải Black Friday, không phải mô phỏng đầy đủ hành trình chuyển đổi khách hàng. SUT chưa trừ tồn kho, chưa xử lý tranh mua và checkout không xác thực giỏ; không bổ sung các nghiệp vụ đó. Không suy ra tỷ lệ bỏ giỏ/chuyển đổi từ mix 40/20/22/18.

## 5. Seed và phân bố Flash Sale

Người thực hiện bổ sung dữ liệu; phần triển khai cung cấp hợp đồng dữ liệu và preflight để không chạy với fixture thiếu.

- Account CSV giữ schema k6 `email,password,name,role`; email duy nhất, role user cho tải. Không nhầm với schema CSV startup backend có `full_name,scenario`.
- Seed sau khi startup DB hoàn tất; xác minh count và một số account qua API. Kiểm tra cả bản gốc/tuned, không chỉ thông báo server đã listen.
- Product CSV giữ schema hiện có, ID ổn định; giữ các fixture mà smoke/baseline cũ cần. Đồng bộ CSV hai backend và xuất manifest cho k6 từ cùng nguồn.
- Manifest đề xuất gồm dataset ID/hash, số record thực tế, keyword/weight và expected product IDs. Không thêm tag riêng cho từng sản phẩm.
- Search của SUT tìm trong `name`, không phải cột metadata `search_keyword`: tên sản phẩm phải thực sự khớp keyword.
- Đề xuất 12 keyword: hot `iPhone` 25%, `Samsung` 20%, `MacBook` 15%; warm `AirPods` 7%, `iPad` 6%, `Apple Watch` 6%, `Sony` 6%; tail `Keychron`, `Logitech`, `Dell`, `Asus`, `Xiaomi` mỗi keyword 3%. Tổng 100%; phải điều chỉnh tên theo seed thực tế trước khi chạy.
- Bản đầu dùng keyword có kết quả. Nếu bổ sung tìm kiếm không có kết quả, phải định nghĩa đó là kết quả hợp lệ cho thao tác search đó; không áp dụng check mảng không rỗng cho nhóm đó.
- Đề xuất giữ cùng trọng số suốt bài và giữa hai backend, để tách tác động tăng tải khỏi đổi hành vi. Mô phỏng đổi độ hot theo thời gian là biến thể sau.

100–500 product là catalogue nhỏ; tăng số user không thay thế độ lớn catalogue. Không diễn giải kết quả thành hiệu năng tìm kiếm trên hàng triệu sản phẩm.

## 6. Profile tải và thời gian

Giữ mô hình đóng theo VU cho đợt đầu: một VU liên tục chọn và thực hiện thao tác kế tiếp sau think time. Khi response chậm, số iteration mới/giây có thể giảm; kết quả không tương đương một luồng khách đến độc lập, không giảm khi server chậm. Xem [mô hình open/closed của k6](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).

### Stress

- Giữ các bậc đề xuất từ script: 500, 750, 1000, 1250, 1500, 1750, 2000, 2200, 2400, 2600, 2800 VU.
- Mỗi bậc ramp 30s và hold **120s**; sau cùng hạ mục tiêu về 50 VU, recovery 60s.
- Tổng lịch nominal: `11 × (30 + 120) + 60 = 1710s = 28m30s`, chưa tính grace cuối.
- Giữ một nguồn profile cho executor, nhãn phase và phép chia RPS. Hold dùng count/120s; recovery vẫn count/60s.
- Các mức VU là điểm xuất phát từ v1, không phải năng lực đã xác minh với workload v2. Pilot xác minh máy phát tải trước; nếu cần đổi dải, chốt lại và dùng cùng dải cho cả cặp.

### Spike

- Đề xuất giữ nominal 50 VU/30s → 1500 VU/60s → 50 VU/60s; tổng 2m30s trước grace cuối.
- Tăng/hạ target tức thời không có nghĩa request hoặc số iteration đang chạy thay đổi tức thời. Lưu VU thực tế và số iteration còn đang hoàn tất khi hạ tải.
- Recovery phải phân biệt drain của iteration cũ với giai đoạn đã về tải thấp. Nếu hết 60s vẫn chưa đủ bằng chứng phục hồi, ghi “chưa xác định trong cửa sổ quan sát”, không tự báo PASS phục hồi hoàn toàn.

### Soak — `soak-test.js`

- 0–5 phút: ramp từ 0 đến `SOAK_VUS`.
- 5–50 phút: giữ tải 45 phút.
- Phút 50: kết thúc thời gian tạo iteration mới; cho tối đa 60s hoàn tất iteration đang chạy.
- Đến phút 60: runner tiếp tục thu telemetry, giữ server sống, không restart/dọn giỏ. Khoảng 10 phút cuối bao gồm drain tối đa 1 phút và idle còn lại; lưu mốc request cuối thực tế.
- Đề xuất `SOAK_VUS` bằng khoảng 50% mức cao nhất của vùng PASS liên tục chung cho hai backend ở stress; chạy pilot 5 phút để kiểm tra lại. Nếu bậc đầu stress đã fail, phải tìm mức thấp hơn trước khi chốt soak.
- Cùng một mức tải cho hai backend, không chọn riêng theo năng lực từng bản. Nếu đo ổn định chỉ với dataset nhỏ thì không tự áp mức đó cho dataset lớn.

`gracefulStop`/`gracefulRampDown` cho phép iteration đang chạy hoàn tất nhưng có thể ngắt khi hết hạn; cần ghi nhận và không biến iteration bị ngắt thành iteration thành công. Xem [graceful stop của k6](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/graceful-stop/).

## 7. Telemetry và kiểm chứng bộ nhớ

### 7.1 Thu mẫu cùng đồng hồ

Mỗi bản ghi có `run_id`, timestamp UTC epoch ms, nguồn và PID khi thích hợp. Ghi thời điểm scenario bắt đầu cùng profile; request gắn phase tại lúc bắt đầu request, iteration gắn thao tác được chọn và phase bắt đầu riêng. Giữ raw timestamp để xử lý request chạy qua ranh giới phase, không suy phase từ thời điểm hoàn tất.

| Nguồn | Chỉ số bắt buộc/đề xuất |
|---|---|
| Node | CPU tiến trình, RSS, heapUsed, heapTotal, external, arrayBuffers; event-loop delay p95/max theo từng khoảng mẫu. |
| Trạng thái cart | Số key trong `userCarts`, tổng item đang giữ, số lần thêm cart thành công. Dùng counter cập nhật O(1) tại điểm tạo giỏ/push, không duyệt toàn bộ giỏ mỗi giây. |
| k6 | CPU/RSS theo PID thật, VU, iterations, request/s, iteration/s, số iteration bị ngắt. Không lấy PID của shell hoặc `tee` thay cho k6. |
| Toàn máy | CPU theo core và tổng, RAM available/used, swap, disk I/O/iowait, dung lượng trống; ghi cả collector nếu đáng kể. |
| DB | Count lỗi theo mã, đặc biệt BUSY/LOCKED; khi cần, thời gian từ gọi query đến callback theo nhóm search/login/checkout, kích thước DB/WAL. |

Đề xuất collector Linux đọc `/proc` bằng Python standard library; xác minh hệ điều hành/công cụ khi triển khai. Node ghi JSONL qua module dùng chung, bật bằng cấu hình telemetry cho cả hai backend. Không cần triển khai Prometheus/Grafana cho vòng đầu.

CPU tiến trình phải ghi quy ước: 100% tương đương một core; toàn máy chuẩn hóa theo số core và ghi rõ. Event-loop delay đổi ns sang ms, reset histogram sau mỗi mẫu. Thời gian query đến callback bao gồm xếp hàng và lịch event loop, không được gọi là thời gian thực thi SQL thuần. Cách đo tham chiếu [Node memoryUsage](https://nodejs.org/api/process.html#processmemoryusage) và [monitorEventLoopDelay](https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions).

### 7.2 Bằng chứng về `userCarts`

- Giữ cùng lỗi ở cả hai backend; không thêm TTL, clear khi checkout hoặc giới hạn item.
- Vẽ cùng trục thời gian: retained cart items, cart users, heapUsed, RSS, cart successes, p95 và throughput.
- Tổng item phải tăng tương ứng thao tác push phía server; không chỉ dựa vào response phía client vì request timeout có thể đã được xử lý.
- Sau phút 50, đợi drain kết thúc rồi kiểm tra count không giảm khi không còn thêm giỏ. Bộ nhớ tăng/giữ cao kết hợp count và code là bằng chứng dữ liệu tiếp tục được giữ.
- So sánh cửa sổ steady 5–15, 20–30, 40–50 phút; báo slope MiB/phút, thay đổi retained items và hiệu năng. Heap dao động theo GC; không gọi điểm thấp của một cửa sổ là “heap sau full GC” nếu chưa quan sát GC.
- RSS tăng một mình không đủ kết luận memory leak. Nếu cần bằng chứng quy thuộc object, thực hiện lần chẩn đoán riêng với heap snapshot/GC observation; không trộn run có snapshot gây pause vào benchmark chính.
- Một giờ không thấy suy giảm không chứng minh hệ thống không có rủi ro dài hạn. Tách kết luận “xác nhận giữ dữ liệu” khỏi “đã chứng minh gây suy giảm/OOM”.

## 8. SLO, tiêu chí hoàn thành và cách đọc kết quả

**Throughput (Thông lượng):** Số lượng request hoặc giao dịch hệ thống xử lý được trong một đơn vị thời gian. Với HTTP request, thường tính bằng **RPS (Requests Per Second)**; với giao dịch, cần ghi rõ giao dịch được định nghĩa là gì.

Trong kế hoạch này, báo cáo riêng:

- **RPS tổng / theo API:** số request ghi nhận trong phase chia cho thời lượng phase tính bằng giây; RPS tổng gồm login, RPS nghiệp vụ không gồm login. Số request gồm cả thành công và lỗi nên không được diễn giải toàn bộ là xử lý thành công.
- **RPS thành công:** số request đạt cả HTTP status và kiểm tra nội dung nghiệp vụ chia cho thời lượng phase. Ví dụ 12.000 request thành công trong hold 120s tương ứng 100 RPS thành công.
- **Thao tác nghiệp vụ thành công/giây:** số thao tác Search/Detail/Cart/Checkout đạt checks chia cho thời gian quan sát; không tính login và không coi iteration chỉ hoàn tất sleep sau lỗi là thao tác thành công.
- **Checkout thành công/giây:** số checkout trả kết quả hợp lệ chia cho thời gian quan sát; chỉ phản ánh API checkout trả kết quả hợp lệ; không chứng minh một chuỗi mua hàng hoàn chỉnh.

RPS theo phase giữ quy ước gắn request lúc bắt đầu ở mục 7; thông lượng thao tác/checkout hoàn tất dùng thời điểm kết thúc. Ghi rõ hai quy ước khi có thao tác vượt ranh giới phase. Đây là số đo phía client; timeout không chứng minh server chưa xử lý request.

### 8.1 Tiêu chí latency và correctness đề xuất

Kế thừa ngưỡng thử nghiệm v1, không coi là SLA production: p95 < 500ms, HTTP error rate < 1%, checks ≥ 99%; yêu cầu có mẫu cho từng endpoint bắt buộc ở cửa sổ đánh giá. Bổ sung login vào đánh giá mỗi plateau vì chính sách account đề xuất làm tăng tần suất login. Metric tổng phải ghi rõ có/không login và luôn có breakdown từng API.

- Stress đánh giá từng hold/recovery; spike đánh giá trước/đỉnh/recovery; soak đánh giá steady và từng cửa sổ 5 phút.
- Đề xuất tỷ lệ thao tác thất bại < 1%, gồm thao tác không gửi được do login lỗi; báo riêng iteration bị ngắt, không loại âm thầm. Không đặt SLO 500ms cho toàn iteration có think time.
- Giữ counter thao tác bị bỏ qua do login lỗi và nguyên nhân. Window không có request là thiếu bằng chứng, không PASS mặc định; percentile ít mẫu phải ghi số mẫu và hạn chế.
- Không abort chỉ vì vi phạm SLO ở stress/spike, nhằm quan sát recovery.

### 8.2 Xác định giới hạn và độ tin cậy

- Báo bậc fail đầu, mức cao nhất của vùng PASS liên tục, RPS nghiệp vụ và thao tác thành công/s tại từng bậc. Không lấy một bậc PASS sau vùng fail làm giới hạn ổn định.
- Mức cao nhất vẫn PASS và chưa thấy suy giảm: báo “chưa tìm được giới hạn trong dải đã thử”.
- Chạy chung máy: nếu k6 thiếu CPU/RAM, có swap hoặc I/O output cạnh tranh đáng kể, kết luận giới hạn môi trường chạy chung; chưa đủ bằng chứng đó là giới hạn riêng server.
- CPU cao cần ghép với latency/event-loop; RAM cao cần ghép với heap/cart/GC; DB error và callback delay giúp khoanh vùng. Không quy nguyên nhân chỉ từ một đường biểu đồ.
- Recovery: đề xuất ít nhất 2 cửa sổ 15s liên tiếp đạt SLO, có đủ mẫu và tải đã về mục tiêu; nếu thiếu mẫu thì chỉ báo quan sát, không khẳng định thời gian phục hồi chính xác.
- Đối chiếu gốc/tuned bằng các lần lặp cùng cấu hình; trình bày median và khoảng min–max của các run. Không lấy trung bình các p95 để tạo “p95 chung”.

### 8.3 Điều kiện hoàn thành triển khai v2

1. Preflight kiểm tra fixture, keyword, account và manifest; không còn ràng buộc đúng 50 account ở workload v2.
2. Mỗi iteration chọn một thao tác theo 40/20/22/18; không thêm chuỗi gọi API ngoài login cần thiết. Account/token đúng và login lỗi chặn request bảo vệ.
3. Stress hold 120s và phép tính phase/RPS nhất quán; spike có đo recovery; soak ngừng tạo iteration ở phút 50 nhưng collector chạy đến phút 60.
4. Có artifact k6, telemetry, manifest và phân tích liên kết theo run ID; report tách quan sát thực đo, giả thuyết và hạn chế.
5. Cả hai backend có đo lường tương đương và giữ nguyên nghiệp vụ, kể cả lỗi cart.

“Triển khai test hoàn thành” không đồng nghĩa “SUT PASS”: bài test phát hiện được lỗi vẫn là kết quả hợp lệ.

## 9. Quy trình chạy trên một máy và evidence

1. Ghi OS/kernel, CPU/core, RAM, Node/k6/SQLite version, giới hạn process, commit hoặc hash source, trạng thái thay đổi local. Chạy một backend tại một thời điểm, cùng cổng/BASE_URL.
2. Restart backend để reset DB/cart trước mỗi run; seed lại, kiểm tra dữ liệu và lưu manifest/hash. Lưu PRAGMA/index thực tế ở cả hai bản, không chỉ mô tả từ source.
3. Smoke/preflight trên fixture; vì có ghi cart/order, restart và reseed lần nữa trước run đo. Kiểm tra read-only cuối cùng không làm bẩn trạng thái.
4. Thu idle trước tải khoảng 30–60s, chạy profile, tiếp tục thu đến hết recovery/soak. Đồng bộ cùng đồng hồ máy; giữ timestamp UTC dù report hiển thị giờ Việt Nam.
5. Đổi thứ tự gốc/tuned qua các cặp lặp, cho máy về trạng thái idle tương đương. Không chạy hai bài tải đồng thời, không seed trong lúc đo.
6. Ghi exit code k6, exit collector/server, stderr, iteration bị ngắt. Exit 99 là threshold fail, không đồng nghĩa crash; collector hỏng làm thiếu bằng chứng tài nguyên.

Đề xuất cấu trúc mỗi run trong `performance/k6/output/v2/<type>-<backend>-<run-id>/`:

```text
manifest.json           # profile, dataset/source hashes, versions, seed ngẫu nhiên
summary.json            # kết quả k6
metrics.json            # raw k6 metrics
k6.log
server.log
server-telemetry.jsonl
host-process.csv
account-audit.jsonl     # chỉ khi bật audit coverage; không chứa bí mật
phase-timeline.json
analysis.json
report.md
```

Ghi raw metrics/audit theo luồng, không giữ toàn bộ trong RAM collector. Pilot đo chi phí ghi đĩa vì chính output có thể gây nhiễu. Nếu đổi output mode, áp dụng đồng nhất cả cặp. Seed bộ sinh số ngẫu nhiên giúp tái lập phân bố dự kiến, nhưng không bảo đảm hai run gửi cùng request tại cùng thời điểm.

Điều kiện dừng bảo vệ máy đề xuất: RAM available < 5% kéo dài 30s, disk trống < 1 GiB, server chết hoặc collector thiết yếu ngừng. Lưu lý do và đánh dấu run bị dừng; các ngưỡng này là bảo vệ thực thi, không phải SLO. Đóng băng ngưỡng sau kiểm tra cấu hình máy.

## 10. Tệp cần xem/chỉnh sửa/tạo mới

Đường dẫn dưới đây tính từ repository `eshop-sut/`. Tệp mới là tên dự kiến, chưa tồn tại và chưa được tạo bởi kế hoạch này.

### Xem và giữ làm đối chiếu

- `backend/database.js`, `tuned-backend/database.js`: vòng đời reset/seed, schema, WAL/index; không thay thuật toán hay tuning.
- `backend/package.json`, `tuned-backend/package.json`: runtime/dependencies để chọn cơ chế telemetry phù hợp.
- `performance/k6/smoke.js`, `performance/k6/baseline.js`, `performance/k6/run-smoke.sh`, `performance/k6/run-baseline.sh`: giữ bài cũ làm regression; baseline cũ không phải baseline v2.
- `performance/k6/reports/03-stress-test-report.md`, `04-spike-test-report.md`, `07-tuned-spike-test-report.md`, `08-tuned-stress-test-report.md`: tham chiếu lịch sử, không ghi đè số đo v1.

### Chỉnh sửa trong bước triển khai sau

| Tệp | Trách nhiệm thay đổi |
|---|---|
| `performance/k6/stress.js`, `performance/k6/spike.js` | Giữ mix random 40/20/22/18 qua helper chung; bỏ fixture 50 user, áp chính sách account/login đã chốt trước triển khai; thêm keyword và dữ liệu product độc lập; đổi hold stress. |
| `performance/k6/run-stress.sh`, `performance/k6/run-spike.sh` | Orchestrate collector, PID, manifest và artifact, cleanup bằng trap, giữ đúng exit code. |
| `performance/k6/data/seed.js` | Nhận fixture quy mô mới, validate/hash và xuất manifest; giữ khả năng chọn DB path, không log credential. |
| `backend/server.js`, `tuned-backend/server.js` | Hook telemetry/counter tại điểm giỏ thay đổi và timing lỗi DB khi cần; giữ nguyên response/nghiệp vụ và tuning. |
| `performance/k6/README.md` | Hướng dẫn v2, tham số, điều kiện một máy, quy trình reset/seed, cách đọc artifact; tách rõ lịch sử v1. |
| `performance/k6/reports/05-soak-test-report.md` | Cập nhật template theo bài một giờ, cửa sổ 10 phút và evidence retention; không điền số liệu chưa đo. |

### Tạo mới dự kiến

| Tệp | Trách nhiệm |
|---|---|
| `performance/k6/lib/data.js` | Nạp SharedArray, validate fixture và weighted keyword selection. |
| `performance/k6/lib/workload.js` | Chọn một thao tác, account/login, payload từ fixture và xử lý lỗi độc lập. |
| `performance/k6/lib/profiles.js` | Profile và phase từ một nguồn cấu hình. |
| `performance/k6/lib/metrics.js` | Checks/counter/tag ổn định, phân biệt thao tác được chọn, request được gửi và login. |
| `performance/k6/data/black-friday.json` | Manifest sản phẩm, keyword/trọng số và dataset ID từ seed. |
| `performance/k6/data/black-friday-accounts.csv` | Tập account v2 riêng, tránh phá fixture đúng 50 user của baseline cũ. |
| `performance/k6/soak-test.js`, `performance/k6/run-soak.sh` | Profile soak và collector sống đến hết quan sát idle. |
| `performance/k6/telemetry/node.cjs` | Module đo Node dùng chung hai backend; không phụ thuộc package mới nếu runtime hỗ trợ. |
| `performance/k6/telemetry/collect.py` | Thu host/process, theo PID và timestamp. |
| `performance/k6/analysis/analyze.py` | Đọc theo luồng, ghép phase, tính RPS/window, unique coverage, xu hướng tài nguyên và xuất báo cáo. |
| `performance/k6/reports/v2/` | Báo cáo từng run và đối chiếu cặp, tách evidence cũ. |

### Có thể ảnh hưởng / người thực hiện bổ sung

- `backend/test-data/test_products.csv`, `tuned-backend/test-data/test_products.csv`: mở rộng đồng bộ; giữ ID fixture cũ hoặc cập nhật kiểm tra phụ thuộc có chủ đích.
- `performance/k6/data/test_accounts.csv`: giữ 50 account cho baseline cũ; v2 dùng file riêng. Seed tool cần hỗ trợ cả hai, không silently đổi mặc định làm hỏng workflow cũ.
- `submission/Bao_cao_seminar_Performance_Testing.md` và `submission/evidence/k6/README.md`: chỉ cập nhật sau khi có số đo, không thuộc bước viết kế hoạch này.

## 11. Các bước triển khai và xác minh

| Bước | Công việc | Điều kiện chuyển bước |
|---|---|---|
| 1. Chốt fixture | Tạo dataset/manifest theo hợp đồng, xác định keyword/trọng số và cấu hình máy. | Hai DB cùng dữ liệu logic; keyword đúng expected IDs; account duy nhất. |
| 2. Xây workload | Helper random và run nhỏ cho từng API, dùng fixture sản phẩm. | Mix đúng; không tự thêm Search/Detail trước Cart; token đúng account; login lỗi chặn thao tác bảo vệ. |
| 3. Gắn telemetry | Instrument hai backend, collector theo PID, counter cart và manifest. | Mẫu có đơn vị/timestamp đúng; checkout không làm giảm counter; overhead được ghi. |
| 4. Đổi profile/runner | Stress 120s, spike và soak; cleanup, grace, idle observation, artifact. | Tổng thời gian và phase đúng; collector còn sống sau k6 ở soak; exit code không bị mất qua pipe. |
| 5. Pilot | 1–5 VU kiểm tra chức năng, run ngắn kiểm tra tài nguyên; thử workload có/không telemetry ở cùng mức nhẹ. | Không có lỗi fixture; đánh giá được overhead, output disk và mức tải k6 phát được. |
| 6. Thu chính thức | Stress/spike theo cặp lặp; chọn tải soak chung rồi chạy một giờ mỗi backend. | Reset/seed mỗi run, manifest đầy đủ, đánh dấu mọi lần bị ngắt/thiếu telemetry. |
| 7. Phân tích | Latency/throughput theo phase, chart tài nguyên và retained items, đối chiếu gốc/tuned. | Mọi nhận định trỏ về run/window; phân biệt kết luận chắc chắn và giả thuyết. |

Kiểm tra có giá trị trước khi chạy tải lớn:

- Fixture sai schema, trùng email, keyword không khớp, weight không tổng 100% phải bị phát hiện trước run.
- Run nhỏ từng API; xác minh mix lựa chọn gần 40/20/22/18 với đủ iteration, tách login khỏi mẫu số; kiểm tra account/token và payload fixture. Không kỳ vọng tỷ lệ chính xác ở run ít mẫu.
- Xác minh nhãn phase ở sát ranh giới, kể cả login vượt sang phase tiếp theo; dùng count/duration đúng cho 120s, 60s và 30s.
- Soak rút ngắn để kiểm tra phút ngừng tạo iteration được thay bằng mốc thử, vẫn thu idle; đây là kiểm tra cơ chế, không phải evidence độ bền một giờ.
- Dừng k6/server có kiểm soát trong pilot để kiểm tra runner lưu status và dọn collector do nó tạo; không kill tiến trình ngoài run.
- Kiểm tra sample thiếu, counter reset do server restart, clock/timestamp lỗi và run không có mẫu; analyzer phải báo thiếu dữ liệu thay vì xuất PASS.

Chưa chạy các kiểm tra trên khi soạn tài liệu. Lệnh cụ thể sẽ được bổ sung sau khi xác minh phiên bản runtime và triển khai các tệp dự kiến.

## 12. Những điểm cần ghi rõ trước khi thu số đo chính thức

- Xác nhận dataset thực tế và danh sách keyword từ người bổ sung seed.
- Mix thao tác 40/20/22/18 đã chốt. Cần đóng băng chính sách account/login: đề xuất account theo iteration và login cho Cart/Checkout (40% iteration kỳ vọng); không mặc nhiên coi lựa chọn này đã được xác nhận cùng mix.
- Ghi cấu hình phần cứng, số lần lặp có thể thực hiện, dải VU sau pilot và `SOAK_VUS` chung.
- Giữ nguyên các giả định trong cả cặp gốc/tuned. Mọi thay đổi workload hoặc telemetry sau đó tạo cấu hình/run mới.
- Chỉ đưa số liệu vào báo cáo sau khi chạy; không biến mức VU dự kiến, SLO đề xuất hoặc counter retention thành kết luận performance đã đo.
