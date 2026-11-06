#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Locate chapter start pages in the exported PDF and write toc_pages.json.

Printed page number = PDF page index - 1 (cover is PDF page 1, body numbering
restarts at 1 on PDF page 2).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw", "pylibs"))
from pypdf import PdfReader  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(ROOT, "CCF-蚂蚁科研基金_项目申请书.pdf")
OUT = os.path.join(ROOT, "toc_pages.json")


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    reader = PdfReader(PDF)
    pages = [norm(p.extract_text() or "") for p in reader.pages]
    with open(os.path.join(ROOT, "proposal.md"), encoding="utf-8") as f:
        titles = [ln[3:].strip() for ln in f.read().split("\n") if ln.startswith("## ")]

    result = {}
    for title in titles:
        key = norm(title)
        for idx, text in enumerate(pages):
            if idx < 2:          # 0 = cover, 1 = TOC page
                continue
            if key and key in text:
                result[title] = idx  # printed page = pdf index - 1 => idx
                break
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    missing = [t for t in titles if t not in result]
    if missing:
        print("MISSING:", missing)


if __name__ == "__main__":
    main()
