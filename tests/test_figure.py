"""figure() and save(): size, footer, logo and stamp."""

# pylint: disable=missing-function-docstring

import matplotlib.pyplot as plt
from PIL import Image

import pureskillgg_datascience_showcase as psgg


def labels(fig):
    return {t.get_label() for t in fig.texts} | {ax.get_label() for ax in fig.axes}


def test_figure_saves_at_preset_size_with_stamp(tmp_path):
    fig, ax = psgg.figure("Kills by weapon", "60 matches", preset="portrait")
    ax.bar(["AK-47", "M4A1-S"], [10, 5])
    path = psgg.save(tmp_path / "chart.png", fig)
    with Image.open(path) as img:
        assert img.size == (1080, 1350)
    stamp = psgg.read_stamp(path)
    assert stamp["psgg:attribution"] == psgg.ATTRIBUTION
    assert stamp["psgg:preset"] == "portrait"
    assert stamp["psgg:theme"] == "dark"
    assert stamp["psgg:official"] == "false"


def test_title_is_upper_case_and_footer_present():
    fig, _ = psgg.figure("kills by weapon")
    title = next(t for t in fig.texts if t.get_label() == "psgg-title")
    assert title.get_text() == "KILLS BY WEAPON"
    assert "psgg-footer" in labels(fig)
    assert "psgg-logo" not in labels(fig)


def test_official_adds_logo(tmp_path):
    fig, _ = psgg.figure("Official", official=True)
    assert "psgg-logo" in labels(fig)
    path = psgg.save(tmp_path / "official.png", fig)
    assert psgg.read_stamp(path)["psgg:official"] == "true"


def test_plain_matplotlib_figure_gets_footer_and_stamp(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [3, 1, 2])
    path = psgg.save(tmp_path / "plain.png")
    assert "psgg-footer" in labels(fig)
    with Image.open(path) as img:
        assert img.size == (1080, 1080)
    assert psgg.read_stamp(path)["psgg:attribution"] == psgg.ATTRIBUTION


def test_scale_two_renders_double(tmp_path):
    fig, _ = psgg.figure("Big", preset="square", scale=2)
    path = psgg.save(tmp_path / "big.png", fig)
    with Image.open(path) as img:
        assert img.size == (2160, 2160)
    assert psgg.read_stamp(path)["psgg:scale"] == "2"


def test_light_theme_uses_light_logo_and_surface(tmp_path):
    fig, _ = psgg.figure("Light", theme="light", official=True)
    path = psgg.save(tmp_path / "light.png", fig)
    with Image.open(path) as img:
        assert img.convert("RGB").getpixel((2, 2)) == (0xF5, 0xF6, 0xF8)
    assert psgg.read_stamp(path)["psgg:theme"] == "light"


def test_long_title_is_fitted_inside_the_canvas():
    fig, _ = psgg.figure("A title that is far too long to fit on one square canvas at full size")
    fig.canvas.draw()
    title = next(t for t in fig.texts if t.get_label() == "psgg-title")
    box = title.get_window_extent()
    assert box.x1 <= fig.bbox.width


def test_grid_of_axes():
    _, axes = psgg.figure("Grid", nrows=2, ncols=2)
    assert axes.shape == (2, 2)


def test_legend_sits_under_the_subtitle_and_shrinks_the_plot():
    fig, ax = psgg.figure("Lines", "Six series")
    for i in range(6):
        ax.plot([0, 1], [i, i + 1], label=f"s{i}")
    fig.canvas.draw()
    before = ax.get_position().y1
    leg = psgg.legend(ax)
    fig.canvas.draw()
    subtitle = next(t for t in fig.texts if t.get_label() == "psgg-subtitle")
    assert leg.get_window_extent().y1 <= subtitle.get_window_extent().y0
    assert ax.get_position().y1 < before
    assert leg.get_window_extent().y0 > ax.get_window_extent().y1


def test_legend_on_a_plain_figure_is_ax_legend():
    _, ax = plt.subplots()
    ax.plot([0, 1], label="a")
    assert psgg.legend(ax) is ax.get_legend()


def test_svg_save_has_no_stamp_but_works(tmp_path):
    fig, _ = psgg.figure("Vector")
    path = psgg.save(tmp_path / "vector.svg", fig)
    assert path.read_text(encoding="utf-8").lstrip().startswith("<?xml")
