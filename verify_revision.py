#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify the revision actually did what the PI asked."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

FORBIDDEN = ["463.471", "492.831", "387.973", "235.930", "261,490", "16,379.61",
             "92.799", "10.945", "1.7%"]


def load(path):
    return open(path, encoding="utf-8").read()


def main(snapshot):
    files = sorted(glob.glob(os.path.join(ROOT, "sections", "*.md")))
    text = "\n".join(load(f) for f in files)
    old = "\n".join(load(f) for f in sorted(glob.glob(os.path.join(ROOT, snapshot, "*.md"))))

    print("== forbidden metrics ==")
    bad = [n for n in FORBIDDEN if n in text]
    print("   still present:", bad if bad else "none ✔")

    print("== jargon counts (new vs old) ==")
    for term in ["overlay", "packed lower", "workspace overlay", "lease + generation fencing",
                 "tombstone", "copy-up", "pcluster"]:
        print("   %-28s %3d -> %3d" % (term, old.count(term), text.count(term)))

    print("== positioning ==")
    first = load(os.path.join(ROOT, "sections", "01-summary.md"))
    head = first[:600]
    for kw in ["Rust", "分布式文件系统", "Agent"]:
        print("   summary mentions %-12s %s" % (kw, "✔" if kw in head else "✘"))

    print("== JuiceFS comparison ==")
    for f in files:
        t = load(f)
        if "JuiceFS" in t:
            hits = len(re.findall("JuiceFS", t))
            print("   %-20s %d mention(s)" % (os.path.basename(f), hits))
    for num in ["149.7", "73.6", "65.8", "37.3", "41.6"]:
        if num not in text:
            print("   !! missing comparison figure", num)
    print("   30 倍/数量级表述:", "有" if ("30 倍" in text or "数量级" in text) else "无")

    print("== mermaid untouched ==")
    def blocks(t):
        return [m.strip() for m in re.findall(r"```mermaid\r?\n(.*?)```", t, flags=re.S)]
    print("   blocks %d -> %d, identical=%s" % (len(blocks(old)), len(blocks(text)),
                                                blocks(old) == blocks(text)))

    han = lambda t: len(re.findall(r"[\u4e00-\u9fff]", t))
    print("== length ==  hanzi %d -> %d (%+.1f%%)" % (han(old), han(text),
                                                      (han(text) - han(old)) * 100.0 / han(old)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sections.bak-20261105-1951")
