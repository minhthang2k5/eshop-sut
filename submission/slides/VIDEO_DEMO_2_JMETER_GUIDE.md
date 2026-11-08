# Kịch bản quay Video demo 2 — JMeter trên EShop

Người trình bày: Võ Hữu Thắng. Thời lượng mục tiêu: 7–9 phút.

Đây là kịch bản **đi từng bước để quay**. Mỗi bước ghi rõ: mở gì/bấm gì, cần nói gì, lệnh nào hiện trên màn hình và kết quả cần thấy. GUI chỉ dùng để giải thích cấu trúc; mọi lần chạy tải đều bằng CLI.

## Mục tiêu cần chứng minh

1. Baseline có 50 users, ramp-up 10 giây và duration 300 giây.
2. Mỗi user login một lần bằng CSV; Regex Extractor lấy JWT và checkout gửi `Authorization: Bearer ${token}`.
3. Workload gồm Search/Detail/Checkout theo tỷ lệ 55%/25%/20%, có think-time và assertions.
4. Smoke CLI chạy được. Đọc trực tiếp HTML baseline: Total có 5.190 samples; ba action có 5.140 samples, đều không lỗi và có p95 từng action dưới 500 ms.

Không để lộ password CSV hoặc JWT thật.

---

## Chuẩn bị trước khi quay (không cần ghi hình)

Mở **PowerShell 1** tại backend:

```powershell
cd <duong-dan>\eshop-sut-main\backend
npm.cmd ci
npm.cmd run reset-db
npm.cmd start
```

Chờ backend hiện URL `http://localhost:3000`; giữ cửa sổ này mở.

Mở **PowerShell 2** tại repo root. JMeter 5.6.3 của test plan này cần chạy với **Java 17**, không chạy với Java 25. Nếu `java -version` hiện Java 25 hoặc smoke từng báo `Unsupported class file major version 69`, cài JDK 17 trước (một lần):

```powershell
winget install --id EclipseAdoptium.Temurin.17.JDK -e
```

Mở PowerShell mới. Đặt biến Java/JMeter theo đường dẫn thực tế trên máy:

```powershell
$env:JAVA_HOME = 'C:\path\to\jdk-17'
$jmeterBin = 'C:\Program Files\apache-jmeter-5.6.3\bin'
$env:PATH = "$env:JAVA_HOME/bin;$jmeterBin;$env:PATH"
cd performance/jmeter

java -version
jmeter.bat --version
```

Ví dụ, JDK Temurin 17 thường nằm trong `C:\Program Files\Eclipse Adoptium\jdk-17...`; dùng `Get-ChildItem 'C:\Program Files\Eclipse Adoptium'` để lấy tên thư mục chính xác. Chỉ tiếp tục khi `java -version` hiển thị `17`. Mở sẵn JMeter, VS Code và PowerShell 2.

---

## Kịch bản quay từng bước

### Bước 1 — Mở đầu (0:00–0:20)

**Hiển thị:** slide 53 hoặc tiêu đề video.

**Nói:**

> “Đây là demo JMeter cho API EShop. Tôi sẽ kiểm tra cấu trúc test plan, cơ chế lấy JWT cho checkout, chạy smoke bằng dòng lệnh, rồi đọc kết quả baseline đã đo. GUI chỉ dùng để xem cấu hình; tải sẽ chạy bằng CLI.”

**Cần thấy:** tiêu đề *Video demo 2: JMeter và đối chiếu*.

### Bước 2 — Xác nhận Java và JMeter (0:20–0:45)

**Thao tác:** tại PowerShell 2, gõ:

```powershell
java -version
jmeter.bat --version
```

**Nói:**

> “JMeter chạy trên Java. Môi trường này dùng Java 17 và Apache JMeter 5.6.3. Test plan chỉ dùng thành phần có sẵn, không cần plugin ngoài.”

**Cần thấy:** Java 17 và JMeter 5.6.3. Cảnh báo thông thường của Java/JMeter không sao nếu lệnh vẫn trả về phiên bản.

### Bước 3 — Xác nhận backend đã sẵn sàng (0:45–1:00)

**Thao tác:** chuyển PowerShell 1, chỉ vào dòng backend chạy tại `http://localhost:3000`.

**Nói:**

> “Backend đã được reset database để seed dữ liệu kiểm thử và đang chạy ở localhost cổng 3000. Tôi giữ server chạy xuyên suốt lúc JMeter gửi request.”

**Cần thấy:** backend không báo lỗi và vẫn đang chạy.

### Bước 4 — Mở test plan, xem baseline (1:00–1:35)

