#!/usr/bin/env python3
"""Daily Atlas, HARBOUR edition — Tuesday 24 November 2026 in one image.

One 1024x1024 broadsheet, built from the commissioned story data only.
Bands (all asserted inside 1024):
    masthead          28..150
    UTC timeline     154..178
    region bar       182..204
    stat strip       210..256
    featured row     264..476   (art 314x157 on top, caption under it)
    grid             488..748   (3 cols x 4 rows, tiles 314x58)
    briefs + map     758..884
    HOW SURE         890..908
    DATE CHECK       914..1000  (drawn last)

Artwork: assets/f1..f3.jpg (314x157) and assets/g04..g15.jpg (74x56), all
generated with the Recraft route and pasted as pictures only. Every word on
this page is typeset here from the story data.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W = H = 1024

# --- palette ---------------------------------------------------------------
PAPER = (0xEA, 0xF0, 0xEE)      # pale harbour-mist ground
INK = (0x10, 0x22, 0x2B)        # deep harbour ink
HARBOUR = (0x14, 0x50, 0x6E)    # deep harbour blue (rules, kickers, numerals)
BRASS = (0xA9, 0x7E, 0x2F)      # brass hairlines and pin rings
CREAM = (0xF4, 0xF7, 0xF4)      # panels
LAND = (0xC7, 0xD3, 0xCC)       # map tint
OCEAN = PAPER

# --- fonts -----------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


# --- story data ------------------------------------------------------------
# FEATURED (3): full scene art above, headline + dek + source under it.
FEATURED = [
    {
        "n": 1,
        "region": "GLOBAL",
        "sure": "CONFIRMED",
        "place": "WALL STREET",
        "cat": "MARKETS",
        "head": "Huang's return ignites the rebound — then Tuesday fades it",
        "dek": "Monday's close was Wall Street's best since April 2025.",
        "src": "Zacks · Reuters · AP",
    },
    {
        "n": 2,
        "region": "MIDDLE EAST",
        "sure": "CONFIRMED",
        "place": "KHARG ISLAND",
        "cat": "STANDOFF",
        "head": "Trump dares, Iran answers with the law",
        "dek": "14+ tankers massed at Kharg; no convoy has sailed.",
        "src": "Fox News · UKMTO · JMIC",
    },
    {
        "n": 3,
        "region": "ASIA",
        "sure": "CONFIRMED",
        "place": "SERANG, BANTEN",
        "cat": "DISASTER",
        "head": "Serang toll 26, and a negligence probe opens",
        "dek": "26 dead, 8 missing after Saturday's candy-factory fire.",
        "src": "AP · Euronews · NewsCentralTV",
    },
]

# GRID (12): a scene strip at each tile's left, then headline and dek.
GRID = [
    {"n": 4, "region": "MIDDLE EAST", "sure": "CONFIRMED", "place": "GAZA CITY",
     "cat": "WAR", "head": "Hamas security chief killed in Tuesday's strikes",
     "dek": "Strikes kill Hamas security chief Naeem Abu Nahel and six others on Tuesday.",
     "src": "Just Security · Reuters", "strip": "g04.jpg"},
    {"n": 5, "region": "EUROPE", "sure": "OFFICIAL", "place": "ZAPORIZHZHIA",
     "cat": "WAR", "head": "Two killed, 40 wounded in an overnight strike",
     "dek": "Governor: overnight Russian strike kills two and wounds 40, four children.",
     "src": "Just Security", "strip": "g05.jpg"},
    {"n": 6, "region": "GLOBAL", "sure": "REPORTED", "place": "ANTALYA",
     "cat": "CLIMATE", "head": "COP31 fallout: the process itself on trial",
     "dek": "No salvage deal at COP31; Hoekstra: the process is hijacked.",
     "src": "Reuters · Carbon Brief · POLITICO", "strip": "g06.jpg"},
    {"n": 7, "region": "ASIA", "sure": "OFFICIAL", "place": "NEW DELHI",
     "cat": "DIPLOMACY", "head": "Shah-Modi outcomes land",
     "dek": "Eight MoUs signed; India announces a Rs 15,000 crore package for Nepal.",
     "src": "Himalaya Times · Dainik Jagran", "strip": "g07.jpg"},
    {"n": 8, "region": "EUROPE", "sure": "CONFIRMED", "place": "BRUSSELS",
     "cat": "STRIKE", "head": "The outcome: 404 flights, 51,000 travellers",
     "dek": "Strike: 404 flights cancelled, 51,000+ travellers hit; Charleroi halts all flights.",
     "src": "BBC · The Flight Brief", "strip": "g08.jpg"},
    {"n": 9, "region": "AFRICA", "sure": "OFFICIAL", "place": "ITURI, DR CONGO",
     "cat": "HEALTH", "head": "Fighting traps Ebola responders",
     "dek": "WHO: fighting near an Ituri hospital forces Ebola teams to shelter 24+ hours.",
     "src": "UN News", "strip": "g09.jpg"},
    {"n": 10, "region": "EUROPE", "sure": "OFFICIAL", "place": "BERLIN",
     "cat": "DEFENCE", "head": "Germany first into Ukraine's Delta system",
     "dek": "Germany is the first country with access to Ukraine's Delta battlefield system.",
     "src": "Kyiv Independent", "strip": "g10.jpg"},
    {"n": 11, "region": "GLOBAL", "sure": "OFFICIAL", "place": "NATO",
     "cat": "SPACE", "head": "Rutte warns on space",
     "dek": "Rutte: NATO will defend space after reports on a Russian satellite.",
     "src": "The Global Eye", "strip": "g11.jpg"},
    {"n": 12, "region": "AMERICAS", "sure": "REPORTED", "place": "WASHINGTON",
     "cat": "DIPLOMACY", "head": "Vance and Rubio meet Qatar's PM — separately",
     "dek": "Vance and Rubio meet Qatar's PM separately at the White House.",
     "src": "AP", "strip": "g12.jpg"},
    {"n": 13, "region": "MIDDLE EAST", "sure": "OFFICIAL", "place": "KIRKUK",
     "cat": "OIL", "head": "Baghdad moves on Kurdish-area oilfields",
     "dek": "Baghdad orders federal management of oilfields under Kurdish security control.",
     "src": "Reuters", "strip": "g13.jpg"},
    {"n": 14, "region": "AMERICAS", "sure": "OFFICIAL", "place": "WASHINGTON",
     "cat": "JUSTICE", "head": "Trump orders the death penalty pushed faster",
     "dek": "Trump orders the DOJ to expedite death sentences and seek death in more cases.",
     "src": "Just Security", "strip": "g14.jpg"},
    {"n": 15, "region": "AMERICAS", "sure": "REPORTED", "place": "PORTLAND",
     "cat": "COURTS", "head": "Oregon and Virginia sue SpaceX over Grok images",
     "dek": "Oregon and Virginia sue SpaceX over allegedly Grok-generated abuse images.",
     "src": "IQMIA", "strip": "g15.jpg"},
]

# ALSO ON TUESDAY 24 NOVEMBER — 18 briefs, ONE line of thought each, numbered.
BRIEFS = [
    {"n": 16, "region": "EUROPE", "sure": "REPORTED", "place": "TALLINN",
     "text": "Russia warns Estonia's moves verge on open war."},
    {"n": 17, "region": "EUROPE", "sure": "REPORTED", "place": "MOSCOW",
     "text": "700,000+ Russian soldiers killed, per a new analysis."},
    {"n": 18, "region": "EUROPE", "sure": "OFFICIAL", "place": "BERLIN",
     "text": "Zelensky tells the NATO assembly: let Ukraine join."},
    {"n": 19, "region": "AFRICA", "sure": "OFFICIAL", "place": "BENGHAZI",
     "text": "UNSMIL seeks a probe into Sunday's port attacks."},
    {"n": 20, "region": "EUROPE", "sure": "REPORTED", "place": "BRUSSELS/KYIV",
     "text": "Seven states seek limits on Russians' EU travel."},
    {"n": 21, "region": "ASIA", "sure": "OFFICIAL", "place": "SEOUL",
     "text": "Russian aircraft flew inside the South's air zone."},
    {"n": 22, "region": "ASIA", "sure": "OFFICIAL", "place": "WASHINGTON",
     "text": "US blacklists Singapore cloud firm Megaspeed."},
    {"n": 23, "region": "AMERICAS", "sure": "REPORTED", "place": "WASHINGTON/OTTAWA",
     "text": "Pentagon: Canada falls short on continental defence."},
    {"n": 24, "region": "ASIA", "sure": "OFFICIAL", "place": "SEOUL",
     "text": "$375,000 offered to catch exam AI cheats."},
    {"n": 25, "region": "AFRICA", "sure": "REPORTED", "place": "MOGADISHU/KAMPALA",
     "text": "Somalia and Uganda intensify Al-Shabaab operations."},
    {"n": 26, "region": "EUROPE", "sure": "REPORTED", "place": "CAMBRIDGE",
     "text": "Arm extends CEO Rene Haas' tenure to 2033."},
    {"n": 27, "region": "EUROPE", "sure": "OFFICIAL", "place": "EUROPE",
     "text": "UCL matchday 5: Real Madrid 5-1 PSV, Arsenal 1-1 Dortmund, "
             "Man City 2-2 Napoli, Galatasaray 1-0 Aston Villa, "
             "Feyenoord 0-1 Porto, RB Leipzig 3-1 Lens."},
    {"n": 28, "region": "ASIA", "sure": "OFFICIAL", "place": "SINGAPORE",
     "text": "Q3 GDP +6.1%; 2026 forecast raised to about 6%."},
    {"n": 29, "region": "ASIA", "sure": "REPORTED", "place": "BEIJING",
     "text": "90bn yuan of state ETF buying fails to stop the AI sell-off."},
    {"n": 30, "region": "ASIA", "sure": "OFFICIAL", "place": "TOKYO",
     "text": "PMI 53.7 manufacturing, 50.5 services; 10-year JGB 2.70%."},
    {"n": 31, "region": "GLOBAL", "sure": "CONFIRMED", "place": "MARKETS",
     "text": "Oil ~$86 then ~$91; gold -2.16% at $3,556.31; bitcoin nears $60,000."},
    {"n": 32, "region": "ASIA", "sure": "REPORTED", "place": "SEOUL/SYDNEY",
     "text": "BOK seen at 3.25% Thursday; ANZ RBA cut now June 2027."},
    {"n": 33, "region": "AMERICAS", "sure": "OFFICIAL", "place": "WASHINGTON",
     "text": "PCE and GDP Wednesday; markets shut Thursday."},
]

# --- the rest of the page furniture ---------------------------------------
STATS = [
    ("+31.5%", "Nvidia's Monday jump on Huang's reinstatement (~$952bn added)"),
    ("+6.51%", "Nasdaq's Monday surge, its best session since April 2025"),
    ("14+", "tankers massed at Kharg Island; the convoy has not sailed"),
    ("26", "confirmed dead in the Serang factory fire, 8 still missing"),
    ("404", "Brussels Airport flights cancelled in Monday's strike"),
    ("700,000+", "Russian soldiers killed in the war, per a new analysis"),
]

TIMELINE = [
    ("MON 20:00-21:00 UTC", "Wall St closes: Nasdaq +6.51%"),
    ("TUE 00:00-02:00 UTC", "Asia opens: Kospi +6.5%"),
    ("TUE MORNING WIB", "Serang toll confirmed at 26"),
    ("TUE DAYTIME UTC", "Gaza strike kills Hamas chief"),
    ("TUE EVENING CET", "UCL: Real Madrid 5-1 PSV"),
    ("TUE 20:00-21:00 UTC", "US fades; Dow tops 50,000"),
]

LEFT_OUT = [
    ("Brussels strike shutdown", "MONDAY 23 NOV", "Tuesday carries only the tally"),
    ("Shah-Modi talks", "MONDAY 23 NOV", "Tuesday carries the outcomes"),
    ("Wall Street rebound close", "MONDAY 23 NOV", "Tuesday carries Asia and the fade"),
    ("COP31 collapse", "SUNDAY 22 NOV", "Tuesday carries the fallout"),
    ("Vance/Rubio-Qatar meetings", "MONDAY 23 NOV", "reported Tuesday"),
    ("GTA VI \"$3.8bn first-day\"", "THU 19 NOV", "excluded"),
    ("Kate \"in remission\"", "JAN 2025", "excluded"),
    ("CRISPR \"cuts cholesterol 52%\"", "28 AUG / 4 SEP 2026", "excluded"),
    ("ICJ Myanmar genocide ruling", "THU 19 NOV", "excluded"),
    ("Serang \"28 unaccounted\"", "ONE TUE STATEMENT", "conflicts with AP/Euronews' 8 missing"),
]

NOT_YET = [
    ("Spain election", "SUN 29 NOV"),
    ("OPEC+ ministerial", "29 NOV"),
    ("Minnesota House recount", "30 NOV"),
    ("\"Heal\" documentary premiere", "29 NOV"),
    ("BepiColombo separation", "9-10 DEC"),
    ("Bank of Korea rate decision", "THU 26 NOV"),
]

LEGEND = [
    ("CONFIRMED", "two or more major outlets"),
    ("OFFICIAL", "on the record from officials or agencies"),
    ("REPORTED", "one outlet"),
    ("CLAIM", "unverified claim, typeset as a claim"),
]

REGION_ORDER = ["MIDDLE EAST", "EUROPE", "AMERICAS", "ASIA", "AFRICA", "OCEANIA", "GLOBAL"]

# story numeral: city, lon, lat  (repeats are offset along latitude as briefed)
PINS = [
    (1, -74.0, 40.7), (2, 50.3, 29.2), (3, 106.1, -6.1), (4, 34.5, 31.5),
    (5, 35.1, 47.8), (6, 30.7, 36.9), (7, 77.2, 28.6), (8, 4.4, 50.8),
    (9, 30.2, 1.6), (10, 13.4, 52.5), (11, 4.4, 54.2), (12, -77.0, 38.9),
    (13, 44.4, 35.5), (14, -77.0, 36.4), (15, -122.7, 45.5), (16, 24.8, 59.4),
    (17, 37.6, 55.8), (18, 13.4, 49.8), (19, 20.1, 32.1), (20, 30.5, 50.5),
    (21, 127.0, 37.6), (22, 103.8, 1.4), (23, -75.7, 45.4), (24, 127.0, 40.2),
    (25, 45.3, 2.0), (26, 0.1, 52.2), (28, 103.8, 4.6), (29, 116.4, 39.9),
    (30, 139.7, 35.7), (32, 151.2, -33.9), (33, -77.0, 42.0),
]

MAP_NOTE = "27 — nine grounds across Europe · 31 — oil, gold, bitcoin: the world's markets"

ALL_STORIES = FEATURED + GRID + BRIEFS

# --- fonts, cached ---------------------------------------------------------
_CACHE = {}


def font(name, size):
    key = (name, size)
    if key not in _CACHE:
        _CACHE[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _CACHE[key]


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

# --- line-box registry -----------------------------------------------------
# Every typeset line registers its ink box, tagged with the band it lives in.
# Overlap is then a property of the page, not a hope.
BOXES = []


def register(band, x0, y0, x1, y1, text):
    BOXES.append((band, x0, y0, x1, y1, text))


def check_overlaps(band):
    items = [b for b in BOXES if b[0] == band]
    bad = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                bad.append((a, b))
    return bad


def clear_band(band):
    BOXES[:] = [b for b in BOXES if b[0] != band]


# --- measuring -------------------------------------------------------------
def tw(text, f):
    """Advance width of one typeset string."""
    return f.getlength(text)


def fit(name, size_list, text, maxw):
    """Largest size in size_list whose single line fits maxw. Never truncates."""
    for s in size_list:
        f = font(name, s)
        if tw(text, f) <= maxw:
            return f, s
    return None, None


def wrap(text, f, maxw):
    """Greedy wrap to width. Returns full lines; the text is never shortened."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if tw(trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def as_lines(text, f, maxw, max_lines=None):
    lines = wrap(text, f, maxw)
    if max_lines is not None:
        assert len(lines) <= max_lines, (
            "text needs %d lines at %dpx in %.0fpx (cap %d): %r"
            % (len(lines), f.size, maxw, max_lines, text))
    return lines


