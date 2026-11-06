p = r"C:\Users\HXY\assist\ant-fund-proposal\build_docx.py"
s = open(p, encoding="utf-8").read()
anchor = '    # gather content'
fix = '''    # cover must not carry a footer; move the reference to the body section
    cover, body_sec = doc.sections[0], doc.sections[1]
    for ref in list(cover._sectPr.findall(qn("w:footerReference"))):
        cover._sectPr.remove(ref)
        body_sec._sectPr.insert(0, ref)

'''
assert anchor in s
s = s.replace(anchor, fix + anchor, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched footer move")
