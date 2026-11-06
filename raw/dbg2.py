t=open("proposal_final.md",encoding="utf-8").read()
import re
for m in re.finditer(r"```mermaid", t):
    i=m.start()
    seg=t[i:i+90].replace("\r","<CR>").replace("\n","<LF>")
    print(m.start(), repr(seg))
