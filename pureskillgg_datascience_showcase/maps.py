"""
Map graphics: stock CS2 radars and world-to-radar coordinates.

CSDS positions are in world units. Valve's overview numbers for each map
(the radar's top-left corner in world units, and world units per radar pixel)
turn them into pixels on the 1024x1024 radar:

    px = (x - pos_x) / scale
    py = (pos_y - y) / scale

Maps with two floors (Nuke, Vertigo, Train, Baggage) have a lower radar;
level_of() says which floor a height (z) is on.

The radar images are Valve's, from the game files.
"""

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

from .palette import get_theme, heat_cmap
from .style import current

RADAR_DIR = Path(__file__).resolve().parent / "radars"


@lru_cache(maxsize=1)
def _overviews():
    return json.loads((RADAR_DIR / "overviews.json").read_text(encoding="utf-8"))


def available_maps():
    """The maps that have a radar, e.g. ['ar_baggage', ..., 'de_vertigo']."""
    return sorted(_overviews())


def overview(map_name):
    """Valve's overview numbers for a map: pos_x, pos_y, scale, levels and labels."""
    try:
        return _overviews()[map_name]
    except KeyError as err:
        raise ValueError(f"No radar for {map_name!r}; available: {', '.join(available_maps())}") from err


def to_radar(map_name, x, y):
    """World x, y (scalars or arrays) to radar pixels (px, py); y grows downwards."""
    ov = overview(map_name)
    px = (np.asarray(x, dtype=float) - ov["pos_x"]) / ov["scale"]
    py = (ov["pos_y"] - np.asarray(y, dtype=float)) / ov["scale"]
    return px, py


def level_of(map_name, z):
    """The floor each height is on: 'default', or 'lower' on two-floor maps. Returns an array."""
    levels = overview(map_name)["levels"]
    z = np.asarray(z, dtype=float)
    out = np.full(z.shape, "default", dtype=object)
    if "lower" in levels:
        lower = levels["lower"]
        out[(z >= lower["min"]) & (z < lower["max"])] = "lower"
    return out


def radar_image(map_name, level="default"):
    """The radar as an RGBA array (1024x1024x4)."""
    levels = overview(map_name)["levels"]
    if level not in levels:
        raise ValueError(f"{map_name} has no {level!r} level; it has {sorted(levels)}")
    with Image.open(RADAR_DIR / levels[level]["image"]) as img:
        return np.asarray(img.convert("RGBA"))


def _erode(mask, k):
    """Keep only pixels whose whole (2k+1)-wide cross neighborhood is set."""
    out = mask.copy()
    padded = np.pad(mask, k, constant_values=False)
    h, w = mask.shape
    for d in range(-k, k + 1):
        out &= padded[k + d : k + d + h, k : k + w]
        out &= padded[k : k + h, k + d : k + d + w]
    return out


def radar_bounds(map_name, level="default", pad=16):
    """(x0, y0, x1, y1) in radar pixels around the drawn part of the radar."""
    # Erode first so hairline borders (Nuke has two) don't count as map.
    drawn = _erode(radar_image(map_name, level)[..., 3] > 32, 2)
    rows = np.flatnonzero(drawn.any(axis=1))
    cols = np.flatnonzero(drawn.any(axis=0))
    h, w = drawn.shape
    return (
        max(0, cols[0] - pad),
        max(0, rows[0] - pad),
        min(w, cols[-1] + 1 + pad),
        min(h, rows[-1] + 1 + pad),
    )


def draw_radar(ax, map_name, *, level="default", dim=0.55, crop=True):
    """
    Draw a map's radar on ax, in radar pixel coordinates, dimmed so data reads on top.

    Plot positions with to_radar(). dim is how much of the radar's brightness
    is kept (1 = untouched). crop zooms to the drawn part of the radar.
    Returns ax.
    """
    img = radar_image(map_name, level).astype(float) / 255
    img[..., :3] *= dim
    h, w = img.shape[:2]
    ax.imshow(img, extent=(0, w, h, 0), interpolation="lanczos", zorder=0)
    x0, y0, x1, y1 = radar_bounds(map_name, level) if crop else (0, 0, w, h)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return ax


def _blur(grid, sigma):
    """Gaussian blur, separable, with numpy only."""
    if sigma <= 0:
        return grid
    radius = int(3 * sigma + 0.5)
    kernel = np.exp(-0.5 * (np.arange(-radius, radius + 1) / sigma) ** 2)
    kernel /= kernel.sum()
    grid = np.apply_along_axis(np.convolve, 0, grid, kernel, mode="same")
    return np.apply_along_axis(np.convolve, 1, grid, kernel, mode="same")


def heatmap(ax, map_name, x, y, *, bins=128, smooth=1.6, cmap=None, alpha=1.0):
    """
    Heat of world positions over the radar already drawn on ax (see draw_radar).

    bins is the grid size across the 1024-pixel radar; smooth is the blur in
    grid cells. Returns the image artist.
    """
    px, py = to_radar(map_name, x, y)
    keep = np.isfinite(px) & np.isfinite(py)
    grid, _, _ = np.histogram2d(px[keep], py[keep], bins=bins, range=[[0, 1024], [0, 1024]])
    grid = _blur(grid.T, smooth)
    if grid.max() > 0:
        grid = grid / grid.max()
    return ax.imshow(
        grid,
        extent=(0, 1024, 1024, 0),
        cmap=cmap or heat_cmap(),
        interpolation="bilinear",
        alpha=alpha,
        zorder=2,
    )


def label_sites(ax, map_name, *, theme=None, fontsize=None):
    """Write A, B and the spawns where Valve's overview puts them. Returns the text artists."""
    th = get_theme(theme or current()["theme"])
    size = fontsize or ax.figure.get_figwidth() * 72 / 36
    out = []
    for label, (fx, fy) in overview(map_name)["labels"].items():
        out.append(
            ax.text(
                fx * 1024,
                fy * 1024,
                label,
                ha="center",
                va="center",
                color=th.strong,
                fontsize=size,
                zorder=3,
            )
        )
    return out
