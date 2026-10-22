# Week 2/B — JMeter D3 (CLI)

Tài liệu này chỉ hướng dẫn chạy JMeter bằng **CLI**.

## Kết quả cần tạo

| File | Mục đích |
| --- | --- |
| `eshop_workload.jmx` | Kịch bản JMeter: login, search, detail, checkout |
| `report.properties` | Cấu hình JTL và HTML report |
| `summarize.cjs` | Tính counts, p50/p95/p99, throughput và error rate |
| `local-runs/<run>/` | Kết quả từng lần chạy lại: JTL, log và HTML report |
| `comparison_d2_vs_d3.md` | Bảng đối chiếu k6 (D2) và JMeter (D3) |

Baseline chính thức dùng **50 users, ramp-up 10 giây, duration 300 giây (bao gồm ramp-up)**. Mỗi user login một lần. Ba action chính có workload mục tiêu **search 55%, detail 25%, checkout 20%**.

## Smoke test là gì?

Smoke test là một lần chạy ngắn với ít user để trả lời câu hỏi: **test plan có chạy đúng từ đầu đến cuối không?** Nó kiểm tra đường đi của kịch bản, không dùng để đo sức chịu tải hay kết luận tỷ lệ 55/25/20.

Trong test plan này, smoke test giúp phát hiện sớm các lỗi sau:

- backend chưa chạy hoặc sai host/port;
- đường dẫn account/product CSV sai;
- account/password seed không đăng nhập được;
- Regular Expression Extractor không lấy được `token`;
- checkout không gửi được `Authorization: Bearer ${token}`;
- product ID/keyword không hợp lệ;
- assertion hoặc response của search/detail/checkout không đúng.

Smoke **1 user** kiểm tra luồng cơ bản và correlation token. Smoke **5 users** kiểm tra thêm việc nhiều thread dùng account riêng, mỗi thread login một lần và dữ liệu CSV được phân phối đúng. Vì smoke có ít mẫu và thời gian ngắn, kết quả của nó chỉ dùng để quyết định “có thể chạy baseline hay chưa”. Baseline 50 users/300 giây mới dùng để tính p95, error rate và workload share.

Sau khi chạy smoke, lệnh `node summarize.cjs <file.jtl>` cho biết:

- `count`: có bao nhiêu request từng label;
- `errors`/`errorPct`: có request hoặc assertion nào thất bại không;
- `byLabel.login.count`: số lần login;
- `actions`: tổng search/detail/checkout, không tính login;
- `slo`: smoke có vượt p95/error threshold hay không. Đây chỉ là tín hiệu kiểm tra nhanh, không phải số liệu baseline.

## 1. Chuẩn bị công cụ

Cần có Java 17, Apache JMeter 5.6.3 và Node.js. Kiểm tra trong PowerShell:

```powershell
java -version
jmeter.bat --version
node --version
```

Trên workspace này, JDK và JMeter portable nằm ở `../.tools/` so với repo `eshop-sut-main`. Từ repo root chạy:

```powershell
$env:JAVA_HOME = (Resolve-Path '../.tools/java/jdk-17.0.20.1+1').Path
$jmeterBin = (Resolve-Path '../.tools/apache-jmeter-5.6.3/bin').Path
$env:PATH = "$env:JAVA_HOME/bin;$jmeterBin;$env:PATH"
cd performance/jmeter
```

Nếu máy khác dùng thư mục khác, sửa hai đường dẫn trên. Không cần cài plugin JMeter.

### Linux/macOS (Bash)

Cài Java 17, Apache JMeter 5.6.3 và Node.js bằng package manager của hệ điều hành hoặc giải nén bản portable. Từ repo root `eshop-sut-main`, đặt biến môi trường:

```bash
export JAVA_HOME="/path/to/jdk-17"
export JMETER_HOME="/path/to/apache-jmeter-5.6.3"
export PATH="$JAVA_HOME/bin:$JMETER_HOME/bin:$PATH"
cd performance/jmeter

java -version
jmeter --version
node --version
```

Thay `/path/to/...` bằng đường dẫn thật trên máy Linux/macOS. Script CLI là `jmeter` (không có đuôi `.bat`).

## 2. Chuẩn bị backend

