"""Palette: order, contrast against the surface, side colors."""

# pylint: disable=missing-function-docstring

import pytest
from matplotlib.colors import to_rgb

import pureskillgg_datascience_showcase as psgg


def luminance(color):
    def channel(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in to_rgb(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


@pytest.mark.parametrize("theme", [psgg.DARK, psgg.LIGHT])
def test_series_and_sides_reach_3_to_1(theme):
    for color in (*theme.series, theme.t, theme.ct):
        assert contrast(color, theme.surface) >= 3.0, color


@pytest.mark.parametrize("theme", [psgg.DARK, psgg.LIGHT])
def test_text_reaches_4_5_to_1(theme):
    assert contrast(theme.ink, theme.surface) >= 4.5
    assert contrast(theme.strong, theme.surface) >= 4.5


def test_series_order_is_fixed():
    assert psgg.series_colors(3) == ["#4fa863", "#5f8ece", "#b84d4f"]
    assert psgg.series_colors(theme="light")[0] == "#459f5b"


def test_too_many_series():
    with pytest.raises(ValueError, match="Other"):
        psgg.series_colors(7)


def test_negative_series_count():
    with pytest.raises(ValueError, match="negative"):
        psgg.series_colors(-1)


def test_helpers_follow_the_theme_in_force():
    psgg.use("light")
    assert psgg.side_color("T") == psgg.LIGHT.t
    assert psgg.series_colors(1) == [psgg.LIGHT.series[0]]


def test_side_colors():
    assert psgg.side_color("T") == "#e89230"
    assert psgg.side_color("ct") == "#84a9dc"
    assert psgg.side_color(2) == "#e89230"
    assert psgg.side_color(3, theme="light") == "#6090d1"
    with pytest.raises(ValueError):
        psgg.side_color("spectator")
