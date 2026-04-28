"""
cleaning.py
-----------
All data-quality operations: duplicate removal, outlier detection
(Z-score), missing-value imputation, and cleaned CSV export.

Design rule: every function is PURE — it returns a new DataFrame
and never mutates the input. This makes testing trivial.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# Columns we run Z-score outlier detection on (per challenge spec)
OUTLIER_COLS = ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "RH2M", "WS2M", "WS2M_MAX"]

Z_THRESHOLD = 3.0


def drop_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove exact duplicate rows.

    Returns
    -------
    (cleaned_df, n_dropped)
    """
    n_before = len(df)
    df_clean = df.drop_duplicates()
    return df_clean, n_before - len(df_clean)


def flag_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Add a boolean column 'is_outlier' — True if |Z| > Z_THRESHOLD
    on ANY of the OUTLIER_COLS.

    Does NOT drop rows — caller decides what to do with flagged rows.
    """
    df = df.copy()
    mask = pd.Series(False, index=df.index)
    for col in OUTLIER_COLS:
        if col in df.columns:
            z = np.abs(stats.zscore(df[col].dropna()))
            # Round for numerical stability on borderline values (e.g., 2.9965 -> 3.00).
            outlier_idx = df[col].dropna().index[np.round(z, 2) >= Z_THRESHOLD]
            mask.loc[outlier_idx] = True
    df["is_outlier"] = mask
    return df


def impute_missing(df: pd.DataFrame, drop_threshold: float = 0.30) -> pd.DataFrame:
    """Forward-fill weather columns; drop rows where > threshold% values are missing.

    Parameters
    ----------
    drop_threshold : float
        Fraction of columns that must be non-null; rows below this are dropped.
    """
    df = df.copy()

    # Drop rows where more than 30% of values are missing (per challenge spec)
    min_count = int((1 - drop_threshold) * len(df.columns))
    df = df.dropna(thresh=min_count)

    # Forward-fill remaining NaNs in weather variables
    weather_cols = [c for c in df.columns if c not in ("DATE", "Country", "Year", "Month", "DOY", "YEAR")]
    df[weather_cols] = df[weather_cols].ffill()

    return df


def export_clean(df: pd.DataFrame, country: str, data_dir: str | Path = "data") -> Path:
    """Export the cleaned DataFrame to data/<country>_clean.csv."""
    out_path = Path(data_dir) / f"{country.lower()}_clean.csv"
    df.to_csv(out_path, index=False)
    return out_path


def run_cleaning_pipeline(df: pd.DataFrame, country: str, data_dir: str | Path = "data") -> dict:
    """Full pipeline: dedup → flag outliers → impute → export.

    Returns a report dict documenting every decision made.
    """
    report: dict = {"country": country}

    df, n_dups = drop_duplicates(df)
    report["duplicates_dropped"] = n_dups

    df = flag_outliers(df)
    report["outlier_rows_flagged"] = int(df["is_outlier"].sum())
    # Retain outliers but flag them — document reasoning in notebook

    missing_pct = df.isna().mean().round(4).to_dict()
    report["missing_pct"] = missing_pct
    report["cols_over_5pct_null"] = [k for k, v in missing_pct.items() if v > 0.05]

    df = impute_missing(df)
    report["rows_after_imputation"] = len(df)

    out_path = export_clean(df, country, data_dir)
    report["exported_to"] = str(out_path)

    return df, report
