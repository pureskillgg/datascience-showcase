"""Shared test setup: a headless backend and a clean style per test."""

import matplotlib

matplotlib.use("Agg")

# pylint: disable=wrong-import-position
import matplotlib.pyplot as plt
import pytest

import pureskillgg_datascience_showcase as psgg


@pytest.fixture(autouse=True)
def reset_style():
    """Each test starts dark and square, and closes its figures."""
    psgg.use("dark", "square", scale=1)
    yield
    plt.close("all")
    psgg.use("dark", "square", scale=1)
