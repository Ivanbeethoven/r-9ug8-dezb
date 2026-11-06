import re, glob
n=0
for f in sorted(glob.glob("sections/*.md")):
    t=open(f,encoding="utf-8").read()
    new=re.sub(r"(?<=）)[ \t]+(?=[\u4e00-\u9fff])","",t)
    new=re.sub(r"(?<=）」)[ \t]+(?=[\u4e00-\u9fff])","",new)
    if new!=t:
        open(f,"w",encoding="utf-8").write(new); n+=1
print("fixed files:",n)
for f in ["sections/04-content.md","sections/08-team.md","sections/01-summary.md"]:
    t=open(f,encoding="utf-8").read()
    bad=re.findall(r"）\s+[\u4e00-\u9fff]{1,3}",t)
    print(f,"remaining bad:",bad[:5])
