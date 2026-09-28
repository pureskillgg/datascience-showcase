"""Presets: sizes, scale and overrides."""

# pylint: disable=missing-function-docstring

import pytest

import pureskillgg_datascience_showcase as psgg


@pytest.mark.parametrize(
    "name,size",
    [
        ("square", (1080, 1080)),
        ("portrait", (1080, 1350)),
        ("vertical", (1080, 1920)),
        ("wide", (1920, 1080)),
        ("link", (1200, 630)),
        ("article", (2400, 1500)),
    ],
)
def test_rendered_pixels(name, size):
    assert psgg.get_preset(name).pixels == size


def test_scale_doubles_pixels_and_dpi():
    preset = psgg.get_preset("square", scale=2)
    assert preset.pixels == (2160, 2160)
    assert preset.dpi == 144


def test_height_override():
    assert psgg.get_preset("article", height=900).pixels == (2400, 1800)


def test_text_sizes_respect_the_floor():
    for preset in psgg.PRESETS.values():
        assert preset.body >= preset.min_text
        assert preset.title > preset.subtitle > preset.min_text or preset.subtitle >= preset.min_text


def test_social_presets_floor_is_30px():
    for name in ("square", "portrait", "vertical", "wide"):
        assert psgg.PRESETS[name].min_text >= 30


def test_unknown_preset():
    with pytest.raises(ValueError, match="Unknown preset"):
        psgg.get_preset("banner")


def test_bad_scale():
    with pytest.raises(ValueError):
        psgg.get_preset("square", scale=0)
