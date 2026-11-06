#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guardrail: compare numeric tokens and tables between two proposal revisions."""
import collections
import re
import sys

TOKEN = re.compile(r"\d+(?:\.\d+)?(?:\s?(?:%|ms|s|MiB/s|GiB|MiB|MiB／s|万|元|篇|项))?")


def tokens(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # drop mermaid blocks so diagram ids (fig numbers) do not pollute the diff
    text = re.sub(r"```mermaid.*?```", "", text, flags=re.S)
    norm = []
    for tok in TOKEN.findall(text):
        norm.append(tok.replace(" ", ""))
    return collections.Counter(norm), text


def table_rows(text):
    rows = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|") and not re.fullmatch(r"\|[\s:\-|]+\|", s):
            rows.append(s)
    return rows


def mermaid_blocks(text):
    return re.findall(r"```mermaid(.*?)```", text, flags=re.S)


def main(a, b):
    ta, txt_a = tokens(a)
    tb, txt_b = tokens(b)
    print("== numeric token diff (only shown when nonzero) ==")
    lost = {k: v - tb.get(k, 0) for k, v in ta.items() if ta[k] - tb.get(k, 0) > 0}
    added = {k: v - ta.get(k, 0) for k, v in tb.items() if tb[k] - ta.get(k, 0) > 0}
    print("lost:", dict(sorted(lost.items())))
    print("added:", dict(sorted(added.items())))

    ra, rb = table_rows(txt_a), table_rows(txt_b)
    print("\n== tables ==  rows %d -> %d" % (len(ra), len(rb)))
    only_a = [r for r in ra if r not in rb]
    only_b = [r for r in rb if r not in ra]
    for r in only_a[:20]:
        print("  - ", r[:120])
    for r in only_b[:20]:
        print("  + ", r[:120])

    ma, mb = mermaid_blocks(txt_a), mermaid_blocks(txt_b)
    print("\n== mermaid blocks ==  %d -> %d" % (len(ma), len(mb)))
    for i, (x, y) in enumerate(zip(ma, mb)):
        if x.strip() != y.strip():
            print("  block %d changed" % (i + 1))

    han = lambda t: len(re.findall(r"[\u4e00-\u9fff]", t))
    print("\nhanzi: %d -> %d (%+d%%)" % (han(txt_a), han(txt_b),
                                         round((han(txt_b) - han(txt_a)) * 100.0 / han(txt_a))))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
