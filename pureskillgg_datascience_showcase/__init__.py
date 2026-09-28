"""
PureSkill.gg graphics for matplotlib.

Importing this package applies the house style, so plain matplotlib code comes
out in PureSkill.gg colors, fonts and sizes:

    import pureskillgg_datascience_showcase as psgg

    fig, ax = psgg.figure("Kills by weapon", "60 matches, July 2026", preset="square")
    ax.barh(...)
    psgg.save("out/kills.png")

Every saved image carries "Data provided by PureSkill.gg." Pass official=True
only for graphics PureSkill.gg itself made; it adds the logo.
"""

from . import maps
from .animation import save_animation
from .data import ENV_VARS, curator, load_env
from .figure import add_footer, figure, legend, read_stamp, save
from .palette import (
    ATTRIBUTION,
    DARK,
    LIGHT,
    THEMES,
    get_theme,
    heat_cmap,
    sequential_cmap,
    series_colors,
    side_color,
    sides_cmap,
)
from .presets import PRESETS, Preset, get_preset
from .style import current, rc_params, title_font, use

__all__ = [
    "ATTRIBUTION",
    "DARK",
    "ENV_VARS",
    "LIGHT",
    "PRESETS",
    "Preset",
    "THEMES",
    "add_footer",
    "curator",
    "current",
    "figure",
    "get_preset",
    "get_theme",
    "heat_cmap",
    "legend",
    "load_env",
    "maps",
    "rc_params",
    "read_stamp",
    "save",
    "save_animation",
    "sequential_cmap",
    "series_colors",
    "side_color",
    "sides_cmap",
    "title_font",
    "use",
]

use()
