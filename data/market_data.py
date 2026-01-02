import yfinance as yf
import numpy as np

def get_stock_price(ticker):
    return float(
        yf.Ticker(ticker)
        .history(period="1d")["Close"]
        .iloc[-1]
    )

def historical_volatility(ticker):
    data = yf.download(ticker, period="1y", progress=False)

    returns = np.log(data["Close"] / data["Close"].shift(1))
    sigma = float(returns.dropna().std() * np.sqrt(252))

    return sigma, data
