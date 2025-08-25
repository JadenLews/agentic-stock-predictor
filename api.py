# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from yfinance_collect import update_stock_values

app = FastAPI()

# allow React dev server to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UpdateReq(BaseModel):
    ticker: str

@app.post("/update")
def update_prices(req: UpdateReq):
    added = update_stock_values(req.ticker)
    return {"ticker": req.ticker, "added": added}