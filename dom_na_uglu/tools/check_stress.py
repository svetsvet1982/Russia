#!/usr/bin/env python3
"""대사(괄호 지문 제외)에서 강세 부호 없는 다음절 단어를 찾는다. 사용법: check_stress.py [파일 ...]"""
import re
import sys
from pathlib import Path

LINE = re.compile(r"^\*\*([^*:]+):\*\*\s+(.*)")
WORD = re.compile(r"[А-Яа-яЁё́-]+")
VOW = set("аеиоуыэюяАЕИОУЫЭЮЯ")
OK = {"Палыч", "Нигора", "Тимур", "Тёма"}  # 이름 표기용 예외 없음: 대사 속 이름은 모두 강세 표기


def bad_words(line):
    line = re.sub(r"\*\([^)]*\)\*", "", line)
    for w in WORD.findall(line):
        for part in w.split("-"):
            if not part or "́" in part or "ё" in part.lower():
                continue
            if sum(ch in VOW for ch in part) >= 2 and part.upper() != part:
                yield part


root = Path(__file__).resolve().parent.parent
files = [Path(p) for p in sys.argv[1:]] or sorted(root.glob("part*/ep*.md"))
total = 0
for f in files:
    text = f.read_text(encoding="utf-8").split("## 한글 해석")[0]
    n = 0
    for line in text.splitlines():
        m = LINE.match(line)
        if m:
            n += 1
            bad = list(bad_words(m.group(2)))
            if bad:
                total += len(bad)
                print(f"{f.name}:{n}: {' '.join(bad)}")
print(f"강세 누락 {total}개")
sys.exit(1 if total else 0)