**Thao tác:** ở PowerShell 2, chạy:

```powershell
jmeter.bat -t eshop_workload.jmx
```

Trong GUI, bấm `EShop baseline - 50 users / 10s / 300s` ở cây bên trái.

**Nói:**

> “Đây là Thread Group của baseline: 50 users, ramp-up 10 giây và duration 300 giây. 300 giây là tổng thời gian chạy, đã bao gồm ramp-up.”

**Cần thấy:** Number of Threads `50`, Ramp-up `10`, Duration `300`.

### Bước 5 — Chỉ dữ liệu test theo user (1:35–2:00)

**Thao tác:** bấm `Load CSV account once and product catalog` trong `Login once per user`. Nếu cần, bấm node gốc để chỉ `accounts_csv` và `products_csv`.

**Nói:**

> “Mỗi thread nhận một account từ CSV và giữ account đó trong cả phiên. Catalog sản phẩm cung cấp keyword, product ID và giá phù hợp cho Search, Detail và Checkout. Tôi không mở CSV vì nó có password kiểm thử.”

**Cần thấy:** node nạp CSV/catalog nằm trong `Login once per user`.

### Bước 6 — Login và nơi token được tạo (2:00–2:35)

**Thao tác:**

1. Bấm dấu `>` bên trái node `login` để bung node con.
2. Bấm `login`, mở tab `Body Data`.
3. Bấm node con `Extract token`.

**Nói khi chọn `login`:**

> “Login gửi POST đến `/api/login`. Body Data chỉ có `${login_body}`. Token chưa tồn tại trước request, nên không có `${token}` trong Basic, Advanced hay Body Data của login.”

**Nói khi chọn `Extract token`:**

> “Sau response login, Regex Extractor này lấy trường token từ JSON và lưu thành biến `${token}` cho đúng thread. JMeter dùng `${token}`, không dùng `{{token}}`.”

**Cần thấy:** `Extract token` **thụt vào dưới** `login`; cấu hình có variable name `token` và regex đọc trường `"token"`.

### Bước 7 — Checkout dùng token (2:35–3:05)

**Thao tác:** bung `checkout 20%` → `checkout`; bấm **HTTP Header Manager thụt vào dưới checkout**.

**Nói:**

> “Header Manager đầu Thread Group chỉ có Content-Type và Accept. Header Manager thụt vào dưới checkout mới thêm xác thực: `Authorization: Bearer ${token}`. Đây là correlation: token tạo sau login được dùng cho checkout.”

**Cần thấy:** dòng `Authorization` có giá trị `Bearer ${token}`. Không mở response chứa JWT thật.

### Bước 8 — Assertions, workload mix và think-time (3:05–3:40)

**Thao tác:**

1. Bấm `HTTP status must be 200` và một `Validate response content`.
2. Bấm lần lượt `search 55%`, `detail 25%`, `checkout 20%`.
3. Chỉ timer: Search 1–3s, Detail 2–5s, Checkout 3–6s.

**Nói:**

> “Test không chỉ kiểm tra HTTP 200. Assertions còn kiểm tra nội dung như token sau login, detail đúng ID và `orderId` sau checkout. Ba Throughput Controller đặt mục tiêu Search 55%, Detail 25%, Checkout 20%. Timer mô phỏng thời gian người dùng suy nghĩ, không phải thời gian phản hồi request.”

**Cần thấy:** ba controller và timer đúng khoảng. Có thể nói: “Tỷ lệ thực tế sẽ đọc ở baseline vì smoke có ít mẫu.”

### Bước 9 — Listener GUI không dùng để load test (3:40–3:55)

**Thao tác:** bấm `View Results Tree - smoke only` và `Summary Report - smoke only`, rồi đóng JMeter GUI.

**Nói:**

> “Hai listener này đang disabled, chỉ để debug. Tôi không chạy tải bằng GUI vì listener có thể tạo overhead; từ đây tôi chạy non-GUI bằng CLI.”

**Cần thấy:** hai listener bị mờ/disabled.

### Bước 10 — Chạy smoke CLI bằng lệnh gốc (3:55–5:20)

**Thao tác:** tại PowerShell 2 (`performance/jmeter`), chạy **từng khối theo thứ tự**. Chỉ sang khối kế tiếp khi PowerShell hiện lại prompt `PS ...>`.

**10.1 — Tạo thư mục output mới:**

```powershell
$smokeDir = 'local-runs/smoke-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
New-Item -ItemType Directory -Path $smokeDir | Out-Null
```

**10.2 — Chạy đúng lệnh smoke gốc:**