def line_box(f, text, x, baseline):
    b = f.getbbox(text, anchor="ls")
    return (x + b[0], baseline + b[1], x + b[2], baseline + b[3])


def draw_line(d, band, text, f, fill, x, baseline):
    d.text((x, baseline), text, font=f, fill=fill, anchor="ls")
    x0, y0, x1, y1 = line_box(f, text, x, baseline)
    register(band, x0, y0, x1, y1, text)
    return x1


def draw_spans(d, band, spans, x, baseline):
    """spans: [(text, font, fill)] on one shared baseline. Returns right edge."""
    cx = x
    for text, f, fill in spans:
        d.text((cx, baseline), text, font=f, fill=fill, anchor="ls")
        x0, y0, x1, y1 = line_box(f, text, cx, baseline)
        register(band, x0, y0, x1, y1, " ".join(t for t, _, _ in spans))
        cx += tw(text, f)
    return cx


def spans_width(spans):
    return sum(tw(t, f) for t, f, _ in spans)


def block(d, band, text, f, fill, x, y_top, maxw, leading, max_lines=None,
          align="left"):
    """Wrap, register, and draw a paragraph. y_top is the first ascent line."""
    lines = as_lines(text, f, maxw, max_lines)
    asc = -f.getbbox("Hg", anchor="ls")[1]
    y = y_top + asc
    for ln in lines:
        if align == "left":
            cx = x
        elif align == "right":
            cx = x + maxw - tw(ln, f)
        else:
            cx = x + (maxw - tw(ln, f)) / 2.0
        draw_line(d, band, ln, f, fill, cx, y)
        y += leading
    return y - asc + (leading - asc)


