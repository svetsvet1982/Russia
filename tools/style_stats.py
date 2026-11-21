#!/usr/bin/env python3
"""Статистика «рубленого» стиля реплик.
frag%  — доля предложений из 1–3 слов;
avg    — средняя длина предложения (слов);
chop%  — доля реплик, где ВСЕ предложения короче 5 слов (перечисление/рубленые фразы);
Пример: python3 tools/style_stats.py naruzhka/part1_*/ep*.md
С флагом --show N печатает N худших реплик файла."""
import re, sys
from pathlib import Path
TURN = re.compile(r"^\*\*(\d+)\. ([^*]+):\*\*(.*)")
W = re.compile(r"[А-Яа-яЁёA-Za-z0-9-]+")
def sents(t):
    t = re.sub(r"\*\([^)]*\)\*|\*\[[^\]]*\]\*", " ", t)
    parts = re.split(r"(?<=[.!?…])\s+|\s+—\s+(?=[А-ЯЁ])", t)
    return [len(W.findall(p)) for p in parts if W.findall(p)]
args = sys.argv[1:]; show = 0
if "--show" in args:
    i = args.index("--show"); show = int(args[i+1]); del args[i:i+2]
for f in args:
    allS, chop, n, bad = [], 0, 0, []
    for line in Path(f).read_text(encoding="utf-8").splitlines():
        m = TURN.match(line)
        if not m: continue
        s = sents(m.group(3)); n += 1; allS += s
        if s and max(s) < 5 and len(s) >= 2: chop += 1; bad.append(line[:160])
    fr = sum(1 for x in allS if x <= 3) * 100 // max(1, len(allS))
    avg = sum(allS) / max(1, len(allS))
    print(f"{Path(f).name}: frag {fr}% · avg {avg:.1f} · chop {chop*100//max(1,n)}% ({chop}/{n})")
    for b in bad[:show]: print("   ", b)
