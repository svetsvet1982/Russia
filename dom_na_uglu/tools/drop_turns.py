#!/usr/bin/env python3
"""대사와 한글 해석에서 같은 번호의 턴을 함께 지운다. 사용법: drop_turns.py 파일 번호 [번호 ...]"""
import re
import sys

LINE = re.compile(r"^\*\*([^*:]+):\*\*\s")
path, *nums = sys.argv[1:]
drop = {int(n) for n in nums}
head, ko = open(path, encoding="utf-8").read().split("## 한글 해석")


def strip(section):
    out, n, skip_blank = [], 0, False
    for line in section.split("\n"):
        if LINE.match(line):
            n += 1
            if n in drop:
                skip_blank = True
                continue
        elif skip_blank and line == "":
            skip_blank = False
            continue
        skip_blank = False
        out.append(line)
    return "\n".join(out)


open(path, "w", encoding="utf-8").write(strip(head) + "## 한글 해석" + strip(ko))
