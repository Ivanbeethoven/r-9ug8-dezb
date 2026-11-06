import re
for f in ("proposal.md","proposal_final.md"):
    t=open(f,encoding="utf-8").read()
    han=len(re.findall(r"[\u4e00-\u9fff]",t))
    print(f, "chars", len(t), "hanzi", han, "h2", len(re.findall(r"(?m)^## ",t)))
t=open("proposal_final.md",encoding="utf-8").read()
i=t.find("### 本研究的三点创新")
print("innovation block at", i)
print(t[i:i+120].replace("\n"," | "))
