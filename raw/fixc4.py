p = "sections/04-content.md"
t = open(p, encoding="utf-8").read()
t = t.replace("统一 Nydus 的 EROFS（只读文件系统格式）镜像加载", "统一 Nydus EROFS（只读文件系统格式）镜像加载")
t = t.replace("### 内容一：让镜像和工作区说同一种版本语言", "### 内容一：统一镜像与工作区的版本格式")
open(p, "w", encoding="utf-8").write(t)
print("ok")
