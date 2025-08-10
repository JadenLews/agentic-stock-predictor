# experiments/offline_test.py
from pathlib import Path
import json
import pandas as pd


DATA_DIR = Path("../data")  # relative to this script
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"

def load_latest_table() -> pd.DataFrame:
    files = sorted(PROC_DIR.glob("news_*.parquet"))
    if not files:
        raise FileNotFoundError("No processed parquet files found in data/processed.")
    latest = files[-1]
    print(f"Loading table: {latest}")
    return pd.read_parquet(latest)

df = load_latest_table()
print(df.head())

if "published_at" in df.columns:
    df["date"] = pd.to_datetime(df["published_at"]).dt.date
    grp = df.groupby(["symbol", "date"]).agg(
        headline_count=("article_id", "nunique"),
        mean_sentiment=("sentiment_score", "mean"),
    ).reset_index()
    print(grp.tail())

    