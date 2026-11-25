#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026 and save entry.png.

Pure Pillow drawing, no network, no randomness beyond a fixed seed, so the
output is byte-identical on every run. Run: python3 render.py
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (179, 32, 44)
NAVY = (11, 30, 58)
GREY = (90, 88, 82)
LIGHT = (255, 255, 255)
AMBER = (255, 176, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_skyline(draw, rng, base_y, color, min_h, max_h, lit):
    x = 36
    while x < 988:
        bw = rng.randint(34, 74)
        bh = rng.randint(min_h, max_h)
        draw.rectangle([x, base_y - bh, x + bw, base_y], fill=color)
        if lit:
            for wy in range(base_y - bh + 8, base_y - 6, 14):
                for wx in range(x + 6, x + bw - 6, 12):
                    if rng.random() < 0.28:
                        draw.rectangle([wx, wy, wx + 5, wy + 7],
                                       fill=(255, 196, 90))
        x += bw + rng.randint(2, 10)


def build():
    rng = random.Random(24)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img, "RGBA")
    # Masthead.
    draw.line([(36, 26), (988, 26)], fill=INK, width=3)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=SERIF_B(56))
    draw.text(((W - tw) / 2, 34), title, font=SERIF_B(56), fill=INK)
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = draw.textlength(date, font=SANS_B(24))
    draw.text(((W - dw) / 2, 100), date, font=SANS_B(24), fill=RED)
    draw.line([(36, 128), (988, 128)], fill=INK, width=2)
    # Hero: night sky.
    top, bot = (8, 20, 44), (38, 74, 110)
    for yy in range(130, 520):
        draw.line([(36, yy), (988, yy)],
                  fill=lerp(top, bot, (yy - 130) / 390))
    for _ in range(70):
        sx, sy = rng.randint(40, 984), rng.randint(134, 300)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 228, 240))
    draw.ellipse([880, 150, 936, 206], fill=(232, 230, 214))
    draw.ellipse([896, 162, 912, 178], fill=(208, 206, 190))
    draw_skyline(draw, rng, 520, (22, 40, 66), 60, 170, False)
    draw_skyline(draw, rng, 520, (13, 26, 46), 40, 120, True)
    # Blast glow and smoke, drawn before the tower so the tower stays crisp.
    ex, ey = 545, 290
    for rad, alpha in ((80, 55), (55, 90), (32, 135)):
        draw.ellipse([ex - rad, ey - rad, ex + rad, ey + rad],
                     fill=(255, 150, 40, alpha))
    for cx, cy, cr in ((500, 232, 15), (478, 210, 11), (556, 222, 12)):
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                     fill=(70, 72, 84, 200))
    # PIF Tower.
    tx0, tx1, top_y = 430, 522, 196
    draw.polygon([(tx0, 520), (tx0, top_y + 46), (tx1, top_y),
                  (tx1, 520)], fill=(30, 52, 88))
    draw.polygon([(tx0, top_y + 46), (tx1, top_y), (tx1, top_y - 26),
                  (tx0, top_y + 20)], fill=(52, 84, 128))
    for yy in range(top_y + 58, 512, 18):
        for xx in range(tx0 + 8, tx1 - 8, 14):
            if rng.random() < 0.45:
                draw.rectangle([xx, yy, xx + 6, yy + 9], fill=(255, 196, 90))
    # Flames licking the tower's right edge at the strike point.
    ex, ey = 522, 282
    draw.polygon([(ex - 30, ey + 46), (ex - 12, ey - 22), (ex + 2, ey + 24),
                  (ex + 18, ey - 34), (ex + 34, ey + 44)],
                 fill=(255, 196, 60))
    draw.polygon([(ex - 14, ey + 32), (ex - 2, ey - 8), (ex + 12, ey + 30)],
                 fill=(255, 120, 30))
    # Drone silhouette above the tower.
    dx, dy = 600, 225
    draw.ellipse([dx - 16, dy - 8, dx + 16, dy + 8], fill=(10, 10, 12))
    draw.line([(dx - 30, dy - 12), (dx + 30, dy - 12)], fill=(10, 10, 12),
              width=4)
    draw.ellipse([dx - 34, dy - 16, dx - 26, dy - 8], fill=(10, 10, 12))
    draw.ellipse([dx + 26, dy - 16, dx + 34, dy - 8], fill=(10, 10, 12))
    draw.ellipse([dx - 4, dy - 3, dx + 4, dy + 5], fill=(255, 60, 60))
    # Hero caption bar.
    draw.rectangle([36, 424, 988, 520], fill=(0, 0, 0, 170))
    draw.text((56, 434), "RIYADH  ·  SAUDI ARABIA",
              font=SANS_B(20), fill=AMBER)
    head = "DRONE ATTACK HITS RIYADH'S TALLEST TOWER"
    draw.text((56, 458), head, font=SANS_B(34), fill=LIGHT)
    deck = "Houthi strike on the PIF Tower injures 11 in the capital's financial district"
    draw.text((56, 496), deck, font=SANS(19), fill=(225, 225, 225))
    # Three columns.
    cols = [
        ("HUAWEI FOUND GUILTY",
         "A New York jury convicts the tech giant of bank fraud and "
         "trade-secret theft.", "gavel"),
        ("MINES IN THE STRAIT OF HORMUZ",
         "Three tankers hit mines and burn; Iran refuses talks until "
         "seven conditions are met.", "ship"),
        ("14 NATIONS BACK ICJ RULING",
         "Britain, Spain, Canada and Australia are among 14 nations "
         "affirming the genocide finding.", "scales"),
    ]
    x = 36
    for title, deck, icon in cols:
        draw.rectangle([x, 536, x + 300, 540], fill=RED)
        draw_icon(draw, x + 4, 548, icon)
        y = 616
        y = text_block(draw, x, y, wrap(draw, title, SANS_B(26), 300),
                       SANS_B(26), INK, 30)
        y += 6
        text_block(draw, x, y + 4, wrap(draw, deck, SANS(18), 300),
                   SANS(18), GREY, 23)
        x += 326
    draw.line([(36, 766), (988, 766)], fill=INK, width=2)
    # Also today strip.
    draw.text((36, 778), "ALSO TODAY", font=SANS_B(22), fill=RED)
    items = [
        ("NVIDIA REINSTATES JENSEN HUANG",
         "Shares jump after the board brings back its chief executive."),
        ("NEPAL QUAKE 5.6",
         "Tremor strikes near the Chinese border."),
        ("GAZA STRIKES KILL HAMAS SECURITY CHIEF",
         "Seven reported dead in Gaza City."),
        ("COP31 ENDS WITH NO DEAL",
         "EU and UK reject a text that omits fossil fuels."),
        ("SENEGAL REGAIN AFRICA CUP",
         "Court restores the 2025 title from Morocco."),
        ("TRUMP READIES TARIFFS ON 16 ECONOMIES",
         "China, the EU and Japan among them."),
    ]
    y = 804
    for i in range(0, 6, 2):
        for j, xx in enumerate((36, 524)):
            t, d = items[i + j]
            draw.rectangle([xx, y + 4, xx + 10, y + 14], fill=RED)
            draw.text((xx + 18, y), t, font=SANS_B(17), fill=INK)
            draw.text((xx + 18, y + 21), d, font=SANS(16), fill=GREY)
        y += 44
    # Footer.
    draw.line([(36, 944), (988, 944)], fill=INK, width=2)
    foot = "Reported on 24 November 2026  ·  Sources: BBC, Al Jazeera, Reuters, Associated Press"
    fw = draw.textlength(foot, font=SANS(16))
    draw.text(((W - fw) / 2, 954), foot, font=SANS(16), fill=GREY)
    return img


