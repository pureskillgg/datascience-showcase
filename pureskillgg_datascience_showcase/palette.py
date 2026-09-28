"""
Colors for PureSkill.gg graphics, taken from the webapp and checked for charts.

Series colors come in a fixed order. Assign them in that order and never cycle
them: a seventh series folds into "Other" or moves to a second chart. Scatter
plots take at most the first three, since any two dots can sit side by side.
"""

from dataclasses import dataclass

from matplotlib.colors import LinearSegmentedColormap, to_rgb

ATTRIBUTION = "Data provided by PureSkill.gg."


@dataclass(frozen=True)
class Theme:
    """Everything a figure needs to know about one background."""

    name: str
    surface: str
    ink: str
    strong: str
    grid: str
    series: tuple
    t: str
    ct: str
    neutral: str


DARK = Theme(
    name="dark",
    surface="#1e2029",
    ink="#8d9ba3",
    strong="#ffffff",
    grid="#2d313f",
    series=("#4fa863", "#5f8ece", "#b84d4f", "#b772cd", "#a66200", "#12a7a7"),
    t="#e89230",
    ct="#84a9dc",
    neutral="#4a5160",
)

LIGHT = Theme(
    name="light",
    surface="#f5f6f8",
    ink="#4a5560",
    strong="#1e2029",
    grid="#dfe3e8",
    series=("#459f5b", "#4d7bba", "#9d3539", "#ad69c3", "#874e00", "#0a9d9d"),
    t="#ce7816",
    ct="#6090d1",
    neutral="#c9ced4",
)

THEMES = {"dark": DARK, "light": LIGHT}

SERIES_NAMES = ("green", "blue", "red", "purple", "amber", "cyan")


def get_theme(theme):
    """Return a Theme from a name or a Theme."""
    if isinstance(theme, Theme):
        return theme
    try:
        return THEMES[theme]
    except KeyError as err:
        raise ValueError(f"Unknown theme {theme!r}; use one of {sorted(THEMES)}") from err


def series_colors(n=None, theme="dark"):
    """The first n series colors, in their fixed order."""
    colors = get_theme(theme).series
    if n is None:
        return list(colors)
    if n > len(colors):
        raise ValueError(
            f"{n} series is more than the {len(colors)} colors that stay distinguishable; "
            "fold the smallest into 'Other' or split the chart"
        )
    return list(colors[:n])


def side_color(side, theme="dark"):
    """The color for a side: 'T' (amber) or 'CT' (blue). Team codes 2 and 3 also work."""
    key = {2: "T", 3: "CT"}.get(side, str(side).upper())
    th = get_theme(theme)
    if key == "T":
        return th.t
    if key == "CT":
        return th.ct
    raise ValueError(f"Unknown side {side!r}; use 'T', 'CT', 2 or 3")


def heat_cmap():
    """Transparent to green to sand: an overlay for heat on top of a radar image."""
    stops = [
        (0.0, (*to_rgb("#53ac67"), 0.0)),
        (0.25, (*to_rgb("#53ac67"), 0.55)),
        (0.6, (*to_rgb("#62cf7b"), 0.85)),
        (1.0, (*to_rgb("#ebc79a"), 1.0)),
    ]
    return LinearSegmentedColormap.from_list("psgg_heat", stops)


def sequential_cmap(theme="dark"):
    """One hue, surface to green: magnitude on an opaque heatmap."""
    th = get_theme(theme)
    end = "#b8e6c2" if th.name == "dark" else "#1f5a2e"
    return LinearSegmentedColormap.from_list(f"psgg_green_{th.name}", [th.surface, th.series[0], end])


def sides_cmap(theme="dark"):
    """Diverging T to CT through a neutral grey: which side a value favors."""
    th = get_theme(theme)
    return LinearSegmentedColormap.from_list(f"psgg_sides_{th.name}", [th.t, th.neutral, th.ct])
