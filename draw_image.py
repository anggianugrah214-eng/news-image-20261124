#!/usr/bin/env python3
"""Draw 'The World in One Day - 24 November 2026'.

A one-page newspaper front page summing up the world's news of
Tuesday 24 November 2026, drawn entirely in code with Pillow:
every panel, chart, ship and letter is a shape or text drawn here.
No photographs, no outside images, no network.

Run:  python3 draw_image.py
Writes: entry.png  (1024 x 1024, deterministic bytes)
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
CW = W - 2 * MARGIN  # 972 content width

PAPER = (246, 241, 230)
INK = (20, 20, 20)
RED = (178, 38, 30)
NAVY = (22, 42, 66)
NAVY_LT = (38, 68, 102)
TEAL = (15, 107, 92)
ORANGE = (214, 108, 0)
GOLD = (201, 162, 39)
GREY = (90, 86, 78)
RULE = (120, 114, 100)
PANEL_BG = (255, 253, 247)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    """Draw lines of text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) // 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x, y, w, fill=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations

def draw_scales(draw, x, y, w, h):
    """Scales of justice, centred in the box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    gold = (201, 162, 39)
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    # pillar
    draw.rectangle([cx - 5, cy - 62, cx + 5, cy + 62], fill=gold)
    draw.ellipse([cx - 16, cy - 78, cx + 16, cy - 62], fill=gold)
    draw.rectangle([cx - 46, cy + 62, cx + 46, cy + 70], fill=gold)
    # beam
    draw.rectangle([cx - 78, cy - 52, cx + 78, cy - 44], fill=gold)
    for s in (-1, 1):
        px = cx + s * 78
        draw.line([(px, cy - 48), (px - 30, cy + 8)], fill=gold, width=3)
        draw.line([(px, cy - 48), (px + 30, cy + 8)], fill=gold, width=3)
        draw.arc([px - 30, cy - 8, px + 30, cy + 34], 0, 180, fill=gold, width=5)
    # gavel, lower right
    draw.rectangle([x + w - 78, y + h - 52, x + w - 18, y + h - 40], fill=(120, 72, 32))
    draw.rectangle([x + w - 66, y + h - 78, x + w - 30, y + h - 52], fill=(150, 96, 44))


def draw_tanker(draw, x, y, w, h):
    """Oil tanker on waves, flames rising from its deck."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(18, 52, 74))
    sea_y = y + h - 42
    # hull
    draw.polygon([(x + 18, sea_y - 26), (x + w - 30, sea_y - 26),
                  (x + w - 52, sea_y + 6), (x + 30, sea_y + 6)], fill=(140, 40, 32))
    # deck + containers
    draw.rectangle([x + 34, sea_y - 52, x + 96, sea_y - 26], fill=(210, 180, 120))
    draw.rectangle([x + 104, sea_y - 46, x + 150, sea_y - 26], fill=(90, 140, 90))
    draw.rectangle([x + w - 118, sea_y - 58, x + w - 82, sea_y - 26], fill=(220, 220, 220))
    draw.rectangle([x + w - 80, sea_y - 44, x + w - 40, sea_y - 26], fill=(200, 200, 200))
    # funnel with smoke
    draw.rectangle([x + w - 130, sea_y - 66, x + w - 108, sea_y - 44], fill=(40, 40, 40))
    for i, r in enumerate((16, 12, 9)):
        draw.ellipse([x + w - 138 + i * 10, y + 18 + i * 16,
                       x + w - 138 + i * 10 + 2 * r, y + 18 + i * 16 + 2 * r],
                      fill=(200, 200, 200))
    # flames
    fx = x + 130
    for dx, fh, col in ((0, 46, ORANGE), (18, 34, (235, 170, 0)), (-18, 30, (235, 170, 0))):
        draw.polygon([(fx + dx - 12, sea_y - 52), (fx + dx, sea_y - 52 - fh),
                      (fx + dx + 12, sea_y - 52)], fill=col)
    # waves
    for wy in (sea_y + 12, sea_y + 26):
        for k in range(4):
            wx = x + 6 + k * 48
            draw.arc([wx, wy - 8, wx + 44, wy + 8], 180, 360, fill=(150, 200, 230), width=4)


