"""«Четвёртая власть»: 기획서 + 집필된 화를 하나의 Markdown으로 묶는다.
사용: python3 tools/pdf/build_vlast.py chetvyortaya_vlast out.md"""
import re, sys
from pathlib import Path

root = Path(sys.argv[1]); out = Path(sys.argv[2])
parts = ["part1_obrushenie", "part2_bely_khalat", "part3_tenevoy_flot", "part4_dvoynoe_naznachenie",
         "part5_krot", "part6_prachechnaya", "part7_zakaz", "part8_istochnik"]
eps_all = [e for p in parts if (root / p).exists() for e in sorted((root / p).glob("ep*.md"))]
buf = ['<div class="cover"><div class="cover-title">ЧЕТВЁРТАЯ ВЛАСТЬ</div>'
       '<div class="cover-sub">제4권력</div>'
       '<div class="cover-meta">8 частей · 120 эпизодов · 150 реплик в эпизоде</div>'
       f'<div class="cover-meta2">기획서 + 대본 (집필 {len(eps_all)}화 / 120화)</div></div>\n']
plan = (root / "기획서.md").read_text(encoding="utf-8").splitlines()[2:]
buf.append('\n<div class="pb"></div>\n\n# 기획서 {.part}\n')
buf.append("\n".join(plan))
for p in parts:
    eps = sorted((root / p).glob("ep*.md")) if (root / p).exists() else []
    if not eps:
        continue
    part_title = eps[0].read_text(encoding="utf-8").splitlines()[1].lstrip("# ").strip()
    buf.append(f'\n\n<div class="pb"></div>\n\n# {part_title} {{.part}}\n')
    for e in eps:
        lines = e.read_text(encoding="utf-8").splitlines()
        assert lines[0].startswith("# ") and lines[1].startswith("## ")
        body, in_comm = [], False
        for l in lines[2:]:
            if l.startswith("## Комментарий"):
                in_comm = True
                l = '<div class="pb"></div>\n\n### ' + l[3:] + " {.commentary}"
            elif l.startswith("### "):
                l = ("#### " if in_comm else "## ") + l[4:]
            body.append(l)
        buf.append('\n\n<div class="pb"></div>\n\n' + "\n".join(body))
out.write_text("\n".join(buf) + "\n", encoding="utf-8")
