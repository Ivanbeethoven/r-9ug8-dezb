import re, io
p = r"C:\Users\HXY\assist\ant-fund-proposal\apply_figs.py"
s = open(p, encoding="utf-8").read()
s = s.replace('out.append("```mermaid\\n" + directive + "\\n" + body)',
              'out.append("```mermaid\\n" + directive + "\\n" + body.rstrip("\\r\\n") + "\\n```")')
open(p, "w", encoding="utf-8").write(s)

q = r"C:\Users\HXY\assist\ant-fund-proposal\make_toc.py"
t = open(q, encoding="utf-8").read()
t = t.replace('sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "pylibs"))',
              'sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw", "pylibs"))')
open(q, "w", encoding="utf-8").write(t)
print("patched both")
