#!/usr/bin/env python3
"""生成 Landrop 项目图标（Pillow 绘制，可复现）。

输出到 assets/: icon.png(1024) / icon-512/256/128/64.png
用法: python3 tools/make_icons.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter

S = 1024          # 母版尺寸
RADIUS = 224      # 圆角（iOS 风格 22%）
C1 = (79, 140, 255)    # #4F8CFF 左上（网页主题蓝）
C2 = (62, 207, 142)    # #3ECF8E 右下（网页成功绿）

# 纸飞机几何（Feather "send" 形状，24 网格 ×34 + 偏移居中）
TIP = (852, 142)    # 机头
FIN = (614, 822)    # 下折翼尖
NOTCH = (478, 516)  # 折痕中点
TAIL = (172, 380)   # 尾部


def gradient_bg():
    """对角渐变底：左上蓝 → 右下绿。"""
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * (S - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(C1, C2))
    return img


def rounded_mask():
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, S, S], radius=RADIUS, fill=255)
    return m


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))

    bg = gradient_bg().convert("RGBA")

    # 投影层：整体机身形状右下偏移 + 高斯模糊
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.polygon([TIP, FIN, NOTCH, TAIL], fill=(10, 20, 40, 90))
    shadow = shadow.transform((S, S), Image.AFFINE, (1, 0, 0, 0, 1, 26))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))

    # 机身两个受光面
    plane = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plane)
    pd.polygon([TIP, NOTCH, TAIL], fill=(255, 255, 255, 255))   # 上主翼
    pd.polygon([TIP, FIN, NOTCH], fill=(255, 255, 255, 214))    # 下折面（暗一档）

    # 顶部高光
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    for i in range(int(S * 0.45)):
        gd.line([(0, i), (S, i)], fill=(255, 255, 255, max(0, 56 - int(56 * i / (S * 0.45)))))

    composed = bg
    for layer in (shadow, plane, gloss):
        composed = Image.alpha_composite(composed, layer)

    master = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    master.paste(composed, (0, 0), rounded_mask())
    master.save("icon.png")

    for size in (512, 256, 128, 64):
        master.resize((size, size), Image.LANCZOS).save(f"icon-{size}.png")

    print("生成完成:", ", ".join(["icon.png"] + [f"icon-{s}.png" for s in (512, 256, 128, 64)]))


if __name__ == "__main__":
    main()
