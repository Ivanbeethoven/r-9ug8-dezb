#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Insert %%figure directives into the mermaid blocks of the final markdown."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

DIRECTIVES = [
    "%%figure:arch|系统分层架构：控制面 / 执行面（runD guest）/ 数据面（BrewFS）",
    "%%figure:seq-start|沙箱冷启动时序与分段预算（4G 冷启动 / 快照恢复）",
    "%%figure:seq-cr|Checkpoint / Restore：一致固化与快速恢复时序",
    "%%figure:roadmap|12 个月阶段计划、关键路径与验收节点",
]


def main(src, dst):
    with open(os.path.join(ROOT, src), encoding="utf-8") as f:
        text = f.read()
    blocks = list(re.finditer(r"```mermaid\r?\n(.*?)```", text, flags=re.S))
    print("found", len(blocks), "mermaid blocks")
    out, last = [], 0
    for idx, m in enumerate(blocks):
        body = m.group(1)
        head = body.strip().split("\n")[0].strip()
        directive = DIRECTIVES[idx] if idx < len(DIRECTIVES) else None
        out.append(text[last:m.start()])
        if directive and not body.lstrip().startswith("%%figure:"):
            out.append("```mermaid\n" + directive + "\n" + body.rstrip("\r\n") + "\n```")
        else:
            out.append(m.group(0))
        last = m.end()
        print("  block %d (%s) -> %s" % (idx + 1, head[:24], (directive or "unchanged")[:48]))
    out.append(text[last:])
    final = "".join(out)
    with open(os.path.join(ROOT, dst), "w", encoding="utf-8") as f:
        f.write(final)
    print("wrote", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
