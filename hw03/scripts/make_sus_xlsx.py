# -*- coding: utf-8 -*-
"""Tạo hw03/usability/SUS_Scoring.xlsx: bảng nhập SUS, dữ liệu nhiệm vụ và thống kê tự tính.

Chạy:  python hw03/scripts/make_sus_xlsx.py   (cần: pip install openpyxl)
Sheet 'SUS':      nhập 10 điểm gốc (1-5) cho mỗi participant; cột 'Điểm SUS' tự tính; thống kê cho P01-P07 (không tính pilot P00).
Sheet 'Nhiệm vụ': nhập thời gian (giây), kết quả (H/HTG/K), số lỗi, số lần trợ giúp, SEQ; thống kê tự tính.
Mọi ô dữ liệu để TRỐNG: chỉ nhập số liệu thật từ các phiên.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parents[1] / "usability" / "SUS_Scoring.xlsx"
PARTS = ["P00 (pilot)"] + [f"P{i:02d}" for i in range(1, 8)]
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(bold=True, color="FFFFFF")


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row, c)
        cell.font, cell.fill = HEAD_FONT, HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")


wb = Workbook()
# ---------------- SUS
ws = wb.active
ws.title = "SUS"
ws.append(["Mã"] + [f"Q{i}" for i in range(1, 11)] + ["Điểm SUS", "Ghi chú"])
style_header(ws, 1, 13)
for p in PARTS:
    r = ws.max_row + 1
    ws.append([p] + [None] * 10 + [
        f'=IF(COUNT(B{r}:K{r})=10,((B{r}-1)+(5-C{r})+(D{r}-1)+(5-E{r})+(F{r}-1)+(5-G{r})+(H{r}-1)+(5-I{r})+(J{r}-1)+(5-K{r}))*2.5,"")', None])
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True, showErrorMessage=True,
                    errorTitle="Giá trị không hợp lệ", error="Nhập số nguyên từ 1 đến 5")
ws.add_data_validation(dv)
dv.add("B2:K9")
last = 9
ws["A11"], ws["B11"] = "THỐNG KÊ (P01 đến P07, không gồm pilot)", None
ws["A11"].font = Font(bold=True)
rng = "L3:L9"
stats = [("Số người đã có điểm", f"=COUNT({rng})"),
         ("Điểm SUS trung bình", f'=IF(COUNT({rng})=0,"",AVERAGE({rng}))'),
         ("Trung vị", f'=IF(COUNT({rng})=0,"",MEDIAN({rng}))'),
         ("Độ lệch chuẩn", f'=IF(COUNT({rng})<2,"",STDEV({rng}))'),
         ("Thấp nhất", f'=IF(COUNT({rng})=0,"",MIN({rng}))'),
         ("Cao nhất", f'=IF(COUNT({rng})=0,"",MAX({rng}))'),
         ("So với mốc ngành (68)", '=IF(B13="","",IF(B13>=80,"Rất tốt (>=80)",IF(B13>=68,"Tốt (68-80)",IF(B13>=51,"Dưới trung bình (51-68)","Kém (<51)"))))')]
for i, (k, f) in enumerate(stats, 12):
    ws.cell(i, 1, k)
    ws.cell(i, 2, f)
ws["A20"] = "Cách tính: câu lẻ = điểm - 1; câu chẵn = 5 - điểm; tổng 10 câu x 2,5 (thang 0-100). Mốc tham khảo: trung bình ngành 68."
ws.column_dimensions["A"].width = 40
for c in range(2, 12):
    ws.column_dimensions[get_column_letter(c)].width = 6
ws.column_dimensions["L"].width = 12
ws.column_dimensions["M"].width = 30
ws.freeze_panes = "B2"

# ---------------- Nhiệm vụ
wt = wb.create_sheet("Nhiệm vụ")
tasks = ["T1 Doanh thu, số đơn", "T2 Thêm nhóm hàng", "T3 Xác nhận đơn 150.000", "T4 Tìm khách vana@example.com"]
subs = ["Thời gian (giây)", "Kết quả (H/HTG/K)", "Số lỗi", "Số lần trợ giúp", "SEQ (1-7)"]
wt.cell(1, 1, "Mã")
col = 2
for t in tasks:
    wt.cell(1, col, t)
    wt.merge_cells(start_row=1, start_column=col, end_row=1, end_column=col + 4)
    for j, s in enumerate(subs):
        wt.cell(2, col + j, s)
    col += 5
wt.cell(2, 1, "")
style_header(wt, 1, col - 1)
style_header(wt, 2, col - 1)
for p in PARTS:
    wt.append([p])
dv2 = DataValidation(type="list", formula1='"H,HTG,K"', allow_blank=True, showErrorMessage=True, error="Chọn H, HTG hoặc K")
dv3 = DataValidation(type="whole", operator="between", formula1="1", formula2="7", allow_blank=True, showErrorMessage=True, error="SEQ từ 1 đến 7")
wt.add_data_validation(dv2)
wt.add_data_validation(dv3)
first, lastr = 3, 2 + len(PARTS)
main_first, main_last = 4, lastr  # P01..P07 (bỏ pilot ở hàng 3)
for k in range(4):
    c0 = 2 + 5 * k
    dv2.add(f"{get_column_letter(c0 + 1)}{first}:{get_column_letter(c0 + 1)}{lastr}")
    dv3.add(f"{get_column_letter(c0 + 4)}{first}:{get_column_letter(c0 + 4)}{lastr}")
sr = lastr + 2
wt.cell(sr, 1, "THỐNG KÊ (P01 đến P07)").font = Font(bold=True)
labels = ["Thời gian trung bình (giây)", "Tỉ lệ hoàn thành không trợ giúp", "Tỉ lệ hoàn thành (kể cả có trợ giúp)", "Tổng số lỗi", "Tổng số lần trợ giúp", "SEQ trung bình"]
for i, lab in enumerate(labels, 1):
    wt.cell(sr + i, 1, lab)
for k in range(4):
    c0 = 2 + 5 * k
    L = lambda j: get_column_letter(c0 + j)
    tr, rs, er, hp, sq = (f"{L(j)}{main_first}:{L(j)}{main_last}" for j in range(5))
    wt.cell(sr + 1, c0, f'=IF(COUNT({tr})=0,"",AVERAGE({tr}))')
    wt.cell(sr + 2, c0, f'=IF(COUNTA({rs})=0,"",COUNTIF({rs},"H")/COUNTA({rs}))').number_format = "0%"
    wt.cell(sr + 3, c0, f'=IF(COUNTA({rs})=0,"",(COUNTIF({rs},"H")+COUNTIF({rs},"HTG"))/COUNTA({rs}))').number_format = "0%"
    wt.cell(sr + 4, c0, f'=IF(COUNT({er})=0,"",SUM({er}))')
    wt.cell(sr + 5, c0, f'=IF(COUNT({hp})=0,"",SUM({hp}))')
    wt.cell(sr + 6, c0, f'=IF(COUNT({sq})=0,"",AVERAGE({sq}))')
wt.column_dimensions["A"].width = 38
for c in range(2, col):
    wt.column_dimensions[get_column_letter(c)].width = 14
wt.freeze_panes = "B3"

wb.save(OUT)
print("Đã tạo", OUT)
