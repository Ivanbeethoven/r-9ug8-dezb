import re, glob

LAT_CJK = re.compile(r"(?<=[A-Za-z0-9%）)])(?=[\u4e00-\u9fff])")
CJK_LAT = re.compile(r"(?<=[\u4e00-\u9fff])(?=[A-Za-z0-9(])")

def space_out(seg):
    seg = LAT_CJK.sub(" ", seg)
    seg = CJK_LAT.sub(" ", seg)
    seg = re.sub(r"[ \t]{2,}", " ", seg)
    return seg

changed = 0
for f in sorted(glob.glob("sections/*.md")):
    t = open(f, encoding="utf-8").read()
    parts = re.split(r"(```.*?```)", t, flags=re.S)
    out = []
    for i, p in enumerate(parts):
        if p.startswith("```"):
            out.append(p)          # keep code fences untouched
        else:
            out.append(space_out(p))
    new = "".join(out)
    new = new.replace("对照 JuiceFS（分布式文件系统）", "对照 JuiceFS")
    if new != t:
        open(f, "w", encoding="utf-8").write(new)
        changed += 1
print("files updated:", changed)
