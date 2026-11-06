import sys
sys.path.insert(0, r"C:\Users\HXY\assist\raw\pylibs")
from pypdf import PdfReader
r = PdfReader(r"C:\Users\HXY\assist\ant-fund-proposal\CCF-蚂蚁科研基金_项目申请书.pdf")
fonts=set()
for p in r.pages:
    res = p.get("/Resources", {})
    f = res.get("/Font", {})
    try:
        for k,v in f.items():
            o=v.get_object()
            bf=o.get("/BaseFont")
            desc=o.get("/FontDescriptor")
            emb=False
            if desc is not None:
                d=desc.get_object()
                emb = any(k2 in d for k2 in ("/FontFile","/FontFile2","/FontFile3"))
            fonts.add((str(bf), emb))
    except Exception as e:
        pass
for f in sorted(fonts): print(f)
print("metadata:", r.metadata)
