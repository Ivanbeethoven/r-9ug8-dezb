p = r"C:\Users\HXY\assist\ant-fund-proposal\build_docx.py"
s = open(p, encoding="utf-8").read()
anchor = '    page_setup(doc.sections[0])'
props = '''    cp = doc.core_properties
    cp.title = "2026 年度 CCF-蚂蚁科研基金（第二批次）项目申请书"
    cp.subject = "面向 AI Agent 沙箱极速冷启动的 Nydus EROFS 按需加载与 Checkpoint/Restore 机制研究"
    cp.author = "冯洋（南京大学计算机学院）"
    cp.last_modified_by = "冯洋"
    cp.category = "超算与智算"
    cp.keywords = "AI Agent 沙箱; Nydus EROFS; lazyload; Checkpoint/Restore; BrewFS; workspace overlay"
    cp.comments = "申请 2026 年度 CCF-蚂蚁科研基金（第二批次）超算与智算方向课题"
'''
assert anchor in s
s = s.replace(anchor, props + anchor, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched properties")
