import pandas as pd
import yfinance as yf
import ta

def get_close_series(df: pd.DataFrame, ticker: str | None = None) -> pd.Series:
    # Multi-ticker -> MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        if ticker is None:
            raise ValueError("Provide `ticker` because DataFrame has MultiIndex columns.")
        s = df["Close"][ticker]
    else:
        s = df["Close"]

    # Ensure 1D Series
    s = s.squeeze()          # (n,1) -> (n,)
    s = pd.to_numeric(s, errors="coerce").dropna()
    s.name = "Close"
    return s

# EXAMPLES
# Single ticker
df = yf.download("AAPL", start="2024-01-01")




close = get_close_series(df, "AAPL")               # no ticker needed


df["RSI"] = ta.momentum.RSIIndicator(close).rsi()

macd_ind = ta.trend.MACD(close)
df["MACD"] = macd_ind.macd()
df["Signal"] = macd_ind.macd_signal()
print(df)
