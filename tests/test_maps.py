"""Radars, overview numbers and the world-to-radar transform."""

# pylint: disable=missing-function-docstring

import numpy as np
import pytest

import pureskillgg_datascience_showcase as psgg
from pureskillgg_datascience_showcase import maps


def test_map_pool_is_present():
    for name in ("de_ancient", "de_anubis", "de_dust2", "de_inferno", "de_mirage", "de_nuke", "de_overpass"):
        assert name in maps.available_maps()


def test_top_left_corner_maps_to_origin():
    ov = maps.overview("de_mirage")
    px, py = maps.to_radar("de_mirage", ov["pos_x"], ov["pos_y"])
    assert px == pytest.approx(0)
    assert py == pytest.approx(0)


def test_transform_scale_and_direction():
    ov = maps.overview("de_mirage")
    px, py = maps.to_radar("de_mirage", [ov["pos_x"] + 50], [ov["pos_y"] - 100])
    assert px[0] == pytest.approx(50 / ov["scale"])
    assert py[0] == pytest.approx(100 / ov["scale"])


def test_nuke_has_two_floors():
    levels = maps.level_of("de_nuke", [0, -400, -600, -1000])
    assert list(levels) == ["default", "default", "lower", "lower"]
    assert maps.radar_image("de_nuke", "lower").shape == (1024, 1024, 4)


def test_single_floor_maps_are_all_default():
    assert set(maps.level_of("de_mirage", [-500, 0, 500])) == {"default"}


def test_unknown_map_and_level():
    with pytest.raises(ValueError, match="No radar"):
        maps.overview("de_shortdust")
    with pytest.raises(ValueError, match="no 'lower'"):
        maps.radar_image("de_mirage", "lower")


def test_radar_bounds_crop_the_empty_border():
    x0, y0, x1, y1 = maps.radar_bounds("de_mirage")
    assert 0 < x0 < x1 < 1024
    assert 0 < y0 < y1 < 1024


def test_draw_radar_heatmap_and_labels(tmp_path):
    fig, ax = psgg.figure("Where players die", preset="square")
    maps.draw_radar(ax, "de_mirage")
    rng = np.random.default_rng(1)
    ov = maps.overview("de_mirage")
    x = ov["pos_x"] + rng.uniform(1000, 4000, 500)
    y = ov["pos_y"] - rng.uniform(1000, 4000, 500)
    art = maps.heatmap(ax, "de_mirage", x, y)
    assert art.get_array().max() == pytest.approx(1.0)
    assert len(maps.label_sites(ax, "de_mirage")) == 4
    path = psgg.save(tmp_path / "map.png", fig)
    assert psgg.read_stamp(path)["psgg:preset"] == "square"
