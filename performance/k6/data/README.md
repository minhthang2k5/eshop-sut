# k6 test data

Thư mục này chứa fixture dùng cho các bài performance test k6. Seed fixture vào database sau khi backend khởi động hoàn tất.

## Dataset hiện tại

| File | Số bản ghi | Schema |
|---|---:|---|
| `test_accounts.csv` | 10.000 account | `email,password,name,role` |
| `test_product.csv` | 200 product | `product_id,name,price,description,image_url,category_id,search_keyword` |

Các account có email duy nhất và role `user`. Product giữ ID ổn định; `search_keyword` phục vụ kiểm tra/phân loại fixture k6, còn backend lưu các cột ID, tên, giá, mô tả, ảnh và category. Năm product đầu giữ các fixture cũ để tương thích với smoke/baseline.

## Seed dữ liệu

Từ thư mục `eshop-sut`, khởi động backend trước để backend tạo schema và database, sau đó ở terminal khác chạy:

```bash
node performance/k6/data/seed.js
```

Seeder đọc cả hai CSV, kiểm tra header, dữ liệu bắt buộc và khóa trùng, rồi thêm hoặc cập nhật account theo email và product theo `product_id` trong cùng transaction. Các account/product khác không có trong CSV không bị xóa. Seeder chỉ in số bản ghi đã thêm/cập nhật, không in password.

Mặc định database đích là `backend/database.sqlite`. Để seed backend tune, truyền đường dẫn DB của backend đó:

```bash
node performance/k6/data/seed.js tuned-backend/database_tuned.sqlite
```

Chạy seeder từ thư mục `eshop-sut` để các đường dẫn trên hoạt động như ví dụ.

## Refresh database

Backend xóa và tạo lại các bảng khi khởi động, sau đó nạp dữ liệu mặc định. Để làm mới dữ liệu test:

1. Dừng backend đang chạy.
2. Khởi động lại backend cần dùng (`backend` hoặc `tuned-backend`) để tạo database/schema mới.
3. Từ `eshop-sut`, chạy seeder với DB tương ứng như phần trên.

Ví dụ refresh backend gốc:

```bash
# Terminal 1, từ eshop-sut
cd backend
node server.js

# Terminal 2, từ eshop-sut
node performance/k6/data/seed.js
```

Nếu cần xóa hẳn database SQLite, dừng backend trước rồi xóa đúng file (`backend/database.sqlite` hoặc `tuned-backend/database_tuned.sqlite`); khởi động backend và seed lại. Không xóa database khi server còn chạy.
