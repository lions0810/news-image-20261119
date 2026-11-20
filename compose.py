#!/usr/bin/env python3
"""Render the front page for Thursday 19 November 2026.

Paper: THE WORLD IN ONE DAY, a 1024x1024 newspaper front page.
Sections, top to bottom: a black masthead band with the date and a
date-check stamp; a 2x2 grid of illustrated lead stories; a six-slot
UTC timeline strip; and a two-column MORE FROM THE DAY list.

All headlines and captions below were written for this edition from
fresh reporting on 19 November 2026. The four illustrations are the
existing panels/*.webp files, reused untouched.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PANEL_DIR = HERE / "panels"
OUT_PATH = HERE / "entry.png"

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 8

PAPER = (251, 250, 245)
INK = (17, 17, 17)
SOFT_INK = (58, 58, 58)
RED = (166, 25, 46)
GOLD = (201, 162, 39)
RULE = (17, 17, 17)
HAIRLINE = (150, 148, 140)

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF_BOLD = FONT_DIR / "dejavu/DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR / "dejavu/DejaVuSerif.ttf"
SANS = FONT_DIR / "dejavu/DejaVuSans.ttf"
SANS_BOLD = FONT_DIR / "dejavu/DejaVuSans-Bold.ttf"


def load(path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Load a TTF at the requested size, failing loudly if it is missing."""
    if not path.exists():
        raise SystemExit(f"missing font: {path}")
    return ImageFont.truetype(str(path), size)


class Fonts:
    """All typefaces used on the page, loaded once."""

    def __init__(self) -> None:
        self.masthead = load(SERIF_BOLD, 60)
        self.date = load(SERIF_BOLD, 27)
        self.stamp = load(SANS_BOLD, 15)
        self.kicker = load(SANS_BOLD, 15)
        self.headline = load(SERIF_BOLD, 24)
        self.section = load(SANS_BOLD, 17)
        self.section_note = load(SANS_BOLD, 13)
        self.utc_time = load(SANS_BOLD, 15)
        self.utc_label = load(SANS, 12)
        self.more = load(SANS, 13)


def wrap_text(draw: ImageDraw.ImageDraw, text: str,
              font: ImageFont.FreeTypeFont, width: int,
              max_lines: int) -> list[str]:
    """Greedy word wrap; returns at most max_lines lines.

    Anything that still overflows the last line is cut with an ellipsis
    and reported, so overlong copy is visible instead of silently lost.
    """
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
            if len(lines) == max_lines:
                break
    if len(lines) < max_lines and current:
        lines.append(current)
    if lines and draw.textlength(lines[-1], font=font) > width:
        clipped = lines[-1]
        while clipped and draw.textlength(clipped + "…", font=font) > width:
            clipped = clipped[:-1]
        lines[-1] = clipped + "…"
        print(f"WARNING: clipped line: {lines[-1]!r}", file=sys.stderr)
    return lines


def cover_crop(img: Image.Image, width: int, height: int) -> Image.Image:
    """Scale the image to cover the box, then crop the centre."""
    scale = max(width / img.width, height / img.height)
    grown = img.resize(
        (round(img.width * scale), round(img.height * scale)),
        Image.LANCZOS,
    )
    left = (grown.width - width) // 2
    top = (grown.height - height) // 2
    return grown.crop((left, top, left + width, top + height))


# ---------------------------------------------------------------------------
# Edition copy — written for 19 November 2026.
# ---------------------------------------------------------------------------

