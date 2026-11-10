// Mở khóa tài khoản admin khi bị khóa do nhập sai mật khẩu (backend cộng 2 lần sai mỗi lần, khóa 3 phút khi >= 3).
// Cách dùng: node hw03/scripts/unlock_admin.js   (chạy từ thư mục eshop-sut)
const path = require("path");
const sqlite3 = require(path.resolve(__dirname, "../../backend/node_modules/sqlite3"));
const db = new sqlite3.Database(path.resolve(__dirname, "../../backend/database.sqlite"));
db.run(
  "UPDATE users SET password = 'Admin123!', login_attempts = 0, locked_until = NULL WHERE email = 'admin@eshop.com'",
  function (err) {
    if (err) return console.error(err.message);
    console.log(`Đã mở khóa admin@eshop.com (${this.changes} dòng).`);
    db.close();
  },
);
