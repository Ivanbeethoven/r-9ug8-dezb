#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Draw the layered architecture figure (figure 1) with Pillow."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "figures", "arch.png")
FONT = r"C:\Windows\Fonts\msyh.ttc"
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"

W, H = 1680, 1020
BG = (255, 255, 255)

BAND = {
    "ctrl": ((238, 243, 250), (176, 196, 222)),
    "exec": ((243, 248, 236), (176, 196, 152)),
    "data": ((252, 246, 238), (214, 186, 150)),
}
BOX_FILL = (255, 255, 255)
BOX_EDGE = (70, 82, 100)
TEXT = (32, 40, 52)
ACCENT = (31, 58, 95)
NOTE = (96, 106, 120)


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def text_w(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def box(draw, x, y, w, h, lines, size=26, bold=False, label=None, label_size=26):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=BOX_FILL, outline=BOX_EDGE, width=3)
    top = y
    if label:
        f = font(label_size, True)
        draw.text((x + 18, y + 10), label, font=f, fill=ACCENT)
        top = y + 10 + label_size + 12
    f = font(size, bold)
    lh = size + 12
    total = lh * len(lines) - 12
    cy = top + ((y + h - top) - total) / 2
    for i, line in enumerate(lines):
        tw = text_w(draw, line, f)
        draw.text((x + (w - tw) / 2, cy + i * lh - 3), line, font=f, fill=TEXT)


def band(draw, x, y, w, h, label, key):
    fill, edge = BAND[key]
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fill, outline=edge, width=3)
    draw.text((x + 22, y + 12), label, font=font(25, True), fill=ACCENT)


def arrow(draw, p1, p2, color=(90, 104, 124), width=4):
    draw.line([p1, p2], fill=color, width=width)
    (x1, y1), (x2, y2) = p1, p2
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 16
    for d in (0.45, -0.45):
        draw.line([(x2, y2), (x2 - L * math.cos(ang - d), y2 - L * math.sin(ang - d))],
                  fill=color, width=width)


def note(draw, x, y, lines, size=22, gap=34):
    for i, line in enumerate(lines):
        draw.text((x, y + i * gap), line, font=font(size), fill=NOTE)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------------- band 1: control plane
    band(d, 40, 30, 1600, 180, "控制面", "ctrl")
    box(d, 90, 92, 300, 84, ["蚂蚁管控面 / K8s"])
    box(d, 470, 92, 240, 84, ["沙箱调度"])
    box(d, 790, 84, 340, 100, ["containerd 创建", "镜像 / 任务生命周期"], size=24)
    arrow(d, (390, 134), (466, 134))
    arrow(d, (710, 134), (786, 134))
    note(d, 1180, 100, ["请求下发、调度决策、任务创建", "并发下争用锁、队列与 GC"])

    # ---------------- band 2: execution plane
    band(d, 40, 254, 1600, 330, "执行面：runD guest（进程 / 网络 / 权限隔离）", "exec")
    box(d, 90, 330, 300, 200, ["runD 运行时", "启动 / 恢复", "执行状态固化"], size=24)
    box(d, 470, 306, 400, 250, [], label="BrewFS 工作区隔离", label_size=24)
    box(d, 492, 372, 356, 60, ["只读基座（lower）", "Nydus EROFS 镜像层"], size=20)
    box(d, 492, 452, 356, 60, ["私有增量层（upper）"], size=21)
    box(d, 950, 330, 320, 200, ["BrewFS FUSE", "文件视图挂载"], size=24)
    arrow(d, (390, 430), (466, 430))
    arrow(d, (870, 430), (946, 430))
    note(d, 1300, 372, ["文件视图与增量", "与执行状态共用", "同一检查点标识"])

    # ---------------- band 3: data plane
    band(d, 40, 624, 1600, 358, "数据面：BrewFS（文件视图、版本事务与对象数据）", "data")
    box(d, 90, 700, 220, 84, ["VFS"])
    box(d, 380, 700, 300, 84, ["元数据事务"])
    box(d, 750, 700, 280, 84, ["元数据后端", "Redis / TiKV"], size=22)
    box(d, 1100, 700, 340, 84, ["写者租约 + 代次", "恰好一个写者"], size=22)
    box(d, 380, 848, 300, 84, ["多级缓存 / 写回"], size=23)
    box(d, 750, 848, 280, 84, ["OSS"], size=24)
    arrow(d, (310, 742), (376, 742))
    arrow(d, (680, 742), (746, 742))
    arrow(d, (1034, 742), (1096, 742))
    arrow(d, (530, 784), (530, 844))
    arrow(d, (680, 890), (746, 890))
    note(d, 1100, 812, ["每次提交核验所有权与代次", "旧写者不得发布可见引用"])

    # ---------------- cross-band arrows
    arrow(d, (960, 184), (960, 250), color=(120, 132, 150))
    arrow(d, (1110, 530), (1110, 620), color=(120, 132, 150))
    note(d, 1124, 548, ["挂载后接收文件请求"], size=21)

    img.save(OUT, "PNG")
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
