import numpy as np
from core.black_scholes import call_price

def run_backtest(data, K, r, T, sigma):
    pnl = []

    # Force scalars once
    K = float(K)
    r = float(r)
    T = float(T)
    sigma = float(sigma)

    prices = data["Close"].dropna().values  # NumPy array

    for price in prices:
        S = float(price)  # 🔑 CRITICAL FIX

        theoretical = call_price(S, K, T, r, sigma)

        # Simulated market price (mispricing)
        market = theoretical * np.random.uniform(0.9, 1.1)

        pnl.append(theoretical - market)

    return np.cumsum(pnl)