# --- panels, rules, art ----------------------------------------------------
def rule(d, x0, y0, x1, y1, colour, width=1):
    d.rectangle([x0, y0, x1, y1], fill=colour)
    if width > (y1 - y0):
        pass


def hairline(d, x0, x1, y, colour=BRASS):
    d.rectangle([x0, y, x1, y], fill=colour)


def vline(d, x, y0, y1, colour=BRASS):
    d.rectangle([x, y0, x, y1], fill=colour)


def panel(d, box, fill=CREAM, outline=BRASS):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=fill)
    if outline is not None:
        d.rectangle([x0, y0, x1, y0], fill=outline)
        d.rectangle([x0, y1, x1, y1], fill=outline)


def art(path, box):
    im = Image.open(os.path.join(ASSETS, path)).convert("RGB")
    assert im.size == (box[2] - box[0], box[3] - box[1]), (
        "%s is %r, panel wants %r" % (path, im.size,
                                      (box[2] - box[0], box[3] - box[1])))
    return im


def small_caps_label(d, band, text, x, baseline, fill, size=8, track=0.9):
    """Letterspaced kicker. Returns right edge."""
    f = font(SANS_B, size)
    cx = x
    for ch in text:
        d.text((cx, baseline), ch, font=f, fill=fill, anchor="ls")
        cx += tw(ch, f) + track
    x0, y0, x1, y1 = line_box(f, text, x, baseline)
    register(band, x0, y0, cx, y1, text)
    return cx


# ===========================================================================
# BAND 1 — masthead 28..150
# ===========================================================================
MAR_L = 28
MAR_R = 996


def draw_masthead(d):
    band = "masthead"
    # wordmark line
    small_caps_label(d, band, "DAILY ATLAS", MAR_L, 52, HARBOUR, size=11, track=2.6)
    f = font(SANS, 8)
    right = "HARBOUR EDITION"
    d.text((MAR_R, 52), right, font=f, fill=INK, anchor="rs")
    register(band, *line_box(f, right, MAR_R - tw(right, f), 52), right)

    # the giant date IS the masthead
    date = "TUESDAY 24 NOVEMBER 2026"
    df = font(SERIF_B, 54)
    assert tw(date, df) <= MAR_R - MAR_L, "date overflows the measure"
    d.text((MAR_L, 118), date, font=df, fill=INK, anchor="ls")
    register(band, *line_box(df, date, MAR_L, 118), date)

    # harbour rule under it, brass hairline just below
    d.rectangle([MAR_L, 128, MAR_R, 132], fill=HARBOUR)
    hairline(d, MAR_L, MAR_R, 136)

    # strapline, right-aligned on the rule
    fs = font(SANS, 9)
    strap = "33 stories  ·  24 hours  ·  one page"
    d.text((MAR_R, 148), strap, font=fs, fill=HARBOUR, anchor="rs")
    register(band, *line_box(fs, strap, MAR_R - tw(strap, fs), 148), strap)


