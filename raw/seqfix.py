p = r"C:\Users\HXY\assist\ant-fund-proposal\draw_seq.py"
s = open(p, encoding="utf-8").read()
s = s.replace("视图 attach 完成，租约就绪", "视图挂载完成，租约就绪")
s = s.replace("探针通过，sandbox ready", "探针通过，沙箱就绪")
s = s.replace("(3, 1, \"探针通过，沙箱就绪\", \"\", \"ret\")", "(3, 1, \"探针通过，沙箱就绪\", \"\", \"ret\")")
open(p,"w",encoding="utf-8").write(s)
print("ok")