```powershell
jmeter.bat -n -t eshop_workload.jmx -q report.properties `
  -Jusers=1 -Jrampup=1 -Jduration=60 `
  -l "$smokeDir/smoke.jtl" -j "$smokeDir/jmeter.log"
```

**10.3 — Chỉ khi lệnh 10.2 không in lỗi Groovy/Java, tổng hợp kết quả:**

```powershell
node summarize.cjs "$smokeDir/smoke.jtl"
```

**Nói trước khi chạy 10.2:**

> “Đây là lệnh smoke gốc: một user, ramp-up một giây, chạy 60 giây. Tôi dùng nó để xác nhận script, dữ liệu và correlation JWT hoạt động. Đây không phải baseline và không sinh HTML report mới.”

**Nói khi lệnh kết thúc:**

> “`-n` chạy non-GUI; `-t` là test plan; `-J` chỉ ghi đè tải tạm thời. `-l` lưu các sample vào JTL và `-j` lưu log để chẩn đoán khi cần.”

**Cần thấy:** `smoke.jtl` và `jmeter.log` được tạo; `summarize.cjs` in JSON có `byLabel`, `actions` và `slo`.

**Dừng ngay, không chạy 10.3, nếu** lệnh 10.2 có `Unsupported class file major version 69`, `summary = 0`, hoặc log báo Java/Groovy. Đây là lỗi Java 25; mở PowerShell mới và bảo đảm `java -version` là Java 17 trước khi chạy lại từ 10.1.

### Bước 11 — Đọc kết quả smoke (5:20–5:55)

**Thao tác:** đọc JSON vừa in ra ở PowerShell.

**Nói:**

> “Smoke phải có login và các action được chọn trong thời gian chạy, không có errors. Nếu checkout bị 401, tôi kiểm tra theo thứ tự account/seed, response login, Extract token, biến `${token}`, rồi Authorization header.”

**Cần thấy:** `errors` bằng 0; có `login` và các label action trong `byLabel`. Nếu một action không xuất hiện trong 60 giây do lựa chọn ngẫu nhiên, có thể chạy lại smoke; không kết luận p95, throughput hay tỷ lệ workload chính thức từ smoke.

### Bước 12 — Mở và đọc HTML baseline thật (5:55–7:50)

**Thao tác:** ở PowerShell 2, chạy:

```powershell
Start-Process "$PWD/results/jmeter-report/index.html"
```

Trong trình duyệt, chọn **Dashboard** ở thanh bên trái nếu cần, rồi cuộn tới bảng **Statistics** như ảnh đã mở. Phóng to để thấy rõ cả dòng `Total` và các dòng `checkout`, `detail`, `login`, `search`. Giữ HTML trên màn hình trong toàn bộ bước 12–13.

Đây là **baseline đã lưu**, không phải kết quả smoke vừa chạy. Số trong bảng dưới đây ứng với HTML `results/jmeter-report/index.html` hiện có; không đọc các số này thay cho số liệu của một run mới.

**12.1 — Chỉ dòng Total và đọc số mẫu:**

> “Đây là HTML report của baseline 50 users, ramp-up 10 giây và tổng duration 300 giây đã lưu. Dòng Total có 5.190 samples, gồm 50 Login và 5.140 request Search, Detail, Checkout. FAIL bằng 0 và Error bằng 0%, nghĩa là không có sample thất bại trong lần chạy này.”

**Cần thấy ở Total:** `#Samples = 5190`, `FAIL = 0`, `Error % = 0.00%`.

**12.2 — Di chuột lần lượt qua các cột thời gian của Total:**

> “Các cột Response Times đều tính bằng mili giây. Average là trung bình 4,96 ms; Min là 0 và Max là 157 ms. Median và 50th percentile cùng bằng 2 ms. Cột 95th percentile là p95, bằng 16 ms; cột 99th percentile là p99, bằng 23 ms. Các số ở dòng Total tính cả Login.”

**Cần thấy ở Total:** `Average = 4.96`, `Min = 0`, `Max = 157`, `Median = 2.00`, `50th pct = 2.00`, `95th pct = 16.00`, `99th pct = 23.00`.

Nếu cần giải thích p95: “Đây là mốc phân vị 95 của thời gian phản hồi, giúp nhìn nhóm request chậm thay vì chỉ đọc trung bình.” `Min = 0 ms` là độ phân giải số đo, không có nghĩa server xử lý không mất thời gian.

**12.3 — Chỉ Throughput và Network của Total:**

> “Transactions mỗi giây ở đây là throughput sample, khoảng 17,40 request/giây, gồm cả Login. Network cho biết tốc độ nhận 7,25 và gửi 4,32 KB/giây. Các cột này không phải số user hay thời gian phản hồi.”