def draw_drone_ship(draw, x, y, w, h):
    """Quadcopter drone above a ship at sea."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(16, 58, 74))
    sea_y = y + h - 30
    # ship
    draw.polygon([(x + 30, sea_y - 18), (x + w - 40, sea_y - 18),
                  (x + w - 62, sea_y + 8), (x + 46, sea_y + 8)], fill=(120, 120, 120))
    draw.rectangle([x + 70, sea_y - 40, x + 130, sea_y - 18], fill=(200, 200, 200))
    draw.rectangle([x + 96, sea_y - 58, x + 104, sea_y - 40], fill=(200, 200, 200))
    # drone
    dx, dy = x + w - 70, y + 42
    draw.ellipse([dx - 22, dy - 10, dx + 22, dy + 10], fill=(220, 220, 220))
    for sx, sy in ((-34, -16), (34, -16), (-34, 16), (34, 16)):
        draw.line([(dx, dy), (dx + sx, dy + sy)], fill=(220, 220, 220), width=3)
        draw.ellipse([dx + sx - 14, dy + sy - 4, dx + sx + 14, dy + sy + 4],
                     outline=(235, 200, 60), width=3)
    draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=RED)
    # dashed strike line from drone to ship
    for i in range(5):
        yy = dy + 26 + i * 12
        draw.line([(dx - 40, yy), (dx - 40, yy + 6)], fill=(235, 200, 60), width=3)
    # waves
    for k in range(4):
        wx = x + 6 + k * 48
        draw.arc([wx, sea_y + 12, wx + 44, sea_y + 24], 180, 360, fill=(150, 200, 230), width=4)


def draw_chart(draw, x, y, w, h):
    """Falling market chart with a red arrow."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(24, 36, 52))
    gx0, gy0, gx1, gy1 = x + 22, y + 14, x + w - 14, y + h - 22
    for gy in range(gy0, gy1, 22):
        draw.line([(gx0, gy), (gx1, gy)], fill=(52, 68, 92), width=1)
    pts = [(gx0, gy0 + 8), (gx0 + 30, gy0 + 22), (gx0 + 60, gy0 + 16),
           (gx0 + 90, gy0 + 44), (gx0 + 120, gy0 + 62), (gx0 + 150, gy0 + 96)]
    draw.line(pts, fill=(235, 200, 60), width=4, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(235, 200, 60))
    # down arrow at the end
    ex, ey = pts[-1]
    draw.polygon([(ex - 2, ey - 26), (ex + 12, ey - 26), (ex + 5, ey - 8)], fill=RED)
    draw.rectangle([ex + 1, ey - 10, ex + 9, ey + 14], fill=RED)


def draw_tower(draw, x, y, w, h):
    """Tall glass tower with smoke and a small drone."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 44, 66))
    tx = x + w // 2 - 34
    ty = y + 22
    draw.polygon([(tx, ty + h - 40), (tx + 68, ty + h - 40),
                  (tx + 58, ty), (tx + 10, ty)], fill=(90, 130, 170))
    for row in range(6):
        wy = ty + 18 + row * 16
        for col in range(3):
            wx = tx + 14 + col * 18
            draw.rectangle([wx, wy, wx + 10, wy + 8], fill=(190, 220, 245))
    # smoke
    for i, r in enumerate((14, 10, 7)):
        draw.ellipse([tx + 52 + i * 12, ty - 6 + i * 12,
                       tx + 52 + i * 12 + 2 * r, ty - 6 + i * 12 + 2 * r],
                      fill=(200, 200, 200))
    # drone
    dx, dy = x + w - 52, y + 30
    draw.ellipse([dx - 10, dy - 4, dx + 10, dy + 4], fill=(220, 220, 220))
    draw.line([(dx - 20, dy - 6), (dx + 20, dy - 6)], fill=(220, 220, 220), width=2)


def draw_trophy(draw, x, y, w, h):
    """Gold trophy cup with a football."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(20, 60, 46))
    cx = x + w // 2
    cy = y + h // 2 - 6
    # handles
    draw.arc([cx - 58, cy - 34, cx - 18, cy + 6], 90, 270, fill=GOLD, width=6)
    draw.arc([cx + 18, cy - 34, cx + 58, cy + 6], 270, 90, fill=GOLD, width=6)
    # cup
    draw.polygon([(cx - 34, cy - 40), (cx + 34, cy - 40), (cx + 22, cy + 8),
                  (cx - 22, cy + 8)], fill=GOLD)
    draw.rectangle([cx - 5, cy + 8, cx + 5, cy + 26], fill=GOLD)
    draw.rectangle([cx - 26, cy + 26, cx + 26, cy + 34], fill=GOLD)
    # ball
    bx, by = x + w - 42, y + h - 30
    draw.ellipse([bx - 15, by - 15, bx + 15, by + 15], fill=(240, 240, 240))
    draw.polygon([(bx, by - 7), (bx + 7, by - 2), (bx + 4, by + 6),
                  (bx - 4, by + 6), (bx - 7, by - 2)], fill=INK)


