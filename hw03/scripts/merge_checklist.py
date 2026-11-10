import csv, re, sys
from pathlib import Path

base = Path(r"D:\HCMUS\Nam_4\Testing\Project\HW3\eshop-sut\hw03")
out_dir = base / "checklist"
out_dir.mkdir(exist_ok=True)

SCREEN_USERS = "Admin: Người dùng"
SCREEN_CATS = "Admin: Danh mục"

def rows(path, id_re, start_marker=None):
    text = path.read_text(encoding="utf-8")
    if start_marker:
        i = text.index(start_marker)
        text = text[i:]
    result = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(id_re, cells[0]) and len(cells) == 7:
            result.append(cells)
    return result

items = []
# Prompt 2 - Lan 2 (29 muc)
p2 = base / "prompts" / "02_heuristics_ia01_ia03_ia04_admin_users.md"
for c in rows(p2, r"AI-0[134]-\d\d", start_marker="Lần 2 (prompt đã chỉnh"):
    items.append(dict(screen=SCREEN_USERS, ia=c[1], control=c[3], src_basis=c[2], check=c[4], expected=c[5], prio=c[6], origin=f"Prompt 2 (Lần 2) – {c[0]}"))
# Prompt 3
p3 = base / "prompts" / "03_per_control_admin_users.md"
for c in rows(p3, r"C3-\d\d"):
    items.append(dict(screen=SCREEN_USERS, ia=c[1], control=c[2], src_basis=c[3], check=c[4], expected=c[5], prio=c[6], origin=f"Prompt 3 – {c[0]}"))
# Prompt 4
p4 = base / "prompts" / "04_form_validation_admin_categories.md"
for c in rows(p4, r"C4-\d\d"):
    items.append(dict(screen=SCREEN_CATS, ia=c[1], control=c[2], src_basis=c[3], check=c[4], expected=c[5], prio=c[6], origin=f"Prompt 4 – {c[0]}"))

screen_order = {SCREEN_USERS: 0, SCREEN_CATS: 1}
items_sorted = sorted(enumerate(items), key=lambda t: (screen_order[t[1]["screen"]], t[1]["ia"], t[0]))
items = [it for _, it in items_sorted]

for n, it in enumerate(items, 1):
    it["id"] = f"D-{n:03d}"

headers = ["ID", "Màn hình", "IA", "Control / Thành phần", "Mục kiểm tra", "Kết quả mong đợi", "Ưu tiên",
           "Nguồn mục", "Nguyên tắc / checklist nguồn", "Kết quả (Passed/Failed)", "Notes", "Screenshot"]

with open(out_dir / "GUI_Checklist_draft.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(headers)
    for it in items:
        w.writerow([it["id"], it["screen"], it["ia"], it["control"], it["check"], it["expected"], it["prio"],
                    "AI – " + it["origin"], it["src_basis"], "", "", ""])

def esc(s): return s.replace("|", "\\|")
lines = ["# GUI Checklist – bản nháp từ AI (Prompt 2, 3, 4)", "",
         f"Tổng số mục: **{len(items)}**. Cột Kết quả, Notes, Screenshot để trống, điền ở bước thực thi.", "",
         "| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
for it in items:
    lines.append("| " + " | ".join(esc(x) for x in [it["id"], it["screen"], it["ia"], it["control"], it["check"], it["expected"], it["prio"],
                 "AI – " + it["origin"], it["src_basis"], "", "", ""]) + " |")
(out_dir / "GUI_Checklist_draft.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

from collections import Counter
print("total", len(items))
print("by screen", Counter(i["screen"] for i in items))
print("by IA", Counter(i["ia"] for i in items))
print("by screen+IA", sorted(Counter((i["screen"], i["ia"]) for i in items).items()))
print("by prio", Counter(i["prio"] for i in items))
print("by origin prompt", Counter(i["origin"].split(" – ")[0] for i in items))
