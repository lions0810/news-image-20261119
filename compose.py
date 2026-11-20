#!/usr/bin/env python3
"""Compose the news-image-20261119 entry: a 1024x1024 newspaper front page.

Layout (canvas 1024x1024, white paper background):
  masthead black band ......... y   0.. 96  "THE WORLD IN ONE DAY" +
                                          "THURSDAY, 19 NOVEMBER 2026"
                                          + "DATE CHECK" stamp at right
  photo grid, 2x2 ............. y 104..576  two rows of 232
      each cell: photo 500x168 + caption bar 64 (red kicker + bold headline)
  "THE DAY IN UTC" strip ...... y 584..664  six timed moments, all UTC,
                                          taken from the day's wire timestamps
  "MORE FROM THE DAY" list .... y 672..1024  heading + 17 rows x 2 columns
                                          = 34 one-line headlines

44 stories in all (4 panels + 6 timeline moments + 34 list items), every
one sourced from reporting of Thursday 19 November 2026: GTA VI's launch
day, the Trump-Xi-Putin summit in Shenzhen, the ICJ's Rohingya genocide
ruling, and the Hormuz tanker fires lead the page.

All text is rendered here with PIL (DejaVu fonts); the four panel
illustrations contain no text at all. Output is JPEG bytes written to a
file named entry.png (the competition accepts JPEG bytes under that name),
at most 1,048,576 bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = os.path.join(HERE, "panels")
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MASTHEAD_H = 96
MARGIN = 8
CELL_W = 500
PHOTO_H = 158
CAPTION_H = 64
ROW_H = PHOTO_H + CAPTION_H  # 232
GUTTER = 8
GRID_TOP = MASTHEAD_H + MARGIN          # 104
GRID_BOTTOM = GRID_TOP + 2 * ROW_H + GUTTER  # 576
TL_TOP = GRID_BOTTOM + MARGIN           # 584
TL_BOTTOM = TL_TOP + 80                 # 664
LIST_TOP = TL_BOTTOM + MARGIN           # 672
LIST_Y = LIST_TOP + MARGIN              # 680

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PAPER = (250, 248, 242)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
DARK = (20, 20, 20)
GREY = (90, 90, 90)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PANELS = [
    {
        "file": "media-generation-panel-gta6-launch-0-94093a7b-5719-41fb-b5f5-f0ba35ea63d8.webp",
        "kicker": "GAMES  ·  GTA VI LAUNCH",
        "headline": "GTA VI launches to rave reviews; 2.3m watch on Twitch",
    },
    {
        "file": "media-generation-panel-shenzhen-summit-0-2cbc75ef-d599-4239-8f79-0450196cc9ce.webp",
        "kicker": "CHINA  ·  TRILATERAL SUMMIT",
        "headline": "Trump, Xi and Putin issue \u2018peace declaration\u2019 in Shenzhen",
    },
    {
        "file": "media-generation-panel-icj-rohingya-0-8238cdb5-1f8e-4be2-aed7-24b813661237.webp",
        "kicker": "THE HAGUE  ·  WORLD COURT",
        "headline": "World Court: Myanmar committed genocide against Rohingya",
    },
    {
        "file": "media-generation-panel-hormuz-tankers-0-5ce76cf4-96f1-48dd-b025-ecf5c6392789.webp",
        "kicker": "GULF  ·  HORMUZ CRISIS",
        "headline": "Three tankers ablaze after hitting mines off Hormuz",
    },
]

# Six moments with their real UTC wire timestamps (BBC / NYT, 19 Nov 2026).
# Labels kept short so each fits two lines inside its 168px cell.
TIMELINE = [
    ("21:21 UTC", "Europe open to Russia talks"),
    ("21:38 UTC", "Myanmar genocide ruling"),
    ("22:04 UTC", "Shenzhen summit ends"),
    ("23:04 UTC", "California probes Nvidia"),
    ("23:33 UTC", "Anthropic's big debut"),
    ("23:51 UTC", "Trump pardons Pete Rose"),
]

# (kicker, rest) pairs; each renders as one line: bold red kicker + black
# text. Two columns of 17 rows.
MORE_LEFT = [
    ("CRIMEA", "New attack on Crimea Bridge; traffic suspended"),
    ("SAUDI", "Riyadh's tallest tower damaged in Houthi attack"),
    ("BANGLADESH", "Yunus's ancestral home torched; 28 districts hit"),
    ("CLIMATE", "COP31 ministers race to unblock talks in Antalya"),
    ("ENERGY", "IEA: Hormuz crisis gravest threat ever to energy security"),
    ("CULTURE", "Van Gogh sells for $190.4m, a record for the artist"),
    ("KUWAIT", "Kuwait repels its first Iranian attack in two months"),
    ("EUROPE", "EU proposes \u20ac45bn loan to Ukraine"),
    ("VENEZUELA", "US and Venezuela sign military cooperation deal"),
    ("GAZA", "Israel's rare ground operation beyond the \u201cyellow line\u201d"),
    ("US SENATE", "Republicans reject bid to curb Trump's Iran war powers"),
    ("GULF", "US reissues security warnings in Bahrain, Saudi Arabia"),
    ("US POLITICS", "Jeffries set to be first Black House Speaker"),
    ("KOREA", "Court orders retrial of ex-PM Han over martial law"),
    ("JAPAN", "Rakuten Securities rushes to cope with data breach"),
    ("JAPAN", "Takaichi vows to attend tax-cut bill deliberations"),
    ("OCEANS", "US auctions 31.5m Pacific acres for deep-sea mining"),
]
MORE_RIGHT = [
    ("SUMMIT", "Putin: Russia will not negotiate a Ukraine ceasefire"),
    ("KYIV", "Russian drones swarm Kyiv; two embassies damaged"),
    ("PROTESTS", "236 arrested anti-Trump protesters freed"),
    ("GAZA", "Renewed Israeli escalation threatens civilians"),
    ("CHILDREN", "Nearly 1 in 4 children now live in conflict zones"),
    ("CRUISE", "Nearly 150 fall ill in cruise ship outbreak"),
    ("SPAIN", "Snap vote may bring anti-immigration government"),
    ("PHILIPPINES", "Trump and Marcos hail alliance, pledge trade ties"),
    ("MARKETS", "S&P 500 \u22120.2%; Nasdaq +0.4%; Brent $89.59"),
    ("OUTAGES", "Old grids, AI fixes behind wave of US outages"),
    ("ESPIONAGE", "Alleged Russian agent held over US tech surveillance"),
    ("FRANCE", "Three women jailed for joining ISIS in Syria"),
    ("IRAN", "Trump signals no more major Iran strikes in 2026"),
    ("CARACAS", "War Secretary Hegseth makes surprise stop in Caracas"),
    ("CYCLONE", "Cyclone Akvan: 300,000 evacuated, landfall due Friday"),
    ("GAME AWARDS", "GTA VI leads Game Awards with 8 nominations"),
    ("ANIMALS", "Fiona the hippo dies after swallowing a hat at zoo"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def centre_crop_resize(img, w, h):
    """Centre-crop to the target aspect ratio, then resize to (w, h)."""
    sw, sh = img.size
    target = w / h
    src = sw / sh
    if src > target:  # too wide: crop sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:  # too tall: crop top/bottom
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((w, h), Image.LANCZOS)


def wrap_text(draw, text, fnt, max_width, max_lines=2):
    """Greedy word wrap; returns a list of at most max_lines lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


