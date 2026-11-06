import sys, re
sys.path.insert(0, r"C:\Users\HXY\assist\raw\pylibs")
from pypdf import PdfReader
r = PdfReader(r"C:\Users\HXY\assist\ant-fund-proposal\CCF-蚂蚁科研基金_项目申请书.pdf")
txt = "\n".join((p.extract_text() or "") for p in r.pages)
print("pages:", len(r.pages), "chars:", len(txt))
for k in ["一、摘要","二、研究背景","三、研究目标","四、研究内容","五、技术路线","六、技术指标","七、研究计划","八、研究基础","九、交付成果","本研究的三点创新","This work was supported"]:
    print(("  OK  " if k in txt.replace(" ","") or k in txt else "  MISS"), k)
print("replacement chars:", txt.count("\ufffd"))
