"""
Canvas sizes for the places graphics end up.

Sizes are in pixels at scale 1. Text sizes are in pixels too: the kit renders
at 72 dpi times the scale, so one point is one pixel at scale 1, and a scale of
2 doubles everything and looks the same.
"""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Preset:
    """One canvas shape with its type sizes."""

    name: str
    width: int
    height: int
    body: float
    title: float
    subtitle: float
    min_text: float
    scale: float = 1.0
    use: str = ""

    @property
    def figsize(self):
        """Figure size in inches at 72 dpi."""
        return (self.width / 72, self.height / 72)

    @property
    def dpi(self):
        """Render dpi: 72 times the scale."""
        return 72 * self.scale

    @property
    def pixels(self):
        """The rendered size in pixels."""
        return (round(self.width * self.scale), round(self.height * self.scale))


PRESETS = {
    "square": Preset("square", 1080, 1080, 30, 52, 32, 30, use="Instagram feed, LinkedIn, Discord"),
    "portrait": Preset("portrait", 1080, 1350, 30, 52, 32, 30, use="Instagram feed, Reddit on phones"),
    "vertical": Preset(
        "vertical",
        1080,
        1920,
        32,
        58,
        34,
        30,
        use="Instagram stories and reels, TikTok photos and videos, YouTube Shorts",
    ),
    "wide": Preset("wide", 1920, 1080, 32, 58, 34, 30, use="YouTube, slides, X, Reddit, Discord"),
    "link": Preset("link", 1200, 630, 28, 46, 30, 26, use="Link previews on X, LinkedIn, Discord, Facebook"),
    "article": Preset("article", 1200, 750, 18, 32, 20, 16, scale=2.0, use="Docs and blog posts"),
}


def get_preset(preset="square", *, height=None, scale=None):
    """
    Return a Preset by name, optionally with a different height or scale.

    height changes the canvas height in pixels at scale 1 (useful for article).
    scale multiplies the rendered resolution: 2 turns 1080x1080 into 2160x2160.
    """
    if isinstance(preset, Preset):
        base = preset
    else:
        try:
            base = PRESETS[preset]
        except KeyError as err:
            raise ValueError(f"Unknown preset {preset!r}; use one of {sorted(PRESETS)}") from err
    changes = {}
    if height is not None:
        changes["height"] = int(height)
    if scale is not None:
        if scale <= 0:
            raise ValueError("scale must be positive")
        changes["scale"] = float(scale)
    return replace(base, **changes) if changes else base
