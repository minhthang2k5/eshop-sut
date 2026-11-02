# Analyzer k6

Đọc dữ liệu đã lưu của baseline, stress hoặc spike; tạo báo cáo Markdown, HTML có SVG và CSV tài nguyên. Chỉ cần Python 3 chuẩn, không cần mạng hoặc thư viện vẽ. Không đọc raw `metrics.json` và không chỉnh sửa dữ liệu đầu vào.

## Cách chạy

Từ thư mục `eshop-sut`:

```bash
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type stress
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type spike
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> --type baseline
```

`--type` bắt buộc. Vẫn hỗ trợ truyền đường dẫn `node-cpu-ram.jsonl` thay cho thư mục run.

Mặc định xuất trong `<run-id>/analysis/`:

- `report.md`, `report.html` (biểu đồ VU target, p95 và CPU/RAM nếu có đủ dữ liệu).
- `node-cpu-ram.csv`: mẫu tài nguyên đã lọc theo cửa sổ đo.
- `cpu-ram-phases.csv`: thống kê tài nguyên từng phase.
- `cpu-ram-before-during-after.csv`: thống kê trước, trong và sau tải.

Để xuất vào nơi khác:

```bash
python3 performance/k6/analyze/analyze.py performance/k6/output/<run-id> \
  --type stress --report-dir performance/k6/reports
```

Khi dùng `--report-dir`, tên báo cáo theo loại test:

| Loại | Markdown | HTML |
|---|---|---|
| baseline | `02-baseline-test-report.md` | `baseline_report.html` |
| stress | `03-stress-test-report.md` | `stress_report.html` |
| spike | `04-spike-test-report.md` | `spike_report.html` |

CSV có tên chung trong thư mục đích; xuất các run/loại khác nhau vào thư mục riêng nếu cần lưu toàn bộ CSV. Chạy lại sẽ thay toàn bộ các tệp đầu ra tương ứng, kể cả ghi chú chỉnh tay. Runner stress tự gọi analyzer với đích `reports/`; runner baseline/spike hiện giữ nguyên, chưa tự gọi hoặc thu telemetry.

## Dữ liệu đầu vào

| Tệp | Cách sử dụng |
|---|---|
| `summary.json` | Metric tổng và submetric phase/endpoint; hỗ trợ giá trị trực tiếp và dạng `values` của `handleSummary` |
| `measurement-timeline.json` | Mốc trước tải, k6 launch, scenario, k6 end, sau tải; `profile` thực tế và `interrupted` nếu có |
| `node-cpu-ram.jsonl` | Mẫu `type=sample`, `ts` (epoch ms), `cpu_pct` (100% = một core), `rss` (bytes) |
| `k6.log` | Khôi phục scenario start/profile từ marker `STRESS_TIMELINE` của runner stress cũ |

Không cộng hoặc lấy trung bình percentile để tạo percentile toàn bài. RPS phase = request count / thời lượng cửa sổ quan sát; khi thiếu mốc thời gian, dùng thời lượng danh định từ profile và ghi `nominal`. Không suy ra thời điểm chạy từ tên thư mục.

Thiếu CPU/RAM không ngăn đánh giá HTTP. Không có scenario start thì không tự gán phase/vẽ CPU theo mốc suy đoán. Không có mẫu thì ghi N/A, không ghi 0. Sample hỏng/nonfinite bị bỏ qua và đếm trong cảnh báo; summary/config/timeline sai cấu trúc sẽ báo lỗi trước khi thay báo cáo.

## Cấu hình và kết quả

`profiles.json` là cấu hình **của analyzer**, tách biệt với script k6. Mỗi loại chứa:

- `profile`: phase, số giây và target VU; dùng khi run không lưu profile thực tế.
- `assess_phases`: phase cần đánh giá, độc lập với tên phase.
- `rules`: `metric`, `stat` (`p(95)`, `rate`, `count`), `op`, `limit`, `scope` (`phase` hoặc `global`), `endpoints` (`null` nghĩa là tổng).
- `title`, `description`, `markdown_name`, `html_name`: nội dung và tên đầu ra.

Sau khi sửa ngưỡng hoặc profile trong script k6, cập nhật cấu hình tương ứng và chạy kiểm thử. Kiểm thử có Node.js đối chiếu threshold của cả ba script với cấu hình; không phát tải và không đọc fixture trong bước khởi tạo giả lập này.

Stress bỏ threshold skipped; login lỗi đã tính vào `business_operations_failed`. Baseline/spike giữ ngưỡng skipped hiện có. Login baseline được đánh giá toàn bài, không bắt buộc xuất hiện trong steady; spike chỉ thống kê login, không thêm SLO riêng.

Báo cáo đánh giá lại số liệu theo cấu hình này, không dùng boolean threshold trong summary lịch sử. Bảng chi tiết nêu điều kiện toàn bài và các điều kiện phase bị vi phạm/thiếu dữ liệu.

- `PASS`: tất cả điều kiện bắt buộc đủ dữ liệu và đạt; cửa sổ không bị biết là thiếu thời lượng.
- `FAIL`: có vi phạm được quan sát, kể cả khi phần khác thiếu dữ liệu.
- `INCOMPLETE`: chưa đủ bằng chứng để xác nhận đạt.
- Độ đầy đủ lần đo tách riêng: `COMPLETE` nếu timeline bao phủ lịch tải, `PARTIAL` nếu bị ngắt/chưa đủ lịch, `UNKNOWN` nếu chưa đủ mốc để xác nhận. PASS trên metric với UNKNOWN không chứng minh run đã hoàn tất lịch tải.

## Cấu trúc và kiểm thử

- `analyze.py`: đọc, kiểm tra, chuẩn hóa metric/tag, đánh giá và tính thống kê; ghi các tệp đầu ra.
- `reporting.py`: nhận kết quả đã tính, dựng Markdown/HTML/SVG; không đánh giá threshold hoặc đọc summary.
- `profiles.json`: cấu hình riêng của ba loại test.

```bash
python3 -m unittest discover -s performance/k6/analyze -v
```

Kiểm thử chính chỉ cần Python. Kiểm thử đối chiếu với script k6 dùng Node.js và được bỏ qua nếu máy chưa cài Node.
