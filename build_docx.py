#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render the merged proposal markdown into a styled .docx.

Input  : proposal.md (fallback: sections/*.md)
Output : CCF-蚂蚁科研基金_项目申请书.docx
Optional: toc_pages.json  {"一、摘要": 3, ...} - printed page numbers for the TOC.
"""
import base64
import json
import os
import re
import urllib.request

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.dirname(os.path.abspath(__file__))
SECTIONS = ["01-summary.md", "02-background.md", "03-goals.md", "04-content.md",
            "05-route.md", "06-eval.md", "07-plan.md", "08-team.md", "09-deliverables.md"]
MERGED = os.path.join(ROOT, "proposal.md")
TOC_JSON = os.path.join(ROOT, "toc_pages.json")
FIGDIR = os.path.join(ROOT, "figures")
OUT_DOCX = os.path.join(ROOT, "CCF-蚂蚁科研基金_项目申请书.docx")

BODY_FONT = "宋体"
HEAD_FONT = "黑体"
LATIN_FONT = "Times New Roman"


# ------------------------------------------------------------------ helpers
def set_run_font(run, size=10.5, bold=False, east=BODY_FONT, latin=LATIN_FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = latin
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), east)


def shade(cell, hexcolor="E8EEF7"):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcpr.append(shd)


def add_field(paragraph, instr, placeholder="1"):
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = placeholder
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    for el in (fld_begin, instr_el, fld_sep, txt, fld_end):
        run._r.append(el)
    set_run_font(run, size=9)


INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def add_inline_runs(paragraph, text, size=10.5, bold=False, east=BODY_FONT):
    text = text.replace("\\", "")
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            set_run_font(r, size=size, bold=bold, east=east)
        token = m.group(0)
        if token.startswith("**"):
            r = paragraph.add_run(token[2:-2])
            set_run_font(r, size=size, bold=True, east=east)
        else:
            r = paragraph.add_run(token[1:-1])
            set_run_font(r, size=size - 0.5, bold=bold, east=east, latin="Consolas")
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        set_run_font(r, size=size, bold=bold, east=east)


def add_body_paragraph(doc, text, indent=True):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if indent:
        pf.first_line_indent = Pt(21)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_inline_runs(p, text, size=10.5)
    return p


def add_heading(doc, text, level):
    sizes = {1: 16, 2: 15, 3: 12.5, 4: 11}
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(16 if level <= 2 else 11)
    pf.space_after = Pt(9 if level <= 2 else 6)
    pf.keep_with_next = True
    pf.line_spacing = 1.25
    r = p.add_run(text)
    set_run_font(r, size=sizes.get(level, 11), bold=True, east=HEAD_FONT)
    if level <= 2:
        r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    return p


# ---------------------------------------------------------------- markdown
def parse_table(lines):
    rows = []
    for ln in lines:
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        if re.fullmatch(r"\|[\s:\-|]+\|", ln):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(cells)
    return rows


def add_table(doc, rows):
    if not rows:
        return
    ncol = max(len(r) for r in rows)
    table = doc.add_table(rows=0, cols=ncol)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    for i, row in enumerate(rows):
        cells = table.add_row().cells
        for j in range(ncol):
            text = row[j] if j < len(row) else ""
            cell = cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            pf = p.paragraph_format
            pf.space_before = Pt(2)
            pf.space_after = Pt(2)
            pf.line_spacing = 1.05
            if i == 0 and len(rows) > 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_inline_runs(p, text, size=9, bold=True, east=HEAD_FONT)
                shade(cell)
            else:
                add_inline_runs(p, text, size=9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def mermaid_to_png(code, name):
    os.makedirs(FIGDIR, exist_ok=True)
    path = os.path.join(FIGDIR, name + ".png")
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return path
    enc = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii").rstrip("=")
    url = "https://mermaid.ink/img/" + enc + "?bgColor=FFFFFF&width=1800"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/140.0 Safari/537.36",
        "Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
    })
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
        if len(data) > 2000:
            with open(path, "wb") as f:
                f.write(data)
            return path
    except Exception as exc:
        print("  [warn] mermaid render failed for %s: %s" % (name, exc))
    return None


def parse_markdown(doc, text, fig_counter):
    lines = text.split("\n")
    i = 0
    table_buf, para_buf = [], []

    def flush_para():
        if para_buf:
            add_body_paragraph(doc, " ".join(x.strip() for x in para_buf))
            para_buf.clear()

    def flush_table():
        if table_buf:
            add_table(doc, parse_table(table_buf))
            table_buf.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_para(); flush_table()
            fence = stripped[3:].strip().lower()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(body)
            if fence.startswith("mermaid"):
                fig_counter[0] += 1
                name = "fig%02d" % fig_counter[0]
                caption = None
                first = body[0].strip() if body else ""
                dm = re.match(r"%%\s*figure:\s*([A-Za-z0-9_\-]+)(?:\|(.+))?$", first)
                if dm:
                    preset = os.path.join(FIGDIR, dm.group(1) + ".png")
                    img = preset if os.path.exists(preset) else mermaid_to_png(code, dm.group(1))
                    caption = (dm.group(2) or "").strip() or None
                else:
                    img = mermaid_to_png(code, name)
                if img:
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_before = Pt(8)
                    p.paragraph_format.space_after = Pt(3)
                    p.paragraph_format.keep_with_next = True
                    p.add_run().add_picture(img, width=Cm(15.0))
                    cap = doc.add_paragraph()
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    cap.paragraph_format.space_after = Pt(10)
                    r = cap.add_run("图 %d" % fig_counter[0] + ("　　" + caption if caption else ""))
                    set_run_font(r, size=9, bold=True, east=HEAD_FONT)
                else:
                    for ln in code.split("\n"):
                        p = doc.add_paragraph()
                        r = p.add_run(ln)
                        set_run_font(r, size=8, latin="Consolas")
            else:
                for ln in code.split("\n"):
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Pt(18)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
                    r = p.add_run(ln if ln else " ")
                    set_run_font(r, size=8.5, latin="Consolas")
            continue

        if stripped.startswith("|"):
            flush_para()
            table_buf.append(stripped)
            i += 1
            continue
        else:
            flush_table()

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para()
            add_heading(doc, m.group(2).strip(), min(len(m.group(1)), 4))
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            flush_para()
            i += 1
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        m = re.match(r"^>\s?(.*)$", stripped)
        if m:
            flush_para()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(18)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.35
            add_inline_runs(p, m.group(1), size=10)
            i += 1
            continue

        m = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        if m:
            flush_para()
            lvl = len(m.group(1)) // 2
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(24 + 18 * lvl)
            p.paragraph_format.first_line_indent = Pt(-12)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.4
            r = p.add_run("• ")
            set_run_font(r, size=10.5)
            add_inline_runs(p, m.group(2), size=10.5)
            i += 1
            continue

        m = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", line)
        if m:
            flush_para()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(28)
            p.paragraph_format.first_line_indent = Pt(-16)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.4
            r = p.add_run(m.group(2) + ". ")
            set_run_font(r, size=10.5)
            add_inline_runs(p, m.group(3), size=10.5)
            i += 1
            continue

        para_buf.append(stripped)
        i += 1

    flush_para()
    flush_table()


# ------------------------------------------------------------------- cover
def build_cover(doc):
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("2026 年度 CCF-蚂蚁科研基金（第二批次）")
    set_run_font(r, size=15, east=HEAD_FONT)
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("项 目 申 请 书")
    set_run_font(r, size=36, bold=True, east=HEAD_FONT)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(30)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("面向 AI Agent 沙箱极速冷启动的\nNydus EROFS 按需加载与 Checkpoint/Restore 机制研究")
    set_run_font(r, size=16, bold=True, east=HEAD_FONT)
    p.paragraph_format.line_spacing = 1.55
    p.paragraph_format.space_after = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("—— 基于 BrewFS workspace overlay 的统一文件视图方法")
    set_run_font(r, size=12, bold=False, east=HEAD_FONT)
    p.paragraph_format.space_after = Pt(36)

    rows = [
        ["申 报 方 向", "超算与智算（AI 基础设施与系统优化）"],
        ["申 请 人", "冯　洋"],
        ["职　　　称", "副教授、博士生导师"],
        ["依 托 单 位", "南京大学计算机学院"],
        ["合 作 企 业", "蚂蚁集团（Ant Group）"],
        ["依 托 项 目", "BrewFS：面向 Agent 负载的 Rust 分布式文件系统"],
        ["申 请 金 额", "人民币 30 万元"],
        ["研 究 周 期", "2027 年 2 月 — 2028 年 1 月（12 个月）"],
        ["申 报 日 期", "2026 年 11 月"],
    ]
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for k, v in rows:
        cells = table.add_row().cells
        for c, width in zip(cells, (Cm(4.4), Cm(10.4))):
            c.width = width
        p0, p1 = cells[0].paragraphs[0], cells[1].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(k)
        set_run_font(r0, size=11, bold=True, east=HEAD_FONT)
        r1 = p1.add_run(v)
        set_run_font(r1, size=11)
        for pp in (p0, p1):
            pp.paragraph_format.space_before = Pt(5)
            pp.paragraph_format.space_after = Pt(5)
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "808080")
        borders.append(el)
    tblPr.append(borders)


def build_toc(doc, entries, pages):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("目　　录")
    set_run_font(r, size=18, bold=True, east=HEAD_FONT)
    p.paragraph_format.space_after = Pt(18)

    for title in entries:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(7)
        pf.line_spacing = 1.35
        pf.tab_stops.add_tab_stop(Cm(15.4), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r = p.add_run(title)
        set_run_font(r, size=11, east=HEAD_FONT)
        page = pages.get(title)
        r2 = p.add_run("\t" + (str(page) if page else ""))
        set_run_font(r2, size=11)


def page_setup(sec):
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.6)
    sec.right_margin = Cm(2.6)
    sec.top_margin = Cm(2.4)
    sec.bottom_margin = Cm(2.2)


def start_body_section(doc):
    body = doc.add_section(WD_SECTION.NEW_PAGE)
    page_setup(body)
    sectPr = body._sectPr
    pgNumType = OxmlElement("w:pgNumType")
    pgNumType.set(qn("w:start"), "1")
    sectPr.append(pgNumType)
    fp = body.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(fp, "PAGE")
    return body


def main():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = LATIN_FONT
    style.font.size = Pt(10.5)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)

    cp = doc.core_properties
    cp.title = "2026 年度 CCF-蚂蚁科研基金（第二批次）项目申请书"
    cp.subject = "面向 AI Agent 沙箱极速冷启动的 Nydus EROFS 按需加载与 Checkpoint/Restore 机制研究"
    cp.author = "冯洋（南京大学计算机学院）"
    cp.last_modified_by = "冯洋"
    cp.category = "超算与智算"
    cp.keywords = "AI Agent 沙箱; Nydus EROFS; lazyload; Checkpoint/Restore; BrewFS; workspace overlay"
    cp.comments = "申请 2026 年度 CCF-蚂蚁科研基金（第二批次）超算与智算方向课题"
    page_setup(doc.sections[0])
    build_cover(doc)
    start_body_section(doc)

    # cover must not carry a footer; move the reference to the body section
    cover, body_sec = doc.sections[0], doc.sections[1]
    for ref in list(cover._sectPr.findall(qn("w:footerReference"))):
        cover._sectPr.remove(ref)
        body_sec._sectPr.insert(0, ref)

    # gather content
    source = None
    for cand in ("proposal_final.md", "proposal_polished.md", "proposal.md"):
        p = os.path.join(ROOT, cand)
        if os.path.exists(p):
            source = p
            break
    if source:
        with open(source, encoding="utf-8") as f:
            content = f.read()
        print("source:", os.path.basename(source))
    else:
        parts = []
        for name in SECTIONS:
            path = os.path.join(ROOT, "sections", name)
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    parts.append(f.read())
        content = "\n\n".join(parts)

    entries = [ln[3:].strip() for ln in content.split("\n") if ln.startswith("## ")]
    pages = {}
    if os.path.exists(TOC_JSON):
        with open(TOC_JSON, encoding="utf-8") as f:
            pages = json.load(f)

    build_toc(doc, entries, pages)
    doc.add_page_break()

    fig_counter = [0]
    parse_markdown(doc, content, fig_counter)

    doc.save(OUT_DOCX)
    print("saved:", OUT_DOCX, "| chapters:", len(entries), "| figures:", fig_counter[0])


if __name__ == "__main__":
    main()
