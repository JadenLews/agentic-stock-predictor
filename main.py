# main.py
from pathlib import Path
from db.write import save_articles_to_db

from api_client import fetch_marketaux
from yfinance_collect import update_stock_values
from fgi_collect import fetch_fgi_since

if __name__ == "__main__":
    pass









def test_apis():

    parameters = {
        "symbols": "TSLA",
        "language": "en",
        "limit": 3,
        "filter_entities": "true",
        "must_have_entities": "true",
        "page": 1,
    }

    # gets news sentiment, only 3 articles at a time, must go by page
    resp = fetch_marketaux(parameters)

    articles_added, hits_added = save_articles_to_db(resp.get("data", []))
    print(f"Inserted {articles_added} new articles, {hits_added} entity hits.")



    #update stock values in db
    print(update_stock_values("TSLA", "2023-01-01"))

    print(fetch_fgi_since('2024-01-01'))

test_apis()