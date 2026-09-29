"""
Kills by weapon, split by the killer's side. A starting point for a gallery item.

Copy this folder to gallery/<your-slug>/, change what you need, then run:

    uv run python gallery/<your-slug>/make.py

It reads the deaths_mirage tome built in docs/getting-data.md and writes
graphic.png next to this file.
"""

from pathlib import Path

import pureskillgg_datascience_showcase as psgg

HERE = Path(__file__).resolve().parent
TOME = "deaths_mirage"
WEAPON_NAMES = {
    "ak47": "AK-47",
    "m4a1": "M4A4",
    "m4a1_silencer": "M4A1-S",
    "m4a1_silencer_off": "M4A1-S",
    "awp": "AWP",
    "deagle": "Desert Eagle",
    "usp_silencer": "USP-S",
    "glock": "Glock-18",
    "galilar": "Galil AR",
    "famas": "FAMAS",
}


def draw(deaths, subtitle, *, preset="square", official=False):
    """The graphic, from a table of deaths with weapon_name and attacker_team_code."""
    d = deaths[deaths["attacker_team_code"].isin([2, 3])]
    d = d.assign(
        weapon=d["weapon_name"].map(lambda w: WEAPON_NAMES.get(w, w)),
        side=d["attacker_team_code"].map({2: "T", 3: "CT"}),
    )
    counts = (
        d.groupby(["weapon", "side"]).size().unstack(fill_value=0).reindex(columns=["T", "CT"], fill_value=0)
    )
    top = counts.assign(total=counts.sum(axis=1)).sort_values("total").tail(8)

    fig, ax = psgg.figure("Kills by weapon", subtitle, preset=preset, official=official)
    ax.barh(top.index, top["T"], color=psgg.side_color("T"), label="T")
    ax.barh(top.index, top["CT"], left=top["T"], color=psgg.side_color("CT"), label="CT")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    psgg.legend(ax)
    return fig


def main():
    """Load the tome, draw, save."""
    deaths = psgg.curator().get_dataframe(TOME)
    subtitle = "Mirage, by the killer's side."
    psgg.save(HERE / "graphic.png", draw(deaths, subtitle))


if __name__ == "__main__":
    main()
