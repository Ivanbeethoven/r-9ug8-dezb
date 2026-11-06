import re
p = "sections/04-content.md"
t = open(p, encoding="utf-8").read()
drop = ["（编程语言）", "（操作系统）", "（固态硬盘）", "（对象存储服务）", "（容器管理服务）", "（镜像服务）", "（读写压测工具）"]
n = 0
for d in drop:
    n += t.count(d)
    t = t.replace(d, "")
open(p, "w", encoding="utf-8").write(t)
print("removed", n, "trivial glosses")
# sanity: show sentences around remaining parenthetical glosses
for m in re.finditer(r"[^。；\n]{0,40}（[^）]{2,12}）[^。；\n]{0,30}", t):
    print("  ", m.group(0))