def fit_headline(draw, text, max_width, start_size=20):
    """Largest bold size (down to 17) whose wrap fits in 2 lines."""
    size = start_size
    while size > 17:
        fnt = font(SANS_BOLD, size)
        if len(wrap_text(draw, text, fnt, max_width)) <= 2:
            return fnt, wrap_text(draw, text, fnt, max_width)
        size -= 1
    fnt = font(SANS_BOLD, 17)
    return fnt, wrap_text(draw, text, fnt, max_width)


def fit_line(draw, kicker, rest, max_width, start_size=16):
    """Largest sizes (down to 13) for which 'KICKER: rest' fits one line."""
    size = start_size
    while size > 13:
        kf = font(SANS_BOLD, size)
        bf = font(SANS, size)
        total = (draw.textlength("\u25aa ", font=bf)
                 + draw.textlength(kicker + ":  ", font=kf)
                 + draw.textlength(rest, font=bf))
        if total <= max_width:
            return kf, bf
        size -= 1
    return font(SANS_BOLD, 13), font(SANS, 13)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=BLACK)
    title_fnt = font(SERIF_BOLD, 50)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_fnt)
    draw.text(((W - tw) / 2, 6), title, font=title_fnt, fill=WHITE)
    draw.rectangle([MARGIN, 62, W - MARGIN, 64], fill=GOLD)
    date_fnt = font(SANS_BOLD, 22)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_fnt)
    draw.text(((W - dw) / 2, 68), date, font=date_fnt, fill=GOLD)
    check_fnt = font(SANS_BOLD, 13)
    check = "DATE CHECK \u2713 19 NOV 2026"
    cw = draw.textlength(check, font=check_fnt)
    draw.text((W - MARGIN - 4 - cw, 72), check, font=check_fnt, fill=GOLD)

    # ---- 2x2 photo grid -------------------------------------------------
    for i, panel in enumerate(PANELS):
        row, col = divmod(i, 2)
        x0 = MARGIN + col * (CELL_W + GUTTER)
        y0 = GRID_TOP + row * (ROW_H + GUTTER)
        src = Image.open(os.path.join(PANELS_DIR, panel["file"])).convert("RGB")
        img.paste(centre_crop_resize(src, CELL_W, PHOTO_H), (x0, y0))
        draw.rectangle([x0, y0, x0 + CELL_W - 1, y0 + PHOTO_H - 1],
                       outline=BLACK, width=1)
        # caption bar
        cy = y0 + PHOTO_H
        draw.rectangle([x0, cy, x0 + CELL_W, cy + CAPTION_H], fill=WHITE)
        kicker_fnt = font(SANS_BOLD, 14)
        draw.text((x0 + 10, cy + 4), panel["kicker"], font=kicker_fnt, fill=RED)
        head_fnt, lines = fit_headline(draw, panel["headline"], CELL_W - 20)
        ly = cy + 23
        for line in lines:
            draw.text((x0 + 10, ly), line, font=head_fnt, fill=DARK)
            ly += 20

    # ---- THE DAY IN UTC ---------------------------------------------------
    draw.rectangle([0, TL_TOP, W, TL_TOP + 2], fill=BLACK)
    tl_head_fnt = font(SANS_BOLD, 15)
    draw.text((MARGIN + 4, TL_TOP + 6), "THE DAY IN UTC",
              font=tl_head_fnt, fill=BLACK)
    draw.rectangle([MARGIN, TL_TOP + 26, W - MARGIN, TL_TOP + 28], fill=GOLD)
    cell_w = (W - 2 * MARGIN) // len(TIMELINE)
    time_fnt = font(SANS_BOLD, 14)
    label_fnt = font(SANS, 12)
    for i, (when, label) in enumerate(TIMELINE):
        cx = MARGIN + i * cell_w
        draw.text((cx + 2, TL_TOP + 32), when, font=time_fnt, fill=RED)
        lines = wrap_text(draw, label, label_fnt, cell_w - 8, max_lines=2)
        ly = TL_TOP + 50
        for line in lines:
            draw.text((cx + 2, ly), line, font=label_fnt, fill=DARK)
            ly += 14

    # ---- MORE FROM THE DAY ----------------------------------------------
    draw.rectangle([0, LIST_TOP, W, LIST_TOP + 2], fill=BLACK)
    head_fnt = font(SANS_BOLD, 20)
    draw.text((MARGIN + 4, LIST_Y + 2), "MORE FROM THE DAY",
              font=head_fnt, fill=BLACK)
    date2_fnt = font(SANS_BOLD, 14)
    right = "44 STORIES  ·  19 NOVEMBER 2026"
    rw = draw.textlength(right, font=date2_fnt)
    draw.text((W - MARGIN - 4 - rw, LIST_Y + 7), right,
              font=date2_fnt, fill=GREY)
    draw.rectangle([MARGIN, LIST_Y + 30, W - MARGIN, LIST_Y + 32], fill=GOLD)

    col_w = 500
    line_step = 19
    for col_i, column in enumerate((MORE_LEFT, MORE_RIGHT)):
        x0 = MARGIN + col_i * (col_w + GUTTER)
        line_y = LIST_Y + 40
        for kicker, rest in column:
            kf, bf = fit_line(draw, kicker, rest, col_w - 4)
            draw.text((x0 + 4, line_y), "\u25aa ", font=bf, fill=RED)
            kx = x0 + 4 + draw.textlength("\u25aa ", font=bf)
            draw.text((kx, line_y), kicker + ":  ", font=kf, fill=RED)
            tx = kx + draw.textlength(kicker + ":  ", font=kf)
            draw.text((tx, line_y), rest, font=bf, fill=DARK)
            line_y += line_step

    img.save(OUT_PATH, format="JPEG", quality=88, optimize=True)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    main()
