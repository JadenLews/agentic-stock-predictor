import pandas as pd
import yfinance as yf
import ta
from db.write import save_stock_values_to_db

def get_close_series(df: pd.DataFrame, ticker: str | None = None) -> pd.Series:
    # Handles both single- and multi-ticker outputs
    if isinstance(df.columns, pd.MultiIndex):
        if ticker is None:
            raise ValueError("Provide `ticker` because DataFrame has MultiIndex columns.")
        s = df["Close"][ticker]
    else:
        s = df["Close"]
    return s.squeeze().astype(float)

def update_stock_values(ticker: str, start_date: str) -> int:
    # 1) Download prices
    df = yf.download(ticker, start=start_date)

    # 2) Select columns (support single or MultiIndex)
    if isinstance(df.columns, pd.MultiIndex):
        close = df["Close"][ticker].astype(float)
        open_ = df["Open"][ticker].astype(float)
        high  = df["High"][ticker].astype(float)
        low   = df["Low"][ticker].astype(float)
        vol   = df["Volume"][ticker].astype("int64")
    else:
        close = df["Close"].astype(float)
        open_ = df["Open"].astype(float)
        high  = df["High"].astype(float)
        low   = df["Low"].astype(float)
        vol   = df["Volume"].astype("int64")

    # 3) Indicators (use the selected 1D close Series)
    rsi = ta.momentum.RSIIndicator(close).rsi()
    macd_ind = ta.trend.MACD(close)
    macd = macd_ind.macd()
    macd_signal = macd_ind.macd_signal()

    # 4) Build the DataFrame the saver expects
    out = pd.DataFrame({
        "date": df.index,          # index -> column
        "ticker": ticker,
        "open_": open_,
        "high":  high,
        "low":   low,
        "close_": close,
        "volume": vol,
        "macd_signal": macd_signal,
        "rsi": rsi,
        "macd": macd,
    })

    # 5) Persist
    added = save_stock_values_to_db(out)
    return added

# Example
print(update_stock_values("AAPL", "2023-01-01"))