**Cần thấy ở Total:** `Transactions/s = 17.40`, `Received = 7.25`, `Sent = 4.32`. Không cộng throughput từng dòng vì mỗi label có khoảng quan sát riêng.

**12.4 — Chỉ từng dòng API và đối chiếu p95/error:**

| Dòng trên HTML | #Samples | Average (ms) | 95th pct (ms) | Error % |
| --- | ---: | ---: | ---: | ---: |
| checkout | 1017 | 14.63 | 21.00 | 0.00% |
| detail | 1283 | 2.39 | 5.80 | 0.00% |
| login | 50 | 32.54 | 157.00 | 0.00% |
| search | 2840 | 2.18 | 5.00 | 0.00% |

> “Tôi đọc riêng ba action nghiệp vụ: Checkout có 1.017 samples, p95 21 ms; Detail có 1.283 samples, p95 5,80 ms; Search có 2.840 samples, p95 5 ms. Cả ba có Error 0%. Login có 50 samples, tương ứng một lần login mỗi user, và được báo riêng.”

> “Cộng ba action được 5.140 samples. Chia số mẫu từng action cho 5.140 cho tỷ lệ khoảng 55,25% Search, 24,96% Detail và 19,79% Checkout, gần mục tiêu 55/25/20.”

**Lưu ý khi quay:** HTML này không có dòng gộp riêng ba action. Không gọi p95 16 ms hoặc throughput 17,40 của `Total` là số chỉ của actions; không lấy trung bình các p95 từng dòng để tính p95 gộp. Bảng Statistics cũng không có cột `Std. Dev.` như Summary Report trong GUI.

### Bước 13 — Kết luận từ HTML (7:50–8:15)

**Hiển thị:** giữ bảng **Statistics**, chỉ các cột `95th pct` và `Error %` của ba action.

**Nói nguyên văn:**

> “Đối chiếu ngưỡng p95 dưới 500 ms và lỗi dưới 1%: Search, Detail và Checkout đều đạt ở từng action, với p95 lần lượt 5, 5,80 và 21 ms; Error đều bằng 0%. Dòng Total, gồm cả Login, cũng đạt hai ngưỡng với p95 16 ms và lỗi 0%. Kết quả baseline này đạt trong workload và môi trường đã đo; chưa cho phép suy ra mọi mức tải hoặc mọi máy đều đạt.”

**Cần thấy:** p95 từng action `5.00`, `5.80`, `21.00` và `Error % = 0.00%`; dòng `Total` có p95 `16.00` và Error `0.00%`.

---

## Xử lý nhanh nếu gặp lỗi lúc quay

| Hiện tượng | Làm gì |
| --- | --- |
| `Connection refused` | Kiểm tra PowerShell 1: backend còn chạy ở `localhost:3000`. |
| `401` hoặc token rỗng ở checkout | Reset DB; kiểm tra lại Bước 6 rồi Bước 7. Không tắt assertion để làm pass giả. |
| Không tìm thấy CSV | Bảo đảm chạy từ `performance/jmeter`; nếu cần truyền đường dẫn tuyệt đối bằng `-Jaccounts_csv=...` và `-Jproducts_csv=...`. |
| Thư mục output đã tồn tại | Chạy lại khối 10.1 để `$smokeDir` nhận timestamp mới. |
| Smoke thiếu một action | Đổi `-Jduration=60` thành `-Jduration=90`, chạy lại Bước 10. |

## Checklist trước khi xuất video

- [ ] Backend đang chạy và seed hoàn tất.
- [ ] Đã thấy Java 17 và JMeter 5.6.3.
- [ ] Đã chỉ Thread Group, CSV/catalog, Regex Extractor, `Bearer ${token}`, assertions, controller và timer.
- [ ] Smoke CLI tạo JTL/log mới, không có sample lỗi.
- [ ] Không lộ password hoặc JWT thật.
- [ ] Đã đọc HTML baseline: Total 5.190 samples (gồm 50 Login), p95 16 ms, p99 23 ms, throughput 17,40 request/s.
- [ ] Đã chỉ p95/error từng action; không nhầm Total với nhóm 5.140 actions.
- [ ] Đã nói giới hạn của kết luận PASS.

Tài liệu liên quan: [hướng dẫn CLI chi tiết](../../performance/jmeter/README.md), [test plan](../../performance/jmeter/eshop_workload.jmx), [baseline summary](../../performance/jmeter/results/baseline-summary.json) và [slide deck](Performance_Testing_EShop_v4.pptx).
