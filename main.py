# main.py
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

from api_client import fetch_marketaux

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

def timestamp() -> str:
    # FIX: return the formatted time
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def flatten_marketaux(resp: dict) -> list[dict]:
    """Turn Marketaux response into row-per-(article,entity) records."""
    rows = []
    for art in resp.get("data", []):
        entities = art.get("entities") or []  # FIX: 'entities' not 'entries'
        if not entities:
            continue  # skip articles without resolved entities
        base = {
            "article_id": art.get("uuid"),
            "published_at": art.get("published_at"),
            "title": art.get("title"),
            "url": art.get("url"),
            "source": art.get("source"),
            "language": art.get("language"),
        }
        for ent in entities:
            score = ent.get("sentiment_score")
            if score is None:
                # skip if API didn't attach a score (rare if you filter properly)
                continue
            rows.append({
                **base,
                "symbol": ent.get("symbol"),
                "company": ent.get("name"),
                "match_score": ent.get("match_score"),
                "sentiment_score": score,
            })
    return rows

def save_table(df: pd.DataFrame, path: Path) -> None:
    # if you get a parquet error, pip install pyarrow or change to CSV
    df.to_parquet(path, index=False)

if __name__ == "__main__":
    parameters = {
        "symbols": "TSLA",
        "language": "en",
        "limit": 50,
        # Recommended so you actually get entity sentiment on each row:
        "filter_entities": "true",
        "must_have_entities": "true",
    }
    resp = fetch_marketaux(parameters)

    # Flatten and save as Parquet
    rows = flatten_marketaux(resp)
    df = pd.DataFrame(rows)
    if not df.empty:
        proc_path = PROC_DIR / f"news_{parameters['symbols']}_{timestamp()}.parquet"
        save_table(df, proc_path)
        print(f"Saved {len(df)} rows -> {proc_path}")
    else:
        print("No rows to save (empty after flatten) — check params or response.")