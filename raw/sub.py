p = r"C:\Users\HXY\assist\ant-fund-proposal\build_docx.py"
s = open(p, encoding="utf-8").read()
old = """    set_run_font(r, size=16, bold=True, east=HEAD_FONT)
    p.paragraph_format.line_spacing = 1.55
    p.paragraph_format.space_after = Pt(40)"""
new = """    set_run_font(r, size=16, bold=True, east=HEAD_FONT)
    p.paragraph_format.line_spacing = 1.55
    p.paragraph_format.space_after = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("—— 基于 BrewFS workspace overlay 的统一文件视图方法")
    set_run_font(r, size=12, bold=False, east=HEAD_FONT)
    p.paragraph_format.space_after = Pt(36)"""
assert old in s
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("cover subtitle added")
