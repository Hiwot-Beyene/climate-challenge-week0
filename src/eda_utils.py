"""
eda_utils.py
------------
Statistical helpers used across EDA notebooks.
"""

from __future__ import annotations

import pandas as pd
from scipy import stats


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return a tidy DataFrame showing null count and % per column."""
    null_counts = df.isna().sum()
    null_pct = (df.isna().mean() * 100).round(2)
    report = pd.DataFrame({"null_count": null_counts, "null_pct": null_pct})
    return report[report["null_count"] > 0].sort_values("null_pct", ascending=False)


def extreme_heat_days(df: pd.DataFrame, threshold: float = 35.0) -> pd.DataFrame:
    """Count days per year where T2M_MAX > threshold (°C)."""
    return (
        df[df["T2M_MAX"] > threshold]
        .groupby(["Country", "Year"])
        .size()
        .reset_index(name="extreme_heat_days")
    )


def consecutive_dry_days(df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
    """Count maximum consecutive dry days (PRECTOTCORR < threshold) per year per country."""
    results = []
    for (country, year), grp in df.groupby(["Country", "Year"]):
        is_dry = grp["PRECTOTCORR"] < threshold
        max_streak = 0
        streak = 0
        for dry in is_dry:
            if dry:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        results.append({"Country": country, "Year": year, "max_dry_streak": max_streak})
    return pd.DataFrame(results)


def kruskal_wallis_t2m(df: pd.DataFrame) -> dict:
    """Run Kruskal–Wallis test on T2M across all countries.

    Returns a dict with H-statistic and p-value.
    """
    groups = [grp["T2M"].dropna().values for _, grp in df.groupby("Country")]
    h_stat, p_val = stats.kruskal(*groups)
    return {"H_statistic": round(h_stat, 4), "p_value": round(p_val, 6)}


def vulnerability_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Build the cross-country vulnerability ranking table for Task 3."""
    heat = extreme_heat_days(df).groupby("Country")["extreme_heat_days"].mean().rename("avg_extreme_heat_days")
    dry  = consecutive_dry_days(df).groupby("Country")["max_dry_streak"].mean().rename("avg_max_dry_streak")
    temp = df.groupby("Country")["T2M"].agg(mean_T2M="mean", std_T2M="std")
    prec = df.groupby("Country")["PRECTOTCORR"].agg(mean_precip="mean", std_precip="std")

    summary = pd.concat([temp, prec, heat, dry], axis=1).round(3)

    # Simple composite vulnerability score (higher = more vulnerable)
    summary["vulnerability_score"] = (
        summary["avg_extreme_heat_days"].rank(ascending=False)
        + summary["avg_max_dry_streak"].rank(ascending=False)
        + summary["std_precip"].rank(ascending=False)
    )
    return summary.sort_values("vulnerability_score", ascending=False)
