# -*- coding: utf-8 -*-
"""Xuất GUI Checklist (bản chính + Đơn hàng) ra một file Excel để thực thi.

Chạy:  python hw03/scripts/export_excel.py   (từ thư mục eshop-sut; cần: pip install openpyxl)
Đầu ra: hw03/checklist/GUI_Checklist.xlsx
  Sheet "Checklist"  - mọi mục (giữ nguyên ID GUI-xxx và ORD-xxx), cột Kết quả có danh sách chọn
  Sheet "Tổng hợp"   - test summary bằng công thức (tự cập nhật khi điền kết quả)
Mục trùng ý được đánh dấu ở cột "Trùng ý" và loại khỏi tổng số mục thực thi.
"""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

CK = Path(__file__).resolve().parents[1] / "checklist"
MAIN = CK / "GUI_Checklist_final.csv"
ORD = CK / "orders" / "GUI_Checklist_final_orders.csv"
OUT = CK / "GUI_Checklist.xlsx"

# Mục trùng ý: giữ mục bên phải, không thực thi mục bên trái.
DUP = {
    "GUI-070": "Trùng ORD-002 (nhãn trạng thái đơn). Không thực thi, dùng ORD-002.",
    "GUI-072": "Trùng ORD-028 (nút hành động theo từng trạng thái, gồm đơn Đã hủy). Không thực thi, dùng ORD-028.",
}

HEAD = ["ID", "Màn hình", "IA", "Control / Thành phần", "Mục kiểm tra", "Kết quả mong đợi", "Ưu tiên", "Nguồn mục",
        "ID nháp (truy vết)", "Nguyên tắc / checklist nguồn", "Vì sao AI bỏ sót", "Kết quả (Passed/Failed)", "Notes",
        "Screenshot", "Trùng ý"]
WIDTH = [10, 18, 7, 24, 55, 50, 11, 20, 28, 28, 40, 16, 40, 22, 38]


def load(path):
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


