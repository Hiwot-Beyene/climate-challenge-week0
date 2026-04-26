"""
Tests for src/data_loader.py

These tests use a synthetic CSV so they work without the real data/ files.
"""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data_loader import load_country, NASA_SENTINEL


@pytest.fixture
def synthetic_csv(tmp_path):
    """Write a minimal NASA POWER-shaped CSV to a temp directory."""
    df = pd.DataFrame({
        "YEAR": [2020, 2020, 2020],
        "DOY":  [1, 2, 3],
        "T2M":  [20.1, NASA_SENTINEL, 21.3],
        "T2M_MAX": [28.0, 29.0, 30.0],
        "T2M_MIN": [14.0, 15.0, 14.5],
        "T2M_RANGE": [14.0, 14.0, 15.5],
        "PRECTOTCORR": [0.0, 5.2, NASA_SENTINEL],
        "RH2M": [60, 65, 70],
        "WS2M": [2.1, 2.3, 2.0],
        "WS2M_MAX": [4.0, 4.2, 3.9],
        "PS":   [101.3, 101.2, 101.4],
        "QV2M": [12.1, 12.3, 12.5],
    })
    csv_path = tmp_path / "ethiopia.csv"
    df.to_csv(csv_path, index=False)
    return tmp_path


def test_load_country_replaces_sentinel(synthetic_csv):
    df = load_country("ethiopia", data_dir=synthetic_csv)
    assert df["T2M"].isna().sum() == 1
    assert df["PRECTOTCORR"].isna().sum() == 1
    assert NASA_SENTINEL not in df.values


def test_load_country_adds_date_column(synthetic_csv):
    df = load_country("ethiopia", data_dir=synthetic_csv)
    assert "DATE" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["DATE"])


def test_load_country_adds_country_column(synthetic_csv):
    df = load_country("ethiopia", data_dir=synthetic_csv)
    assert "Country" in df.columns
    assert df["Country"].iloc[0] == "Ethiopia"


def test_load_country_adds_month_column(synthetic_csv):
    df = load_country("ethiopia", data_dir=synthetic_csv)
    assert "Month" in df.columns
    assert df["Month"].iloc[0] == 1  # DOY=1 → January
