# main.py
from pathlib import Path
from db.write import save_articles_to_db

from api_client import fetch_marketaux

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    parameters = {
        "symbols": "TSLA",
        "language": "en",
        "limit": 10,
        # Recommended so you actually get entity sentiment on each row:
        "filter_entities": "true",
        "must_have_entities": "true",
        "page": 1,
    }

    for i in range(10, 15):
        parameters["page"] = i
        print(parameters)
        
        resp = fetch_marketaux(parameters)

        articles_added, hits_added = save_articles_to_db(resp.get("data", []))
        print(f"Inserted {articles_added} new articles, {hits_added} entity hits.")
