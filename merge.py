#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Merge section markdown files into one proposal with normalized chapter headings."""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

CHAPTERS = [
    ("01-summary.md", "一、摘要"),
    ("02-background.md", "二、研究背景与问题分析"),
    ("03-goals.md", "三、研究目标、关键科学问题与可行性"),
    ("04-content.md", "四、研究内容"),
    ("05-route.md", "五、技术路线与系统架构"),
    ("06-eval.md", "六、技术指标与评测方案"),
    ("07-plan.md", "七、研究计划与里程碑"),
    ("08-team.md", "八、研究基础与团队"),
    ("09-deliverables.md", "九、交付成果、经费预算、风险与知识产权"),
]

OUT = os.path.join(ROOT, "proposal.md")

CN_NUM = {"01": "一", "02": "二", "03": "三", "04": "四", "05": "五",
          "06": "六", "07": "七", "08": "八", "09": "九"}

FIXUPS = [
    ("BRIEF 的 2026-09-22 阿里云对齐评测", "团队 2026-09-22 的阿里云对齐评测"),
    ("BRIEF 的 2026-11-02", "团队 2026-11-02"),
    ("BRIEF", "前期工作"),
]


def fixup(text):
    for old, new in FIXUPS:
        text = text.replace(old, new)
    # "第 03 章" -> "第三章"
    def repl(m):
        return "第" + CN_NUM.get(m.group(1), m.group(1)) + "章"
    text = re.sub(r"第\s*(0\d)\s*章", repl, text)
    return text



def normalize(text, title):
    lines = text.split("\n")
    out = []
    replaced = False
    for ln in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            level = len(m.group(1))
            body = m.group(2).strip()
            if not replaced and level <= 2:
                out.append("## " + title)
                replaced = True
                continue
            # drop a redundant "摘要" subheading right under the chapter title
            if level == 3 and body in ("摘要", "项目摘要") and "摘要" in title:
                continue
            # strip numeric prefixes such as "04 " / "06 " from subheadings
            body = re.sub(r"^0\d\s+", "", body)
            out.append("#" * level + " " + body)
            continue
        out.append(ln)
    if not replaced:
        out.insert(0, "## " + title)
    return "\n".join(out).strip("\n")


def main():
    chunks = []
    for name, title in CHAPTERS:
        path = os.path.join(ROOT, "sections", name)
        if not os.path.exists(path):
            print("[warn] missing", name)
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        chunks.append(fixup(normalize(text, title)))
    merged = "\n\n".join(chunks) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(merged)
    han = len(re.findall(r"[\u4e00-\u9fff]", merged))
    print("wrote %s: %d chars, %d hanzi" % (OUT, len(merged), han))


if __name__ == "__main__":
    main()
