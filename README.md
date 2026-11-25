# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Kodoku05/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Kodoku05/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

The World Today — Wednesday 25 November 2026: a deterministic newspaper
poster covering the verified world news of the day in one 1024×1024 PNG.
The page has four illustrated lead stories, the Gulf explainer, 46 short
briefs, a UTC timeline, a location map, and a dated older-news check box.

`draw_poster.py` uses Pillow to draw the original flat-vector artwork. The
Node 22 entrypoint copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR`
or `/output` when no directory is supplied.

```sh
MAKEFUN_OUTPUT_DIR=./out node main.ts
```
