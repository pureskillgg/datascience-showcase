---
name: make-graphic
description: Make a PureSkill.gg-style graphic from CS2 match data in this repo, from the question to a checked, attributed image (a chart, a map graphic or an animation) and, if wanted, a gallery item. Use whenever the user asks for a chart, plot, graph, map, heatmap, visualization, animation or gallery item from PureSkill.gg data.
---

# Make a graphic

Work through these steps in order. Don't skip step 7.

## 1. Pin down the graphic

Settle four things before writing code. Ask the user about anything you can't infer:
- **The question** the graphic answers, in one sentence. It becomes the title.
- **Where it will be posted.** That picks the preset:

  | Destination | Preset |
  | --- | --- |
  | Instagram feed, LinkedIn, Discord | `square` |
  | Instagram feed (more screen), Reddit on phones | `portrait` |
  | Stories, reels, TikTok, YouTube Shorts | `vertical` |
  | YouTube, slides, X, Reddit | `wide` |
  | Link previews | `link` |
  | Docs, blog posts | `article` |

- **Official or not.** Only PureSkill.gg's own graphics are official. If the user isn't clearly PureSkill.gg making its own graphic, it's not official.
- **Dark (default) or light.** Light is for white pages and print.

## 2. Pick the form

Let the data's job choose the chart:
- **Comparing amounts:** bars, horizontal when the labels are long, like weapon names.
- **Change over rounds or time:** lines.
- **Where things happen:** a map, with `psgg.maps`.
- **Two measures per thing** (per player, per match): a scatter plot, with at most three groups.
- **One striking number:** a big number with a short line of context.
- **T against CT:** side colors (`psgg.side_color`), or the `psgg_sides_*` colormap.

Six series at most. A seventh goes into "Other", or the chart is split.

## 3. Get the data

- Load `.env` and the curator: `curator = psgg.curator()`. If it fails, ask the user where their data and tomes are. Never make data up.
- Read `docs/data-primer.md` for the columns you'll use. The usual traps:
  - team code 2 is T and 3 is CT;
  - `m4a1` is the M4A4;
  - `theta_ang` is yaw;
  - `*_id_fixed` columns can load as floats;
  - rank columns mix two scales;
  - two-floor maps need splitting by height.
- Work the transform out on one match (`curator.get_match_by_index(0).get_channels()`). Then build a tome with `make_tome` and `ds_reading_instructions` naming only the columns you need (`docs/getting-data.md`). Reuse a tome that already exists.
- Keep a note of **how many matches and which dates**; the subtitle needs them.

## 4. Draw it with the kit

```python
import pureskillgg_datascience_showcase as psgg

fig, ax = psgg.figure("Kills by weapon", "60 matches, 2026-08-01 to 08-07.", preset="square")
ax.barh(labels, values)                 # colors come from the style; don't pass your own
psgg.legend(ax)                         # when there are two or more series
psgg.save("out/kills.png", fig)         # adds the attribution, stamps the PNG
```

- Don't set colors, fonts, sizes or the figure size by hand. For series use the color cycle or `psgg.series_colors(n)`; for sides, `psgg.side_color("T")`.
- Maps: `psgg.maps.draw_radar(ax, map_name)`, then `psgg.maps.heatmap(...)` or `ax.scatter(*psgg.maps.to_radar(map_name, x, y))`, then `psgg.maps.label_sites(ax, map_name)`.
- Animations: build a `FuncAnimation` on a `psgg.figure()` canvas and render it with `psgg.save_animation(anim, "out/clip.mp4")`. Use `vertical` for TikTok and Shorts.
- Label directly when it's clearer: values at bar ends, series names at line ends (four series or fewer).
- `official=True` only if step 1 said official.

## 5. Write it to out/

Save work in progress to `out/`, which git ignores. Only a finished gallery image goes in `gallery/`.

## 6. Render

Run the script or notebook. Make sure the PNG exists at the preset's size.

## 7. Look at it

**Open the saved PNG and look at it.** Then check each of these, fix what fails, and render again:
- [ ] Nothing overlaps: tick labels, legend, title, value labels, the footer.
- [ ] The text is readable at the posted size. The kit's sizes are right, so if something is cramped, cut the text, don't shrink it.
- [ ] The title answers the question, and the subtitle gives the matches, dates and what the colors mean.
- [ ] The legend or direct labels name every series; the colors follow the kit's order; T is amber and CT blue.
- [ ] "Data provided by PureSkill.gg." is at the bottom right. The logo is there only if the graphic is official.
- [ ] The numbers are plausible: totals add up, shares sum to 100%, and nothing is missing that shouldn't be.

## 8. Gallery item (if wanted)

1. Copy `templates/gallery-item/` to `gallery/<slug>/`.
2. Put the drawing code in `make.py` so it rebuilds the image in one command.
3. Save the final PNG there with `psgg.save()`.
4. Fill in the README front matter: `title`, `author`, `official`, `data`, `image`, and `video` if there's one.
5. For a video, publish it, commit a still frame (`psgg.save()`), and put the link in `video`.
6. Run `make gallery`, then `make check`, `make lint` and `make test`.

## 9. Report back

Tell the user where the image is, what it shows in one sentence, how many matches and which dates it covers, and anything in the data that surprised you or that you filtered out.
