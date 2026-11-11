#!/usr/bin/env python3
"""《Дом на углу》 회차 검사: 대사 120턴, 한글 해석 120줄, 같은 장면 안 같은 화자 연속 금지.

사용법: python3 check_episode.py [파일 ...]   (인수 없으면 part*/ep*.md 전부)
"""
import re
import sys
from pathlib import Path

TURNS = 120
LINE = re.compile(r"^\*\*([^*:]+):\*\*\s+\S")
KO_HEAD = "## 한글 해석"


def turns(lines):
    out, scene = [], 0
    for line in lines:
        if line.strip() == "---":
            scene += 1
        elif m := LINE.match(line):
            out.append((m.group(1).strip(), scene))
    return out


def check(path: Path) -> bool:
    text = path.read_text(encoding="utf-8").splitlines()
    try:
        k = text.index(KO_HEAD)
    except ValueError:
        print(f"FAIL {path}: '{KO_HEAD}' 섹션 없음")
        return False
    ru, ko = turns(text[:k]), turns(text[k:])
    ok = len(ru) == TURNS and len(ko) == TURNS
    for i, ((a, s1), (b, s2)) in enumerate(zip(ru, ru[1:]), 1):
        if a == b and s1 == s2:
            print(f"WARN {path}: {i}·{i + 1}턴 연속 화자 {a}")
            ok = False
    speakers = sorted({s for s, _ in ru})
    print(f"{'OK  ' if ok else 'FAIL'} {path}: 대사 {len(ru)}턴, 해석 {len(ko)}줄, 화자 {len(speakers)}명 {speakers}")
    return ok


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    files = [Path(p) for p in sys.argv[1:]] or sorted(root.glob("part*/ep*.md"))
    sys.exit(0 if all([check(f) for f in files]) else 1)
