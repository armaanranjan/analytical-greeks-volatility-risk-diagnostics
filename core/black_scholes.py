import numpy as np
from scipy.stats import norm

def call_price(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def put_price(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def _d1(S, K, T, r, sigma):
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return np.nan
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def delta(S, K, T, r, sigma, option_type="call"):
    d1 = _d1(S, K, T, r, sigma)
    if np.isnan(d1):
        return np.nan

    if option_type.lower() == "call":
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1


def gamma(S, K, T, r, sigma):
    d1 = _d1(S, K, T, r, sigma)
    if np.isnan(d1):
        return np.nan

    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def vega(S, K, T, r, sigma):
    d1 = _d1(S, K, T, r, sigma)
    if np.isnan(d1):
        return np.nan

    return S * norm.pdf(d1) * np.sqrt(T) / 100  # per 1% volatility

def theta_call(S, K, T, r, sigma):
    S, K, T, r, sigma = map(float, [S, K, T, r, sigma])
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return (
        - (S * norm.pdf(d1) * sigma) / (2*np.sqrt(T))
        - r * K * np.exp(-r*T) * norm.cdf(d2)
    )
