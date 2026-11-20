#!/usr/bin/env python3
"""Считает слова реплик (без ремарок в скобках/курсиве) в эпизодах.
Пример: python3 tools/count_words.py naruzhka/part1_*/ep*.md"""
import re, sys
from pathlib import Path
TURN = re.compile(r"^\*\*(\d+)\. [^*]+:\*\*(.*)")
TARGET = re.compile(r"^> Реплик: (\d+)")
for f in sys.argv[1:]:
    words, target = 0, 150
    for line in Path(f).read_text(encoding="utf-8").splitlines():
        if t := TARGET.match(line): target = int(t.group(1))
        elif m := TURN.match(line):
            text = re.sub(r"\*\([^)]*\)\*|\*\[[^\]]*\]\*", "", m.group(2))
            words += len(re.findall(r"[А-Яа-яЁёA-Za-z0-9-]+", text))
    goal = round(3000 + (target - 120) * 1300 / 30)  # 120→3000, 150→4300 (기획서 5절)
    print(f"{Path(f).name}: {words} слов / цель ≈{goal} ({words*100//goal}%)")
