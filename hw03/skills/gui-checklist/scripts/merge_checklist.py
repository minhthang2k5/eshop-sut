# -*- coding: utf-8 -*-
"""Gộp nhiều bảng checklist (Markdown) thành MỘT bảng nháp, đánh ID nháp D-001...

Mỗi bảng nguồn có 7 cột:  ID | IA | A | B | Mục kiểm tra | Kết quả mong đợi | Ưu tiên
  --order pc : A = nguyên tắc nguồn, B = thành phần        (prompt theo nguyên tắc)
  --order cb : A = control,          B = checklist nguồn   (prompt theo control / form)

Dùng:
  python merge_checklist.py --out DIR \
      --source "FILE::MÀN HÌNH::REGEX_ID::pc[::MARKER]" \
      --source "FILE::MÀN HÌNH::REGEX_ID::cb"
  MARKER (tùy chọn): chỉ đọc phần văn bản bắt đầu từ chuỗi này (ví dụ chọn "Lần 2" của một prompt).

Đầu ra trong DIR:  GUI_Checklist_draft.csv  và  GUI_Checklist_draft.md
Thứ tự: theo thứ tự màn hình khai báo, trong mỗi màn hình theo IA-01..IA-04.
Script chỉ đọc và gộp, không sửa nội dung mục nào.
"""
import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

HEADERS = ["ID", "Màn hình", "IA", "Control / Thành phần", "Mục kiểm tra", "Kết quả mong đợi", "Ưu tiên",
           "Nguồn mục", "Nguyên tắc / checklist nguồn", "Kết quả (Passed/Failed)", "Notes", "Screenshot"]


def read_rows(path: Path, id_re: str, marker):
    text = path.read_text(encoding="utf-8")
    if marker:
        text = text[text.index(marker):]
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and re.fullmatch(id_re, cells[0]):
            rows.append(cells)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="thư mục đầu ra")
    ap.add_argument("--source", action="append", required=True,
                    help='"FILE::MÀN HÌNH::REGEX_ID::pc|cb[::MARKER]"')
    ap.add_argument("--prefix", default="D", help="tiền tố ID nháp (mặc định D)")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    items, screens = [], []
    for spec in args.source:
        parts = spec.split("::")
        if len(parts) < 4:
            sys.exit(f"source sai định dạng: {spec}")
        file, screen, id_re, order = parts[:4]
        marker = parts[4] if len(parts) > 4 else None
        if order not in ("pc", "cb"):
            sys.exit(f"order phải là pc hoặc cb: {spec}")
        path = Path(file)
        got = read_rows(path, id_re, marker)
        if not got:
            sys.exit(f"Không đọc được dòng nào từ {path} với regex {id_re}")
        if screen not in screens:
            screens.append(screen)
        for c in got:
            basis, control = (c[2], c[3]) if order == "pc" else (c[3], c[2])
            items.append(dict(screen=screen, ia=c[1], control=control, basis=basis, check=c[4],
                              expected=c[5], prio=c[6], origin=f"AI – {path.stem} – {c[0]}"))

    sorder = {s: i for i, s in enumerate(screens)}
    items = [it for _, it in sorted(enumerate(items), key=lambda t: (sorder[t[1]["screen"]], t[1]["ia"], t[0]))]
    for n, it in enumerate(items, 1):
        it["id"] = f"{args.prefix}-{n:03d}"

    def row(it):
        return [it["id"], it["screen"], it["ia"], it["control"], it["check"], it["expected"], it["prio"],
                it["origin"], it["basis"], "", "", ""]

    with open(out / "GUI_Checklist_draft.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        for it in items:
            w.writerow(row(it))

    esc = lambda s: str(s).replace("|", "\\|")
    md = ["# GUI Checklist – bản nháp từ AI", "",
          f"Tổng số mục: **{len(items)}**. Cột Kết quả, Notes, Screenshot để trống, điền ở bước thực thi.", "",
          "| " + " | ".join(HEADERS) + " |", "|" + "---|" * len(HEADERS)]
    for it in items:
        md.append("| " + " | ".join(esc(x) for x in row(it)) + " |")
    (out / "GUI_Checklist_draft.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("total", len(items))
    print("by screen", dict(Counter(i["screen"] for i in items)))
    print("by IA", dict(sorted(Counter(i["ia"] for i in items).items())))
    print("by prio", dict(Counter(i["prio"] for i in items)))
    vague = [i["id"] for i in items if re.search(r"hoặc|nếu |và/hoặc", i["expected"], re.I)]
    print("Kết quả mong đợi có 'hoặc/nếu' (cần xem lại khi review):", vague)


if __name__ == "__main__":
    main()
