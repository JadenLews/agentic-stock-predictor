# api_client.py
import httpx
from config import MARKETAUX_API_KEY

BASE_URL = "https://api.marketaux.com/v1/news/all"

def fetch_marketaux(params: dict):
    headers = {"Authorization": f"Bearer {MARKETAUX_API_KEY}"}
    r = httpx.get(BASE_URL, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()




def fetch_reddit():
    request = f"https://tradestie.com/api/v1/apps/reddit'"
    r = httpx.get(request)
    r.raise_for_status()
    return r.json()


print(fetch_reddit())