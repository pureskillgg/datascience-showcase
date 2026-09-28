"""
Render the images in docs/style.md from the kit itself.

    uv run python scripts/render_style_guide.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

# pylint: disable=wrong-import-position
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import pureskillgg_datascience_showcase as psgg

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"


def palette():
    """Series, side and colormap swatches for both themes."""
    psgg.use("dark", "article")
    height = 760
    fig = plt.figure(figsize=(1200 / 72, height / 72), layout="none")
    band = 330 / height
    for row, theme in enumerate((psgg.DARK, psgg.LIGHT)):
        y0 = 1 - band * (row + 1)
        # A full-band background axes, so later axes (the colormap strips) draw on top of it.
        bg = fig.add_axes((0, y0, 1, band), zorder=0)
        bg.set_facecolor(theme.surface)
        bg.set_axis_off()
        bg.add_patch(Rectangle((0, 0), 1, 1, transform=bg.transAxes, color=theme.surface))
        fig.text(0.03, y0 + band * 0.86, theme.name.title(), fontsize=20, color=theme.strong, va="center")
        swatches = [
            (c, f"{i + 1}. {n}") for i, (c, n) in enumerate(zip(theme.series, psgg.palette.SERIES_NAMES))
        ]
        swatches += [(theme.t, "T"), (theme.ct, "CT")]
        for i, (color, label) in enumerate(swatches):
            x = 0.03 + i * 0.12
            bg.add_patch(Rectangle((x, 0.42), 0.05, 0.3, transform=bg.transAxes, color=color))
            fig.text(x, y0 + band * 0.3, label, fontsize=17, color=theme.ink)
            fig.text(x, y0 + band * 0.17, color, fontsize=16, color=theme.ink)
        for j, (cmap, label) in enumerate(
            ((psgg.sequential_cmap(theme), "sequential"), (psgg.sides_cmap(theme), "T to CT"))
        ):
            ax = fig.add_axes((0.03 + j * 0.3, y0 + band * 0.04, 0.2, band * 0.06), zorder=1)
            ax.imshow(np.linspace(0, 1, 256)[None, :], aspect="auto", cmap=cmap)
            ax.set_axis_off()
            fig.text(0.24 + j * 0.3, y0 + band * 0.07, label, fontsize=16, color=theme.ink, va="center")
    psgg.save(OUT / "palette.png", fig)
    plt.close(fig)


def layout():
    """The canvas anatomy, on made-up numbers."""
    fig, ax = psgg.figure("Title in capitals", "One line of context under it", preset="square", official=True)
    rounds = np.arange(1, 25)
    rng = np.random.default_rng(3)
    for name in ("Series one", "Series two", "Series three"):
        ax.plot(rounds, np.clip(rng.normal(30, 6, 24).cumsum() / rounds, 0, None), label=name)
    ax.set_xlabel("Round")
    psgg.legend(ax)
    notes = [
        (0.945, 0.945, "right", "title: Russo One"),
        (0.945, 0.87, "right", "subtitle"),
        (0.945, 0.815, "right", "psgg.legend()"),
        (0.055, 0.125, "left", "logo: official only"),
        (0.945, 0.125, "right", "attribution: always"),
    ]
    for x, y, ha, text in notes:
        fig.text(x, y, text, fontsize=30, color=psgg.DARK.t, ha=ha, va="top", style="italic")
    psgg.save(OUT / "layout.png", fig)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    palette()
    layout()
    print(f"wrote {OUT}")
