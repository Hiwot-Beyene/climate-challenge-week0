"""
Tests for src/cleaning.py

Run with: uv run pytest tests/ -v
"""

import numpy as np
import pandas as pd
import pytest

from src.cleaning import drop_duplicates, flag_outliers, impute_missing


@pytest.fixture
def sample_df():
    """Minimal DataFrame that mirrors NASA POWER structure."""
    return pd.DataFrame({
        "DATE": pd.date_range("2015-01-01", periods=10),
        "T2M":         [20.1, 21.3, np.nan, 22.0, 20.5, 21.0, 22.1, 19.8, 20.3, 21.1],
        "T2M_MAX":     [28.0, 29.0, 30.0, 31.0, 27.5, 28.5, 100.0, 28.0, 29.0, 30.0],  # 100 is outlier
        "T2M_MIN":     [14.0, 15.0, 14.5, 16.0, 13.0, 14.0, 15.0, 13.5, 14.0, 15.0],
        "PRECTOTCORR": [0.0, 5.2, 0.0, 12.1, 0.0, 3.4, 0.0, 0.5, 0.0, 2.1],
        "RH2M":        [60, 65, 70, 68, 62, 64, 66, 63, 61, 67],
        "WS2M":        [2.1, 2.3, 2.0, 2.5, 1.9, 2.2, 2.4, 2.1, 2.0, 2.3],
        "WS2M_MAX":    [4.0, 4.2, 3.9, 4.5, 3.8, 4.1, 4.3, 4.0, 3.9, 4.2],
        "Country":     ["Ethiopia"] * 10,
    })


def test_drop_duplicates_removes_exact_dupes():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    cleaned, n_dropped = drop_duplicates(df)
    assert n_dropped == 1
    assert len(cleaned) == 2


def test_drop_duplicates_no_dupes():
    df = pd.DataFrame({"a": [1, 2, 3]})
    cleaned, n_dropped = drop_duplicates(df)
    assert n_dropped == 0


def test_flag_outliers_marks_extreme_value(sample_df):
    flagged = flag_outliers(sample_df)
    assert "is_outlier" in flagged.columns
    # The row with T2M_MAX=100 should be flagged
    assert flagged.loc[flagged["T2M_MAX"] == 100.0, "is_outlier"].all()


def test_impute_missing_fills_nans(sample_df):
    cleaned = impute_missing(sample_df)
    # After forward-fill, T2M should have no NaNs
    assert cleaned["T2M"].isna().sum() == 0


def test_drop_duplicates_does_not_mutate_input():
    df = pd.DataFrame({"a": [1, 1, 2]})
    original_len = len(df)
    drop_duplicates(df)
    assert len(df) == original_len  # input must be unchanged
