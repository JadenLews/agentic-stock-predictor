# fgi_collect.py
import requests, csv, json, urllib
import pandas as pd
import time
from fake_useragent import UserAgent
import os
from datetime import datetime, timezone
from pathlib import Path
ua = UserAgent()
from db.write import save_fgi_to_db



BASE_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"
#START_DATE = '2024-01-01'
START_DATE = '2025-08-01'
OUT_CSV = Path("all_fng.csv")
END_DATE = '2026-01-01'

def fetch_fgi_since(start_date: str) -> list[dict]:
   # CNN returns {x: ms_epoch, y: value}
   URL = BASE_URL + start_date
   headers = {
   'User-Agent': ua.random,
   }
   r = requests.get(URL, headers=headers, timeout=30)
   js = r.json()

   # series = js.get("fear_and_greed_historical", {}).get("data", [])
   # rows = []
   # for pt in series:
   #    ts = pd.to_datetime(pt["x"], unit="ms", utc=True).date()
   #    val = int(pt["y"])
   #    rows.append({"Date": ts, "Fear Greed": val})
   # return rows
   return js




def main():

   resp = fetch_fgi_since(START_DATE)  # if this returns the whole JSON
   rows = resp["fear_and_greed_historical"]["data"]
   added = save_fgi_to_db(rows)
   print(f"Added {added} new records")


main()



 