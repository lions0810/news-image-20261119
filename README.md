# The World in One Day — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/lions0810/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/lions0810/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page for Thursday 19 November 2026, built
for the [news-image-20261119](https://make.fun/bounty/news-image-20261119)
bounty on make.fun.

## What is on the page

The front page covers the day in 44 stories:

- **Four illustrated leads** — GTA VI launch day, the first-ever
  Trump–Xi–Putin trilateral summit in Shenzhen, the World Court ruling
  that Myanmar committed genocide against the Rohingya, and three oil
  tankers ablaze after striking mines east of the Strait of Hormuz.
- **A UTC timeline strip** — six moments from the day, from the
  early-hours conflict-zone figures to the late-night word from
  Washington on Iran.
- **More from the day** — 34 further stories in two columns, from the
  Crimean Bridge strike and Wall Street's fifth straight fall to
  Voyager 1 reaching one light-day from Earth.

Every headline was written for this edition from the day's reporting;
the four illustrations are the panels in `panels/`.

## Files

- `entry.png` — the finished 1024×1024 front page (the entry itself).
- `compose.py` — the renderer that draws the page with Pillow:
  masthead, 2×2 illustrated leads, UTC strip, and the two-column
  story list. Run it to rebuild `entry.png`.
- `main.py` — the deterministic entry runner. It copies the bundled
  `entry.png` to an output directory and verifies the copy is
  byte-identical (matching SHA-256) and within the 1 MiB limit.
- `panels/` — the four lead illustrations (WebP), reused as supplied.

## Reproduce

```sh
python3 compose.py        # rebuild entry.png from the panels
python3 main.py           # copy entry.png to out/ and verify it
python3 main.py -o out2   # a second run must produce identical bytes
```

Both `main.py` runs print the same SHA-256 digest.

## License

MIT — see `LICENSE`.