Mở một PowerShell riêng tại repo root `eshop-sut-main`:

```powershell
cd backend
npm.cmd ci
npm.cmd run reset-db
npm.cmd start
```

Trên Windows, `npm.cmd` là wrapper chính thức của npm dành cho Command Prompt/PowerShell. Gọi rõ `npm.cmd` giúp tránh trường hợp PowerShell ưu tiên `npm.ps1` rồi bị chặn bởi Execution Policy. Nếu máy bạn chạy `npm` bình thường thì `npm ci`, `npm run reset-db` và `npm start` cũng tương đương; chỉ cần dùng nhất quán một cách.

Trên Linux/macOS, mở terminal backend tại repo root `eshop-sut-main` và dùng lệnh npm thông thường:

```bash
cd backend
npm ci
npm run reset-db
npm start
```

Giữ terminal này chạy. Chờ log báo backend ở `http://localhost:3000` và dữ liệu seed hoàn tất. Dataset dùng cho Week 2 gồm:

- 50 account trong `backend/test-data/test_accounts.csv`;
- 5 product trong `backend/test-data/test_products.csv`.

Trước mỗi run mới, chờ JMeter kết thúc rồi reset/start backend lại để các lần đo bắt đầu với DB sạch:

```powershell
Ctrl+C
npm.cmd run reset-db
npm.cmd start
```

Không reset DB khi JMeter còn đang chạy.

Trước mỗi run mới trên Linux/macOS: nhấn `Ctrl+C` ở terminal backend, rồi chạy lại `npm run reset-db` và `npm start`.

## 3. Tham số của test plan

Không sửa `eshop_workload.jmx` để đổi tải. Truyền thuộc tính bằng `-J`:

| Thuộc tính | Mặc định |
| --- | --- |
| `users` | `50` |
| `rampup` | `10` giây |
| `duration` | `300` giây, bao gồm ramp-up |
| `host` | `localhost` |
| `port` | `3000` |
| `protocol` | `http` |
| `accounts_csv` | `../../backend/test-data/test_accounts.csv` |
| `products_csv` | `../../backend/test-data/test_products.csv` |

`eshop_workload.jmx` tự thực hiện các bước sau:

1. Đọc account/product từ hai CSV.
2. Login một lần cho mỗi thread và lấy trường `token` bằng Regular Expression Extractor.
3. Gửi `Authorization: Bearer ${token}` khi checkout.
4. Chạy search/detail/checkout qua ba Throughput Controller theo tỷ lệ 55/25/20.
5. Thêm think-time tương ứng search 1–3 giây, detail 2–5 giây, checkout 3–6 giây.
6. Kiểm tra status/content response bằng assertions.

## 4. Chạy smoke CLI (khuyến nghị)

Smoke chỉ kiểm tra kịch bản hoạt động, không dùng để đánh giá tỷ lệ workload. Từ `performance/jmeter`:

```powershell
$smokeDir = 'local-runs/smoke-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
New-Item -ItemType Directory -Path $smokeDir | Out-Null

jmeter.bat -n -t eshop_workload.jmx -q report.properties `
  -Jusers=1 -Jrampup=1 -Jduration=60 `
  -l "$smokeDir/smoke.jtl" -j "$smokeDir/jmeter.log"

if ($LASTEXITCODE -ne 0) { throw "JMeter lỗi; xem $smokeDir/jmeter.log" }
node summarize.cjs "$smokeDir/smoke.jtl"
```

Linux/macOS:

```bash
smokeDir="local-runs/smoke-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$smokeDir"

jmeter -n -t eshop_workload.jmx -q report.properties \
  -Jusers=1 -Jrampup=1 -Jduration=60 \
  -l "$smokeDir/smoke.jtl" -j "$smokeDir/jmeter.log"

status=$?
if [ "$status" -ne 0 ]; then
  echo "JMeter lỗi; xem $smokeDir/jmeter.log" >&2
  exit "$status"
fi
node summarize.cjs "$smokeDir/smoke.jtl"
```

Kết quả mong đợi: một login, có thể quan sát được các label search/detail/checkout, `errors = 0`, checkout trả về `orderId`. Nếu một action chưa xuất hiện trong smoke ngắn, hãy chạy lại với duration 60 giây; không dùng việc thiếu một mẫu smoke để kết luận workload baseline.

