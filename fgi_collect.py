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
START_DATE = '2024-01-01'
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

   rows = fetch_fgi_since(str(START_DATE))
   added = save_fgi_to_db(rows)
   print(f"Added {added} new records")





#    # first run: creates new df; others load and update
#    if OUT_CSV.exists() and OUT_CSV.stat().st_size > 0:
#       df = pd.read_csv(OUT_CSV, parse_dates=["Date"])
#       start_next = max(df["Date"])
#       #fetch from day latest record is stored
#       rows = fetch_fgi_since(str(start_next))
#       if rows:
#          df_new = pd.DataFrame(rows)
#          df = pd.concat([df, df_new], ignore_index=True)
#    else:
#       # first run: fetch from START_DATE
#       rows = fetch_fgi_since(str(START_DATE))
#       df = pd.DataFrame(rows)

#    if not df.empty:
#       df.drop_duplicates(subset=["Date"]).sort_values("Date")
#       df.to_csv("all_fng.csv", index=False)
#       print(f"Saved {len(df)} rows -> all_fng.csv")
#    else:
#       print("No data returned from CNN endpoint. Try a different START_DATE.")



main()