def load_results():
    """Đọc kết quả thực thi (nếu có) từ execution_results.py cạnh script này."""
    import importlib.util
    p = Path(__file__).with_name("execution_results.py")
    if not p.exists():
        return {}
    spec = importlib.util.spec_from_file_location("execution_results", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.R


def main():
    rows = load(MAIN) + load(ORD)
    ids = [r["ID"] for r in rows]
    assert len(ids) == len(set(ids)), "ID bị trùng giữa hai checklist"
    assert set(DUP) <= set(ids)

    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    ws.append(HEAD)
    results = load_results()
    assert set(results) <= set(ids), set(results) - set(ids)
    for r in rows:
        res = results.get(r["ID"], ("", "", ""))
        shot = res[2] or ("Chưa chụp" if res[0] == "Failed" else "")
        ws.append([r["ID"], r["Màn hình"], r["IA"], r["Control / Thành phần"], r["Mục kiểm tra"], r["Kết quả mong đợi"],
                   r["Ưu tiên"], r["Nguồn mục"], r["ID nháp (truy vết)"], r["Nguyên tắc / checklist nguồn"],
                   r["Vì sao AI bỏ sót"], res[0], res[1], shot, DUP.get(r["ID"], "")])
    n = len(rows)
    last = n + 1

    thin = Side(style="thin", color="BBBBBB")
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    for i, w in enumerate(WIDTH, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2, max_row=last):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
        if row[14].value:  # mục trùng ý
            for c in row:
                c.fill = PatternFill("solid", fgColor="EEEEEE")
                c.font = Font(color="888888", italic=True)
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(HEAD))}{last}"

    dv = DataValidation(type="list", formula1='"Passed,Failed"', allow_blank=True, showErrorMessage=True,
                        errorTitle="Giá trị không hợp lệ", error="Chọn Passed hoặc Failed")
    ws.add_data_validation(dv)
    dv.add(f"L2:L{last}")
    ws.conditional_formatting.add(f"L2:L{last}", CellIsRule(operator="equal", formula=['"Passed"'], fill=PatternFill("solid", bgColor="C6EFCE")))
    ws.conditional_formatting.add(f"L2:L{last}", CellIsRule(operator="equal", formula=['"Failed"'], fill=PatternFill("solid", bgColor="FFC7CE")))

    # ---- Tổng hợp
    s = wb.create_sheet("Tổng hợp")
    R = lambda col: f"Checklist!${col}$2:${col}${last}"
    s["A1"] = "Test summary – GUI Checklist (Admin: Người dùng, Danh mục, Đơn hàng, Dashboard, Home)"
    s["A1"].font = Font(bold=True, size=13)
    s.append([])
    s.append(["Chỉ tiêu", "Giá trị"])
    s.append(["Tổng số mục đã thiết kế", f"=COUNTA({R('A')})"])
    s.append(["  Trong đó do AI sinh (gồm đã sửa/gộp/tách)", f'=COUNTIF({R("H")},"AI*")'])
    s.append(["  Trong đó tự thêm", f'=COUNTIF({R("H")},"Tự thêm*")'])
    s.append(["Mục trùng ý (loại khỏi thực thi)", f'=COUNTA({R("O")})'])
    s.append(["Số mục cần thực thi", "=B4-B7"])
    s.append(["Đã thực thi", "=B10+B11"])
    s.append(["  Passed", f'=COUNTIFS({R("L")},"Passed",{R("O")},"")'])
    s.append(["  Failed", f'=COUNTIFS({R("L")},"Failed",{R("O")},"")'])
    s.append(["Chưa thực thi", "=B8-B9"])
    s.append(["Tỉ lệ Passed trên mục đã thực thi", '=IF(B9=0,"",B10/B9)'])
    s["B13"].number_format = "0.0%"

    s.append([])
    s.append(["Theo IA", "Cần thực thi", "Passed", "Failed", "Chưa chạy"])
    start = s.max_row + 1
    for ia in ["IA-01", "IA-02", "IA-03", "IA-04"]:
        r = s.max_row + 1
        s.append([ia, f'=COUNTIFS({R("C")},A{r},{R("O")},"")',
                  f'=COUNTIFS({R("C")},A{r},{R("L")},"Passed",{R("O")},"")',
                  f'=COUNTIFS({R("C")},A{r},{R("L")},"Failed",{R("O")},"")', f"=B{r}-C{r}-D{r}"])
    s.append([])
    s.append(["Theo màn hình", "Cần thực thi", "Passed", "Failed", "Chưa chạy"])
    for sc in sorted({r["Màn hình"] for r in rows}):
        r = s.max_row + 1
        s.append([sc, f'=COUNTIFS({R("B")},A{r},{R("O")},"")',
                  f'=COUNTIFS({R("B")},A{r},{R("L")},"Passed",{R("O")},"")',
                  f'=COUNTIFS({R("B")},A{r},{R("L")},"Failed",{R("O")},"")', f"=B{r}-C{r}-D{r}"])
    s.append([])
    s.append(["Ghi chú: các cột Kết quả để trống cho tới khi thực thi; số liệu tự cập nhật khi bạn điền Passed/Failed ở sheet Checklist."])
    for row in s.iter_rows():
        for c in row:
            if c.row in (3,) or (c.value in ("Theo IA", "Theo màn hình")):
                pass
    for r in range(1, s.max_row + 1):
        if s.cell(r, 1).value in ("Chỉ tiêu", "Theo IA", "Theo màn hình"):
            for c in s[r]:
                if c.value is not None:
                    c.font = Font(bold=True, color="FFFFFF")
                    c.fill = PatternFill("solid", fgColor="1F3864")
    s.column_dimensions["A"].width = 48
    for col in "BCDE":
        s.column_dimensions[col].width = 16

    wb.save(OUT)
    print(f"Đã xuất {OUT} ({n} dòng, {len(DUP)} mục trùng ý)")
    from collections import Counter
    live = [r for r in rows if r["ID"] not in DUP]
    print("Cần thực thi:", len(live), "| theo IA:", dict(sorted(Counter(r["IA"] for r in live).items())))
    print("Theo màn hình:", dict(Counter(r["Màn hình"] for r in live)))
    print("AI:", sum(r["Nguồn mục"].startswith("AI") for r in rows), "| tự thêm:", sum(r["Nguồn mục"].startswith("Tự thêm") for r in rows))


if __name__ == "__main__":
    main()