Có thể kiểm tra account riêng theo thread bằng smoke 5 users. Reset backend trước khi chạy:

```powershell
$checkDir = 'local-runs/check5-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
New-Item -ItemType Directory -Path $checkDir | Out-Null

jmeter.bat -n -t eshop_workload.jmx -q report.properties `
  -Jusers=5 -Jrampup=1 -Jduration=60 `
  -l "$checkDir/check5.jtl" -j "$checkDir/jmeter.log"

if ($LASTEXITCODE -ne 0) { throw "JMeter lỗi; xem $checkDir/jmeter.log" }
node summarize.cjs "$checkDir/check5.jtl"
```

Linux/macOS:

```bash
checkDir="local-runs/check5-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$checkDir"

jmeter -n -t eshop_workload.jmx -q report.properties \
  -Jusers=5 -Jrampup=1 -Jduration=60 \
  -l "$checkDir/check5.jtl" -j "$checkDir/jmeter.log"

status=$?
if [ "$status" -ne 0 ]; then
  echo "JMeter lỗi; xem $checkDir/jmeter.log" >&2
  exit "$status"
fi
node summarize.cjs "$checkDir/check5.jtl"
```

Kết quả mong đợi: 5 login trên 5 thread, mỗi thread login một lần, không có HTTP/assertion failure. Đây là kiểm tra dữ liệu/account và correlation; chưa phải phép đo hiệu năng chính thức.

## 5. Chạy baseline và sinh HTML report

Reset/start backend theo mục 2. Từ `performance/jmeter` chạy:

```powershell
$runDir = 'local-runs/baseline-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
New-Item -ItemType Directory -Path $runDir | Out-Null

jmeter.bat -n -t eshop_workload.jmx -q report.properties `
  -Jusers=50 -Jrampup=10 -Jduration=300 `
  -l "$runDir/baseline.jtl" `
  -j "$runDir/jmeter.log" `
  -e -o "$runDir/jmeter-report"

if ($LASTEXITCODE -ne 0) { throw "JMeter/report lỗi; xem $runDir/jmeter.log" }
node summarize.cjs "$runDir/baseline.jtl" | Tee-Object "$runDir/summary.json"
```

Linux/macOS:

```bash
runDir="local-runs/baseline-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$runDir"

jmeter -n -t eshop_workload.jmx -q report.properties \
  -Jusers=50 -Jrampup=10 -Jduration=300 \
  -l "$runDir/baseline.jtl" \
  -j "$runDir/jmeter.log" \
  -e -o "$runDir/jmeter-report"

status=$?
if [ "$status" -ne 0 ]; then
  echo "JMeter/report lỗi; xem $runDir/jmeter.log" >&2
  exit "$status"
fi
node summarize.cjs "$runDir/baseline.jtl" | tee "$runDir/summary.json"
```

Các option chính:

| Option | Công dụng |
| --- | --- |
| `-n` | Chạy CLI |
| `-t` | Đọc test plan `.jmx` |
| `-q` | Đọc `report.properties` |
| `-J` | Override users/ramp-up/duration, host hoặc CSV |
| `-l` | Ghi kết quả từng request vào JTL |
| `-j` | Ghi log JMeter |
| `-e -o` | Sinh HTML report vào thư mục chỉ định |

Không dùng lại thư mục report đã có dữ liệu. Mỗi lần chạy dùng thư mục timestamp mới như lệnh trên.

`local-runs/` chỉ là quy ước lưu kết quả chạy lại trên máy cá nhân, không phải thư mục bắt buộc của JMeter. Mỗi thư mục timestamp chứa JTL, log và report của **một** lần chạy, giúp:

- không ghi đè baseline hoặc nối nhầm kết quả smoke vào baseline;
- tránh lỗi HTML report vì thư mục output đã có dữ liệu;
- giữ lại log/JTL để tìm lỗi hoặc tái kiểm tra;
- phân biệt rõ cấu hình và kết quả của từng lần chạy.

