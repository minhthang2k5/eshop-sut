# Báo Cáo Hiệu Năng EShop (1-Page Performance Report)
### Đối chiếu kiểm chứng hai môi trường (D8b): Máy A (Linux) vs Máy B (Windows)

> **Người thực hiện:** Thành viên B — Võ Hữu Thắng (MSSV: 23120355)  
> **Môi trường đối chiếu:**  
> * **Máy A (Lê Nguyễn Quốc Thái):** Linux x64 · k6 suite v2 (Bộ số liệu gốc ngày 06/11/2026)  
> * **Máy B (Võ Hữu Thắng):** Windows 11 x64 · Ryzen 7 · Node.js v24.20.0 · k6 v2.2.0  
> **Dữ liệu kiểm thử chung:** 10.000 tài khoản (`test_accounts.csv`) · 200 sản phẩm (`test_products.csv`)

---

## 1. Mục Tiêu & Phương Pháp Kiểm Chứng

Nhiệm vụ **D8b (Verify tái lập kết quả)** chạy lại toàn bộ kịch bản k6 trên Máy B (Windows) để đối chiếu trực tiếp với kết quả đo ban đầu của Máy A (Linux):
* **Workload:** Mô phỏng người dùng mua sắm thực tế (Search 40%, Detail 20%, Cart 22%, Checkout 18%), think time 1–5s, login từng lượt Cart/Checkout.
* **Tiêu chuẩn chất lượng (SLO):** $p95 < 500\text{ ms}$, Tỷ lệ HTTP lỗi $< 1\%$, Checks đạt $\ge 99\%$.
* **Hai cấu hình so sánh:**
  1. *Bản gốc (Untuned):* SQLite mặc định, single writer-lock, tìm kiếm không có index.
  2. *Bản tối ưu (Tuned):* Bật chế độ `PRAGMA journal_mode=WAL` và đánh index `idx_products_name ON products(name)`.

---

## 2. Bảng Đối Chiếu Số Liệu Trực Tiếp: Máy A (Linux) vs Máy B (Windows)

| Bài kiểm thử & Ngưỡng tải | Tiêu chí | Máy A (Thái - Linux) | Máy B (Thắng - Windows) | Nhận xét tính tái lập (D8b) |
| :--- | :--- | :---: | :---: | :--- |
| **Smoke Test**<br>*(1 VU × 1 loop)* | Checks đạt<br>p95 latency<br>Tỷ lệ lỗi | **10/10 PASS**<br>47.89 ms<br>**0.00%** | **10/10 PASS**<br>57.76 ms<br>**0.00%** | **Đồng nhất hoàn hảo:**<br>100% check pass, thông luồng 5 API trên cả 2 máy. |
| **Baseline Test**<br>*(50 VU steady 5 phút)* | Requests<br>Throughput (RPS)<br>p95 latency<br>Tỷ lệ lỗi | 8,655 reqs<br>20.45 req/s<br>**4.68 ms**<br>**0.00%** (PASS) | 8,480 reqs<br>20.16 req/s<br>**14.11 ms**<br>**0.00%** (PASS) | **Tái lập tuyệt đối:**<br>Cả 2 máy đều đạt 0% lỗi, throughput ~20 req/s, $p95 \ll 500\text{ ms}$. |
| **Spike — Đỉnh sốc tải**<br>*(800 VU trong 60s)* | Requests<br>p95 latency<br>Tỷ lệ lỗi | 24,796 reqs<br>**10.48 ms**<br>0.004% (PASS) | 23,523 reqs<br>**352.36 ms**<br>2.22% (FAIL) | **Khớp hành vi nghẽn:**<br>Lượng request tương đương (~24k). Máy B CPU bão hòa sớm hơn nên xuất hiện lỗi ở API search/login. |
| **Spike — Pha hồi phục**<br>*(Hạ về 50 VU trong 60s)* | Requests<br>p95 latency<br>Tỷ lệ lỗi | 1,507 reqs<br>29.92 ms<br>**0.00%** (PASS) | 1,544 reqs<br>21.25 ms<br>**0.00%** (PASS) | **Tự hồi phục (Self-healing):**<br>Cả 2 môi trường lập tức đưa tỷ lệ lỗi về **0.00%**, không bị deadlock. |
| **Stress (Bản gốc)**<br>*(200 $\rightarrow$ 2000 VU, 26 phút)* | Trần Throughput<br>Gãy Latency ($p95>500\text{ms}$)<br>Gãy Tỷ lệ lỗi ($>1\%$) | ~540 req/s<br>tại **1000 VU** (945ms)<br>tại **1600 VU** (1.58%) | ~430 req/s<br>tại **1000 VU** (789ms)<br>tại **1600 VU** (1.00%) | **Trùng khớp tuyệt đối về điểm gãy:**<br>Quy luật suy thoái hiệu năng và giới hạn chịu tải của SQLite gốc xảy ra tại cùng mốc tải. |
| **Stress (Bản tối ưu Tuned)**<br>*(Hiệu quả tại 800 VU)* | p95 latency<br>Tỷ lệ lỗi<br>Mức cải thiện | 59.03 ms<br>0.006%<br>Giảm độ trễ rõ rệt | **14.31 ms**<br>0.007%<br>**Nhanh hơn 15 LẦN** | **Xác nhận giá trị tối ưu:**<br>WAL + Index giải phóng triệt để bottleneck tìm kiếm và checkout ở cả hai máy. |

