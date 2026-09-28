"""The repo check catches data, secrets, videos, notebook outputs and unstamped gallery images."""

# pylint: disable=missing-function-docstring

import importlib.util
import json
from pathlib import Path

from PIL import Image

import pureskillgg_datascience_showcase as psgg

_spec = importlib.util.spec_from_file_location(
    "check_repo", Path(__file__).resolve().parent.parent / "scripts" / "check_repo.py"
)
check_repo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_repo)


def problems(root, rel):
    return check_repo.check([Path(rel)], root)


def write(root, rel, data=b""):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def test_clean_files_pass(tmp_path):
    write(tmp_path, "README.md", b"# hi")
    write(tmp_path, ".env.example", b"X=1")
    assert not problems(tmp_path, "README.md")
    assert not problems(tmp_path, ".env.example")


def test_secrets_data_and_video_are_refused(tmp_path):
    write(tmp_path, ".env", b"SECRET=1")
    write(tmp_path, "x/player_death.parquet", b"PAR1....")
    write(tmp_path, "clip.mp4", b"....")
    write(tmp_path, "loop.gif", b"GIF89a")
    assert "secrets" in problems(tmp_path, ".env")[0]
    assert "data file" in problems(tmp_path, "x/player_death.parquet")[0]
    assert "video" in problems(tmp_path, "clip.mp4")[0]
    assert "video" in problems(tmp_path, "loop.gif")[0]


def test_parquet_without_extension_is_refused(tmp_path):
    write(tmp_path, "match/player_death", b"PAR1\x00\x00")
    assert "parquet" in problems(tmp_path, "match/player_death")[0]


def test_notebook_outputs_are_refused(tmp_path):
    nb = {"cells": [{"cell_type": "code", "execution_count": 3, "outputs": [{"text": "hi"}], "source": []}]}
    clean = {"cells": [{"cell_type": "code", "execution_count": None, "outputs": [], "source": []}]}
    write(tmp_path, "a.ipynb", json.dumps(nb).encode())
    write(tmp_path, "b.ipynb", json.dumps(clean).encode())
    assert "outputs" in problems(tmp_path, "a.ipynb")[0]
    assert not problems(tmp_path, "b.ipynb")


def test_gallery_images_need_the_stamp(tmp_path):
    plain = tmp_path / "gallery" / "item" / "plain.png"
    plain.parent.mkdir(parents=True)
    Image.new("RGB", (10, 10)).save(plain)
    write(tmp_path, "gallery/item/photo.jpg", b"\xff\xd8\xff")
    fig, _ = psgg.figure("Stamped")
    psgg.save(tmp_path / "gallery" / "item" / "stamped.png", fig)
    assert "stamp" in problems(tmp_path, "gallery/item/plain.png")[0]
    assert "PNG" in problems(tmp_path, "gallery/item/photo.jpg")[0]
    assert not problems(tmp_path, "gallery/item/stamped.png")


def test_images_outside_the_gallery_need_no_stamp(tmp_path):
    path = tmp_path / "docs" / "shot.png"
    path.parent.mkdir(parents=True)
    Image.new("RGB", (10, 10)).save(path)
    assert not problems(tmp_path, "docs/shot.png")


def test_big_files_are_refused(tmp_path):
    write(tmp_path, "big.txt", b"x" * (check_repo.MAX_BYTES + 1))
    assert "limit" in problems(tmp_path, "big.txt")[0]
