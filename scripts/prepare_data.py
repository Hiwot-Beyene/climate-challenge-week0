"""
scripts/prepare_data.py
-----------------------
Automates the loading and cleaning of all five country datasets
from raw CSVs in data/ to cleaned CSVs for the dashboard.
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from src.cleaning import run_cleaning_pipeline
from src.data_loader import COUNTRIES, load_country


def main():
    data_dir = Path("data")
    print(f"🚀 Starting data preparation in {data_dir}...")

    for country in COUNTRIES:
        try:
            print(f"📦 Processing {country}...")
            df = load_country(country, data_dir)
            df_clean, report = run_cleaning_pipeline(df, country, data_dir)
            print(f"✅ Cleaned {country}: {report['rows_after_imputation']} rows exported to {report['exported_to']}")
        except Exception as e:
            print(f"❌ Error processing {country}: {e}")

    print("\n✨ All cleaned CSVs generated successfully!")

if __name__ == "__main__":
    main()
