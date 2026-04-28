"""
app/main.py
-----------
Streamlit dashboard — EthioClimate Analytics COP32 Explorer

Run locally:
    uv run streamlit run app/main.py

Reads cleaned CSVs from data/*_clean.csv (never committed to git).
"""

from pathlib import Path

import streamlit as st

from app.utils import (
    load_combined,
    precipitation_boxplot,
    temperature_chart,
    vulnerability_table,
)

st.set_page_config(
    page_title="EthioClimate COP32 Explorer",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 EthioClimate Analytics — COP32 Climate Explorer")
st.caption("African climate trends · 2015–2026 · NASA POWER data")

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    countries = st.multiselect(
        "Countries",
        options=["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"],
        default=["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"],
    )
    year_range = st.slider("Year range", min_value=2015, max_value=2026, value=(2015, 2026))
    variable = st.selectbox(
        "Variable",
        options=["T2M", "PRECTOTCORR", "RH2M", "T2M_MAX", "WS2M"],
        index=0,
    )

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_combined(data_dir=Path("data"))

try:
    df = get_data()
except FileNotFoundError:
    st.error("No cleaned CSVs found in data/. Run the EDA notebooks first to generate *_clean.csv files.")
    st.stop()

filtered = df[
    df["Country"].isin(countries) &
    df["Year"].between(*year_range)
]

# ── Charts ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.subheader("Temperature trends")
    st.plotly_chart(temperature_chart(filtered), use_container_width=True)

with col2:
    st.subheader("Precipitation distribution")
    st.plotly_chart(precipitation_boxplot(filtered), use_container_width=True)

st.subheader("Climate vulnerability ranking")
st.dataframe(vulnerability_table(df), use_container_width=True)
