"""
Branded canvases and saving.

figure() lays out a canvas: the title and subtitle at the top left, the
attribution line at the bottom right, and the logo at the bottom left on
official graphics. save() makes sure the attribution is there and stamps PNGs
so the repo's checks can tell a kit-made image from any other.
"""

import textwrap
import weakref
from importlib import metadata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.layout_engine import ConstrainedLayoutEngine
from PIL import Image

from . import style
from .palette import ATTRIBUTION, get_theme
from .presets import get_preset

ASSET_DIR = Path(__file__).resolve().parent / "assets"
STAMP_KEY = "psgg:attribution"

_meta = weakref.WeakKeyDictionary()


def _version():
    try:
        return metadata.version("pureskillgg-datascience-showcase")
    except metadata.PackageNotFoundError:
        return "dev"


def _layout(fig):
    """Pixel geometry (at scale 1) for a figure: width, height, margin, preset, theme."""
    info = _meta.get(fig)
    state = style.current()
    preset = info["preset"] if info else get_preset(state["preset"], scale=state["scale"])
    theme = info["theme"] if info else get_theme(state["theme"])
    width, height = (fig.get_size_inches() * 72).tolist()
    margin = 0.055 * min(width, height)
    return width, height, margin, preset, theme


def _fit_title(fig, artist, max_width, min_size):
    """Shrink a title until it fits max_width pixels, then wrap it if it still doesn't."""
    renderer = fig.canvas.get_renderer()
    scale = fig.dpi / 72
    size = artist.get_fontsize()
    while artist.get_window_extent(renderer).width / scale > max_width and size > min_size:
        size -= 1
        artist.set_fontsize(size)
    if artist.get_window_extent(renderer).width / scale > max_width:
        words = artist.get_text()
        width = max(8, int(len(words) * max_width / (artist.get_window_extent(renderer).width / scale)))
        artist.set_text("\n".join(textwrap.wrap(words, width)))


def _wrap_to(fig, artist, max_width):
    """Wrap a line of text by words so it fits max_width pixels."""
    renderer = fig.canvas.get_renderer()
    scale = fig.dpi / 72
    text = artist.get_text()
    measured = artist.get_window_extent(renderer).width / scale
    if measured <= max_width:
        return
    width = max(10, int(len(text) * max_width / measured))
    while width > 10:
        artist.set_text("\n".join(textwrap.wrap(text, width)))
        if artist.get_window_extent(renderer).width / scale <= max_width:
            return
        width -= 2


def _add_logo(fig):
    width, height, margin, preset, theme = _layout(fig)
    logo = np.asarray(Image.open(ASSET_DIR / f"logo-{theme.name}.png"))
    logo_h = preset.body * 1.5
    logo_w = logo_h * logo.shape[1] / logo.shape[0]
    bottom = margin * 0.65
    ax = fig.add_axes([margin / width, bottom / height, logo_w / width, logo_h / height], label="psgg-logo")
    ax.imshow(logo, interpolation="lanczos")
    ax.set_axis_off()
    ax.set_in_layout(False)
    return ax


def _has(fig, label):
    return any(getattr(a, "get_label", lambda: "")() == label for a in fig.get_children()) or any(
        ax.get_label() == label for ax in fig.axes
    )


def add_footer(fig=None, *, official=False):
    """
    Add the attribution line (and the logo, if official) to a figure.

    save() calls this for you. Only mark a graphic official if PureSkill.gg made it.
    """
    fig = fig or plt.gcf()
    width, height, margin, preset, theme = _layout(fig)
    if not _has(fig, "psgg-footer"):
        fig.text(
            1 - margin / width,
            margin * 0.65 / height,
            ATTRIBUTION,
            fontsize=preset.body,
            color=theme.ink,
            ha="right",
            va="bottom",
            label="psgg-footer",
        )
        engine = fig.get_layout_engine()
        if isinstance(engine, ConstrainedLayoutEngine) and fig not in _meta:
            bottom = (margin * 0.65 + preset.body * 2.2) / height
            side = margin / width
            engine.set(rect=(side, bottom, 1 - 2 * side, 1 - bottom - margin / height))
    if official and not _has(fig, "psgg-logo"):
        _add_logo(fig)
    info = _meta.setdefault(fig, {"preset": preset, "theme": theme, "official": False, "plain": True})
    info["official"] = info["official"] or official
    return fig


