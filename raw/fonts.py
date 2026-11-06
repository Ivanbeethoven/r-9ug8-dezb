import matplotlib
from matplotlib import font_manager as fm
names = sorted({f.name for f in fm.fontManager.ttflist})
want = [n for n in names if any(k in n for k in ("YaHei","SimHei","SimSun","Noto Sans CJK","Source Han","DengXian","KaiTi","FangSong"))]
print("cjk fonts:", want[:20])
print("total fonts:", len(names))
