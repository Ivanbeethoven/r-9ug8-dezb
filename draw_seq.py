#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Draw the two sequence figures (cold start, checkpoint/restore) with Pillow."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "figures")
FONT = r"C:\Windows\Fonts\msyh.ttc"
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"

TEXT = (32, 40, 52)
ACCENT = (31, 58, 95)
NOTE = (105, 115, 130)
LINE = (88, 100, 118)
HEAD_FILL = (233, 240, 250)
HEAD_EDGE = (140, 160, 190)


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def tw(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def arrow_head(draw, p1, p2, color=LINE, size=14):
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for dd in (0.42, -0.42):
        draw.line([p2, (p2[0] - size * math.cos(ang - dd), p2[1] - size * math.sin(ang - dd))],
                  fill=color, width=3)


def sequence(path, title, parts, steps, width=1560, head_h=92, gap=76, top=150, tail=70):
    height = top + gap * len(steps) + tail
    img = Image.new("RGB", (width, height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    n = len(parts)
    xs = [int(width * (i + 1) / (n + 1)) for i in range(n)]

    if title:
        f_title = font(26, True)
        d.text(((width - tw(d, title, f_title)) / 2, 16), title, font=f_title, fill=ACCENT)

    # participant headers
    f_head = font(23, True)
    for x, name in zip(xs, parts):
        w = max(tw(d, name, f_head) + 34, 150)
        d.rounded_rectangle([x - w / 2, 62, x + w / 2, 62 + head_h], radius=8,
                            fill=HEAD_FILL, outline=HEAD_EDGE, width=2)
        d.text((x - tw(d, name, f_head) / 2, 62 + (head_h - 24) / 2 - 2), name, font=f_head, fill=TEXT)

    y0 = 62 + head_h
    for x in xs:
        y = y0
        while y < height - 30:
            d.line([(x, y), (x, min(y + 7, height - 30))], fill=(190, 198, 210), width=2)
            y += 14

    f_msg = font(22)
    f_tag = font(19)
    for i, (a, b, label, tag, kind) in enumerate(steps):
        y = top + i * gap
        if kind == "self":
            x = xs[a]
            d.line([(x, y), (x + 62, y), (x + 62, y + 26), (x, y + 26)], fill=LINE, width=3)
            arrow_head(d, (x + 20, y + 26), (x, y + 26))
            d.text((x + 76, y - 6), label, font=f_msg, fill=TEXT)
            if tag:
                d.text((x + 76, y + 20), tag, font=f_tag, fill=NOTE)
            continue
        x1, x2 = xs[a], xs[b]
        dash = kind == "ret"
        if dash:
            step = 12
            sgn = 1 if x2 > x1 else -1
            x = x1
            while (x2 - x) * sgn > 0:
                xe = x + sgn * min(step, abs(x2 - x))
                d.line([(x, y), (xe, y)], fill=LINE, width=3)
                x = xe + sgn * step
            arrow_head(d, (x2 - 12 * sgn, y), (x2, y))
        else:
            d.line([(x1, y), (x2, y)], fill=LINE, width=3)
            arrow_head(d, (x1, y), (x2, y))
        cx = (x1 + x2) / 2
        label_w = tw(d, label, f_msg)
        d.text((cx - label_w / 2, y - 34), label, font=f_msg, fill=TEXT)
        if tag:
            tag_w = tw(d, tag, f_tag)
            d.text((cx - tag_w / 2, y + 6), tag, font=f_tag, fill=NOTE)

    img.save(path, "PNG")
    print("saved", path, img.size)


def main():
    os.makedirs(FIG, exist_ok=True)

    seq1 = [
        (0, 1, "下发创建请求", "[段1 100 / 10 ms]", "call"),
        (1, 3, "节点绑定、预备基础 guest", "[并入 runD 段]", "call"),
        (1, 2, "申请工作区：元数据清单与挂载", "[段2 100 / 10 ms]", "call"),
        (2, 4, "取元数据清单、索引与租约", "[并入段3]", "call"),
        (4, 2, "返回已校验元数据", "", "ret"),
        (2, 1, "视图挂载完成，租约就绪", "", "ret"),
        (3, 2, "guest 内建立 FUSE 挂载", "", "call"),
        (3, 4, "lazyload 读取启动必读数据", "[段3 500 / 40 ms]", "call"),
        (4, 3, "解码、校验后按需返回", "", "ret"),
        (3, 3, "启动应用 / 恢复执行状态", "[段4 100 / 20 ms]", "self"),
        (3, 1, "探针通过，沙箱就绪", "", "ret"),
        (1, 0, "返回就绪给调用方", "", "ret"),
    ]
    sequence(
        os.path.join(FIG, "seq-start.png"),
        "",
        ["管控面 / K8s", "调度 / containerd", "工作区服务", "runD / guest", "OSS / 缓存"],
        seq1,
        width=1560, gap=82, top=196, tail=70,
    )

    seq2 = [
        (0, 3, "禁止新写入，暂停应用", "", "call"),
        (3, 2, "排空写入并落盘，固定文件视图", "", "call"),
        (2, 4, "上传文件对象与元数据清单", "", "call"),
        (3, 4, "上传进程 / 内存 / 设备状态", "", "call"),
        (4, 2, "校验通过回执", "", "ret"),
        (2, 1, "核验租约与代次，原子发布", "", "call"),
        (1, 0, "生成快照引用", "", "ret"),
        (0, 2, "解析快照，检查格式与兼容性", "", "call"),
        (2, 1, "取租约与新代次", "", "call"),
        (2, 2, "重建挂载，保持禁止写入", "", "self"),
        (2, 4, "读取并校验首触数据", "", "call"),
        (2, 3, "提交匹配的文件视图与状态", "", "call"),
        (3, 3, "恢复进程与内存状态并校验", "", "self"),
        (3, 2, "探针通过，复验租约后开写", "", "ret"),
    ]
    sequence(
        os.path.join(FIG, "seq-cr.png"),
        "",
        ["管控面 / K8s", "元数据后端", "工作区服务", "runD / guest", "OSS"],
        seq2,
        width=1560, gap=78, top=196, tail=70,
    )


if __name__ == "__main__":
    main()
