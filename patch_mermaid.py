#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Localize labels inside mermaid blocks (figures are redrawn separately)."""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGETS = ["sections/05-route.md", "sections/07-plan.md"]

PAIRS = [
    ("workspace overlay", "工作区隔离"),
    ("不可变 packed lower", "只读基座"),
    ("私有可写 upper", "私有增量层"),
    ("lease + generation fencing", "租约 + 代次"),
    ("manifest / 视图 attach", "元数据清单 / 视图挂载"),
    ("视图 attach", "视图挂载"),
    ("manifest/revision", "元数据清单/版本"),
    ("manifest", "元数据清单"),
]


def main():
    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        blocks = list(re.finditer(r"```mermaid\r?\n(.*?)```", text, flags=re.S))
        if not blocks:
            continue
        out, last, changed = [], 0, 0
        for m in blocks:
            body = m.group(1)
            new = body
            for a, b in PAIRS:
                new = new.replace(a, b)
            if new != body:
                changed += 1
            out.append(text[last:m.start()])
            out.append("```mermaid\n" + new + "```")
            last = m.end()
        out.append(text[last:])
        if changed:
            open(path, "w", encoding="utf-8").write("".join(out))
        print("%s: %d mermaid block(s), %d changed" % (rel, len(blocks), changed))


if __name__ == "__main__":
    main()
