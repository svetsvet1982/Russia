#!/usr/bin/env python3
"""대사 속 문구가 몇 번째 턴인지 찾는다. 사용법: turn_of.py 파일 "문구" ["문구" ...]"""
import re
import sys

LINE = re.compile(r"^\*\*([^*:]+):\*\*\s+(.*)")
path, *needles = sys.argv[1:]
text = open(path, encoding="utf-8").read().split("## 한글 해석")[0]
plain = lambda s: s.replace("́", "")  # noqa: E731
turns = [m.group(2) for m in map(LINE.match, text.splitlines()) if m]
for n in needles:
    hits = [i for i, t in enumerate(turns, 1) if plain(n) in plain(t)]
    print(f"{hits}  {n}")
