"""
data_loader.py
--------------
Responsible for loading raw NASA POWER CSVs and performing the
initial date-parsing that every downstream notebook depends on.

Rules that must NEVER be broken:
- Replace -999 with np.nan BEFORE any computation.
- Parse YEAR + DOY into a proper datetime column.
- Do NOT modify the raw data/ files.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# NASA POWER sentinel value for missing / out-of-range data
NASA_SENTINEL = -999

COUNTRIES = ["ethiopia", "kenya", "sudan", "tanzania", "nigeria"]


def load_country(country: str, data_dir: str | Path = "data") -> pd.DataFrame:
    """Load a single country CSV, replace sentinels, parse dates.

    Parameters
    ----------
    country : str
        Lowercase country name, e.g. "ethiopia".
    data_dir : str | Path
        Directory containing the raw CSV files.

    Returns
    -------
    pd.DataFrame
        Clean-dated DataFrame with a DATE column and a Country column.
    """
    path = Path(data_dir) / f"{country}.csv"
    df = pd.read_csv(path)

    # Step 1 — replace NASA sentinel BEFORE any statistics
    df.replace(NASA_SENTINEL, np.nan, inplace=True)

    # Step 2 — add country label
    df["Country"] = country.capitalize()

    # Step 3 — build proper datetime from YEAR + DOY
    df["DATE"] = pd.to_datetime(
        df["YEAR"] * 1000 + df["DOY"], format="%Y%j"
    )

    # Step 4 — convenience columns
    df["Month"] = df["DATE"].dt.month
    df["Year"] = df["DATE"].dt.year

    return df


def load_all(data_dir: str | Path = "data") -> pd.DataFrame:
    """Load and concatenate all five country datasets."""
    frames = [load_country(c, data_dir) for c in COUNTRIES]
    return pd.concat(frames, ignore_index=True)
