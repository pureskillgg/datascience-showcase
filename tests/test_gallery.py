"""The gallery index builder and the gallery item template."""

# pylint: disable=missing-function-docstring

import importlib.util
from pathlib import Path

import pandas as pd

import pureskillgg_datascience_showcase as psgg

ROOT = Path(__file__).resolve().parent.parent


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_gallery = load("scripts/build_gallery.py", "build_gallery")
template = load("templates/gallery-item/make.py", "template_make")


def write_item(gallery, slug, meta, image=True):
    folder = gallery / slug
    folder.mkdir(parents=True)
    lines = ["---", *(f"{k}: {v}" for k, v in meta.items()), "---", "", "Text."]
    (folder / "README.md").write_text("\n".join(lines), encoding="utf-8")
    if image:
        fig, _ = psgg.figure("Item", official=meta.get("official") == "true")
        psgg.save(folder / meta.get("image", "graphic.png"), fig)


META = {
    "title": "Deaths on Mirage",
    "author": "someone",
    "official": "false",
    "data": "60 matches",
    "image": "graphic.png",
}


def test_empty_gallery_renders_placeholder(tmp_path):
    assert "Nothing here yet" in build_gallery.render(build_gallery.items(tmp_path))


def test_items_are_listed_with_their_kind(tmp_path):
    write_item(tmp_path, "b-item", {**META, "official": "true", "video": "https://example.com/v"})
    write_item(tmp_path, "a-item", META)
    entries = build_gallery.items(tmp_path)
    assert [slug for slug, _, _ in entries] == ["a-item", "b-item"]
    assert all(not problems for _, _, problems in entries)
    text = build_gallery.render(entries)
    assert "Community · by someone" in text
    assert "Official · by someone" in text
    assert "[video](https://example.com/v)" in text


def test_missing_fields_and_image_are_reported(tmp_path):
    write_item(tmp_path, "bad", {"title": "Bad", "official": "maybe", "image": "gone.png"}, image=False)
    problems = build_gallery.items(tmp_path)[0][2]
    assert any("author" in p for p in problems)
    assert any("true or false" in p for p in problems)
    assert any("gone.png" in p for p in problems)


def test_image_must_be_a_png_inside_the_item(tmp_path):
    write_item(tmp_path, "outside", {**META, "image": "../elsewhere.png"}, image=False)
    (tmp_path / "elsewhere.png").write_bytes(b"")
    write_item(tmp_path, "readme", {**META, "image": "README.md"}, image=False)
    problems = {slug: ps for slug, _, ps in build_gallery.items(tmp_path)}
    assert any("inside the item's folder" in p for p in problems["outside"])
    assert any("must be a PNG" in p for p in problems["readme"])


def test_official_must_match_the_image_stamp(tmp_path):
    write_item(tmp_path, "claims-official", {**META, "official": "true"}, image=False)
    fig, _ = psgg.figure("Not official")
    psgg.save(tmp_path / "claims-official" / "graphic.png", fig)
    folder = tmp_path / "hides-logo"
    folder.mkdir()
    (folder / "README.md").write_text(
        "\n".join(["---", *(f"{k}: {v}" for k, v in META.items()), "---"]), encoding="utf-8"
    )
    fig, _ = psgg.figure("Official", official=True)
    psgg.save(folder / "graphic.png", fig)
    problems = {slug: ps for slug, _, ps in build_gallery.items(tmp_path)}
    assert any("doesn't match" in p for p in problems["claims-official"])
    assert any("doesn't match" in p for p in problems["hides-logo"])


def test_template_readme_has_every_field():
    meta = build_gallery.front_matter(ROOT / "templates" / "gallery-item" / "README.md")
    assert all(meta.get(k) for k in build_gallery.REQUIRED)


def test_template_draws_from_a_deaths_table(tmp_path):
    deaths = pd.DataFrame(
        {
            "weapon_name": ["ak47", "ak47", "m4a1_silencer", "awp", "glock", "knife"],
            "attacker_team_code": [2, 2, 3, 3, 2, None],
        }
    )
    fig = template.draw(deaths, "Six deaths.")
    path = psgg.save(tmp_path / "graphic.png", fig)
    assert psgg.read_stamp(path)["psgg:attribution"] == psgg.ATTRIBUTION
    labels = [t.get_text() for t in fig.axes[0].get_yticklabels()]
    assert "AK-47" in labels and "M4A1-S" in labels
