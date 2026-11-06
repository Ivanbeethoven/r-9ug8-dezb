import re, os
t=open("proposal_final.md",encoding="utf-8").read()
blocks=re.findall(r"```mermaid\r?\n(.*?)```", t, flags=re.S)
print("blocks:",len(blocks))
for b in blocks:
    print(repr(b.split("\n")[0])[:60])
print("files:", [f for f in os.listdir("figures")])
