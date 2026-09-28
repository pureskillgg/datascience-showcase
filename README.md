# PureSkill.gg Data Science Showcase

Make PureSkill.gg-style graphics from Counter-Strike 2 match data.

Clone this repo, point it at your data, and matplotlib plots in the house style: the PureSkill.gg colors, fonts and sizes, canvases sized for Instagram, TikTok, YouTube, X, slides and articles, and the attribution line on every image.

## Quickstart

You need [Python 3.14](https://www.python.org/) and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/pureskillgg/datascience-showcase.git
cd datascience-showcase
uv sync
make hooks   # the pre-commit checks
```

```python
import pureskillgg_datascience_showcase as psgg

fig, ax = psgg.figure("Kills by weapon", "60 matches, July 2026", preset="square")
ax.barh(["AK-47", "M4A1-S", "AWP"], [2927, 1414, 813])
psgg.save("out/kills.png")
```

Importing the package applies the style, so plain `plt.subplots()` code comes out branded too, and `psgg.save()` adds the attribution line to it.

| Preset | Size | For |
| --- | --- | --- |
| `square` | 1080×1080 | Instagram feed, LinkedIn, Discord |
| `portrait` | 1080×1350 | Instagram feed, Reddit on phones |
| `vertical` | 1080×1920 | Stories, reels, TikTok, YouTube Shorts |
| `wide` | 1920×1080 | YouTube, slides, X, Reddit, Discord |
| `link` | 1200×630 | Link previews |
| `article` | 1200 wide, rendered at 2× | Docs and blog posts |

`scale=2` renders any preset at double resolution and looks the same. `theme="light"` switches to the light background.

## Attribution and the logo

The data license requires **"Data provided by PureSkill.gg."** on anything you publish. `psgg.save()` puts it on every image.

`official=True` adds the PureSkill.gg logo. **Only PureSkill.gg's own graphics are official.** If you didn't make it as PureSkill.gg, don't mark it official, and don't add the logo any other way.

## License

The code is under the [MIT license](LICENSE.txt). The MIT license covers the code, not the PureSkill.gg name or logo.

The bundled fonts, [Russo One](pureskillgg_datascience_showcase/fonts/OFL-RussoOne.txt) and [Assistant](pureskillgg_datascience_showcase/fonts/OFL-Assistant.txt), are under the SIL Open Font License.

The match data is licensed separately, when you subscribe to it; see [docs.pureskill.gg](https://docs.pureskill.gg/datascience/).
