# -*- coding: utf-8 -*-
"""Tạo hw03/usability/Usability_Sessions.xlsx: sổ làm việc dùng cho pilot (P00) và 7 phiên chính (P01-P07).

Chạy:  python hw03/scripts/make_usability_workbook.py   (cần: pip install openpyxl)
Các sheet:
  Hướng dẫn phiên : checklist trước/trong/sau phiên, lời giới thiệu, 4 nhiệm vụ, thang gợi ý
  P00..P07        : mỗi người một sheet (thông tin, nhiệm vụ, SUS tự tính, probe, quan sát, giả thuyết, nhận xét)
  Tổng hợp        : thống kê tự tính từ P01..P07 (pilot P00 KHÔNG tính)
  Phát hiện       : bảng xếp mức độ = nghiêm trọng x xác suất
Mọi ô dữ liệu để TRỐNG (nền vàng nhạt = chỗ cần điền). Không chứa thông tin cá nhân của participant.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parents[1] / "usability" / "Usability_Sessions.xlsx"
PARTS = [f"P{i:02d}" for i in range(0, 8)]
MAIN = PARTS[1:]
FORMAT = {"P00": "In-person", "P01": "In-person", "P02": "In-person", "P03": "In-person",
          "P04": "Remote", "P05": "Remote", "P06": "Remote", "P07": "Remote"}

NAVY = PatternFill("solid", fgColor="1F3864")
INPUT = PatternFill("solid", fgColor="FFF9DB")
SEC = PatternFill("solid", fgColor="D9E2F3")
WHITE_B = Font(bold=True, color="FFFFFF")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
WRAP = Alignment(wrap_text=True, vertical="top")

TASKS = [("T1", "Cho tôi biết tổng doanh thu và tổng số đơn hàng."),
         ("T2", "Thêm nhóm hàng mới tên 'Màn hình' vào cửa hàng."),
         ("T3", "Tìm đơn 150.000 ₫, cho biết trạng thái, rồi xác nhận đơn."),
         ("T4", "Kiểm tra khách hàng có email vana@example.com đã đăng ký chưa.")]
SUS_Q = ["Tôi nghĩ rằng tôi sẽ muốn dùng trang quản trị này thường xuyên.",
         "Tôi thấy trang quản trị này phức tạp không cần thiết.",
         "Tôi thấy trang quản trị này dễ sử dụng.",
         "Tôi nghĩ rằng tôi cần sự giúp đỡ của một người có kỹ thuật để dùng được trang này.",
         "Tôi thấy các chức năng của trang này được kết hợp với nhau hợp lý.",
         "Tôi thấy trang này có quá nhiều chỗ không nhất quán.",
         "Tôi nghĩ hầu hết mọi người sẽ học cách dùng trang này rất nhanh.",
         "Tôi thấy trang này rất rườm rà, khó dùng.",
         "Tôi cảm thấy rất tự tin khi dùng trang này.",
         "Tôi cần học rất nhiều thứ trước khi có thể bắt đầu dùng trang này."]
PROBE = [("Rõ ràng", "Hãy kể lại những gì bạn thấy trên màn hình đầu tiên. Có gì bạn không hiểu không?"),
         ("Rõ ràng", "Các con số và tên gọi trên trang (doanh thu, trạng thái đơn, tên nút) có rõ nghĩa không? Chỗ nào bạn phải đoán?"),
         ("Rõ ràng", "Khi cần tìm chức năng, bạn nhìn vào đâu trước? Vì sao?"),
         ("Rõ ràng", "Có chỗ nào bạn tưởng một thứ nhưng hóa ra là thứ khác?"),
         ("Phục hồi lỗi", "Có lúc nào bạn làm nhầm hoặc nghĩ mình làm nhầm không? Chuyện gì xảy ra và bạn làm gì tiếp?"),
         ("Phục hồi lỗi", "Sau khi làm xong một việc (thêm nhóm hàng, xác nhận đơn), làm sao bạn biết nó đã thành công?"),
         ("Phục hồi lỗi", "Nếu lỡ xóa nhầm một thứ, bạn mong trang này giúp gì cho bạn?"),
         ("Tốc độ", "Việc nào bạn thấy mất nhiều thời gian hơn bạn nghĩ? Điều gì làm nó chậm?"),
         ("Tốc độ", "Có lúc nào bạn chờ mà không biết trang đang làm gì không?"),
         ("Tốc độ", "Bạn có phải làm lại hoặc quay lại bước nào không?"),
         ("Tin cậy", "Bạn có tin các con số trên trang tổng quan không? Vì sao?"),
         ("Tin cậy", "Khi bấm Xác nhận, Hủy, Xóa, bạn có yên tâm không? Điều gì làm bạn lo?"),
         ("Tin cậy", "Bạn có dám dùng trang này cho cửa hàng thật của bạn không? Điều gì khiến bạn ngần ngại?"),
         ("Tin cậy", "Điều gì làm bạn tin hoặc không tin trang này?"),
         ("Kết", "Nếu được thay đổi MỘT điều để trang dễ dùng hơn, đó là điều gì?"),
         ("Kết", "Bạn muốn nói thêm gì không?")]
HYP = ["T1: tin con số doanh thu dù nó gấp đôi tổng các đơn Đã giao (BUG-08)",
       "T2: không chắc đã thêm được vì không có thông báo thành công (BUG-09)",
       "T2: bấm nút nhiều lần vì không thấy phản hồi (BUG-12)",
       "T3: lo lắng hoặc thao tác nhầm khi bấm Xác nhận/Hủy không có xác nhận (BUG-04)",
       "T3: hiểu sai nhãn trạng thái hoặc tên nút (BUG-22)",
       "T4: mất thời gian tìm người dùng vì không có cột Tên/ô tìm kiếm (BUG-23)",
       "Cả luồng: F5 làm lạc hướng vì quay về Dashboard (BUG-14)"]

# --- bố cục sheet cá nhân (hằng số dùng cho công thức ở sheet Tổng hợp)
R_TASK0, R_SUS0, R_SUS_TOTAL, R_PROBE0, R_OBS0, R_OBS_N, R_HYP0 = 15, 22, 32, 36, 55, 30, 88


def hdr(ws, row, values, fill=NAVY, font=WHITE_B):
    for i, v in enumerate(values, 1):
        c = ws.cell(row, i, v)
        c.fill, c.font, c.border = fill, font, BOX
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")


def section(ws, row, text, ncols=8):
    for c in range(1, ncols + 1):
        ws.cell(row, c).fill = SEC
    ws.cell(row, 1, text).font = Font(bold=True, size=12)


def fill_in(ws, rng):
    for row in ws[rng]:
        for c in row:
            c.fill, c.border, c.alignment = INPUT, BOX, WRAP


wb = Workbook()
# ============================================================ Hướng dẫn phiên
g = wb.active
g.title = "Hướng dẫn phiên"
g.column_dimensions["A"].width = 6
g.column_dimensions["B"].width = 110
rows = [
    ("TITLE", "HƯỚNG DẪN PHIÊN USABILITY – dùng chung cho pilot (P00) và 7 phiên chính (P01 đến P07)"),
    ("SEC", "A. TRƯỚC PHIÊN (khoảng 15 phút)"),
    ("☐", "Backend và Admin đang chạy (node backend/server.js, npm run dev trong frontend-admin)."),
    ("☐", "Khởi động lại backend (seed sạch), rồi chạy: python hw03/scripts/usability_seed.py"),
    ("☐", "Mở Chrome, đăng nhập Admin sẵn, để ở Dashboard. Participant KHÔNG đăng nhập (sai mật khẩu 2 lần là khóa 3 phút)."),
    ("☐", "Bật quay màn hình nếu participant đồng ý (Win+G). Phiên remote: thử trước chia sẻ màn hình/điều khiển từ xa."),
    ("☐", "Mở sheet của participant (P00..P07) để ghi; chuẩn bị đồng hồ bấm giờ."),
    ("SEC", "B. LỜI GIỚI THIỆU (đọc gần nguyên văn)"),
    ("", "\"Cảm ơn bạn. Hôm nay tôi muốn thử một trang quản trị cửa hàng online. Tôi đang kiểm thử trang web, KHÔNG phải kiểm thử bạn; nếu thấy khó thì đó là lỗi của trang. "
         "Khi làm, bạn hãy nói to điều bạn đang nghĩ: đang nhìn gì, định làm gì, thấy khó hiểu ở đâu. Tôi sẽ ngồi quan sát và ít nói. "
         "Tôi xin phép quay màn hình (và tiếng nói nếu bạn đồng ý), không công khai. Bạn có thể dừng bất cứ lúc nào. Bạn đồng ý chứ?\""),
    ("", "Kịch bản: \"Bạn là chủ một cửa hàng online nhỏ bán đồ điện tử. Sáng nay bạn mở trang quản trị của cửa hàng để làm vài việc.\""),
    ("SEC", "C. BỐN NHIỆM VỤ (đưa từng cái một; sau mỗi cái hỏi SEQ 1-7)"),
    ("T1", "\"Bạn muốn biết cửa hàng đang kinh doanh ra sao. Hãy cho tôi biết tổng doanh thu và tổng số đơn hàng.\"  (thành công: đọc đúng 2 số hiển thị; chuẩn 1 phút)"),
    ("T2", "\"Bạn vừa nhập một nhóm hàng mới là Màn hình. Hãy thêm nhóm hàng này vào cửa hàng.\"  (thành công: dòng 'Màn hình' xuất hiện; chuẩn 1 phút)"),
    ("T3", "\"Một khách vừa đặt đơn 150.000 ₫. Hãy tìm đơn đó, cho tôi biết nó đang ở trạng thái nào, rồi xác nhận đơn.\"  (thành công: đơn thành 'Đã xác nhận'; chuẩn 2 phút)"),
    ("T4", "\"Bạn muốn biết khách hàng có email vana@example.com đã đăng ký tài khoản chưa. Hãy kiểm tra.\"  (thành công: nói đúng 'đã có'; chuẩn 1,5 phút)"),
    ("SEC", "D. QUY TẮC CAN THIỆP (chỉ khi bí hoàn toàn quá 2 phút; ghi cấp vào cột 'Cấp gợi ý')"),
    ("1", "\"Bạn đang nghĩ gì ở bước này?\" (hỏi lại, không gợi ý)"),
    ("2", "\"Bạn thử nhìn kỹ lại màn hình xem?\""),
    ("3", "\"Bạn nghĩ chức năng này nằm ở khu vực nào của trang?\""),
    ("4", "Chỉ vào khu vực chung (ví dụ 'ở menu bên trái'), không chỉ nút cụ thể."),
    ("5", "Cho bước tiếp theo (nhiệm vụ tính là Không hoàn thành), rồi chuyển nhiệm vụ sau."),
    ("", "KHÔNG: nói đúng/sai, khen, giải thích giao diện, nhắc tên nút, biện hộ cho trang."),
    ("SEC", "E. KẾT QUẢ NHIỆM VỤ: H = hoàn thành không trợ giúp; HTG = hoàn thành có trợ giúp; K = không hoàn thành"),
    ("SEC", "F. CUỐI PHIÊN"),
    ("☐", "Đưa bảng SUS (10 câu, 1-5) để participant tự khoanh; nhập 10 điểm vào sheet của họ."),
    ("☐", "Hỏi 16 câu probe (trong sheet của participant), hỏi sâu vào chỗ họ vướng."),
    ("☐", "Hỏi lại họ có đồng ý để TA liên hệ xác minh không (có thể bị gọi ngẫu nhiên 2 người)."),
    ("☐", "Lưu video (đặt tên P0x_ngày), ghi ngay nhận xét tổng quát, git commit cho phiên này."),
    ("SEC", "G. LƯU Ý"),
    ("", "Pilot P00 dùng để sửa bài test; KHÔNG tính vào Tổng hợp. Sau pilot nếu sửa kịch bản thì dùng bản mới cho cả 7 phiên chính và không sửa giữa chừng."),
    ("", "Mỗi phiên phải seed lại dữ liệu vì người trước đã thêm nhóm hàng và xác nhận đơn."),
    ("", "Ô nền vàng nhạt = chỗ cần điền. Sheet 'Tổng hợp' tự tính từ P01..P07."),
]
r = 1
for tag, text in rows:
    if tag == "TITLE":
        g.cell(r, 1, text).font = Font(bold=True, size=14)
    elif tag == "SEC":
        for c in (1, 2):
            g.cell(r, c).fill = SEC
        g.cell(r, 1, text).font = Font(bold=True)
    else:
        g.cell(r, 1, tag).alignment = Alignment(horizontal="center", vertical="top")
        c = g.cell(r, 2, text)
        c.alignment = WRAP
    r += 1

# ============================================================ sheet cá nhân
dv_res = DataValidation(type="list", formula1='"H,HTG,K"', allow_blank=True, showErrorMessage=True, error="Chọn H, HTG hoặc K")
dv_seq = DataValidation(type="whole", operator="between", formula1="1", formula2="7", allow_blank=True, showErrorMessage=True, error="SEQ từ 1 đến 7")
dv_sus = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True, showErrorMessage=True, error="Nhập số nguyên từ 1 đến 5")
dv_lvl = DataValidation(type="whole", operator="between", formula1="0", formula2="5", allow_blank=True, showErrorMessage=True, error="Cấp gợi ý từ 0 đến 5")
dv_yn = DataValidation(type="list", formula1='"Có,Không"', allow_blank=True)
dv_form = DataValidation(type="list", formula1='"In-person,Remote"', allow_blank=True)
dv_type = DataValidation(type="list", formula1='"điểm vướng,lỗi,do dự,lời bực,điều tốt"', allow_blank=True)
dv_sev = DataValidation(type="whole", operator="between", formula1="1", formula2="4", allow_blank=True, showErrorMessage=True, error="Mức 1 đến 4")
dv_tsk = DataValidation(type="list", formula1='"T1,T2,T3,T4,Cả luồng"', allow_blank=True)

for p in PARTS:
    s = wb.create_sheet(p)
    for col, w in zip("ABCDEFGH", [34, 26, 18, 14, 14, 14, 12, 50]):
        s.column_dimensions[col].width = w
    s["A1"] = f"PHIÊN {p}" + ("  (PILOT – không tính vào Tổng hợp)" if p == "P00" else "")
    s["A1"].font = Font(bold=True, size=14)
    section(s, 2, "THÔNG TIN PHIÊN")
    info = [("Mã participant", p), ("Ngày (dd/mm/2026)", None), ("Giờ", None), ("Hình thức", FORMAT[p]), ("Người điều phối", None),
            ("Tên file video (nếu có)", None), ("Đồng ý quay hình/ghi âm", None), ("Kinh nghiệm bán hàng/quản trị online", None), ("Mức dùng máy tính (thấp/vừa/cao)", None)]
    for i, (k, v) in enumerate(info, 3):
        s.cell(i, 1, k).font = Font(bold=True)
        s.cell(i, 2, v)
    fill_in(s, "B4:B11")
    s["B3"].font = Font(bold=True)
    dv_form.add("B6")
    dv_yn.add("B9")

    section(s, 13, "NHIỆM VỤ")
    hdr(s, 14, ["Nhiệm vụ", "Thời gian (giây)", "Kết quả (H/HTG/K)", "Số lỗi", "Số lần trợ giúp", "Cấp gợi ý cao nhất (0-5)", "SEQ (1-7)", "Ghi chú vướng mắc"])
    for i, (t, txt) in enumerate(TASKS):
        rr = R_TASK0 + i
        s.cell(rr, 1, f"{t}: {txt}").alignment = WRAP
        s.row_dimensions[rr].height = 32
    fill_in(s, f"B{R_TASK0}:H{R_TASK0 + 3}")
    dv_res.add(f"C{R_TASK0}:C{R_TASK0 + 3}")
    dv_lvl.add(f"F{R_TASK0}:F{R_TASK0 + 3}")
    dv_seq.add(f"G{R_TASK0}:G{R_TASK0 + 3}")

    section(s, 20, "SUS (điểm gốc 1 đến 5; điểm tự tính)")
    hdr(s, 21, ["Câu", "Điểm gốc (1-5)", "Đóng góp (tự tính)"])
    for i, q in enumerate(SUS_Q):
        rr = R_SUS0 + i
        s.cell(rr, 1, f"{i + 1}. {q}").alignment = WRAP
        s.row_dimensions[rr].height = 30
        s.cell(rr, 3, f'=IF(B{rr}="","",B{rr}-1)' if i % 2 == 0 else f'=IF(B{rr}="","",5-B{rr})').border = BOX
    fill_in(s, f"B{R_SUS0}:B{R_SUS0 + 9}")
    dv_sus.add(f"B{R_SUS0}:B{R_SUS0 + 9}")
    s.cell(R_SUS_TOTAL, 1, "ĐIỂM SUS (0-100)").font = Font(bold=True)
    c = s.cell(R_SUS_TOTAL, 2, f'=IF(COUNT(B{R_SUS0}:B{R_SUS0 + 9})=10,SUM(C{R_SUS0}:C{R_SUS0 + 9})*2.5,"")')
    c.font, c.border = Font(bold=True, size=12), BOX

    section(s, 34, "CÂU HỎI PROBE (ghi tóm tắt, câu quan trọng ghi nguyên văn)")
    hdr(s, 35, ["Chủ đề", "Câu hỏi", "", "", "Trả lời"])
    for i, (topic, q) in enumerate(PROBE):
        rr = R_PROBE0 + i
        s.cell(rr, 1, topic).alignment = WRAP
        s.cell(rr, 2, q).alignment = WRAP
        s.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=4)
        s.merge_cells(start_row=rr, start_column=5, end_row=rr, end_column=8)
        s.row_dimensions[rr].height = 34
    fill_in(s, f"E{R_PROBE0}:H{R_PROBE0 + 15}")

    section(s, 53, "NHẬT KÝ QUAN SÁT (mỗi dòng một sự kiện)")
    hdr(s, 54, ["Giờ video / giờ phiên", "Nhiệm vụ", "Loại", "Mức (1-4)", "", "", "", "Mô tả và câu nói nguyên văn"])
    fill_in(s, f"A{R_OBS0}:H{R_OBS0 + R_OBS_N - 1}")
    dv_tsk.add(f"B{R_OBS0}:B{R_OBS0 + R_OBS_N - 1}")
    dv_type.add(f"C{R_OBS0}:C{R_OBS0 + R_OBS_N - 1}")
    dv_sev.add(f"D{R_OBS0}:D{R_OBS0 + R_OBS_N - 1}")

    section(s, 86, "GIẢ THUYẾT (quan sát được trong phiên này?)")
    hdr(s, 87, ["Giả thuyết", "Có / Không", "", "", "", "", "", "Ghi chú"])
    for i, h in enumerate(HYP):
        rr = R_HYP0 + i
        s.cell(rr, 1, h).alignment = WRAP
        s.row_dimensions[rr].height = 30
    fill_in(s, f"B{R_HYP0}:B{R_HYP0 + 6}")
    fill_in(s, f"H{R_HYP0}:H{R_HYP0 + 6}")
    dv_yn.add(f"B{R_HYP0}:B{R_HYP0 + 6}")

    section(s, 96, "NHẬN XÉT TỔNG QUÁT CỦA NGƯỜI ĐIỀU PHỐI (vấn đề nổi bật, điều tốt, điều bất ngờ)")
    s.merge_cells("A97:H101")
    fill_in(s, "A97:H101")
    s.freeze_panes = "A3"
    for d in (dv_res, dv_seq, dv_sus, dv_lvl, dv_yn, dv_form, dv_type, dv_sev, dv_tsk):
        s.add_data_validation(d)
    # mỗi sheet cần đối tượng validation riêng cho openpyxl: tạo lại sau mỗi vòng
    dv_res = DataValidation(type="list", formula1='"H,HTG,K"', allow_blank=True, showErrorMessage=True, error="Chọn H, HTG hoặc K")
    dv_seq = DataValidation(type="whole", operator="between", formula1="1", formula2="7", allow_blank=True, showErrorMessage=True, error="SEQ từ 1 đến 7")
    dv_sus = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True, showErrorMessage=True, error="Nhập số nguyên từ 1 đến 5")
    dv_lvl = DataValidation(type="whole", operator="between", formula1="0", formula2="5", allow_blank=True, showErrorMessage=True, error="Cấp gợi ý từ 0 đến 5")
    dv_yn = DataValidation(type="list", formula1='"Có,Không"', allow_blank=True)
    dv_form = DataValidation(type="list", formula1='"In-person,Remote"', allow_blank=True)
    dv_type = DataValidation(type="list", formula1='"điểm vướng,lỗi,do dự,lời bực,điều tốt"', allow_blank=True)
    dv_sev = DataValidation(type="whole", operator="between", formula1="1", formula2="4", allow_blank=True, showErrorMessage=True, error="Mức 1 đến 4")
    dv_tsk = DataValidation(type="list", formula1='"T1,T2,T3,T4,Cả luồng"', allow_blank=True)

# ============================================================ Tổng hợp
t = wb.create_sheet("Tổng hợp", 1)
t["A1"] = "TỔNG HỢP USABILITY – tự tính từ sheet P01 đến P07 (pilot P00 không tính)"
t["A1"].font = Font(bold=True, size=14)
cols = ["Mã", "Điểm SUS"]
for tk, _ in TASKS:
    cols += [f"{tk} thời gian (s)", f"{tk} kết quả", f"{tk} số lỗi", f"{tk} trợ giúp", f"{tk} SEQ"]
hdr(t, 3, cols)
for i, p in enumerate(MAIN):
    rr = 4 + i
    t.cell(rr, 1, p)
    t.cell(rr, 2, f"=IF('{p}'!B{R_SUS_TOTAL}=\"\",\"\",'{p}'!B{R_SUS_TOTAL})")
    for k in range(4):
        src = R_TASK0 + k
        for j, colx in enumerate("BCDEG"):
            t.cell(rr, 3 + k * 5 + j, f"=IF('{p}'!{colx}{src}=\"\",\"\",'{p}'!{colx}{src})")
    for c in range(1, len(cols) + 1):
        t.cell(rr, c).border = BOX
first, last = 4, 10
section(t, 12, "THỐNG KÊ", len(cols))
lab = ["Số người đã có dữ liệu", "Trung bình", "Trung vị", "Độ lệch chuẩn", "Thấp nhất", "Cao nhất"]
rng = f"B{first}:B{last}"
fs = [f"=COUNT({rng})", f'=IF(COUNT({rng})=0,"",AVERAGE({rng}))', f'=IF(COUNT({rng})=0,"",MEDIAN({rng}))',
      f'=IF(COUNT({rng})<2,"",STDEV({rng}))', f'=IF(COUNT({rng})=0,"",MIN({rng}))', f'=IF(COUNT({rng})=0,"",MAX({rng}))']
t.cell(13, 1, "SUS").font = Font(bold=True)
for i, (l, f) in enumerate(zip(lab, fs)):
    t.cell(14 + i, 1, l)
    t.cell(14 + i, 2, f)
t.cell(20, 1, "Đánh giá so với mốc 68")
t.cell(20, 2, '=IF(B15="","",IF(B15>=80,"Rất tốt (>=80)",IF(B15>=68,"Tốt (68-80)",IF(B15>=51,"Dưới trung bình (51-68)","Kém (<51)"))))')
t.cell(22, 1, "NHIỆM VỤ").font = Font(bold=True)
tl = ["Thời gian trung bình (giây)", "Tỉ lệ hoàn thành không trợ giúp (H)", "Tỉ lệ hoàn thành kể cả có trợ giúp (H+HTG)", "Tổng số lỗi", "Tổng số lần trợ giúp", "SEQ trung bình (1-7)"]
for i, l in enumerate(tl):
    t.cell(23 + i, 1, l)
for k in range(4):
    c0 = 3 + k * 5
    L = lambda j: get_column_letter(c0 + j)
    tm, rs, er, hp, sq = (f"{L(j)}{first}:{L(j)}{last}" for j in range(5))
    t.cell(23, c0, f'=IF(COUNT({tm})=0,"",AVERAGE({tm}))')
    n = f'(COUNTIF({rs},"H")+COUNTIF({rs},"HTG")+COUNTIF({rs},"K"))'  # chỉ đếm ô đã có kết quả (COUNTA đếm cả "" của công thức)
    t.cell(24, c0, f'=IF({n}=0,"",COUNTIF({rs},"H")/{n})').number_format = "0%"
    t.cell(25, c0, f'=IF({n}=0,"",(COUNTIF({rs},"H")+COUNTIF({rs},"HTG"))/{n})').number_format = "0%"
    t.cell(26, c0, f'=IF(COUNT({er})=0,"",SUM({er}))')
    t.cell(27, c0, f'=IF(COUNT({hp})=0,"",SUM({hp}))')
    t.cell(28, c0, f'=IF(COUNT({sq})=0,"",AVERAGE({sq}))')
    t.cell(22, c0, TASKS[k][0]).font = Font(bold=True)
t.cell(30, 1, "GIẢ THUYẾT: số participant (trên 7) đã quan sát được").font = Font(bold=True)
for i, h in enumerate(HYP):
    rr = 31 + i
    t.cell(rr, 1, h).alignment = WRAP
    t.cell(rr, 2, "=" + "+".join(f"COUNTIF('{p}'!B{R_HYP0 + i},\"Có\")" for p in MAIN))
    t.row_dimensions[rr].height = 30
t.column_dimensions["A"].width = 48
for c in range(2, len(cols) + 1):
    t.column_dimensions[get_column_letter(c)].width = 12
t.freeze_panes = "B4"

# ============================================================ Phát hiện
f = wb.create_sheet("Phát hiện", 2)
f["A1"] = "PHÁT HIỆN VÀ XẾP MỨC ĐỘ (ưu tiên = mức nghiêm trọng x xác suất; xác suất = số người gặp / 7)"
f["A1"].font = Font(bold=True, size=13)
hdr(f, 3, ["#", "Phát hiện (mô tả ngắn)", "Nhiệm vụ", "Loại (đơn lẻ / hệ thống)", "Mức nghiêm trọng (1-4)", "Số người gặp (0-7)", "Xác suất", "Ưu tiên (4 x 1 = cao nhất)", "Bug Task 1 liên quan", "Khuyến nghị"])
for i in range(1, 31):
    rr = 3 + i
    f.cell(rr, 1, i)
    f.cell(rr, 7, f'=IF(F{rr}="","",F{rr}/7)').number_format = "0%"
    f.cell(rr, 8, f'=IF(OR(E{rr}="",F{rr}=""),"",E{rr}*F{rr}/7)').number_format = "0.00"
    for c in range(1, 11):
        f.cell(rr, c).border = BOX
        if c not in (1, 7, 8):
            f.cell(rr, c).fill, f.cell(rr, c).alignment = INPUT, WRAP
dv_a = DataValidation(type="whole", operator="between", formula1="1", formula2="4", allow_blank=True)
dv_b = DataValidation(type="whole", operator="between", formula1="0", formula2="7", allow_blank=True)
dv_c = DataValidation(type="list", formula1='"đơn lẻ,hệ thống"', allow_blank=True)
dv_d = DataValidation(type="list", formula1='"T1,T2,T3,T4,Cả luồng"', allow_blank=True)
for d, rg in ((dv_a, "E4:E33"), (dv_b, "F4:F33"), (dv_c, "D4:D33"), (dv_d, "C4:C33")):
    f.add_data_validation(d)
    d.add(rg)
for c, w in zip("ABCDEFGHIJ", [5, 50, 12, 18, 14, 14, 10, 16, 18, 45]):
    f.column_dimensions[c].width = w
f["A35"] = "Mức nghiêm trọng: 4 = Blocker (không hoàn thành); 3 = Major (hoàn thành nhưng mất nhiều thời gian/phải trợ giúp); 2 = Minor; 1 = Cosmetic."
f["A36"] = "Phân loại: 'đơn lẻ' = chỉ 1 người gặp, có thể do cá nhân; 'hệ thống' = nhiều người gặp cùng chỗ, là vấn đề thiết kế."
f.freeze_panes = "A4"

wb.save(OUT)
print("Đã tạo", OUT, "| sheet:", wb.sheetnames)
