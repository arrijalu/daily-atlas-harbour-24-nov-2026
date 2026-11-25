[![make.fun - news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/jusst01/daily-atlas-harbour-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/jusst01/daily-atlas-harbour-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# THE DAILY ATLAS — Tuesday 24 November 2026

The harbour edition of the Daily Atlas: a 1024x1024 newspaper front
page that sums up one day's world news in a single image — 33 stories on one
flat, clean page. A dated masthead, a region-count bar, a UTC timeline, a
six-number stat strip, three featured stories with full flat-editorial
artwork, a numbered grid of twelve, eighteen briefs and a world map whose pins
carry the same story numbers, and a DATE CHECK strip naming the other days'
stories that were deliberately left out.

## How it is built

- `draw.py` renders the page from the story data with Pillow and numpy and
  asserts its own layout: no clipped or overlapping text, all 33 story numbers
  drawn, region counts summing to 33, output a 1024x1024 PNG under 1 MiB.
- `assets/*.jpg` are generated flat-editorial illustrations (no baked-in text).
- `main.py` is the submitted entrypoint: standard library only, it copies the
  bundled `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`) via a
  staged file plus an atomic rename.

## How to run it

```bash
python3 -m venv .venv
.venv/bin/pip install pillow numpy
.venv/bin/python draw.py          # writes entry.png next to draw.py

MAKEFUN_OUTPUT_DIR=./out python3 main.py   # deploys entry.png
```

## Bounty

Competition page: <https://make.fun/c/news-image-20261124>
