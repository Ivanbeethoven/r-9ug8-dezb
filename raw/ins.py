import io, os
root = r"C:\Users\HXY\assist\ant-fund-proposal"
block = open(os.path.join(root, "raw", "innovation_block.md"), encoding="utf-8").read()
p = os.path.join(root, "proposal_final.md")
t = open(p, encoding="utf-8").read()
marker = "## 五、技术路线与系统架构"
assert marker in t, "marker missing"
assert "本研究的三点创新" not in t, "already inserted"
t = t.replace(marker, block + marker, 1)
open(p, "w", encoding="utf-8").write(t)
print("inserted, total chars", len(t))
