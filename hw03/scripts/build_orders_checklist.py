# -*- coding: utf-8 -*-
"""Dựng checklist cuối cho màn hình Admin: Đơn hàng (chạy skill gui-checklist, bước 6-8).

Chạy:  python hw03/scripts/build_orders_checklist.py   (từ thư mục eshop-sut)
Đầu vào:  hw03/checklist/orders/GUI_Checklist_draft.csv   (34 mục nháp DO-001..DO-034)
Đầu ra (hw03/checklist/orders/):
  GUI_Checklist_final_orders.csv / .md
  AI_Review_Decisions_orders.md
  Added_Items_orders.md
ID cuối dạng ORD-001 để không trùng ID GUI-xxx của checklist chính (Người dùng, Danh mục...).
"""
import csv
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CK = BASE / "checklist" / "orders"
DRAFT = CK / "GUI_Checklist_draft.csv"
SCREEN = "Admin: Đơn hàng"

PROMPT = "Chất lượng prompt"
MODEL = "Giới hạn của model"
SCR = "Đặc thù giao diện"

# Quyết định review (theo gợi ý đã trao đổi). a: Giữ | Sửa | Gộp | Gộp vào | Bỏ
DEC = {
 "DO-001": dict(a="Giữ", r="Đo được, Pass/Fail rõ."),
 "DO-002": dict(a="Giữ", r="Rõ ràng. Lưu ý: trùng ý với mục GUI-070 của checklist chính; khi gộp hai checklist chỉ giữ một mục."),
 "DO-003": dict(a="Giữ", r="Đo được bằng công cụ, có ngưỡng 4.5:1."),
 "DO-004": dict(a="Giữ", r="Đo được bằng công cụ, có ngưỡng 4.5:1."),
 "DO-005": dict(a="Giữ", r="Đo được bằng DevTools."),
 "DO-006": dict(a="Bỏ", r="Chủ quan: đặc tả không quy định màu nút Hủy; 'nút hủy phải đỏ' chỉ là quy ước chung nên không có tiêu chí Pass/Fail khách quan."),
 "DO-007": dict(a="Giữ", r="Quan sát trực tiếp, Pass/Fail rõ."),
 "DO-008": dict(a="Giữ", r="Có cách tạo dữ liệu (POST /api/checkout), tiêu chí rõ."),
 "DO-009": dict(a="Sửa", r="Mục đòi hỏi tính năng mà đặc tả FR-18 không nêu; bỏ nhánh 'ghi nhận thiếu nếu không có' và gắn rõ là yêu cầu bổ sung để có một tiêu chí.",
                set=dict(check="Đối chiếu các cột hiển thị với nhu cầu phân biệt đơn mới và đơn cũ (yêu cầu bổ sung, đặc tả FR-18 không nêu cột thời gian)",
                         expected="Bảng có cột thời gian đặt hàng")),
 "DO-010": dict(a="Giữ", r="Rõ ràng."),
 "DO-011": dict(a="Giữ", r="Đối chiếu được với API."),
 "DO-012": dict(a="Giữ", r="Có căn cứ trong đặc tả FR-18 (địa chỉ hiển thị an toàn, không render HTML)."),
 "DO-013": dict(a="Giữ", r="Cần tạo 30 đơn bằng API (làm được); tiêu chí rõ."),
 "DO-014": dict(a="Bỏ", r="Yếu: đặc tả không quy định hành vi nhấp đúp; kết quả 'không có thay đổi bất ngờ' không có ngưỡng Pass/Fail."),
 "DO-015": dict(a="Bỏ", r="Yếu: hiệu ứng hover dòng không thuộc đặc tả và giá trị thấp."),
 "DO-016": dict(a="Giữ", r="Rõ ràng; dùng đơn thử nên an toàn."),
 "DO-017": dict(a="Bỏ", r="Yếu: hiệu ứng hover nút không có tiêu chí khách quan, giá trị thấp so với các mục khác."),
 "DO-018": dict(a="Giữ", r="Đo được bằng DevTools > Accessibility."),
 "DO-019": dict(a="Giữ", r="Đo được, có ngưỡng 24×24 px (WCAG 2.5.8)."),
 "DO-020": dict(a="Giữ", r="Đo được, có ngưỡng khoảng cách."),
 "DO-021": dict(a="Giữ", r="Rõ ràng."),
 "DO-022": dict(a="Giữ", r="Rõ ràng."),
 "DO-023": dict(a="Giữ", r="Rõ ràng."),
 "DO-024": dict(a="Sửa", r="Mục đòi hỏi tính năng mà đặc tả không nêu; bỏ nhánh 'ghi nhận thiếu nếu không có' và gắn rõ là yêu cầu bổ sung.",
                set=dict(check="Tìm cách xem chi tiết một đơn (sản phẩm, số lượng) từ dòng đơn hàng (yêu cầu bổ sung, đặc tả FR-18 không nêu)",
                         expected="Có cách mở chi tiết đơn từ chính dòng đó (ví dụ nút \"Xem\")")),
 "DO-025": dict(a="Giữ", r="Rõ ràng."),
 "DO-026": dict(a="Giữ", r="Rõ ràng. Lưu ý: liên quan mục GUI-073 (xác nhận khi Hủy) của checklist chính nhưng khác nút; không gộp."),
 "DO-027": dict(a="Gộp", r="Gộp với DO-034: cả hai kiểm tra cột Hành động của từng trạng thái; mục 'Đã giao không còn nút' là một dòng của mục 'nút theo trạng thái'. Lưu ý: trùng ý với GUI-072 của checklist chính.",
                set=dict(control="Nút theo trạng thái", check="Với từng trạng thái (5 đơn thử), ghi các nút hành động hiển thị trong cột Hành động",
                         expected="Chờ xác nhận: Xác nhận, Hủy; Đã xác nhận: Giao hàng, Hủy; Đang giao: Hoàn thành; Đã giao và Đã hủy: không có nút chuyển trạng thái (trạng thái kết thúc theo FR-10)",
                         basis="Nielsen #5 Error prevention; Shneiderman #4; đặc tả FR-10")),
 "DO-028": dict(a="Giữ", r="Cách giả lập bằng DevTools, không mất dữ liệu."),
 "DO-029": dict(a="Giữ", r="Đo được số yêu cầu trong tab Network."),
 "DO-030": dict(a="Giữ", r="Khả thi bằng DevTools > Slow 3G."),
 "DO-031": dict(a="Giữ", r="Cách giả lập bằng DevTools, không mất dữ liệu."),
 "DO-032": dict(a="Giữ", r="Cần tài khoản khách đặt đơn mới; làm được."),
 "DO-033": dict(a="Giữ", r="Đối chiếu được hai con số."),
 "DO-034": dict(a="Gộp vào", into="DO-027", r="Trùng ý với DO-027."),
}

