# -*- coding: utf-8 -*-
"""Tạo dữ liệu chuẩn cho mỗi phiên usability (Task 2).

Cách dùng (backend phải đang chạy ở http://localhost:3000 và VỪA được khởi động lại để seed sạch):
    node backend/server.js                       # khởi động lại backend (seed lại DB)
    python hw03/scripts/usability_seed.py

Kết quả:
  - 13 tài khoản khách, trong đó 'Nguyen Van A' (vana@example.com) nằm giữa danh sách cho nhiệm vụ T4.
  - 6 đơn hàng: #1 Đã giao, #2 Đã hủy, #3 Đang giao, #4 Đã xác nhận, #5 Chờ xác nhận, #6 Chờ xác nhận 150.000 đ (nhiệm vụ T3).
  - Dashboard sẽ hiện 6 đơn; chưa có danh mục 'Màn hình' (nhiệm vụ T2).
Script từ chối chạy nếu đã có đơn hàng, để không tạo trùng dữ liệu giữa các phiên.
"""
import json
import sys
import urllib.error
import urllib.request

B = "http://localhost:3000/api"


def call(path, method="GET", body=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(B + path, method=method, data=json.dumps(body).encode() if body is not None else None, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]
    except urllib.error.URLError as e:
        sys.exit(f"Không kết nối được backend ({e.reason}). Hãy chạy: node backend/server.js")


def main():
    s, a = call("/login", "POST", {"email": "admin@eshop.com", "password": "Admin123!"})
    if s != 200:
        sys.exit(f"Đăng nhập admin thất bại ({s}: {a}). Nếu bị khóa, chạy: node hw03/scripts/unlock_admin.js")
    at = a["token"]
    s, orders = call("/admin/orders", token=at)
    if orders:
        sys.exit(f"Đã có {len(orders)} đơn hàng. Khởi động lại backend (seed lại DB) rồi chạy lại script.")

    # 12 khách khác để nhiệm vụ T4 phải thực sự tìm (bảng không có cột Tên và ô tìm kiếm); vana đứng giữa danh sách
    others = ["tran.b", "le.hoa", "pham.nam", "nguyen.linh", "vo.thanh", "dang.mai", "bui.khoa",
              "do.phuong", "ngo.tuan", "ly.trang", "huynh.duc", "truong.yen"]
    for i, handle in enumerate(others):
        if i == 6:
            call("/register", "POST", {"name": "Nguyen Van A", "email": "vana@example.com", "password": "Test1234!"})
        call("/register", "POST", {"name": handle.replace(".", " ").title(), "email": f"{handle}@example.com", "password": "Test1234!"})
    s, u = call("/login", "POST", {"email": "test@eshop.com", "password": "Test1234!"})
    ut = u["token"]

    data = [(500000, "12 Le Loi, Q1, TP.HCM"), (1250000, "45 Nguyen Hue, Q1, TP.HCM"), (300000, "7 Tran Hung Dao, Q5, TP.HCM"),
            (2000000, "99 CMT8, Q3, TP.HCM"), (750000, "21 Hai Ba Trung, Q1, TP.HCM"), (150000, "3 Le Thanh Ton, Q1, TP.HCM")]
    for amount, addr in data:
        s, _ = call("/checkout", "POST", {"total_amount": amount, "shipping_address": addr}, ut)
        assert s == 200, (s, amount)

    s, orders = call("/admin/orders", token=at)
    ids = sorted(o["id"] for o in orders)
    path = {1: ["confirmed", "shipping", "delivered"], 2: ["canceled"], 3: ["confirmed", "shipping"], 4: ["confirmed"]}
    for i, steps in path.items():
        for st in steps:
            s, _ = call(f"/admin/orders/{ids[i - 1]}/status", "PUT", {"status": st}, at)
            assert s == 200, (ids[i - 1], st, s)

    s, orders = call("/admin/orders", token=at)
    print("Đã tạo dữ liệu chuẩn:")
    for o in sorted(orders, key=lambda x: x["id"]):
        print(f"  #{o['id']}  {o['total_amount']:>9,}  {o['status']}")
    print("Tài khoản khách: vana@example.com (cho T4). Hãy đăng nhập Admin và để ở Dashboard trước khi bắt đầu phiên.")


if __name__ == "__main__":
    main()
