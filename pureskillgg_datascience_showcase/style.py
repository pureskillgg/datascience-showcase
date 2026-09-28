"""
The PureSkill.gg matplotlib style.

Importing the package calls use(), so plain matplotlib code comes out in the
house style: the colors, the fonts, the sizes and the series order.
"""

from pathlib import Path

import matplotlib as mpl
from cycler import cycler
from matplotlib import colormaps, font_manager

from .palette import get_theme, heat_cmap, sequential_cmap, sides_cmap
from .presets import get_preset

FONT_DIR = Path(__file__).resolve().parent / "fonts"
BODY_FAMILY = "Assistant"
TITLE_FILE = FONT_DIR / "RussoOne-Regular.ttf"

_state = {"theme": "dark", "preset": "square", "scale": None}


def register_fonts():
    """Make the bundled fonts known to matplotlib. Safe to call more than once."""
    known = {Path(f.fname).resolve() for f in font_manager.fontManager.ttflist}
    for path in sorted(FONT_DIR.glob("*.ttf")):
        if path.resolve() not in known:
            font_manager.fontManager.addfont(str(path))


def title_font():
    """FontProperties for titles: Russo One, set in capitals by the caller."""
    return font_manager.FontProperties(fname=str(TITLE_FILE))


def register_colormaps():
    """Register psgg_heat, psgg_green_dark/light and psgg_sides_dark/light."""
    maps = [heat_cmap()]
    for name in ("dark", "light"):
        maps += [sequential_cmap(name), sides_cmap(name)]
    for cmap in maps:
        if cmap.name not in colormaps:
            colormaps.register(cmap)


def rc_params(theme="dark", preset="square", scale=None):
    """The rcParams for one theme and preset, as a dict."""
    th = get_theme(theme)
    pr = get_preset(preset, scale=scale)
    return {
        "figure.figsize": pr.figsize,
        "figure.dpi": 72,
        "savefig.dpi": pr.dpi,
        "figure.facecolor": th.surface,
        "savefig.facecolor": th.surface,
        "figure.constrained_layout.use": True,
        "figure.constrained_layout.h_pad": 0.2,
        "figure.constrained_layout.w_pad": 0.2,
        "axes.facecolor": th.surface,
        "axes.edgecolor": th.grid,
        "axes.labelcolor": th.ink,
        "axes.titlecolor": th.strong,
        "axes.titlelocation": "left",
        "axes.titlesize": pr.subtitle,
        "axes.titlepad": 16,
        "axes.labelsize": pr.body,
        "axes.labelpad": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "axes.prop_cycle": cycler(color=list(th.series)),
        "grid.color": th.grid,
        "grid.linewidth": 2,
        "text.color": th.ink,
        "font.family": BODY_FAMILY,
        "font.size": pr.body,
        "xtick.color": th.ink,
        "ytick.color": th.ink,
        "xtick.labelsize": pr.body,
        "ytick.labelsize": pr.body,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.minor.size": 0,
        "ytick.minor.size": 0,
        "xtick.major.pad": 10,
        "ytick.major.pad": 10,
        "legend.frameon": False,
        "legend.fontsize": pr.body,
        "legend.labelcolor": th.ink,
        "legend.title_fontsize": pr.body,
        "legend.handlelength": 1.0,
        "legend.handleheight": 0.6,
        "legend.handletextpad": 0.4,
        "legend.columnspacing": 1.4,
        "lines.linewidth": 4,
        "lines.markersize": 12,
        "lines.solid_capstyle": "round",
        "patch.edgecolor": th.surface,
        "patch.force_edgecolor": True,
        "patch.linewidth": 2,
        "image.cmap": f"psgg_green_{th.name}",
        "savefig.bbox": "standard",
    }


def use(theme=None, preset=None, *, scale=None):
    """
    Apply the style. With no arguments, reapply the current theme and preset.

    theme is "dark" (the default) or "light"; preset is a name from PRESETS.
    Figures made afterwards, with plain matplotlib or with figure(), follow it.
    """
    if theme is not None:
        _state["theme"] = get_theme(theme).name
    if preset is not None:
        _state["preset"] = get_preset(preset).name
    if scale is not None:
        _state["scale"] = scale
    register_fonts()
    register_colormaps()
    mpl.rcParams.update(rc_params(_state["theme"], _state["preset"], _state["scale"]))


def current():
    """The theme name, preset name and scale in force."""
    return dict(_state)