# Mục tự thêm (bước 7). obs=True: đã thấy hiện tượng khi chạy thật (10/11/2026).
NEW = [
 dict(ia="IA-01", control="Bố cục điện thoại", check="DevTools Device Toolbar 375×812, mở tab Đơn hàng, đo vùng nội dung và độ rộng bảng",
      expected="Bảng nằm gọn trong vùng nội dung, không phải cuộn ngang bên trong vùng nội dung",
      prio="Mandatory", basis="Nielsen #8; Responsive design",
      why=PROMPT, why_d="Prompt chỉ mô tả bảng ở độ rộng desktop. Chạy thật ở 375 px: menu trái chiếm 256 px nên vùng nội dung chỉ còn 119 px, bảng rộng 413 px và nội dung rộng 445 px nên phải cuộn ngang.", obs=True),
 dict(ia="IA-01", control="Nhãn nút ở độ rộng hẹp", check="Ở 375×812, đo chiều cao các nút hành động, đặc biệt nút \"Đánh dấu Đã giao\"",
      expected="Nhãn mỗi nút không xuống quá 2 dòng và mọi nút cao tối thiểu 24 px",
      prio="Optional", basis="WCAG 2.5.8; Nielsen #8",
      why=MODEL, why_d="Chỉ lộ ra khi chạy thật: ở 375 px mọi nút chỉ rộng 47 px; nút \"Đánh dấu Đã giao\" bị bẻ thành nhiều dòng cao 72 px, nút \"Hủy\" cao 24 px.", obs=True),
 dict(ia="IA-04", control="Tên nút so với trạng thái đích", check="Bấm \"Hoàn thành\" ở một đơn Đang giao (đơn thử), đọc nhãn trạng thái mới",
      expected="Từ trên nút khớp với từ trên nhãn trạng thái đích",
      prio="Optional", basis="Norman Mapping; Nielsen #2 Match between system and real world",
      why=MODEL, why_d="Mô tả liệt kê tên nút và tên trạng thái rời nhau nên AI không nối được nút nào dẫn tới trạng thái nào; nút \"Hoàn thành\" đưa đơn sang \"Đã giao\" (theo đặc tả FR-10). Cần bấm để xác nhận.", obs=False),
 dict(ia="IA-01", control="Phân biệt người đặt", check="Tạo thêm một tài khoản khách cũng tên \"Test User\" (POST /api/register), đặt một đơn, xem cột Người đặt",
      expected="Hai đơn của hai khách khác nhau phân biệt được (cột hiển thị thêm email của người đặt)",
      prio="Optional", basis="Nielsen #6 Recognition rather than recall",
      why=SCR, why_d="Cột Người đặt chỉ hiển thị tên; với dữ liệu mẫu toàn \"Test User\" AI không thấy được rủi ro trùng tên. Cần tạo dữ liệu trùng để xác nhận.", obs=False),
 dict(ia="IA-01", control="Cột Tổng tiền", check="Tạo đơn có tổng tiền 9,999,999,999 bằng POST /api/checkout, quan sát cột Tổng tiền",
      expected="Số hiển thị đầy đủ có dấu phân cách hàng nghìn, không tràn và không đè cột bên cạnh",
      prio="Optional", basis="Nielsen #8; Domain boundary",
      why=PROMPT, why_d="Prompt chỉ yêu cầu thử địa chỉ dài, không yêu cầu thử số tiền rất lớn.", obs=False),
 dict(ia="IA-03", control="Focus sau khi đổi trạng thái", check="Dùng Tab focus nút \"Xác nhận\" của đơn thử, nhấn Enter, rồi kiểm tra phần tử đang focus (document.activeElement)",
      expected="Focus nằm ở một phần tử trong bảng, không rơi về thẻ body",
      prio="Optional", basis="WCAG 2.4.3 Focus Order; Nielsen #7",
      why=MODEL, why_d="Chỉ lộ ra khi thao tác bằng bàn phím trên giao diện thật: nút bị thay bằng nút khác sau khi đổi trạng thái nên focus có thể mất.", obs=False),
]


