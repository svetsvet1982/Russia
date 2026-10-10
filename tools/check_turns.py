#!/usr/bin/env python3
"""Проверка нумерации реплик: в каждом эпизоде должно быть ровно 150 реплик подряд."""
import re
import sys
from pathlib import Path

TURN = re.compile(r"^\*\*(\d+)\. ([А-ЯЁA-Z][А-ЯЁA-Z\- ]*):\*\*")


def check(path: Path) -> bool:
    nums = [int(m.group(1)) for line in path.read_text(encoding="utf-8").splitlines()
            if (m := TURN.match(line))]
    ok = nums == list(range(1, 151))
    if not ok:
        gaps = [i for i, n in enumerate(nums, 1) if n != i]
        print(f"FAIL {path}: {len(nums)} реплик, первое расхождение на позиции {gaps[:1]}")
    else:
        print(f"OK   {path}: 150 реплик")
    return ok


if __name__ == "__main__":
    files = [Path(p) for p in sys.argv[1:]] or sorted(Path(".").glob("part*/ep*.md"))
    sys.exit(0 if all(check(f) for f in files) else 1)
