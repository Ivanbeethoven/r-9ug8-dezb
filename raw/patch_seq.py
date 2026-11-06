import re
p = r"C:\Users\HXY\assist\ant-fund-proposal\draw_seq.py"
s = open(p, encoding="utf-8").read()
s = s.replace('''    f_title = font(26, True)
    d.text(((width - tw(d, title, f_title)) / 2, 22), title, font=f_title, fill=ACCENT)''',
'''    if title:
        f_title = font(26, True)
        d.text(((width - tw(d, title, f_title)) / 2, 16), title, font=f_title, fill=ACCENT)''')
s = s.replace('"图 2  沙箱冷启动时序：分段预算（4G 冷启动 / 快照恢复）"', '""')
s = s.replace('"图 3  Checkpoint / Restore：一致固化与快速恢复时序"', '""')
s = s.replace('width=1560, gap=80, top=170, tail=96,', 'width=1560, gap=82, top=196, tail=70,')
s = s.replace('width=1560, gap=76, top=170, tail=96,', 'width=1560, gap=78, top=196, tail=70,')
open(p, "w", encoding="utf-8").write(s)
print("patched")