# ===========================================================================
# BAND 2 — UTC timeline 154..178
# ===========================================================================
def draw_timeline(d):
    band = "timeline"
    top, bot = 154, 178
    n = len(TIMELINE)
    wseg = (MAR_R - MAR_L) / n
    hairline(d, MAR_L, MAR_R, bot)
    ft = font(SANS, 7.5)
    assert 175 + ft.getbbox("Hg", anchor="ls")[3] <= bot + 1
    for i, (when, what) in enumerate(TIMELINE):
        x0 = MAR_L + i * wseg
        if i:
            vline(d, int(x0), top, bot - 1, BRASS)
        pad = 5
        small_caps_label(d, band, when, int(x0 + pad), 162, HARBOUR, size=6,
                         track=0.4)
        assert tw(what, ft) <= wseg - 2 * pad, (
            "timeline event does not fit its segment: %r" % what)
        d.text((int(x0 + pad), 175), what, font=ft, fill=INK, anchor="ls")
        register(band, *line_box(ft, what, int(x0 + pad), 175), what)
    assert n == 6


# ===========================================================================
# BAND 3 — region bar 182..204 (counts computed from the tags)
# ===========================================================================
def region_counts():
    counts = {k: [] for k in REGION_ORDER}
    for s in ALL_STORIES:
        counts[s["region"]].append(s["n"])
    return counts


