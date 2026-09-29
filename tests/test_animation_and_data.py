"""save_animation() writes an MP4; load_env() finds .env from a subfolder."""

# pylint: disable=missing-function-docstring

import os

from matplotlib.animation import FuncAnimation

import pureskillgg_datascience_showcase as psgg


def test_save_animation_writes_mp4(tmp_path):
    fig, ax = psgg.figure("Moving", preset="square", scale=0.25)
    (line,) = ax.plot([], [])
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    def update(frame):
        line.set_data(range(frame + 1), range(frame + 1))
        return (line,)

    anim = FuncAnimation(fig, update, frames=3)
    path = psgg.save_animation(anim, tmp_path / "moving.mp4", fps=3)
    data = path.read_bytes()
    assert len(data) > 1000
    assert data[4:8] == b"ftyp"


def test_load_env_walks_up(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("PURESKILLGG_TOME_DS_TYPE=csds_test\n", encoding="utf-8")
    sub = tmp_path / "gallery" / "item"
    sub.mkdir(parents=True)
    monkeypatch.chdir(sub)
    monkeypatch.delenv("PURESKILLGG_TOME_DS_TYPE", raising=False)
    found = psgg.load_env()
    assert found == tmp_path / ".env"
    assert os.environ["PURESKILLGG_TOME_DS_TYPE"] == "csds_test"


def test_list_tomes_counts_pages(tmp_path):
    base = tmp_path / "tome" / "csds"
    (base / "deaths_mirage").mkdir(parents=True)
    for page in ("dataframe_00000", "dataframe_00001", "keyset_00000", "tome"):
        (base / "deaths_mirage" / page).write_bytes(b"")
    (base / "empty_one").mkdir()
    assert psgg.list_tomes(collection=tmp_path, ds_type="csds") == {"deaths_mirage": 2, "empty_one": 0}
    assert not psgg.list_tomes(collection=tmp_path / "nowhere", ds_type="csds")


def test_load_env_keeps_existing_values(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("PURESKILLGG_TOME_DS_TYPE=from_file\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PURESKILLGG_TOME_DS_TYPE", "from_env")
    psgg.load_env()
    assert os.environ["PURESKILLGG_TOME_DS_TYPE"] == "from_env"
