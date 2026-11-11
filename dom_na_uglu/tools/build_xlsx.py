#!/usr/bin/env python3
"""plan_data.py → 기획서 .xlsx 와 .md 생성.

사용법: python3 build_xlsx.py <출력 디렉터리>
"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan_data as D  # noqa: E402

TURNS = 120
N = len(D.EPISODES)
LAST = N + 1  # 마지막 데이터 행(화별 개요)
EP = "'화별 개요'"

THIN = Side(style="thin", color="FFBFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD_FILL = PatternFill("solid", fgColor="FF1F3864")
HEAD_FONT = Font(bold=True, size=10, color="FFFFFFFF")
BODY_FONT = Font(size=10)
INPUT_FONT = Font(size=10, color="FF0000FF")


def head(ws, row, values):
    for c, v in enumerate(values, 1):
        cell = ws.cell(row, c, v)
        cell.font, cell.fill, cell.border = HEAD_FONT, HEAD_FILL, BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center")


def body(ws, row, values, fill=None, wrap=True, fonts=None):
    for c, v in enumerate(values, 1):
        cell = ws.cell(row, c, v)
        cell.font = (fonts or {}).get(c, BODY_FONT)
        cell.border = BORDER
        cell.alignment = Alignment(wrap_text=wrap, vertical="top")
        if fill:
            cell.fill = PatternFill("solid", fgColor=fill)


def widths(ws, ws_widths):
    for col, w in ws_widths.items():
        ws.column_dimensions[col].width = w


def part_of(i):
    return i // 18


def build(out: Path):
    wb = Workbook()

    # 개요
    ws = wb.active
    ws.title = "개요"
    ws["A1"] = D.TITLE
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = D.SUBTITLE
    ws["A2"].font = Font(size=10)
    head(ws, 4, ["항목", "내용"])
    r = 5
    for k, v in D.OVERVIEW:
        body(ws, r, [k, v])
        r += 1
    r += 1
    ws.cell(r, 1, "집계 (\"화별 개요\" 시트에서 자동 계산)").font = Font(bold=True, size=10)
    r += 1
    first = r
    rows = [
        ("총 화수", f"=COUNTA({EP}!B2:B{LAST})"),
        ("화당 턴 수", TURNS),
        ("총 턴 수", f"=SUM({EP}!G2:G{LAST})"),
        ("부 수", len(D.PARTS)),
        ("부당 화수", f"=B{first}/B{first + 3}"),
    ]
    for k, v in rows:
        body(ws, r, [k, v], wrap=False, fonts={2: INPUT_FONT} if k == "화당 턴 수" else None)
        r += 1
    ws.cell(r, 1, "※ 화당 턴 수(파란색)는 기준값입니다. 총 턴 수는 화별 개요 시트 G열(턴 수)의 합계로 갱신됩니다.").font = Font(size=9, italic=True)
    ws.freeze_panes = "A5"
    widths(ws, {"A": 18, "B": 110})

    # 진행 현황
    ws = wb.create_sheet("진행 현황")
    head(ws, 1, ["부", "전체 화수", "작성 완료(초고+검수)", "진행률", "총 턴 수"])
    rng = lambda col: f"{EP}!{col}2:{col}{LAST}"  # noqa: E731
    for i, p in enumerate(D.PARTS):
        rr = i + 2
        body(ws, rr, [
            p,
            f"=COUNTIF({rng('C')},A{rr})",
            f"=COUNTIFS({rng('C')},A{rr},{rng('H')},\"초고완료\")+COUNTIFS({rng('C')},A{rr},{rng('H')},\"검수완료\")",
            f"=IF(B{rr}=0,0,C{rr}/B{rr})",
            f"=SUMIFS({rng('G')},{rng('C')},A{rr})",
        ], wrap=False)
        ws.cell(rr, 1).fill = PatternFill("solid", fgColor=D.PART_FILLS[i])
        ws.cell(rr, 4).number_format = "0%"
    tr = len(D.PARTS) + 2
    body(ws, tr, ["합계", f"=SUM(B2:B{tr-1})", f"=SUM(C2:C{tr-1})", f"=IF(B{tr}=0,0,C{tr}/B{tr})", f"=SUM(E2:E{tr-1})"], wrap=False)
    for c in range(1, 6):
        ws.cell(tr, c).font = Font(bold=True, size=10)
    ws.cell(tr, 4).number_format = "0%"
    ws.cell(tr + 1, 1, D.STATUS_NOTE).font = Font(size=9, italic=True)
    widths(ws, {"A": 34, "B": 12, "C": 20, "D": 10, "E": 12})

    # 등장인물
    ws = wb.create_sheet("등장인물")
    head(ws, 1, ["이름", "설정", "맡는 소재", "원안 대응"])
    for i, row in enumerate(D.CHARACTERS, 2):
        body(ws, i, list(row))
    ws.freeze_panes = "A2"
    widths(ws, {"A": 34, "B": 70, "C": 40, "D": 16})

    # 난이도 설계
    ws = wb.create_sheet("난이도 설계")
    head(ws, 1, ["부", "시기", "상황", "주 난이도", "A2", "B1", "B2", "C1", "합계", "ТРКИ 대응"])
    for i, (p, s, sit, lv, a2, b1, b2, c1, trki) in enumerate(D.DIFFICULTY, 2):
        body(ws, i, [p, s, sit, lv, a2, b1, b2, c1, f"=SUM(E{i}:H{i})", trki], wrap=False,
             fonts={c: INPUT_FONT for c in range(5, 9)})
        for c in range(5, 10):
            ws.cell(i, c).number_format = "0%"
    ws.cell(len(D.DIFFICULTY) + 3, 1, "참고: ТБУ≈A2, ТРКИ-1≈B1, ТРКИ-2≈B2, ТРКИ-3≈C1 (러시아어 능력 시험 단계)").font = Font(size=9, italic=True)
    ws.freeze_panes = "A2"
    widths(ws, {"A": 18, "B": 14, "C": 16, "D": 12, "I": 10, "J": 18})

    # 화별 개요
    ws = wb.create_sheet("화별 개요")
    head(ws, 1, ["화", "제목", "부", "난이도", "사건", "학습 포인트", "턴 수", "작성 상태", "연결 현안·문화", "시기"])
    for i, (title, event, learn, issue, when) in enumerate(D.EPISODES):
        p = part_of(i)
        rr = i + 2
        body(ws, rr, [i + 1, title, D.PARTS[p], D.LEVELS[p], event, learn, TURNS, D.EP_STATUS.get(i + 1, "미작성"), issue, when],
             fill=D.PART_FILLS[p])
        for c in (1, 4, 7, 8, 10):
            ws.cell(rr, c).alignment = Alignment(vertical="top", wrap_text=False)
    dv = DataValidation(type="list", formula1='"미작성,작성중,초고완료,검수완료"', allow_blank=False)
    dv.add(f"H2:H{LAST}")
    ws.add_data_validation(dv)
    ws.auto_filter.ref = f"A1:J{LAST}"
    ws.freeze_panes = "A2"
    widths(ws, {"A": 6, "B": 34, "C": 24, "D": 10, "E": 62, "F": 48, "G": 8, "H": 12, "I": 36, "J": 16})

    # 원안 대비 비틀기
    ws = wb.create_sheet("원안 대비 비틀기")
    head(ws, 1, ["항목", "원안 《Das Eckhaus》(베를린)", "모스크바판 《Дом на углу》", "이유"])
    for i, row in enumerate(D.TWISTS, 2):
        body(ws, i, list(row))
    ws.freeze_panes = "A2"
    widths(ws, {"A": 16, "B": 40, "C": 52, "D": 60})

    # 문체 원칙
    ws = wb.create_sheet("문체 원칙")
    head(ws, 1, ["항목", "원칙"])
    for i, row in enumerate(D.STYLE, 2):
        body(ws, i, list(row))
    ws.freeze_panes = "A2"
    widths(ws, {"A": 20, "B": 110})

    # 부별 어휘 영역
    ws = wb.create_sheet("부별 어휘 영역")
    head(ws, 1, ["부", "핵심 어휘 영역"])
    for i, row in enumerate(D.VOCAB, 2):
        body(ws, i, list(row))
    ws.freeze_panes = "A2"
    widths(ws, {"A": 14, "B": 110})

    # 소재별 배치
    ws = wb.create_sheet("소재별 배치")
    head(ws, 1, ["소재", "주요 화", "담당 인물"])
    for i, row in enumerate(D.TOPICS, 2):
        body(ws, i, list(row))
    ws.freeze_panes = "A2"
    widths(ws, {"A": 24, "B": 36, "C": 44})

    # 모스크바·러시아 현안
    ws = wb.create_sheet("모스크바·러시아 현안")
    head(ws, 1, ["현안", "2026년 기준 핵심 내용", "반영 화", "집필 시 확인"])
    for i, row in enumerate(D.ISSUES, 2):
        body(ws, i, list(row))
    ws.cell(len(D.ISSUES) + 3, 1, "※ 수치·시행 시점은 기획 시점(2026년 11월) 기준 정리이며, 각 화 집필 직전 공식 출처로 재확인할 것.").font = Font(size=9, italic=True)
    ws.freeze_panes = "A2"
    widths(ws, {"A": 26, "B": 84, "C": 20, "D": 26})

    out.mkdir(parents=True, exist_ok=True)
    xlsx = out / "Дом_на_углу_기획서.xlsx"
    wb.save(xlsx)
    return xlsx


def md_table(headers, rows):
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")  # noqa: E731
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(lines)


def build_md(out: Path):
    parts = [f"# {D.TITLE}", "", f"> {D.SUBTITLE}", "", "## 개요", "",
             md_table(["항목", "내용"], D.OVERVIEW), "",
             "## 원안 대비 비틀기", "", md_table(["항목", "원안(베를린)", "모스크바판", "이유"], D.TWISTS), "",
             "## 등장인물", "", md_table(["이름", "설정", "맡는 소재", "원안 대응"], D.CHARACTERS), "",
             "## 난이도 설계", "",
             md_table(["부", "시기", "상황", "주 난이도", "A2", "B1", "B2", "C1", "ТРКИ"],
                      [(p, s, si, lv, f"{a:.0%}", f"{b:.0%}", f"{c:.0%}", f"{d:.0%}", t)
                       for p, s, si, lv, a, b, c, d, t in D.DIFFICULTY]), ""]
    for p, name in enumerate(D.PARTS):
        parts += [f"## 화별 개요 — {name} ({D.LEVELS[p]})", ""]
        rows = [(i + 1, t, e, l, iss, w) for i, (t, e, l, iss, w) in enumerate(D.EPISODES) if part_of(i) == p]
        parts += [md_table(["화", "제목", "사건", "학습 포인트", "연결 현안·문화", "시기"], rows), ""]
    parts += ["## 문체 원칙", "", md_table(["항목", "원칙"], D.STYLE), "",
              "## 부별 어휘 영역", "", md_table(["부", "핵심 어휘 영역"], D.VOCAB), "",
              "## 소재별 배치", "", md_table(["소재", "주요 화", "담당 인물"], D.TOPICS), "",
              "## 모스크바·러시아 현안", "", md_table(["현안", "2026년 기준 핵심 내용", "반영 화", "집필 시 확인"], D.ISSUES), "",
              "> 수치·시행 시점은 기획 시점(2026년 11월) 기준이며, 각 화 집필 직전 공식 출처로 재확인할 것.", ""]
    md = out / "기획서.md"
    md.write_text("\n".join(parts), encoding="utf-8")
    return md


if __name__ == "__main__":
    assert N == 90, N
    o = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(build(o), build_md(o))
