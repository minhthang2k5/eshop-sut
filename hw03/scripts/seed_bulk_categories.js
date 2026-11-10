// Tạo / xóa nhiều danh mục thử để kiểm tra bảng dữ liệu lớn (GUI checklist, nhóm "Dữ liệu lớn").
// Cách dùng (backend phải đang chạy ở http://localhost:3000):
//   node hw03/scripts/seed_bulk_categories.js add 150     -> thêm 150 danh mục "BulkTest i"
//   node hw03/scripts/seed_bulk_categories.js clean       -> xóa mọi danh mục bắt đầu bằng "BulkTest"
// Tài khoản admin lấy từ dữ liệu seed (backend/database.js).
const API = "http://localhost:3000/api";
const [, , mode = "add", nArg = "150"] = process.argv;

async function login() {
  const r = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "admin@eshop.com", password: "Admin123!" }),
  });
  const j = await r.json();
  if (!j.token) throw new Error("Đăng nhập thất bại: " + JSON.stringify(j));
  return j.token;
}

(async () => {
  const token = await login();
  const h = { "Content-Type": "application/json", Authorization: `Bearer ${token}` };
  if (mode === "add") {
    const n = parseInt(nArg, 10);
    for (let i = 1; i <= n; i++) {
      await fetch(`${API}/categories`, { method: "POST", headers: h, body: JSON.stringify({ name: `BulkTest ${i}` }) });
    }
  } else if (mode === "clean") {
    const cats = await (await fetch(`${API}/categories`)).json();
    for (const c of cats.filter((c) => (c.name || "").startsWith("BulkTest") || c.name === "")) {
      await fetch(`${API}/categories/${c.id}`, { method: "DELETE", headers: h });
    }
  }
  const total = (await (await fetch(`${API}/categories`)).json()).length;
  console.log(`Xong (${mode}). Số danh mục hiện tại: ${total}`);
})().catch((e) => { console.error(e.message); process.exit(1); });
