import re, os
p = "申报要求与提交清单.md"
t = open(p, encoding="utf-8").read()
before = t
t = t.replace("raw/ccf-mulu.pdf", "sources/2026-CCF-蚂蚁科研基金-第二批次-申报指南.pdf")
t = t.replace("raw/ccf-kt.pdf", "sources/2026-CCF-蚂蚁科研基金-第二批次-申报课题介绍.pdf")
t = t.replace("raw/apply-form-strings.txt", "sources/蚂蚁申报页-表单字段.txt")
t = t.replace("raw/ccf-kt.txt", "sources/申报课题介绍-正文提取.txt")
t = t.replace("raw/ccf-mulu.txt", "sources/申报指南-正文提取.txt")
open(p, "w", encoding="utf-8").write(t)
print("updated refs:", before != t)