def draw_icon(draw, x, y, kind):
    if kind == "gavel":
        draw.polygon([(x + 8, y + 44), (x + 44, y + 8), (x + 54, y + 18),
                      (x + 18, y + 54)], fill=RED)
        draw.line([(x + 30, y + 30), (x + 58, y + 58)], fill=INK, width=7)
        draw.line([(x + 4, y + 58), (x + 30, y + 58)], fill=INK, width=5)
    elif kind == "ship":
        draw.polygon([(x + 4, y + 30), (x + 60, y + 30), (x + 52, y + 52),
                      (x + 12, y + 52)], fill=RED)
        draw.rectangle([x + 14, y + 12, x + 26, y + 30], fill=INK)
        draw.rectangle([x + 30, y + 16, x + 42, y + 30], fill=INK)
        for cx in (x + 8, x + 56):
            draw.ellipse([cx - 5, y + 4, cx + 5, y + 14], fill=INK)
    else:  # scales
        draw.line([(x + 32, y + 4), (x + 32, y + 52)], fill=INK, width=5)
        draw.line([(x + 8, y + 12), (x + 56, y + 12)], fill=INK, width=5)
        draw.polygon([(x + 2, y + 34), (x + 14, y + 34), (x + 8, y + 14)],
                     fill=RED)
        draw.polygon([(x + 50, y + 34), (x + 62, y + 34), (x + 56, y + 14)],
                     fill=RED)
        draw.line([(x + 20, y + 52), (x + 44, y + 52)], fill=INK, width=5)


def main():
    img = build()
    out = HERE / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
