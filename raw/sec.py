import zipfile, re
z = zipfile.ZipFile(r"C:\Users\HXY\assist\ant-fund-proposal\CCF-蚂蚁科研基金_项目申请书.docx")
xml = z.read("word/document.xml").decode("utf-8")
secs = re.findall(r"<w:sectPr.*?</w:sectPr>", xml, flags=re.S)
print("sections:", len(secs))
for i,s in enumerate(secs):
    refs = re.findall(r'<w:footerReference[^/]*/>', s)
    pg = re.findall(r'<w:pgNumType[^/]*/>', s)
    print(i, "footerRefs:", refs, "pgNum:", pg, "len:", len(s))
print("footer parts:", [n for n in z.namelist() if "footer" in n])
