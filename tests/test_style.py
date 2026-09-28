"""The style applied on import, and switching it."""

# pylint: disable=missing-function-docstring

import matplotlib as mpl
from matplotlib import font_manager

import pureskillgg_datascience_showcase as psgg


def test_import_applies_dark_square():
    assert mpl.rcParams["figure.facecolor"] == psgg.DARK.surface
    assert mpl.rcParams["axes.prop_cycle"].by_key()["color"] == list(psgg.DARK.series)
    assert tuple(mpl.rcParams["figure.figsize"]) == (15.0, 15.0)
    assert mpl.rcParams["font.size"] == 30


def test_fonts_are_registered():
    names = {f.name for f in font_manager.fontManager.ttflist}
    assert "Assistant" in names
    assert "Russo One" in names
    assert font_manager.findfont("Assistant", fallback_to_default=False).endswith(".ttf")


def test_title_font_is_russo_one():
    assert psgg.title_font().get_name() == "Russo One"


def test_switch_to_light_and_wide():
    psgg.use("light", "wide")
    assert mpl.rcParams["axes.facecolor"] == psgg.LIGHT.surface
    assert mpl.rcParams["axes.prop_cycle"].by_key()["color"] == list(psgg.LIGHT.series)
    assert tuple(mpl.rcParams["figure.figsize"]) == (1920 / 72, 1080 / 72)
    assert psgg.current()["theme"] == "light"


def test_colormaps_registered():
    for name in ("psgg_heat", "psgg_green_dark", "psgg_green_light", "psgg_sides_dark", "psgg_sides_light"):
        assert name in mpl.colormaps