Bạn có thể đổi sang thư mục khác, ví dụ `D:/jmeter-runs/baseline-01`, miễn là thư mục report đích chưa có dữ liệu. `local-runs/` đã được Git ignore nên kết quả cá nhân không bị đưa vào commit; artifact chính thức đã đo được lưu trong `results/`.

## 6. Đọc kết quả

Sau khi JMeter in thông báo kết thúc, mở file:

```text
local-runs/baseline-<timestamp>/jmeter-report/index.html
```

Trong HTML report xem các cột `# Samples`, `Error %`, `Median`, `95th pct` và `99th pct`. Dashboard tổng gồm cả login.

File `summary.json` do `summarize.cjs` tạo có các phần:

- `byLabel`: số lượng, p50/p95/p99, lỗi và throughput của `login`, `search`, `detail`, `checkout`;
- `actions`: tổng ba action, loại login;
- `slo`: kết quả SLO của ba action;
- `actionSharePct`: tỷ lệ search/detail/checkout trên tổng action.

SLO của Week 2 là:

- `actions.p95 < 500 ms`;
- `actions.errorPct < 1%`.

Nếu `slo.p95Below500ms` và `slo.errorsBelow1pct` đều là `true`, baseline đạt SLO. Nếu `false`, ghi nhận kết quả thật trong báo cáo, không bỏ assertion hoặc sửa workload.

Để xem request lỗi và số login/thread:

```powershell
$rows = Import-Csv "$runDir/baseline.jtl"
$rows | Where-Object success -ne 'true' | Select-Object label,responseCode,failureMessage
$rows | Where-Object label -eq 'login' | Group-Object threadName | Select-Object Name,Count
```

Kết quả hợp lệ phải có 50 login và mỗi thread chỉ có một login.

## 7. Lỗi thường gặp

| Lỗi | Cách xử lý |
| --- | --- |
| `java` hoặc `jmeter.bat` không nhận | Kiểm tra `JAVA_HOME` và `PATH` ở mục 1 |
| `Connection refused` | Kiểm tra backend đã start và port là 3000 |
| Không tìm thấy CSV | Dùng `-Jaccounts_csv=...` và `-Jproducts_csv=...` với đường dẫn tuyệt đối |
| EOF/thiếu account | Không chạy quá 50 users với CSV hiện tại |
| Token rỗng, 401/403 | Kiểm tra seed account, extractor và Bearer header; đọc `jmeter.log` |
| Product không tồn tại | Reset DB, dùng product ID 1–5 từ `test_products.csv` |
| Report directory không rỗng | Chạy lại với thư mục timestamp mới |
| Thiếu login hoặc thiếu action | Không nhận run này làm baseline; kiểm tra backend, CSV và log |

## 8. Output tương ứng với Week 2

| Task Week 2 của B | Output tương ứng |
| --- | --- |
| D3 — JMeter workload | `eshop_workload.jmx` |
| D3 — Thread Group 50 users, ramp-up 10s | Thread Group trong `.jmx`; lệnh baseline truyền `-Jusers=50 -Jrampup=10 -Jduration=300` |
| D3 — Regular Expression Extractor và Bearer token | Các node login/extractor/Header Manager trong `.jmx`; checkout thành công trong JTL/report |
| D3 — Workload 55/25/20 | Ba Throughput Controller trong `.jmx`; `actionSharePct` trong `summary.json` |
| D3 — Chạy CLI và sinh report | `local-runs/<baseline>/baseline.jtl`, `jmeter.log`, `jmeter-report/`; artifact mẫu đã đo nằm ở `results/` |
| Bảng đối chiếu D2 vs D3 | `comparison_d2_vs_d3.md` — cột JMeter đã có, cột k6 chờ A bàn giao D2 |

Week 2 được nghiệm thu bằng các lệnh CLI và artifact kết quả. Phần còn chờ duy nhất của B là điền phía D2 trong bảng đối chiếu sau khi A cung cấp report k6; phần D3 CLI đã có đầy đủ artifact.

Tham khảo: [Task Assignment Detail](../../docs/Task_Assignment_Detail.md), [Tool Survey Proposal](../../docs/Tool_Survey_Proposal.md), [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html), [JMeter HTML dashboard](https://jmeter.apache.org/usermanual/generating-dashboard.html).
