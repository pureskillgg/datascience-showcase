"""
Finding your data.

dsdk's tome curator reads four PURESKILLGG_TOME_* variables. Put them in a
.env file at the repo root (copy .env.example); load_env() finds it from any
folder inside the repo, so a notebook in gallery/<item>/ works too.
"""

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

ENV_VARS = (
    "PURESKILLGG_TOME_DS_COLLECTION_PATH",
    "PURESKILLGG_TOME_COLLECTION_PATH",
    "PURESKILLGG_TOME_DS_TYPE",
    "PURESKILLGG_TOME_DEFAULT_HEADER_NAME",
)


def load_env(*, verbose=False):
    """
    Load the nearest .env above the working directory. Returns its path, or None.

    Variables already set in the environment win over the file.
    """
    found = find_dotenv(usecwd=True)
    if found:
        load_dotenv(found, override=False)
    if verbose:
        print(f".env: {found or 'not found'}")
        for name in ENV_VARS:
            value = os.environ.get(name)
            print(f"  {name} = {value}" if value else f"  {name} is not set")
    return Path(found) if found else None


def list_tomes(*, collection=None, ds_type=None):
    """
    The tomes in your tome collection, as {name: page count}.

    A tome with 0 pages is empty or unfinished, and get_dataframe() fails on it
    ("The tome has no pages"). collection and ds_type default to .env.
    """
    load_env()
    root = Path(collection or os.environ["PURESKILLGG_TOME_COLLECTION_PATH"])
    folder = root / "tome" / (ds_type or os.environ.get("PURESKILLGG_TOME_DS_TYPE", "csds"))
    if not folder.is_dir():
        return {}
    return {p.name: len(list(p.glob("dataframe_*"))) for p in sorted(folder.iterdir()) if p.is_dir()}


def curator(**kwargs):
    """A dsdk TomeCuratorFs for your local data, after loading .env."""
    load_env()
    from pureskillgg_dsdk.tome import TomeCuratorFs  # pylint: disable=import-outside-toplevel

    return TomeCuratorFs(**kwargs)
