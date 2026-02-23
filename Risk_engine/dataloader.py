import yfinance as yf
import pandas as pd
def fetch_price_data(tickers, start="2023-01-01"):
    data = yf.download(tickers, start=start)
    
    if "Adj Close" in data.columns:
        data = data["Adj Close"]
    elif "Close" in data.columns:
        data = data["Close"]
    else:
        raise ValueError("No price column found.")
    
    return data.dropna()
def calculate_returns(price_df):
    returns = price_df.pct_change().dropna()
    return returns

