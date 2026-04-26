"""
app/utils.py
------------
Data loading and Plotly chart builders for the Streamlit app.
Isolated here so main.py stays thin and testable.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px

COUNTRIES = ["ethiopia", "kenya", "sudan", "tanzania", "nigeria"]

COUNTRY_COLORS = {
    "Ethiopia":  "#E63946",
    "Kenya":     "#2A9D8F",
    "Sudan":     "#E9C46A",
    "Tanzania":  "#F4A261",
    "Nigeria":   "#264653",
}


def load_combined(data_dir: Path = Path("data")) -> pd.DataFrame:
    """Load all *_clean.csv files and return a single concatenated DataFrame."""
    frames = []
    for country in COUNTRIES:
        path = data_dir / f"{country}_clean.csv"
        if path.exists():
            df = pd.read_csv(path, parse_dates=["DATE"])
            frames.append(df)
    if not frames:
        raise FileNotFoundError("No cleaned CSV files found in data/")
    combined = pd.concat(frames, ignore_index=True)
    if "Year" not in combined.columns:
        combined["Year"] = combined["DATE"].dt.year
    return combined


def temperature_chart(df: pd.DataFrame):
    """Monthly mean T2M line chart — one line per country."""
    monthly = (
        df.groupby(["Country", "Year", "Month"])["T2M"]
        .mean()
        .reset_index()
    )
    monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(day=1))
    fig = px.line(
        monthly, x="Date", y="T2M", color="Country",
        color_discrete_map=COUNTRY_COLORS,
        labels={"T2M": "Mean temperature (°C)"},
    )
    fig.update_layout(template="plotly_white", legend_title_text="")
    return fig


def precipitation_boxplot(df: pd.DataFrame):
    """Side-by-side boxplots of daily PRECTOTCORR per country."""
    fig = px.box(
        df, x="Country", y="PRECTOTCORR",
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        labels={"PRECTOTCORR": "Daily precipitation (mm)"},
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig


def vulnerability_table(df: pd.DataFrame) -> pd.DataFrame:
    """Simple vulnerability summary for the dashboard table."""
    return (
        df.groupby("Country")
        .agg(
            mean_T2M=("T2M", "mean"),
            mean_precip=("PRECTOTCORR", "mean"),
            std_precip=("PRECTOTCORR", "std"),
        )
        .round(3)
        .sort_values("mean_T2M", ascending=False)
        .reset_index()
    )