# ---------------------------------------------------------------- page build

def story_panel(draw, x, y, w, h, kicker, headline, deck, art, art_w=200):
    """A bordered panel: kicker, headline, deck, illustration on the right."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=PANEL_BG, outline=INK, width=2)
    tx = x + 14
    tw = w - art_w - 28
    cy = y + 10
    draw.text((tx, cy), kicker, font=font(SANS_B, 13), fill=RED)
    cy += 20
    hl = wrap(draw, headline, font(SERIF_B, 23), tw)
    cy = text_block(draw, tx, cy, hl, font(SERIF_B, 23), leading=26)
    cy += 4
    dl = wrap(draw, deck, font(SANS, 15), tw)
    text_block(draw, tx, cy, dl, font(SANS, 15), leading=19)
    art(draw, x + w - art_w - 8, y + 8, art_w, h - 16)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = MARGIN

    # ---- masthead
    d.text((MARGIN, y), "ONE DAY  ·  ONE PICTURE  ·  THE WORLD'S NEWS",
           font=font(SANS_B, 13), fill=GREY)
    d.text((MARGIN + CW - d.textlength("TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 13)),
            y), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 13), fill=RED)
    y += 22
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 58)
    d.text(((W - d.textlength(title, font=tf)) // 2, y), title, font=tf, fill=INK)
    y += 74
    hrule(d, MARGIN, y, CW, width=3)
    y += 8
    date_line = "TUESDAY, 24 NOVEMBER 2026"
    df = font(SERIF_B, 22)
    d.text(((W - d.textlength(date_line, font=df)) // 2, y), date_line, font=df, fill=INK)
    y += 30
    hrule(d, MARGIN, y, CW, width=2)
    y += 10

    # ---- lead story: Huawei verdict
    lead_h = 224
    d.rectangle([MARGIN, y, MARGIN + CW - 1, y + lead_h - 1],
                fill=PANEL_BG, outline=INK, width=2)
    lx, lw = MARGIN + 16, 600
    cy = y + 12
    d.text((lx, cy), "LEAD  ·  UNITED STATES", font=font(SANS_B, 14), fill=RED)
    cy += 22
    hl = wrap(d, "HUAWEI GUILTY IN U.S. TRADE-SECRETS TRIAL",
              font(SERIF_B, 40), lw)
    cy = text_block(d, lx, cy, hl, font(SERIF_B, 40), leading=44)
    cy += 6
    deck = ("A New York jury convicts the Chinese telecom giant on 10 of 12 "
            "counts \u2014 conspiracy to steal trade secrets, bank fraud and "
            "sanctions violations \u2014 but clears it of racketeering. "
            "Huawei says it will appeal; sentencing is set for September 2027.")
    dl = wrap(d, deck, font(SANS, 17), lw)
    text_block(d, lx, cy, dl, font(SANS, 17), leading=22)
    draw_scales(d, MARGIN + CW - 330, y + 10, 314, lead_h - 20)
    y += lead_h + 8

    # ---- two rows of two stories
    row_h = 168
    col_w = (CW - 8) // 2
    story_panel(d, MARGIN, y, col_w, row_h,
                "STRAIT OF HORMUZ",
                "HORMUZ IN FLAMES",
                "Iran says four tankers hit mines in the strait. Its Guard "
                "says it attacked a ship. Monitors: unconfirmed.",
                draw_tanker)
    story_panel(d, MARGIN + col_w + 8, y, col_w, row_h,
                "WAR IN UKRAINE",
                "UKRAINE'S SEA DRONES STRIKE",
                "Kyiv says its sea drones hit Russian ships off Libya and "
                "in the Gulf of Finland.",
                draw_drone_ship)
    y += row_h + 8
    story_panel(d, MARGIN, y, col_w, row_h,
                "WALL STREET",
                "NVIDIA'S RALLY FADES",
                "Shares fall about 8% a day after surging 32% on Jensen "
                "Huang's return as CEO. S&P -0.5%; Nasdaq -1.5%.",
                draw_chart)
    story_panel(d, MARGIN + col_w + 8, y, col_w, row_h,
                "SAUDI ARABIA",
                "DRONE HITS RIYADH TOWER",
                "A suspected Houthi drone strikes the PIF tower in Riyadh, "
                "wounding 11 \u2014 the second hit in under a week.",
                draw_tower)
    y += row_h + 8

    # ---- sport band: Senegal
    band_h = 96
    d.rectangle([MARGIN, y, MARGIN + CW - 1, y + band_h - 1],
                fill=PANEL_BG, outline=INK, width=2)
    draw_trophy(d, MARGIN + 8, y + 8, 150, band_h - 16)
    tx = MARGIN + 172
    d.text((tx, y + 10), "SPORT  ·  FOOTBALL", font=font(SANS_B, 13), fill=RED)
    hl = wrap(d, "SENEGAL CHAMPIONS AGAIN", font(SERIF_B, 30), CW - 200)
    cy = text_block(d, tx, y + 30, hl, font(SERIF_B, 30), leading=34)
    deck = ("The Court of Arbitration for Sport reinstates Senegal as winners "
            "of the 2025 Africa Cup of Nations.")
    dl = wrap(d, deck, font(SANS, 15), CW - 200)
    text_block(d, tx, cy + 2, dl, font(SANS, 15), leading=19)
    y += band_h + 8

    # ---- also today strip
    strip_h = 120
    d.rectangle([MARGIN, y, MARGIN + CW - 1, y + strip_h - 1],
                fill=(232, 226, 210), outline=INK, width=2)
    d.text((MARGIN + 12, y + 8), "ALSO TODAY", font=font(SANS_B, 14), fill=RED)
    items = [
        "Gaza issues a meningitis epidemic alert after cases surge eightfold.",
        "Israeli strike kills Hamas internal security chief in Gaza.",
        "Turkish military helicopter crashes, killing five crew.",
        "Gunmen hold 25 hostage in a Cartagena supermarket.",
        "EU proposes UN voting reform after COP31 ends with no deal.",
        "El Chapo Isidro captured in Mexico with U.S. drone help.",
    ]
    col_w2 = (CW - 24) // 2
    for i, item in enumerate(items):
        cx = MARGIN + 12 + (i % 2) * col_w2
        cy2 = y + 32 + (i // 2) * 30
        d.text((cx, cy2), "\u25aa", font=font(SANS_B, 13), fill=RED)
        lines = wrap(d, item, font(SANS, 14), col_w2 - 20)
        text_block(d, cx + 16, cy2, lines[:1], font(SANS, 14), leading=18)
    y += strip_h + 8

    # ---- footer
    foot = ("Every event above happened, or was first reported, on 24 November 2026  ·  "
            "Drawn entirely in code \u2014 no photographs")
    ff = font(SANS, 13)
    d.text(((W - d.textlength(foot, font=ff)) // 2, y), foot, font=ff, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
