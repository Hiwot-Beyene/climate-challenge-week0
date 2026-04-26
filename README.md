# kaim-week0
Climate data analysis project exploring temperature, precipitation, and extreme weather patterns across five African countries (2015–2026). The project focuses on transforming raw climate data into actionable insights to support Ethiopia’s COP32 climate policy strategy.


# 🌍 Climate Data Analysis for COP32 – African Climate Trends (2015–2026)

This project explores historical climate data across five African countries—Ethiopia, Kenya, Sudan, Tanzania, and Nigeria—to uncover key climate trends, seasonal patterns, and extreme events. The analysis supports Ethiopia’s preparation for hosting COP32 by generating **data-driven insights for climate policy and negotiation**.

## 🎯 Objective

To transform raw climate data into **evidence-backed insights** that highlight Africa’s climate vulnerabilities and inform policy discussions at global climate forums.

## 📊 Key Features

* Data cleaning and preprocessing of NASA POWER climate datasets
* Exploratory Data Analysis (EDA) for each country
* Time series analysis of temperature and precipitation trends
* Cross-country comparison of climate patterns
* Extreme event detection (heatwaves, droughts)
* Climate vulnerability ranking based on data evidence

## 🛠️ Tech Stack

* Python (Pandas, NumPy, Matplotlib, Seaborn)
* Jupyter Notebooks
* Git & GitHub (version control + CI/CD)
* Streamlit (optional dashboard)

## Project overview

Exploratory analysis of historical climate data (2015–2026) for Ethiopia, Kenya, Sudan, Tanzania, and Nigeria using NASA POWER satellite data, in support of Ethiopia's position ahead of COP32 in Addis Ababa.

---

## Quickstart (using uv)

### 1. Install uv (if not already installed)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repo

```bash
git clone https://github.com/Hiwot-Beyene/climate-challenge-week0.git
cd climate-challenge-week0
```

### 3. Create the virtual environment and install all dependencies

```bash
uv sync --extra dev
```

This creates `.venv/` automatically — no separate `python -m venv` needed.

### 4. Activate (optional — uv run handles this automatically)

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 5. Add the data

Download the five country CSVs from the Google Drive link in the challenge doc and place them in `data/`. They are gitignored and must never be committed.

```
data/
├── ethiopia.csv
├── kenya.csv
├── sudan.csv
├── tanzania.csv
└── nigeria.csv
```

### 6. Run the notebooks

```bash
uv run jupyter notebook
```

Open `notebooks/ethiopia_eda.ipynb` to start Task 2.

### 7. Run the tests

```bash
uv run pytest tests/ -v
```

### 8. Run the Streamlit dashboard (bonus)

```bash
uv run streamlit run app/main.py
```

---

## Project structure

```
climate-challenge-week0/
├── .github/workflows/ci.yml       # GitHub Actions CI — runs on every push
├── .vscode/settings.json          # Editor settings (uv venv path, ruff formatter)
├── .gitignore                     # Excludes data/, .venv/, secrets
├── pyproject.toml                 # uv project config + pinned dependencies
├── README.md                      # This file
│
├── data/                          # GITIGNORED — raw + cleaned CSVs live here
│
├── notebooks/
│   ├── ethiopia_eda.ipynb         # Task 2 — Ethiopia
│   ├── kenya_eda.ipynb            # Task 2 — Kenya
│   ├── sudan_eda.ipynb            # Task 2 — Sudan
│   ├── tanzania_eda.ipynb         # Task 2 — Tanzania
│   ├── nigeria_eda.ipynb          # Task 2 — Nigeria
│   └── compare_countries.ipynb   # Task 3 — Cross-country comparison
│
├── src/
│   ├── data_loader.py             # Load + sentinel-replace + date-parse
│   ├── cleaning.py                # Dedup, outliers, imputation, export
│   ├── eda_utils.py               # Statistical helpers (Kruskal-Wallis, etc.)
│   └── visualization.py          # Reusable publication-quality plots
│
├── tests/
│   ├── test_cleaning.py           # Unit tests for cleaning functions
│   └── test_data_loader.py        # Unit tests for data loading
│
├── app/
│   ├── main.py                    # Streamlit app (bonus)
│   └── utils.py                  # Chart + data helpers for Streamlit
│
└── scripts/                       # Standalone utility scripts
```

---

## Branch strategy

| Branch | Purpose |
|---|---|
| `main` | Protected — merge via PR only |
| `setup-task` | Task 1: environment + CI setup |
| `eda-ethiopia` | Task 2: Ethiopia EDA |
| `eda-kenya` | Task 2: Kenya EDA |
| `eda-sudan` | Task 2: Sudan EDA |
| `eda-tanzania` | Task 2: Tanzania EDA |
| `eda-nigeria` | Task 2: Nigeria EDA |
| `compare-countries` | Task 3: cross-country analysis |
| `dashboard-dev` | Bonus: Streamlit dashboard |

---

## CI/CD

GitHub Actions runs on every push. The workflow (`.github/workflows/ci.yml`):
1. Installs uv
2. Runs `uv sync --extra dev`
3. Lints with ruff
4. Runs pytest

---

## Data source

NASA Prediction of Worldwide Energy Resources (NASA POWER)
https://power.larc.nasa.gov/

**Important:** `-999` is NASA's sentinel value for missing/invalid data. It is replaced with `np.nan` as the very first operation in `data_loader.py`, before any statistics are computed.


## 📌 Outcomes

* Clear visualization of climate trends across Africa
* Identification of high-risk regions and climate variability
* Policy-relevant insights linking climate patterns to real-world impacts

## 🚀 Goal

To bridge the gap between **data analysis and climate policy**, demonstrating how data can support strategic decision-making in global climate negotiations.
