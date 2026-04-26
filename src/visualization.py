"""
visualization.py
----------------
Reusable, publication-quality plotting functions.

Every figure follows the three-layer framework from the challenge spec:
  1. What is changing?   (trend + baseline + uncertainty)
  2. What did it cause?  (impact annotation when data supports it)
  3. What does it demand? (left for markdown cells in notebooks)

Style rules:
- Consistent color palette across all countries (COUNTRY_COLORS)
- All axes labeled with units
- savefig() always called alongside plt.show() for reproducibility
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# ── Consistent country colors across all charts ───────────────────────────────
COUNTRY_COLORS = {
    "Ethiopia":  "#E63946",
    "Kenya":     "#2A9D8F",
    "Sudan":     "#E9C46A",
    "Tanzania":  "#F4A261",
    "Nigeria":   "#264653",
}

plt.rcParams.update({
    "figure.dpi": 120,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
})


def monthly_temperature(df: pd.DataFrame, country: str, save_dir: Path | None = None) -> None:
    """Line chart: monthly average T2M over 2015–2026."""
    monthly = df.groupby(["Year", "Month"])["T2M"].mean().reset_index()
    monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(day=1))

    warmest = monthly.loc[monthly["T2M"].idxmax()]
    coolest = monthly.loc[monthly["T2M"].idxmin()]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly["Date"], monthly["T2M"], color=COUNTRY_COLORS.get(country, "#333"), linewidth=1.5)
    ax.annotate(f"Warmest\n{warmest['T2M']:.1f}°C",
                xy=(warmest["Date"], warmest["T2M"]),
                xytext=(10, 10), textcoords="offset points", fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate(f"Coolest\n{coolest['T2M']:.1f}°C",
                xy=(coolest["Date"], coolest["T2M"]),
                xytext=(10, -20), textcoords="offset points", fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_title(f"{country} — Monthly mean temperature (2015–2026)", fontsize=13)
    ax.set_xlabel("Date")
    ax.set_ylabel("T2M (°C)")
    fig.tight_layout()
    if save_dir:
        fig.savefig(Path(save_dir) / f"{country.lower()}_monthly_t2m.png", bbox_inches="tight")
    plt.show()


def monthly_precipitation(df: pd.DataFrame, country: str, save_dir: Path | None = None) -> None:
    """Bar chart: monthly total PRECTOTCORR."""
    monthly = df.groupby(["Year", "Month"])["PRECTOTCORR"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(day=1))
    peak = monthly.loc[monthly["PRECTOTCORR"].idxmax()]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(monthly["Date"], monthly["PRECTOTCORR"], width=25,
           color=COUNTRY_COLORS.get(country, "#333"), alpha=0.7)
    ax.annotate(f"Peak\n{peak['PRECTOTCORR']:.0f} mm",
                xy=(peak["Date"], peak["PRECTOTCORR"]),
                xytext=(10, 5), textcoords="offset points", fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_title(f"{country} — Monthly total precipitation (2015–2026)", fontsize=13)
    ax.set_xlabel("Date")
    ax.set_ylabel("PRECTOTCORR (mm/month)")
    fig.tight_layout()
    if save_dir:
        fig.savefig(Path(save_dir) / f"{country.lower()}_monthly_precip.png", bbox_inches="tight")
    plt.show()


def correlation_heatmap(df: pd.DataFrame, country: str, save_dir: Path | None = None) -> None:
    """Correlation heatmap for all numeric columns."""
    numeric = df.select_dtypes(include=np.number).drop(columns=["YEAR", "DOY", "Year", "Month"], errors="ignore")
    corr = numeric.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                linewidths=0.4, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title(f"{country} — Correlation matrix", fontsize=13)
    fig.tight_layout()
    if save_dir:
        fig.savefig(Path(save_dir) / f"{country.lower()}_correlation.png", bbox_inches="tight")
    plt.show()


def multi_country_temperature(combined: pd.DataFrame, save_dir: Path | None = None) -> None:
    """Single line chart with one line per country — Task 3."""
    monthly = (
        combined.groupby(["Country", "Year", "Month"])["T2M"]
        .mean()
        .reset_index()
    )
    monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(day=1))

    fig, ax = plt.subplots(figsize=(16, 6))
    for country, grp in monthly.groupby("Country"):
        ax.plot(grp["Date"], grp["T2M"],
                label=country, color=COUNTRY_COLORS.get(country, "#888"), linewidth=1.5)
    ax.set_title("Monthly mean temperature — all five countries (2015–2026)", fontsize=13)
    ax.set_xlabel("Date")
    ax.set_ylabel("T2M (°C)")
    ax.legend(frameon=False)
    fig.tight_layout()
    if save_dir:
        fig.savefig(Path(save_dir) / "compare_temperature.png", bbox_inches="tight")
    plt.show()