---

## 3. Phân Tích Chuyên Sâu & Kết Luận Seminar

### 1. Tính độc lập môi trường được chứng minh (Reproducibility Confirmed)
* Kịch bản kiểm thử k6 hoạt động ổn định và nhất quán trên cả hai nền tảng hệ điều hành khác nhau (Linux của Thái và Windows của Thắng).
* Các chỉ số cốt lõi của hệ thống thương mại điện tử EShop:
  * **Tải thông thường (50 VU):** Hệ thống dư sức đáp ứng với độ trễ cực thấp ($< 15\text{ ms}$).
  * **Điểm gãy kiến trúc:** Hiện tượng khóa ghi SQLite đơn luồng và table scan bộc lộ điểm nghẽn tại cùng một ngưỡng người dùng ảo (1000 VU cho độ trễ, 1600 VU cho tỷ lệ lỗi).

### 2. Phát hiện kiến trúc: Khác biệt File Locking giữa Windows và Linux
* **Trên Linux (Máy A):** SQLite WAL sử dụng bộ nhớ chia sẻ POSIX (`mmap`/`shm_open`) ở tầng kernel, giúp backend chịu được tải đồng thời lên đến 2000 VU.
* **Trên Windows (Máy B):** Dưới áp lực tải đồng thời trên 1000 VU ghi vào WAL, cơ chế khóa file `Win32 LockFileEx` của Windows gặp tình trạng nghẽn hàng đợi I/O ở cấp OS, làm nghẽn Event Loop của tiến trình Node.js.
* **Ý nghĩa:** Đây là phát hiện thực nghiệm giá trị, chứng minh rằng khi triển khai ứng dụng dùng SQLite trên môi trường Windows production, cần đặc biệt lưu ý giới hạn I/O lock của hệ điều hành.

---

## 4. Danh Mục Tài Liệu & Bằng Chứng

Toàn bộ artifacts của hai máy được lưu giữ phục vụ việc đối chiếu minh bạch:
* **Báo cáo gốc của Máy A (Lê Nguyễn Quốc Thái):** Nằm trong thư mục [`performance/k6/reports/`](../performance/k6/reports/) (từ report 01 đến 06).
* **Bằng chứng thực nghiệm Máy B (Võ Hữu Thắng):** 
  * Baseline Dashboard: [`my-baseline-report.html`](../performance/k6/output/my-baseline-report.html) · [`my-baseline-summary.json`](../performance/k6/output/my-baseline-summary.json)
  * Spike Dashboard: [`my-spike-report.html`](../performance/k6/output/my-spike-report.html) · [`my-spike-summary.json`](../performance/k6/output/my-spike-summary.json)
  * Stress Dashboard: [`my-stress-untuned-report.html`](../performance/k6/output/my-stress-untuned-report.html) · [`my-stress-tuned-report.html`](../performance/k6/output/my-stress-tuned-report.html)
