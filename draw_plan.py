#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Draw the 12-month roadmap figure (figure 4) with Pillow."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "figures", "roadmap.png")
FONT = r"C:\Windows\Fonts\msyh.ttc"
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"

W, H = 1560, 660
TEXT = (32, 40, 52)
ACCENT = (31, 58, 95)
NOTE = (105, 115, 130)
CARD = (255, 255, 255)
EDGE = (150, 165, 185)
BAND_FILL = [(233, 240, 250), (233, 244, 233), (250, 243, 230), (243, 236, 246)]
BAND_EDGE = [(140, 160, 190), (150, 180, 150), (200, 175, 130), (175, 150, 190)]


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    phases = [
        ("Q1", "2027-02 — 04", "格式对齐", ["格式与接口规范 v1", "兼容矩阵与三类镜像基线", "lazyload 挂载与 fork 演示"]),
        ("Q2", "2027-05 — 07", "原型实现", ["原型 v0.1", "冷启动与 C/R 复现脚本", "中期报告与初测分布"]),
        ("Q3", "2027-08 — 10", "蚂蚁环境联调", ["联调版本 v0.2", "100 并发长尾定位", "消融与跨环境复测"]),
        ("Q4", "2027-11 — 2028-01", "指标收敛与结题", ["原型 v1.0 与验收包", "论文底稿与专利交底", "结项报告与开源 PR"]),
    ]

    n = len(phases)
    gap = 42
    x0, x1 = 44, W - 44
    cw = (x1 - x0 - gap * (n - 1)) / n
    top, bottom = 132, 512

    for i, (q, date, name, items) in enumerate(phases):
        x = x0 + i * (cw + gap)
        d.rounded_rectangle([x, top, x + cw, bottom], radius=12, fill=CARD, outline=EDGE, width=3)
        d.rounded_rectangle([x, top, x + cw, top + 104], radius=12, fill=BAND_FILL[i], outline=BAND_EDGE[i], width=0)
        d.text((x + 20, top + 14), q, font=font(34, True), fill=ACCENT)
        d.text((x + 20, top + 62), date, font=font(21), fill=NOTE)
        f_name = font(23, True)
        d.text((x + 20, top + 122), name, font=f_name, fill=TEXT)
        for j, it in enumerate(items):
            y = top + 168 + j * 46
            d.ellipse([x + 20, y + 9, x + 28, y + 17], fill=ACCENT)
            d.text((x + 38, y), it, font=font(21), fill=TEXT)
        if i < n - 1:
            ax = x + cw
            d.line([(ax + 6, (top + bottom) / 2), (ax + gap - 8, (top + bottom) / 2)], fill=(120, 132, 150), width=4)
            ang = 0
            L = 14
            for dd in (0.5, -0.5):
                d.line([(ax + gap - 8, (top + bottom) / 2),
                        (ax + gap - 8 - L * math.cos(ang - dd), (top + bottom) / 2 - L * math.sin(ang - dd))],
                       fill=(120, 132, 150), width=4)

    # milestone spine
    y_spine = 70
    d.line([(x0, y_spine), (x1, y_spine)], fill=(200, 208, 220), width=3)
    mid_x = x0 + 2 * (cw + gap) - gap / 2
    for mx, label in ((mid_x, "中期检查 2027-07-31"), (x0 + 3 * (cw + gap) + cw / 2, "结项验收 2028-01-31")):
        d.ellipse([mx - 8, y_spine - 8, mx + 8, y_spine + 8], fill=ACCENT)
        f = font(21, True)
        d.text((mx - tw(d, label, f) / 2, y_spine + 18), label, font=f, fill=ACCENT)

    d.text((x0, 566), "关键路径：格式对齐 → 原型 → 联调 → 指标收敛 → 论文与专利；回归测试与故障注入贯穿全周期",
           font=font(21), fill=NOTE)

    img.save(OUT, "PNG")
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
