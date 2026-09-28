# AGENTS.md

Instructions for any coding agent working in this repo (Claude Code, Codex and others read this file). People are welcome to read it too.

## What this repo is

A kit for making PureSkill.gg-style graphics from Counter-Strike 2 match data: charts for social posts, articles and slides, map graphics, and animations. Importing `pureskillgg_datascience_showcase` makes matplotlib plot in the house style. Finished graphics go in `gallery/`, one folder each.

## Setup

```sh
uv sync          # Python 3.14 and every dependency
make hooks       # the pre-commit checks
cp .env.example .env   # then point it at the user's data
```

The user's data lives outside the repo. `docs/getting-data.md` explains how to get it and build tomes. If `.env` isn't set up, or there are no tomes, ask the user where their data is. Don't invent data or paths.

## Making a graphic

Follow **`.agents/skills/make-graphic/SKILL.md`** every time. It is the procedure, from the question to a checked image. The short version:

1. Know what the graphic is for and where it will be posted; that picks the preset.
2. Build or load a tome with only the columns you need.
3. Draw with the kit: `fig, ax = psgg.figure(title, subtitle, preset=...)`, `psgg.legend(ax)`, `psgg.save(path, fig)`.
4. **Open the saved image and look at it** before you call it done.

## Rules

- **Use the kit for all styling.** Don't set colors, fonts, font sizes or figure sizes by hand. Series colors come from the axes' color cycle or `psgg.series_colors(n)`, in their fixed order. Side colors come from `psgg.side_color("T" | "CT")`. `docs/style.md` has the full style guide.
- **At most six series; scatter plots at most three groups.** Fold the rest into "Other" or split the chart.
- **Every published image carries "Data provided by PureSkill.gg."** `psgg.save()` adds it. Don't remove it or cover it.
- **`official=True` (the logo) is only for PureSkill.gg's own graphics.** Use it only when the user tells you the graphic is PureSkill.gg's and they are PureSkill.gg. Otherwise never set it, and never draw the logo any other way.
- **Look before you finish.** After every render, open the PNG and check it:
  - no overlapping labels;
  - the text is readable at the size people will see it;
  - the title and subtitle say what's shown and which matches and dates;
  - the chart answers the question.
  Fix what you find and render again.
- **Check the data before you trust a column.** `docs/data-primer.md` lists the traps: team codes, the M4 names, the angle names, missing-value codes, the rank scales, dates, two-floor maps. For anything else, see the [CSDS spec](https://docs.pureskill.gg/datascience/adx/cs2/csds/spec). If the data can't answer the question, stop and tell the user. Offer the nearest question it can answer, and never switch questions silently.
- **Data never goes in git:** no parquet, CSV or other tables, no downloaded matches or tomes, no `.env`. Work output goes in `out/`, which git ignores.
- **Videos never go in git.** Render them to `out/` with `psgg.save_animation()`. In the gallery, commit a still frame (a `psgg.save()` PNG) and put the video's link in the item's README.
- **Notebooks are committed without outputs.** The pre-commit hook strips them.
- **Don't change the kit's look** (palette, fonts, presets, layout) unless the user asks for exactly that; it's the brand.
- **Don't publish, tag or bump versions.** This repo isn't released.

## Gallery items

Copy `templates/gallery-item/` to `gallery/<slug>/` (lowercase, hyphens). An item has:
- `make.py`, the notebook, or both;
- the images, as PNGs saved with `psgg.save()`;
- a `README.md` whose front matter has `title`, `author`, `official` (`true` or `false`), `data` (which matches and dates), `image` (the main PNG), and optionally `video` (a link).

Then run `make gallery` to rebuild `gallery/README.md`.

## Checks

Run these before you commit; CI runs the same:

```sh
make test    # pytest
make lint    # pylint and black
make check   # no data, secrets, videos or unstamped gallery images; gallery index up to date
```

`scripts/check_repo.py` refuses data files, `.env`, videos, notebooks with outputs, files over 10 MB, and gallery images that aren't stamped PNGs.

## Where things are

| Path | What |
| --- | --- |
| `pureskillgg_datascience_showcase/` | The kit: `style`, `palette`, `presets`, `figure`, `maps`, `animation`, `data` |
| `pureskillgg_datascience_showcase/radars/` | Stock CS2 radars and Valve's overview numbers |
| `docs/getting-data.md` | Subscribing, downloading, `.env`, building tomes |
| `docs/data-primer.md` | What's in a match, and the traps |
| `docs/style.md` | The style guide |
| `templates/gallery-item/` | A gallery item to copy |
| `gallery/` | Finished graphics |
| `scripts/` | The repo check, the gallery index, the style-guide images |
