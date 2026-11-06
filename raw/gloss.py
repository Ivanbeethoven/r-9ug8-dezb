import re, glob
files = sorted(glob.glob("sections/*.md"))
gloss = re.compile(r"（(?:编程语言|操作系统|固态硬盘|对象存储服务|容器管理服务|读写压测工具|镜像服务|用户态文件系统接口|安全容器运行时|容器镜像规范|文件系统测试|文件语义测试|只读文件系统格式)）")
total = 0
for f in files:
    t = open(f, encoding="utf-8").read()
    hits = gloss.findall(t)
    if hits:
        print(f, len(hits), set(hits))
        total += len(hits)
print("total trivial glosses:", total)
