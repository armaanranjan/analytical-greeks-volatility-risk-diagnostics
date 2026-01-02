from scipy.optimize import brentq
from core.black_scholes import call_price, put_price
import numpy as np

def implied_volatility(market_price, S, K, T, r, option_type="call"):
    if market_price <= 0 or T <= 0:
        return np.nan

    def objective(sigma):
        if option_type == "call":
            return call_price(S, K, T, r, sigma) - market_price
        else:
            return put_price(S, K, T, r, sigma) - market_price

    try:
        return brentq(objective, 1e-6, 5)
    except ValueError:
        # No valid implied volatility
        return np.nan
