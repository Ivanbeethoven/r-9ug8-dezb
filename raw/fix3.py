p = r"C:\Users\HXY\assist\ant-fund-proposal\build_docx.py"
s = open(p, encoding="utf-8").read()

old_setup = s[s.index("def setup_sections(doc):"):s.index("def main():")]
new_setup = '''def page_setup(sec):
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


'''
s = s.replace(old_setup, new_setup)

s = s.replace('''    setup_sections(doc)
    build_cover(doc)''', '''    page_setup(doc.sections[0])
    build_cover(doc)
    start_body_section(doc)''')
open(p, "w", encoding="utf-8").write(s)
print("patched build_docx")