def figure(
    title=None,
    subtitle=None,
    *,
    preset=None,
    theme=None,
    official=False,
    scale=None,
    height=None,
    nrows=1,
    ncols=1,
    **subplots_kw,
):
    """
    Make a branded canvas and return (fig, ax), or (fig, axes) for a grid.

    title is set in capitals in the title font; subtitle is one line under it,
    wrapped if long. preset, theme and scale switch the style for what follows,
    like use(). height overrides the preset's height for this figure only.
    official adds the logo: use it only for graphics PureSkill.gg made.
    """
    if theme is not None or preset is not None or scale is not None:
        style.use(theme, preset, scale=scale)
    state = style.current()
    pr = get_preset(state["preset"], height=height, scale=state["scale"])
    th = get_theme(state["theme"])

    fig = plt.figure(figsize=pr.figsize, dpi=72)
    _meta[fig] = {"preset": pr, "theme": th, "official": official, "plain": False}
    width, height_px = pr.width, pr.height
    margin = 0.055 * min(width, height_px)
    top = height_px - margin

    if title:
        artist = fig.text(
            margin / width,
            top / height_px,
            str(title).upper(),
            fontproperties=style.title_font(),
            fontsize=pr.title,
            color=th.strong,
            ha="left",
            va="top",
            label="psgg-title",
        )
        _fit_title(fig, artist, width - 2 * margin, pr.subtitle * 1.1)
        top -= artist.get_window_extent(fig.canvas.get_renderer()).height + pr.body * 0.35
    if subtitle:
        artist = fig.text(
            margin / width,
            top / height_px,
            str(subtitle),
            fontsize=pr.subtitle,
            color=th.ink,
            ha="left",
            va="top",
            label="psgg-subtitle",
        )
        _wrap_to(fig, artist, width - 2 * margin)
        top -= artist.get_window_extent(fig.canvas.get_renderer()).height
    header = top
    if title or subtitle:
        top -= pr.body * 0.8

    add_footer(fig, official=official)
    bottom = margin * 0.65 + pr.body * 1.5 + pr.body * 0.8
    _meta[fig]["layout"] = {
        "width": width,
        "height": height_px,
        "margin": margin,
        "header": header,
        "top": top,
        "bottom": bottom,
    }
    fig.set_layout_engine(ConstrainedLayoutEngine(h_pad=0.1, w_pad=0.1))
    _set_plot_area(fig)
    axes = fig.subplots(nrows, ncols, **subplots_kw)
    return fig, axes


def _set_plot_area(fig):
    lay = _meta[fig]["layout"]
    w, h, m = lay["width"], lay["height"], lay["margin"]
    fig.get_layout_engine().set(
        rect=(m / w, lay["bottom"] / h, 1 - 2 * m / w, (lay["top"] - lay["bottom"]) / h)
    )


def legend(ax=None, *, ncols=None, **kwargs):
    """
    A legend under the subtitle, left-aligned with the title, for a figure() canvas.

    The plot area shrinks to make room. On a plain matplotlib figure this is
    just ax.legend(). Charts with two or more series always get a legend.
    """
    ax = ax or plt.gca()
    fig = ax.figure
    handles, labels = ax.get_legend_handles_labels()
    info = _meta.get(fig)
    if not info or "layout" not in info:
        return ax.legend(ncols=ncols or 1, **kwargs)
    lay, pr = info["layout"], info["preset"]
    ncols = ncols or min(len(labels), 3) or 1
    rows = -(-len(labels) // ncols)
    anchor_y = lay["header"] - pr.body * 0.2
    leg = fig.legend(
        handles,
        labels,
        loc="upper left",
        bbox_to_anchor=(lay["margin"] / lay["width"], anchor_y / lay["height"]),
        ncols=ncols,
        borderaxespad=0,
        borderpad=0,
        **kwargs,
    )
    leg.set_in_layout(False)
    lay["top"] = min(lay["top"], anchor_y - rows * pr.body * 1.45 - pr.body * 0.8)
    _set_plot_area(fig)
    return leg


def save(path, fig=None, *, official=None):
    """
    Save a figure with the attribution line, at the preset's resolution.

    PNGs carry a stamp (text chunks naming the kit, preset, theme and whether
    the graphic is official) that the gallery check looks for. Returns the path.
    """
    fig = fig or plt.gcf()
    add_footer(fig, official=bool(official))
    info = _meta[fig]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    kwargs = {"dpi": info["preset"].dpi, "facecolor": info["theme"].surface}
    if path.suffix.lower() == ".png":
        kwargs["metadata"] = {
            "Software": f"pureskillgg_datascience_showcase {_version()}",
            STAMP_KEY: ATTRIBUTION,
            "psgg:preset": info["preset"].name,
            "psgg:theme": info["theme"].name,
            "psgg:official": "true" if info["official"] else "false",
            "psgg:scale": f"{info['preset'].scale:g}",
        }
    fig.savefig(path, **kwargs)
    return path


def read_stamp(path):
    """The kit's stamp from a PNG, as a dict; empty if there is none."""
    with Image.open(path) as img:
        text = dict(getattr(img, "text", {}) or {})
    return {k: v for k, v in text.items() if k.startswith("psgg:")}
