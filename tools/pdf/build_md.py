import re, sys
from pathlib import Path
root = Path(sys.argv[1]); out = Path(sys.argv[2])
parts = sorted(p.name for p in root.glob("part*") if p.is_dir())
buf = []
title, sub, meta = (sys.argv[3:6] + [None]*3)[:3]
title = title or "СМОЛЕНСКАЯ ПЛОЩАДЬ"; sub = sub or "스몰렌스카야 광장"
meta = meta or "Сезон первый · 4 части · 48 эпизодов · 7 200 реплик"
buf.append(f'<div class="cover"><div class="cover-title">{title}</div>'
           f'<div class="cover-sub">{sub}</div>'
           f'<div class="cover-meta">{meta}</div>'
           '<div class="cover-meta2">기획서 + 대본 전편</div></div>\n')
plan = (root/"기획서.md").read_text(encoding="utf-8").splitlines()
plan = [l for l in plan[2:]]
buf.append('\n<div class="pb"></div>\n\n# 기획서 {.part}\n')
buf.append("\n".join(plan))
for p in parts:
    eps = sorted((root/p).glob("ep*.md"))
    first = eps[0].read_text(encoding="utf-8").splitlines()
    part_title = first[1].lstrip("# ").strip()
    buf.append(f'\n\n<div class="pb"></div>\n\n# {part_title} {{.part}}\n')
    for e in eps:
        lines = e.read_text(encoding="utf-8").splitlines()
        assert lines[0].startswith("# ") and lines[1].startswith("## ")
        body = lines[2:]
        body = [re.sub(r"^### ", "## ", l) for l in body]
        buf.append('\n\n<div class="pb"></div>\n\n' + "\n".join(body))
out.write_text("\n".join(buf)+"\n", encoding="utf-8")
