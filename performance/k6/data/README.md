# Dữ liệu k6

| File | Nội dung |
|---|---|
| `test_accounts.csv` | 10.000 account; `email,password,name,role` |
| `test_products.csv` | 200 sản phẩm; ID, tên, giá, mô tả, ảnh, category và keyword |
| `test-data-manifest.json` | Manifest dữ liệu dùng chung cho baseline/stress/soak/spike; chứa hash CSV, sản phẩm và 12 keyword và tập ID kỳ vọng |

## Seed

Chạy từ `eshop-sut`, **sau khi backend khởi động xong**:

```bash
# Backend gốc
node performance/k6/data/seed.js

# Hoặc tuned
node performance/k6/data/seed.js tuned-backend/database_tuned.sqlite
```

Seed thêm/cập nhật account theo email và sản phẩm theo ID trong cùng transaction. Dữ liệu ngoài CSV được giữ lại. Muốn bắt đầu mới: restart backend rồi seed lại.

Sau khi sửa CSV, cập nhật fixture stress:

```bash
node performance/k6/data/build-manifest.cjs
```

Search tìm trong **tên sản phẩm**; cột `search_keyword` là metadata fixture. Baseline kiểm tra toàn bộ CSV và cấp 50 account đầu cho 50 VU; sản phẩm ID 1 / iPhone được đọc từ CSV. Spike vẫn yêu cầu đúng 50 account nên chưa dùng được CSV 10.000 account này. Smoke dùng tài khoản startup, không cần seed.

Trọng số chọn keyword nằm trong `../lib/data.js` (`keywordWeights`), tổng bằng 100. Sửa trọng số không cần build lại manifest.