LEADS = [
    {
        "file": "media-generation-panel-gta6-launch-0-94093a7b-5719-41fb-b5f5-f0ba35ea63d8.webp",
        "kicker": "GAMES  ·  GTA VI LAUNCH",
        "headline": "GTA VI launches to rave reviews; 19m copies sold in a day",
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

UTC_STRIP = [
    ("00:29 UTC", "One child in four lives in a war zone"),
    ("05:00 UTC", "GTA VI unlocks in the US"),
    ("07:00 UTC", "Take-Two hails record game"),
    ("14:30 UTC", "Anthropic IPO starts trading"),
    ("20:41 UTC", "Putin, Xi praise summit"),
    ("23:26 UTC", "No new Iran strikes in 2026"),
]

MORE = [
    ("CRIMEA", "Ukraine hits Crimean Bridge a third time; rail halted"),
    ("MARKETS", "S&P 500 drops 2.0% for a fifth straight loss"),
    ("ANTHROPIC", "IPO raises about $81.3bn; shares close up 17%"),
    ("GAZA", "Israeli tanks push past the Yellow Line near Nuseirat"),
    ("KOREA", "North Korea expanding uranium enrichment, IAEA says"),
    ("CYCLONE", "Akvan to hit Andhra–Odisha coast as weaker storm"),
    ("TANKER", "LPG carrier Gas Husky sinks off Bulgaria after strike"),
    ("COP31", "Final-stage talks split over fossil-fuel phaseout"),
    ("BANGLADESH", "Opposition shutdown brings fresh political violence"),
    ("VENEZUELA", "US asks top court to block restored migrant protections"),
    ("ALASKA", "Begich keeps Alaska\u2019s sole House seat after recount"),
    ("SPEAKER", "Jeffries poised to be first Black House Speaker"),
    ("GREENLAND", "Denmark approves security deal 109\u20130"),
    ("BITCOIN", "Dips below $63,000, then recovers; ETFs shed $157.8m"),
    ("CANADA", "Carney closes APEC with China trade gains to Dec 2028"),
    ("CHILDREN", "Nearly one child in four now lives in a conflict zone"),
    ("SPACE", "Voyager 1 first human object one light-day from Earth"),
    ("MERCURY", "BepiColombo reaches Mercury orbit"),
    ("SCIENCE", "Compound burns fat without losing muscle, team finds"),
    ("FOOTBALL", "Lee Kang-in named Asia\u2019s overseas player of the year"),
    ("CRICKET", "Litton Das sets Test record for dismissals in an innings"),
    ("ROSE", "Trump posthumously pardons Pete Rose"),
    ("ESPIONAGE", "Alleged Russian agent held over US tech surveillance"),
    ("FRANCE", "Three women jailed for joining ISIS in Syria"),
    ("GULF", "US reissues security warnings for Bahrain and Saudi Arabia"),
    ("FAITH", "Muslims on track to outnumber Christians by 2035"),
    ("CRUISE", "Nearly 150 fall ill in shipboard outbreak"),
    ("BORDER", "38,000 rounds of ammo seized at Texas crossing"),
    ("HARRY", "Prince Harry says he is ready to re-enlist to fight Russia"),
    ("INDIA", "Jaishankar: India, Japan vital to a free Indo-Pacific"),
    ("HERITAGE", "ASI monuments offer free entry for World Heritage Week"),
    ("SPORT", "Pistons end Spurs\u2019 12-game winning streak, 105\u201393"),
    ("MUSIC", "Ella Langley wins a record six CMA Awards"),
    ("CHESS", "Carlsen leads Fast Classic after forfeits hit rivals"),
]

STORY_TOTAL = len(LEADS) + len(UTC_STRIP) + len(MORE)


class FrontPage:
    """Builds the 1024x1024 front page section by section."""

    def __init__(self) -> None:
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.draw = ImageDraw.Draw(self.img)
        self.fonts = Fonts()

    # -- masthead ---------------------------------------------------------
    def masthead(self) -> int:
        d = self.draw
        band_h = 98
        d.rectangle([0, 0, PAGE_W, band_h], fill=INK)
        title = "THE WORLD IN ONE DAY"
        tw = d.textlength(title, font=self.fonts.masthead)
        d.text(((PAGE_W - tw) / 2, 6), title, font=self.fonts.masthead,
               fill=(255, 255, 255))
        d.line([0, 68, PAGE_W, 68], fill=GOLD, width=2)
        date = "THURSDAY, 19 NOVEMBER 2026"
        d.text((MARGIN + 2, 72), date, font=self.fonts.date, fill=GOLD)
        stamp = "DATE CHECK \u2713  19 NOV 2026"
        sw = d.textlength(stamp, font=self.fonts.stamp)
        d.text((PAGE_W - MARGIN - 2 - sw, 78), stamp,
               font=self.fonts.stamp, fill=GOLD)
        return band_h + 4

    # -- lead panels ------------------------------------------------------
    def leads(self, top: int) -> int:
        d = self.draw
        gap = 8
        cell_w = (PAGE_W - 2 * MARGIN - gap) // 2
        pic_h = 148
        cell_h = 240
        for row in range(2):
            y = top + row * (cell_h + 4)
            for col in range(2):
                lead = LEADS[row * 2 + col]
                x = MARGIN + col * (cell_w + gap)
                self._lead_cell(x, y, cell_w, pic_h, lead)
        return top + 2 * cell_h + 4

    def _lead_cell(self, x: int, y: int, width: int, pic_h: int,
                   lead: dict) -> None:
        d = self.draw
        path = PANEL_DIR / lead["file"]
        with Image.open(path) as art:
            art = art.convert("RGB")
            pic = cover_crop(art, width, pic_h)
        self.img.paste(pic, (x, y))
        d.rectangle([x, y, x + width - 1, y + pic_h - 1],
                    outline=INK, width=1)
        ky = y + pic_h + 5
        d.text((x, ky), lead["kicker"], font=self.fonts.kicker, fill=RED)
        lines = wrap_text(d, lead["headline"], self.fonts.headline,
                          width, 2)
        hy = ky + 20
        for line in lines:
            d.text((x, hy), line, font=self.fonts.headline, fill=INK)
            hy += 27

    # -- UTC strip --------------------------------------------------------
    def utc_strip(self, top: int) -> int:
        d = self.draw
        d.text((MARGIN, top), "THE DAY IN UTC",
               font=self.fonts.section, fill=INK)
        d.line([MARGIN, top + 22, PAGE_W - MARGIN, top + 22],
               fill=RULE, width=2)
        col_w = (PAGE_W - 2 * MARGIN) // len(UTC_STRIP)
        y = top + 30
        for i, (when, label) in enumerate(UTC_STRIP):
            x = MARGIN + i * col_w
            d.text((x, y), when, font=self.fonts.utc_time, fill=RED)
            lines = wrap_text(d, label, self.fonts.utc_label,
                              col_w - 8, 2)
            ly = y + 19
            for line in lines:
                d.text((x, ly), line, font=self.fonts.utc_label, fill=INK)
                ly += 15
        return top + 30 + 19 + 2 * 15 + 6

    # -- more stories -----------------------------------------------------
    def more_list(self, top: int) -> int:
        d = self.draw
        d.text((MARGIN, top), "MORE FROM THE DAY",
               font=self.fonts.section, fill=INK)
        note = f"{STORY_TOTAL} STORIES  \u00b7  19 NOVEMBER 2026"
        nw = d.textlength(note, font=self.fonts.section_note)
        d.text((PAGE_W - MARGIN - nw, top + 3), note,
               font=self.fonts.section_note, fill=SOFT_INK)
        d.line([MARGIN, top + 22, PAGE_W - MARGIN, top + 22],
               fill=RULE, width=2)
        gap = 12
        col_w = (PAGE_W - 2 * MARGIN - gap) // 2
        half = (len(MORE) + 1) // 2
        row_h = 18
        y0 = top + 30
        for col in range(2):
            items = MORE[col * half:(col + 1) * half]
            x = MARGIN + col * (col_w + gap)
            for i, (tag, head) in enumerate(items):
                y = y0 + i * row_h
                d.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
                self._more_line(x + 12, y, col_w - 12, tag, head)
        return y0 + half * row_h

    def _more_line(self, x: int, y: int, width: int, tag: str,
                   head: str) -> None:
        d = self.draw
        size = 13
        while size > 10:
            font = load(SANS_BOLD, size)
            body = load(SANS, size)
            tag_w = d.textlength(tag + ":  ", font=font)
            if tag_w + d.textlength(head, font=body) <= width:
                break
            size -= 1
        d.text((x, y), tag + ": ", font=font, fill=RED)
        d.text((x + tag_w, y), head, font=body, fill=INK)

    # -- build ------------------------------------------------------------
    def build(self) -> Image.Image:
        y = self.masthead()
        y = self.leads(y)
        y = self.utc_strip(y)
        y = self.more_list(y)
        if y > PAGE_H - MARGIN:
            print(f"WARNING: content ends at y={y}, page is {PAGE_H}",
                  file=sys.stderr)
        return self.img


def main() -> None:
    page = FrontPage()
    img = page.build()
    img.save(OUT_PATH, format="PNG")
    size = OUT_PATH.stat().st_size
    print(f"wrote {OUT_PATH} ({img.width}x{img.height}, {size} bytes, "
          f"{STORY_TOTAL} stories)")
    if size > 1_048_576:
        raise SystemExit("entry.png exceeds the 1 MiB limit")


if __name__ == "__main__":
    main()