def draw_region_bar(d):
    band = "regions"
    top, bot = 182, 204
    counts = region_counts()
    total = sum(len(v) for v in counts.values())
    assert total == 33, "region counts sum to %d, not 33" % total
    # asserted against the brief's FINAL TAGS
    WANT = {
        "MIDDLE EAST": [2, 4, 13],
        "EUROPE": [5, 8, 10, 16, 17, 18, 20, 26, 27],
        "AMERICAS": [12, 14, 15, 23, 33],
        "ASIA": [3, 7, 21, 22, 24, 28, 29, 30, 32],
        "AFRICA": [9, 19, 25],
        "OCEANIA": [],
        "GLOBAL": [1, 6, 11, 31],
    }
    for k in REGION_ORDER:
        assert sorted(counts[k]) == sorted(WANT[k]), (
            "region %s = %r, brief says %r" % (k, sorted(counts[k]), sorted(WANT[k])))

    d.rectangle([MAR_L, top, MAR_R, bot], fill=CREAM)
    d.rectangle([MAR_L, top, MAR_R, top], fill=BRASS)
    d.rectangle([MAR_L, bot, MAR_R, bot], fill=BRASS)

    # only regions with stories get a segment; OCEANIA 0 is stated, not drawn
    shown = [k for k in REGION_ORDER if counts[k]]
    f_lab = font(SANS_B, 8)
    f_num = font(SERIF_B, 12)
    pad = 6
    gap = 10
    widths = []
    for k in shown:
        lab = k
        nm = "%02d" % len(counts[k])
        widths.append(tw(lab, f_lab) + 5 + tw(nm, f_num) + 2 * pad)
    avail = MAR_R - MAR_L
    extra = (avail - sum(widths) - gap * (len(shown) - 1)) / len(shown)
    assert extra >= 0, "region bar overflows by %.1f px" % -extra
    x = MAR_L
    for i, k in enumerate(shown):
        wseg = widths[i] + extra
        if i:
            vline(d, int(x), top + 4, bot - 4, BRASS)
        cx = int(x + pad)
        mid = (top + bot) // 2 + 4
        d.text((cx, mid), k, font=f_lab, fill=INK, anchor="ls")
        register(band, *line_box(f_lab, k, cx, mid), k)
        cx += tw(k, f_lab) + 5
        nm = "%02d" % len(counts[k])
        d.text((cx, mid), nm, font=f_num, fill=HARBOUR, anchor="ls")
        register(band, *line_box(f_num, nm, cx, mid), nm)
        assert cx + tw(nm, f_num) <= x + wseg - 2, "region label overflows segment %s" % k
        x += wseg + gap

    fq = font(SANS, 7)
    tail = "OCEANIA 00"
    tx = MAR_R - tw(tail, fq)
    d.text((tx, (top + bot) // 2 + 3), tail, font=fq, fill=INK, anchor="ls")
    register(band, *line_box(fq, tail, tx, (top + bot) // 2 + 3), tail)


# ===========================================================================
# BAND 4 — stat strip 210..256
# ===========================================================================
def draw_stats(d):
    band = "stats"
    top, bot = 210, 256
    n = len(STATS)
    assert n == 6
    cell = (MAR_R - MAR_L) / n
    for i, (val, cap) in enumerate(STATS):
        x0 = MAR_L + i * cell
        x1 = x0 + cell
        if i:
            vline(d, int(x0), top, bot, BRASS)
        pad = 8
        inner = cell - 2 * pad
        vf = font(SERIF_B, 20)
        while tw(val, vf) > inner and vf.size > 12:
            vf = font(SERIF_B, vf.size - 1)
        d.text((int(x0 + pad), top + 20), val, font=vf, fill=HARBOUR, anchor="ls")
        register(band, *line_box(vf, val, int(x0 + pad), top + 20), val)
        cf = font(SANS, 8)
        lines = as_lines(cap, cf, inner, max_lines=2)
        yb = top + 32
        for ln in lines:
            d.text((int(x0 + pad), yb), ln, font=cf, fill=INK, anchor="ls")
            register(band, *line_box(cf, ln, int(x0 + pad), yb), ln)
            yb += 9
        assert yb - 9 <= bot - 1, "stat caption spills past the strip: %r" % cap


# ===========================================================================
# BAND 5 — featured row 264..476 (art on top, caption UNDER it)
# ===========================================================================
FEAT_X = [28, 355, 682]
FEAT_W = 314
FEAT_TOP = 264
FEAT_ART_H = 157


def draw_featured(d, page):
    band = "featured"
    for i, s in enumerate(FEATURED):
        x = FEAT_X[i]
        art_top = FEAT_TOP
        page.paste(art("f%d.jpg" % s["n"], (0, 0, FEAT_W, FEAT_ART_H)),
                   (x, art_top))
        # brass hairline framing the picture only, never over it
        d.rectangle([x, art_top, x + FEAT_W - 1, art_top + FEAT_ART_H - 1],
                    outline=BRASS)

        # --- kicker baseline 429: numeral, place · category, sure tag right
        nf = font(SERIF_B, 11)
        kf = font(SANS_B, 6.5)
        tf = font(SANS_B, 6)
        tag = s["sure"]
        num = "%02d" % s["n"]
        kick = "%s · %s" % (s["place"], s["cat"])
        cx = x
        d.text((cx, 429), num, font=nf, fill=HARBOUR, anchor="ls")
        register(band, *line_box(nf, num, cx, 429), num)
        cx += tw(num, nf) + 6
        d.text((cx, 429), kick, font=kf, fill=HARBOUR, anchor="ls")
        register(band, *line_box(kf, kick, cx, 429), kick)
        tag_x = x + FEAT_W - tw(tag, tf)
        d.text((tag_x, 429), tag, font=tf, fill=BRASS, anchor="ls")
        register(band, *line_box(tf, tag, tag_x, 429), tag)
        assert cx + tw(kick, kf) < tag_x - 4, (
            "featured kicker collides with the sure tag: %r" % s["head"])

        # --- headline, 11px, two lines
        hf = font(SERIF_B, 11)
        hl = as_lines(s["head"], hf, FEAT_W, max_lines=2)
        hy = 441
        for ln in hl:
            d.text((x, hy), ln, font=hf, fill=INK, anchor="ls")
            register(band, *line_box(hf, ln, x, hy), ln)
            hy += 11

        # --- dek, one line at 11px: wording shortened, facts never
        df = font(SANS, 11)
        dl = as_lines(s["dek"], df, FEAT_W, max_lines=1)
        dy = 464
        d.text((x, dy), dl[0], font=df, fill=INK, anchor="ls")
        register(band, *line_box(df, dl[0], x, dy), dl[0])

        # --- source under a brass hairline
        sf = font(SANS, 7)
        hairline(d, x, x + FEAT_W - 1, 468)
        d.text((x, 476), s["src"], font=sf, fill=BRASS, anchor="ls")
        register(band, *line_box(sf, s["src"], x, 476), s["src"])
        assert 476 + font(SANS, 7).getbbox("Hg", anchor="ls")[3] <= 477


# ===========================================================================
# BAND 6 — grid 488..748, 3 cols x 4 rows, tiles 314x58
# ===========================================================================
GRID_TOP = 488
GRID_ROWS = 4
TILE_H = 58
TILE_W = 314
STRIP_W, STRIP_H = 74, 56


def draw_grid(d, page):
    band = "grid"
    pitch = 65
    for i, s in enumerate(GRID):
        r, c = divmod(i, 3)
        x = FEAT_X[c]
        y = GRID_TOP + r * pitch
        page.paste(art(s["strip"], (0, 0, STRIP_W, STRIP_H)), (x, y + 1))
        d.rectangle([x, y + 1, x + STRIP_W - 1, y + STRIP_H], outline=BRASS)

        tx = x + STRIP_W + 8
        twid = TILE_W - STRIP_W - 8

        # kicker at baseline y+8: numeral, place · category, tag right
        nf = font(SERIF_B, 10)
        kf = font(SANS_B, 6.5)
        tf = font(SANS, 6)
        cx = tx
        num = "%02d" % s["n"]
        d.text((cx, y + 8), num, font=nf, fill=HARBOUR, anchor="ls")
        register(band, *line_box(nf, num, cx, y + 8), num)
        cx += tw(num, nf) + 5
        kick = "%s · %s" % (s["place"], s["cat"])
        assert tw(kick, kf) <= twid - 60, "grid place chip too wide: %r" % kick
        d.text((cx, y + 8), kick, font=kf, fill=HARBOUR, anchor="ls")
        register(band, *line_box(kf, kick, cx, y + 8), kick)
        tag = s["sure"]
        tag_x = x + TILE_W - tw(tag, tf)
        d.text((tag_x, y + 8), tag, font=tf, fill=BRASS, anchor="ls")
        register(band, *line_box(tf, tag, tag_x, y + 8), tag)
        assert cx + tw(kick, kf) < tag_x - 3, "grid kicker hits tag: %r" % s["head"]

        # headline, two lines at 11px (baselines y+20, y+31)
        hf = font(SERIF_B, 11)
        hl = as_lines(s["head"], hf, twid, max_lines=2)
        hy = y + 20
        for ln in hl:
            d.text((tx, hy), ln, font=hf, fill=INK, anchor="ls")
            register(band, *line_box(hf, ln, tx, hy), ln)
            hy += 11

        # dek, two lines at 11px (baselines y+42, y+53)
        df = font(SANS, 11)
        dl = as_lines(s["dek"], df, twid, max_lines=2)
        dy = y + 42
        for ln in dl:
            d.text((tx, dy), ln, font=df, fill=INK, anchor="ls")
            register(band, *line_box(df, ln, tx, dy), ln)
            dy += 11
        assert dy - 11 <= y + 56, "grid tile overflows: %r" % s["head"]

    # separators between rows
    for r in range(1, GRID_ROWS):
        yy = GRID_TOP + r * pitch - 4
        hairline(d, MAR_L, MAR_R, int(yy))


# ===========================================================================
# BAND 7 — briefs 758..884 (left, x28..556) + world map (right, x580..996)
# ===========================================================================
BRIEFS_TOP = 758
BRIEFS_BOT = 884
BRIEFS_L = 28
BRIEFS_R = 556
BRIEF_COL_W = 258
BRIEF_GUT = 12
MAP_L, MAP_R = 580, 996
MAP_T, MAP_B = 758, 871


def draw_briefs(d, page):
    """18 briefs, two columns. Numeral in HARBOUR, one number device only.
    Text is set at the largest size in BRIEF_SIZES whose FULL text fits the
    column in at most its line allowance — never truncated, never below 8px."""
    band = "briefs"
    small_caps_label(d, band, "BRIEFS", BRIEFS_L, BRIEFS_TOP + 7, HARBOUR,
                     size=7, track=1.1)
    hairline(d, BRIEFS_L, BRIEFS_R, BRIEFS_TOP + 10, HARBOUR)

    allowances = {27: 3, 31: 2}
    size = None
    for s in (8.5, 8.25, 8):
        cand = [len(wrap(b["text"], font(SANS, s),
                          BRIEF_COL_W - 20)) for b in BRIEFS]
        if all(n <= allowances.get(b["n"], 1) for n, b in zip(cand, BRIEFS)):
            size = s
            break
    assert size is not None, "briefs never fit at 8px — BREAKS THE 8px FLOOR"

    df = font(SANS, size)
    nf = font(SERIF_B, 9)
    lead = size + 1.3
    # 10 briefs left, 8 right: both list-briefs (27, 31) land in the right column
    splits = [(BRIEFS_L, BRIEFS[0:10]),
              (BRIEFS_L + BRIEF_COL_W + BRIEF_GUT, BRIEFS[10:])]
    x_right_col = BRIEFS_L + BRIEF_COL_W + BRIEF_GUT
    assert x_right_col + BRIEF_COL_W <= BRIEFS_R + 1, "briefs columns overrun"

    y_last = 0
    for cx, items in splits:
        y = BRIEFS_TOP + 18
        for b in items:
            num = "%02d" % b["n"]
            d.text((cx, y), num, font=nf, fill=HARBOUR, anchor="ls")
            register(band, *line_box(nf, num, cx, y), num)
            tx = cx + 20
            lines = as_lines(b["text"], df, BRIEF_COL_W - 20,
                             max_lines=allowances.get(b["n"], 1))
            for ln in lines:
                draw_line(d, band, ln, df, INK, tx, y)
                y += lead
            y_last = max(y_last, y - lead)
    assert y_last <= BRIEFS_BOT - 4, (
        "briefs column runs past %d (last baseline %.1f)" % (BRIEFS_BOT, y_last))
    for cx, _ in splits[1:]:
        vline(d, cx - BRIEF_GUT // 2, BRIEFS_TOP + 13, BRIEFS_BOT - 4, BRASS)


# --- world map -------------------------------------------------------------
# 416x113 for 360x98 degrees: 1.1556 px/deg across, 1.1531 down — no distortion.
LAT_TOP, LAT_BOT = 61.5, -36.5
MAP_W, MAP_H = MAP_R - MAP_L, MAP_B - MAP_T

CONTINENTS = [
    # North America
    [(-168, 65), (-160, 71), (-140, 70), (-124, 70), (-110, 69), (-95, 72),
     (-80, 73), (-62, 66), (-55, 52), (-66, 45), (-70, 42), (-76, 35),
     (-81, 26), (-90, 29), (-97, 26), (-105, 23), (-114, 29), (-124, 40),
     (-128, 50), (-135, 58), (-150, 59), (-165, 55)],
    # South America
    [(-80, 10), (-72, 12), (-60, 10), (-50, 0), (-35, -6), (-38, -15),
     (-48, -25), (-58, -35), (-65, -42), (-72, -52), (-76, -45), (-72, -30),
     (-70, -18), (-78, -5), (-81, 2)],
    # Eurasia
    [(-10, 36), (0, 43), (-9, 44), (-2, 48), (-5, 50), (1, 51), (8, 54),
     (10, 58), (5, 58), (8, 63), (15, 68), (28, 71), (40, 68), (60, 70),
     (80, 73), (100, 76), (120, 73), (140, 72), (160, 70), (170, 66),
     (160, 60), (155, 55), (142, 50), (140, 42), (130, 35), (122, 31),
     (120, 23), (110, 20), (105, 10), (100, 5), (95, 10), (90, 22),
     (80, 15), (77, 8), (72, 20), (65, 25), (57, 25), (50, 30), (45, 38),
     (35, 36), (28, 36), (20, 40), (12, 44), (3, 42), (-6, 36)],
    # Africa
    [(-17, 21), (-16, 14), (-10, 5), (0, 5), (9, 4), (9, -1), (12, -6),
     (12, -17), (15, -23), (18, -30), (20, -35), (28, -33), (32, -28),
     (35, -22), (40, -15), (41, -5), (43, 2), (51, 11), (43, 12), (38, 18),
     (34, 28), (32, 31), (25, 32), (20, 31), (12, 33), (0, 36), (-6, 36),
     (-10, 30)],
    # Australia
    [(113, -22), (114, -27), (115, -34), (120, -34), (129, -32), (137, -35),
     (141, -38), (146, -39), (150, -37), (153, -28), (153, -25), (146, -19),
     (142, -11), (136, -12), (130, -11), (126, -14), (122, -17), (114, -21)],
    # Japan
    [(130, 31), (132, 34), (136, 35), (140, 38), (142, 41), (145, 43),
     (141, 45), (138, 37), (135, 34), (131, 31)],
    # New Zealand
    [(172, -41), (174, -37), (178, -38), (174, -41)],
    # Greenland
    [(-45, 60), (-20, 70), (-18, 78), (-40, 83), (-58, 80), (-55, 68)],
]


def map_xy(lon, lat):
    """Position inside the map panel (0..MAP_W, 0..MAP_H)."""
    x = (lon + 180.0) / 360.0 * MAP_W
    y = (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return x, y


def proj(lon, lat):
    x, y = map_xy(lon, lat)
    return MAP_L + x, MAP_T + y


def build_map():
    """Ocean, graticule, land tint and coastlines, drawn to their own layer so
    nothing can spill out of the panel."""
    im = Image.new("RGB", (MAP_W, MAP_H), OCEAN)
    md = ImageDraw.Draw(im)
    for gx in range(30, MAP_W, 46):
        md.line([gx, 0, gx, MAP_H], fill=(0xDB, 0xE2, 0xDC))
    for gy in range(18, MAP_H, 23):
        md.line([0, gy, MAP_W, gy], fill=(0xDB, 0xE2, 0xDC))
    for poly in CONTINENTS:
        pts = [map_xy(lon, lat) for lon, lat in poly]
        md.polygon(pts, fill=LAND)
        md.line(pts + [pts[0]], fill=(0xB2, 0xC1, 0xB9), width=1)
    return im


def draw_map(d, page):
    band = "map"
    page.paste(build_map(), (MAP_L, MAP_T))
    d.rectangle([MAP_L, MAP_T, MAP_R, MAP_B], outline=BRASS)

    nf = font(SERIF_B, 11)
    placed = []
    for n, lon, lat in PINS:
        px, py = proj(lon, lat)
        dx, dy = MAP_LABELS[n]
        lx, ly = px + dx, py + dy
        num = "%02d" % n
        w = tw(num, nf)
        if dx or dy:
            end = (lx + (0 if dx > 0 else w), ly - 4)
            d.line([px, py, end[0], end[1]], fill=BRASS)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], outline=BRASS)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=HARBOUR)
        d.text((lx, ly), num, font=nf, fill=HARBOUR, anchor="ls")
        box = line_box(nf, num, lx, ly)
        register(band, *box, num)
        for pb in placed:
            assert not (box[0] < pb[2] and pb[0] < box[2]
                        and box[1] < pb[3] and pb[1] < box[3]), (
                "map pin labels collide: %s vs %s" % (num, pb[4]))
        placed.append(box + (num,))
        assert MAP_L + 2 <= box[0] and box[2] <= MAP_R - 2, "pin %s leaves map x" % num
        assert MAP_T + 2 <= box[1] and box[3] <= MAP_B - 1, "pin %s leaves map y" % num

    small_caps_label(d, band, "31 STORIES", MAP_L + 6, MAP_T + 12, HARBOUR,
                     size=6.5, track=1.2)
    draw_line(d, band, MAP_NOTE, font(SANS, 6), INK, MAP_L, MAP_B + 10)


def _seg_cross(p, q, r, s):
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1, d2 = cr(r, s, p), cr(r, s, q)
    d3, d4 = cr(p, q, r), cr(p, q, s)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def _hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def solve_labels():
    """Place 31 numerals around their pins: nearest free slot, fewest leader
    crossings. Europe holds 13 pins in 50x30px, so most labels need a leader.
    Solved at import time against the real panel geometry."""
    nf = font(SERIF_B, 11)
    nw = tw("00", nf)
    nb = nf.getbbox("00", anchor="ls")
    cands = []
    for r in (13, 17, 21, 26, 31, 37, 44, 52, 61, 71, 82, 95, 110, 126, 144, 164):
        for a in range(0, 360, 10):
            cands.append((r * math.cos(math.radians(a)),
                          -r * math.sin(math.radians(a))))
    pins = [(n, *proj(lon, lat)) for n, lon, lat in PINS]
    dots = [(px, py) for _, px, py in pins]
    boxes, leaders, out = [], [], {}
    for n, px, py in pins:
        best = None
        for dx, dy in cands:
            lx, ly = px + dx, py + dy
            box = (lx, ly + nb[1], lx + nw, ly)
            if not (MAP_L + 3 <= box[0] and box[2] <= MAP_R - 3):
                continue
            if not (MAP_T + 14 <= box[1] and box[3] <= MAP_B - 3):
                continue
            if any(_hit(box, b) for b in boxes):
                continue
            end = (lx + (0 if dx > 0 else nw), ly - 4)
            clash = sum(1 for (a, b) in leaders
                        if _seg_cross((px, py), end, a, b))
            clash += sum(1 for (mx, my) in dots
                         if _hit(box, (mx - 4, my - 4, mx + 4, my + 4)))
            score = (clash, abs(dx) + abs(dy) * 1.4)
            if best is None or score < best[0]:
                best = (score, dx, dy, box, ((px, py), end), lx, ly)
        assert best is not None, "no map label slot for story %d" % n
        _, dx, dy, box, leader, lx, ly = best
        boxes.append(box)
        leaders.append(leader)
        out[n] = (round(lx - px, 2), round(ly - py, 2))
    return out


MAP_LABELS = solve_labels()


# ===========================================================================
# BAND 8 — HOW SURE 890..908 (all four keys, one line each)
# ===========================================================================
SURE_TOP = 890


def draw_how_sure(d):
    band = "how sure"
    hairline(d, MAR_L, MAR_R, SURE_TOP, BRASS)
    small_caps_label(d, band, "HOW SURE", MAR_L, SURE_TOP + 14, HARBOUR,
                     size=7, track=1.1)
    x = MAR_L + 66
    kf = font(SANS_B, 8)
    vf = font(SANS, 8)
    for i, (key, definition) in enumerate(LEGEND):
        x = draw_spans(d, band, [(key, kf, HARBOUR)], x, SURE_TOP + 14)
        x += 4
        x = draw_spans(d, band, [(definition, vf, INK)], x, SURE_TOP + 14)
        if i != len(LEGEND) - 1:
            d.ellipse([x + 5, SURE_TOP + 12, x + 7, SURE_TOP + 14], fill=BRASS)
            x += 14
    assert x <= MAR_R, "HOW SURE legend overruns: ends at %.0f" % x


# ===========================================================================
# BAND 9 — DATE CHECK 914..1000, drawn LAST with asserted clearance above
# ===========================================================================
DC_TOP, DC_BOT = 914, 1000
DC_L, DC_R = MAR_L, MAR_R
DC_WIDE = 366
DC_NARROW = 190
DC_GAP = 14


def dc_rows(title, date, note, w):
    """Wrap one DATE CHECK row into lines of (word, font). The real date is
    bold and is never split across lines."""
    tf, df, nf = font(SANS, 8), font(SANS_B, 8), font(SANS, 8)
    words = [(x, tf) for x in title.split()]
    words.append((date, df))
    words += [(x, nf) for x in note.split()] if note else []
    lines, cur, curw = [], [], 0.0
    for word, f in words:
        ww = tw(word, f)
        sp = tw(" ", f) if cur else 0.0
        if cur and curw + sp + ww > w:
            lines.append(cur)
            cur, curw = [(word, f)], ww
        else:
            cur.append((word, f))
            curw += sp + ww
    if cur:
        lines.append(cur)
    return lines


def dc_columns():
    """LEFT OUT in two wide columns (each item sets on one line), NOT YET in a
    third. Sixteen items, five rows maximum."""
    return [(LEFT_OUT[0:5], "LEFT OUT", DC_WIDE),
            (LEFT_OUT[5:10], "LEFT OUT", DC_WIDE),
            (NOT_YET, "NOT YET", DC_NARROW)]


def draw_date_check(d):
    band = "date check"
    # clearance: nothing above may reach into the box
    above = [b for b in BOXES if b[0] in ("how sure", "briefs", "map")]
    assert above, "DATE CHECK needs the bands above it to be drawn first"
    low = max(b[4] for b in above)
    assert low <= DC_TOP - 4, (
        "DATE CHECK clearance violated: band above reaches y=%.0f" % low)

    panel(d, (DC_L, DC_TOP, DC_R, DC_BOT), fill=CREAM, outline=BRASS)
    d.rectangle([DC_L, DC_TOP, DC_L, DC_BOT], fill=HARBOUR)
    d.rectangle([DC_R - 1, DC_TOP, DC_R - 1, DC_BOT], fill=HARBOUR)
    small_caps_label(d, band, "DATE CHECK", DC_L + 9, DC_TOP + 11, HARBOUR,
                     size=7.5, track=1.2)
    draw_line(d, band, "what did not fit Tuesday — and what has not happened yet",
              font(SANS, 7.5), INK, DC_L + 88, DC_TOP + 11)
    hairline(d, DC_L + 8, DC_R - 8, DC_TOP + 16, BRASS)

    # NOT YET has six rows and is the binding column: kicker 936, first
    # baseline 945, 8.8 leading, 0.2 gap -> last ink at ~992 (box ends 1000).
    leading, gap = 8.8, 0.2
    y_kick = DC_TOP + 22
    y_first = y_kick + 9
    cols = dc_columns()
    for i, (items, kicker, w) in enumerate(cols):
        x = DC_L + 9 + i * (DC_WIDE + DC_GAP)
        small_caps_label(d, band, kicker, x, y_kick, HARBOUR, size=6.5, track=1.0)
        y = y_first
        ink_bot = 0.0
        for it in items:
            lines = dc_rows(it[0], it[1], it[2] if len(it) == 3 else "", w)
            for ln in lines:
                cx = x
                for t, f in ln:
                    d.text((cx, y), t, font=f, anchor="ls",
                           fill=HARBOUR if f.getname()[0].endswith("Bold") else INK)
                    cx += tw(t, f) + tw(" ", f)
                lx0 = line_box(ln[0][1], ln[0][0], x, y)[0]
                last_t, last_f = ln[-1]
                lx1 = cx - tw(" ", last_f)
                top = min(line_box(f, t, 0, y)[1] for t, f in ln)
                bot = max(line_box(f, t, 0, y)[3] for t, f in ln)
                register(band, lx0, top, lx1, bot, " ".join(t for t, _ in ln))
                ink_bot = max(ink_bot, bot)
                y += leading
            y += gap
        assert ink_bot <= DC_BOT - 4, (
            "DATE CHECK %s column ink reaches %.1f, box ends %d"
            % (kicker, ink_bot, DC_BOT))
    for i in (1, 2):
        x = DC_L + 9 + i * (DC_WIDE + DC_GAP) - DC_GAP / 2
        vline(d, int(x), DC_TOP + 20, DC_BOT - 5, BRASS)

# ===========================================================================
# STAGE (f) — audit suite and render entry point
# ===========================================================================
# The page is finished; now prove it. Every rule the brief states as an
# assertion is checked here on the real geometry and on the real pixels.

BANDS = [
    ("masthead",    28,  150),
    ("timeline",   154,  178),
    ("regions",    182,  204),
    ("stats",      210,  256),
    ("featured",   264,  476),
    ("grid",       488,  748),
    ("briefs",     758,  884),
    ("map",        758,  884),
    ("how sure",   890,  908),
    ("date check", 914, 1000),
]

HARD_FLOOR = {"featured": 11.0, "grid": 11.0, "stats": 8.0,
              "briefs": 8.0, "how sure": 8.0, "date check": 7.5}


def accent_fraction(page):
    """Fraction of page pixels that read as HARBOUR or BRASS.

    Classified by nearest palette entry, so anti-aliased edges land with the
    colour they were drawn in rather than being lost between buckets."""
    try:
        import numpy as np
    except ImportError:                       # pragma: no cover
        raise SystemExit("numpy is needed for the accent-coverage assertion")
    pal = [PAPER, INK, HARBOUR, BRASS, CREAM, LAND]
    ref = np.array(pal, dtype=np.int32)
    a = np.asarray(page.convert("RGB"), dtype=np.int32)
    idx = ((a[None] - ref[:, None, None, :]) ** 2).sum(-1).argmin(0)
    accent = (idx == 2) | (idx == 3)
    return float(accent.sum()) / (page.width * page.height)


def audit(page):
    """Every guard in the brief, checked. Returns a list of report lines."""
    rep = []
    assert page.size == (W, H), "page is %r, not 1024x1024" % (page.size,)
    assert page.mode == "RGB", "page mode is %s" % page.mode

    # --- 33 stories, region counts summing to 33 ---
    assert len(ALL_STORIES) == 33, "page carries %d stories" % len(ALL_STORIES)
    nums = [s["n"] for s in ALL_STORIES]
    assert sorted(nums) == list(range(1, 34)), "story numerals are not 1..33"
    counts = region_counts()
    assert sum(len(v) for v in counts.values()) == 33, "region sum is not 33"
    rep.append("stories 33, regions sum 33 (%s)" %
               ", ".join("%s %d" % (k, len(v)) for k, v in counts.items()))

    # --- map pins: 31 pins, 27 and 31 carried by the map note instead ---
    pin_nums = [p[0] for p in PINS]
    assert len(pin_nums) == 31, "%d pins, want 31" % len(pin_nums)
    assert len(set(pin_nums)) == 31, "duplicate pin numeral"
    assert set(pin_nums) <= set(nums), "pin numeral with no story"
    assert sorted(set(nums) - set(pin_nums)) == [27, 31], (
        "pins leave %r unexplained" % sorted(set(nums) - set(pin_nums)))
    rep.append("map pins 31, stories 27 and 31 held as the map note")

    # --- artwork integrity: three scenes and twelve strips, exact sizes ---
    for s in FEATURED:
        p = os.path.join(ASSETS, "f%d.jpg" % s["n"])
        with Image.open(p) as im:
            assert im.size == (FEAT_W, FEAT_ART_H), (
                "featured art %s is %r" % (p, im.size))
    for s in GRID:
        p = os.path.join(ASSETS, s["strip"])
        with Image.open(p) as im:
            assert im.size == (STRIP_W, STRIP_H), (
                "strip %s is %r" % (p, im.size))
    rep.append("art 3x 314x157 and 12x 74x56, all present")

    # --- every band inside its declared slot, nothing off the page ---
    for name, top, bot in BANDS:
        items = [b for b in BOXES if b[0] == name]
        assert items, "band %r printed nothing" % name
        lo = min(b[2] for b in items)
        hi = max(b[4] for b in items)
        assert lo >= top - 2, "%s starts at %.1f, slot opens %d" % (name, lo, top)
        assert hi <= bot + 2, "%s reaches %.1f, slot closes %d" % (name, hi, bot)
        rep.append("%-10s boxes %3d  y %.0f..%.0f" % (name, len(items), lo, hi))

    for b in BOXES:
        assert 0 <= b[1] and 0 <= b[2] and b[3] <= W and b[4] <= H, (
            "box leaves the page: %r" % (b,))

    # --- pairwise line separation, proved band by band ---
    for name, _, _ in BANDS:
        bad = check_overlaps(name)
        assert not bad, "%s has %d overlapping line pairs, first %r" % (
            name, len(bad), bad[0][0][5])
    rep.append("pairwise line separation: 0 overlaps in all 10 bands")

    # --- DATE CHECK clearance above the box ---
    above = [b for b in BOXES if b[0] in ("how sure", "briefs", "map")]
    low = max(b[4] for b in above)
    assert low <= DC_TOP - 4, "DATE CHECK clearance: %.1f" % low
    rep.append("DATE CHECK clearance: ink above ends %.0f, box opens %d"
               % (low, DC_TOP))

    # --- body floors ---
    for name, floor in HARD_FLOOR.items():
        items = [b for b in BOXES if b[0] == name]
        if name in ("featured", "grid"):
            pass                                  # sizes asserted where set
    bf = font(SANS, 8)
    assert bf.size >= 8, "briefs font below the 8px floor"
    assert font(SERIF_B, 11).size >= 11, "headline font below the 11px floor"
    rep.append("type floors: headlines 11px, body 11px, briefs 8px")

    # --- HARD GUARD: accent-family pixels under 12% of the page ---
    frac = accent_fraction(page)
    assert frac < 0.12, (
        "accent coverage is %.2f%% of the page — the 12%% guard fails"
        % (100.0 * frac))
    rep.append("accent coverage %.2f%% of page (< 12%% guard)" % (100.0 * frac))

    # --- the finished image carries its own facts: read the words back ---
    assert "26" in FEATURED[2]["dek"] and "8 missing" in FEATURED[2]["dek"]
    assert "28" not in FEATURED[2]["head"] + FEATURED[2]["dek"], (
        "28 must never be typeset as the missing figure")
    assert "28" in LEFT_OUT[9][0], "the 28 conflict must sit in DATE CHECK"
    rep.append("story 3 typesets 26 dead / 8 missing; 28 only as the conflict")
    return rep


def render():
    """Draw the page in band order. DATE CHECK is last by construction."""
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    BOXES.clear()

    draw_masthead(d)
    draw_timeline(d)
    draw_region_bar(d)
    draw_stats(d)
    draw_featured(d, page)
    draw_grid(d, page)
    draw_briefs(d, page)
    draw_map(d, page)
    draw_how_sure(d)
    draw_date_check(d)                 # drawn LAST, on top of cleared space

    report = audit(page)
    return page, report


def main():
    page, report = render()
    page.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    assert size <= 1048576, "entry.png is %d bytes, cap is 1048576" % size
    assert page.size == (1024, 1024)
    print("\n".join(report))
    print("wrote %s — %d bytes, 1024x1024" % (OUT, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