def main():
    draft = list(csv.reader(open(DRAFT, encoding="utf-8-sig")))[1:]
    rows = [dict(did=r[0], ia=r[2], control=r[3], check=r[4], expected=r[5], prio=r[6], origin=r[7], basis=r[8]) for r in draft]
    assert len(rows) == 34 and set(DEC) == {r["did"] for r in rows}, len(rows)

    items = []
    for r in rows:
        dec = DEC[r["did"]]
        a = dec["a"]
        if a in ("Bỏ", "Gộp vào"):
            continue
        it = {**r, **dec.get("set", {})}
        sub = r["origin"].replace("AI – ", "")
        if a == "Giữ":
            it["source"], it["ref"] = "AI", f"{r['did']} ({sub})"
        elif a == "Sửa":
            it["source"], it["ref"] = "AI (đã sửa)", f"{r['did']} ({sub})"
        else:  # Gộp
            other = [k for k, v in DEC.items() if v.get("into") == r["did"]][0]
            osub = [x for x in rows if x["did"] == other][0]["origin"].replace("AI – ", "")
            it["source"], it["ref"] = "AI (đã sửa – gộp)", f"{r['did']} ({sub}) + {other} ({osub})"
        items.append(it)
    for n in NEW:
        items.append(dict(n, did="—", ref="—", source="Tự thêm – quan sát thật" if n["obs"] else "Tự thêm",
                          why_full=f"{n['why']}: {n['why_d']}"))

    items = [it for _, it in sorted(enumerate(items), key=lambda t: (t[1]["ia"], t[0]))]
    for i, it in enumerate(items, 1):
        it["id"] = f"ORD-{i:03d}"

    H = ["ID", "Màn hình", "IA", "Control / Thành phần", "Mục kiểm tra", "Kết quả mong đợi", "Ưu tiên", "Nguồn mục",
         "ID nháp (truy vết)", "Nguyên tắc / checklist nguồn", "Vì sao AI bỏ sót", "Kết quả (Passed/Failed)", "Notes", "Screenshot"]
    row = lambda it: [it["id"], SCREEN, it["ia"], it["control"], it["check"], it["expected"], it["prio"], it["source"],
                      it["ref"], it["basis"], it.get("why_full", ""), "", "", ""]
    with open(CK / "GUI_Checklist_final_orders.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(H); [w.writerow(row(it)) for it in items]

    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    n_ai = sum(1 for it in items if it["source"].startswith("AI")); n_new = len(items) - n_ai
    by_ia = Counter(it["ia"] for it in items)
    md = ["# GUI Checklist – Admin: Đơn hàng (bản cuối sau review)", "",
          f"Tổng số mục: **{len(items)}** (từ AI: {n_ai}; tự thêm: {n_new}). Theo IA: " + ", ".join(f"{k}: {by_ia[k]}" for k in sorted(by_ia)) + ".",
          "Cột Kết quả, Notes, Screenshot để trống, điền khi thực thi. Chi tiết review: [AI_Review_Decisions_orders.md](AI_Review_Decisions_orders.md); "
          "mục bổ sung: [Added_Items_orders.md](Added_Items_orders.md).", "",
          "| " + " | ".join(H) + " |", "|" + "---|" * len(H)]
    md += ["| " + " | ".join(esc(c) for c in row(it)) + " |" for it in items]
    (CK / "GUI_Checklist_final_orders.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    new_id = {}
    for it in items:
        for ref in it["ref"].split(" + "):
            d = ref.split(" ")[0]
            if d.startswith("DO-"):
                new_id.setdefault(d, []).append(it["id"])
    cnt = Counter(DEC[r["did"]]["a"] for r in rows)
    rv = ["# Review 34 mục AI sinh – Admin: Đơn hàng", "",
          "Thống kê: " + ", ".join(f"{k}: {cnt[k]}" for k in ["Giữ", "Sửa", "Gộp", "Gộp vào", "Bỏ"]) + ".  ",
          f"34 mục nháp → {n_ai} mục AI trong checklist cuối ({cnt['Bỏ']} bỏ, {cnt['Gộp vào']} gộp vào mục khác).", "",
          "| ID nháp | Nguồn AI | Mục (tóm tắt) | Quyết định | Lý do | ID mới |", "|---|---|---|---|---|---|"]
    for r in rows:
        d = DEC[r["did"]]
        a = d["a"] + (f" {d['into']}" if d.get("into") else "")
        rv.append(f"| {r['did']} | {esc(r['origin'].replace('AI – ', ''))} | {esc(r['control'])}: {esc(r['check'][:70])}{'…' if len(r['check']) > 70 else ''} | {a} | {esc(d['r'])} | {', '.join(new_id.get(r['did'], ['—']))} |")
    (CK / "AI_Review_Decisions_orders.md").write_text("\n".join(rv) + "\n", encoding="utf-8")

    added = [it for it in items if it["source"].startswith("Tự thêm")]
    wc = Counter(it["why"] for it in added)
    ad = ["# Mục bổ sung và lý do AI bỏ sót – Admin: Đơn hàng", "",
          f"Tổng {len(added)} mục tự thêm; " + ", ".join(f"{k}: {wc[k]}" for k in [PROMPT, MODEL, SCR])
          + f". {sum(1 for it in added if it['obs'])} mục đã thấy hiện tượng khi chạy thật (10/11/2026); các mục còn lại cần xác nhận khi thực thi.", "",
          "| ID | IA | Mục bổ sung | Nguyên nhân AI bỏ sót | Giải thích | Quan sát thật |", "|---|---|---|---|---|---|"]
    ad += [f"| {it['id']} | {it['ia']} | {esc(it['control'])} | {it['why']} | {esc(it['why_d'])} | {'Có' if it['obs'] else '—'} |" for it in added]
    (CK / "Added_Items_orders.md").write_text("\n".join(ad) + "\n", encoding="utf-8")

    print(f"Final: {len(items)} mục (AI {n_ai}, tự thêm {n_new}); theo IA {dict(by_ia)}")
    print("Quyết định:", dict(cnt), "| Lý do bỏ sót:", dict(wc))


if __name__ == "__main__":
    main()
