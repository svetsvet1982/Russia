#!/usr/bin/env python3
"""Проверка нумерации реплик.

Число реплик берётся из строки заголовка «> Реплик: N» (если её нет — 150).
Пример: python3 tools/check_turns.py naruzhka/part1_*/ep*.md
"""
import re
import sys
from pathlib import Path

TARGET = re.compile(r"^> Реплик: (\d+)")
TURN = re.compile(r"^\*\*(\d+)\. ([А-ЯЁA-Z][А-ЯЁA-Z\- ]*):\*\*")


def check(path: Path) -> bool:
    turns, scene, target = [], 0, 150
    for line in path.read_text(encoding="utf-8").splitlines():
        if t := TARGET.match(line):
            target = int(t.group(1))
        elif line.strip() == "---":
            scene += 1
        elif m := TURN.match(line):
            turns.append((int(m.group(1)), m.group(2), scene))
    nums = [n for n, _, _ in turns]
    ok = nums == list(range(1, target + 1))
    for (n1, a, s1), (n2, b, s2) in zip(turns, turns[1:]):
        if a == b and s1 == s2:
            print(f"WARN {path}: реплики {n1} и {n2} подряд у {a}")
    if not ok:
        gaps = [i for i, n in enumerate(nums, 1) if n != i]
        print(f"FAIL {path}: {len(nums)} реплик из {target}, первое расхождение на позиции {gaps[:1]}")
    else:
        print(f"OK   {path}: {target} реплик")
    return ok


if __name__ == "__main__":
    files = [Path(p) for p in sys.argv[1:]] or sorted(Path(".").glob("part*/ep*.md"))
    sys.exit(0 if all(check(f) for f in files) else 1)
