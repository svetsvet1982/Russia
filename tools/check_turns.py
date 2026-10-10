#!/usr/bin/env python3
"""Проверка нумерации реплик: в каждом эпизоде должно быть ровно 150 реплик подряд."""
import re
import sys
from pathlib import Path

TURN = re.compile(r"^\*\*(\d+)\. ([А-ЯЁA-Z][А-ЯЁA-Z\- ]*):\*\*")


def check(path: Path) -> bool:
    turns = [(int(m.group(1)), m.group(2)) for line in path.read_text(encoding="utf-8").splitlines()
             if (m := TURN.match(line))]
    nums = [n for n, _ in turns]
    ok = nums == list(range(1, 151))
    for (n1, a), (n2, b) in zip(turns, turns[1:]):
        if a == b:
            print(f"WARN {path}: реплики {n1} и {n2} подряд у {a}")
    if not ok:
        gaps = [i for i, n in enumerate(nums, 1) if n != i]
        print(f"FAIL {path}: {len(nums)} реплик, первое расхождение на позиции {gaps[:1]}")
    else:
        print(f"OK   {path}: 150 реплик")
    return ok


if __name__ == "__main__":
    files = [Path(p) for p in sys.argv[1:]] or sorted(Path(".").glob("part*/ep*.md"))
    sys.exit(0 if all(check(f) for f in files) else 1)
