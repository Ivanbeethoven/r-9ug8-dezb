import re

p = r"C:\Users\HXY\assist\ant-fund-proposal\draw_arch.py"
s = open(p, encoding="utf-8").read()
s = s.replace('[], label="workspace overlay", label_size=25', '[], label="BrewFS 工作区隔离", label_size=24')
s = s.replace('["不可变 packed lower", "（Nydus EROFS 镜像层）"], size=20', '["只读基座（lower）", "Nydus EROFS 镜像层"], size=20')
s = s.replace('["私有可写 upper（增量）"], size=21', '["私有增量层（upper）"], size=21')
s = s.replace('["租约 + generation", "恰好一个写者"], size=22', '["写者租约 + 代次", "恰好一个写者"], size=22')
open(p, "w", encoding="utf-8").write(s)

q = r"C:\Users\HXY\assist\ant-fund-proposal\draw_seq.py"
t = open(q, encoding="utf-8").read()
pairs = [
 ("workspace 服务", "工作区服务"),
 ("申请 workspace：manifest / attach", "申请工作区：元数据清单与挂载"),
 ("取 manifest、索引与租约记录", "取元数据清单、索引与租约"),
 ("stop admission：暂停写入", "禁止新写入，暂停应用"),
 ("drain writes / fsync，固定文件视图", "排空写入并落盘，固定文件视图"),
 ("上传文件对象与 manifest", "上传文件对象与元数据清单"),
 ("核验租约与 generation，原子发布", "核验租约与代次，原子发布"),
 ("取 lease 与新 generation", "取租约与新代次"),
 ("恢复进程与内存状态，跑探针", "恢复进程与内存状态并校验"),
 ("探针通过，复验租约后开放写入", "探针通过，复验租约后开写"),
 ("重建挂载，写闸保持关闭", "重建挂载，保持禁止写入"),
 ("提交匹配的文件视图与状态引用", "提交匹配的文件视图与状态"),
]
for a,b in pairs:
    t = t.replace(a,b)
open(q, "w", encoding="utf-8").write(t)
print("scripts updated")
