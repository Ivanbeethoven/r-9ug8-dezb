p = r"C:\Users\HXY\assist\ant-fund-proposal\make_toc.py"
s = open(p, encoding="utf-8").read()
s = s.replace("""        for idx, text in enumerate(pages):
            if key and key in text:""",
"""        for idx, text in enumerate(pages):
            if idx < 2:          # 0 = cover, 1 = TOC page
                continue
            if key and key in text:""")
open(p, "w", encoding="utf-8").write(s)
print("patched")
