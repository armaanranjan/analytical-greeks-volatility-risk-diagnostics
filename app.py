import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from core.black_scholes import call_price, put_price, delta
from core.implied_vol import implied_volatility
from core.monte_carlo import monte_carlo_price
from data.market_data import get_stock_price, historical_volatility
from backtesting.backtest import run_backtest
from analysis.vol_smile import compute_vol_smile
from core.black_scholes import gamma, vega, theta_call
from data.nse_option_chain import get_nse_option_chain

def ensure_dataframe(x, col_name="price"):
    if isinstance(x, pd.Series):
        return x.to_frame(name=col_name)
    return x



st.set_page_config("Quant Trading Bot", layout="wide")

st.title("📈 Black–Scholes Quant Trading Bot")
st.markdown("**Analytical • Monte Carlo • Implied Volatility • Backtesting**")

# Sidebar
st.sidebar.header("Parameters")
ticker = st.sidebar.text_input("Ticker", "AAPL")
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
K = st.sidebar.number_input("Strike Price", value=150.0)
days = st.sidebar.number_input("Days to Expiry", value=30)
r = st.sidebar.number_input("Risk-Free Rate", value=0.05)
market_price = st.sidebar.number_input("Market Option Price", value=5.0)
use_nse = st.sidebar.checkbox("Use NSE Option Chain (India)")


T = days / 365

try:
    S = get_stock_price(ticker)
    sigma, hist_data = historical_volatility(ticker)

    if use_nse:
        try:
            option_chain = get_nse_option_chain("NIFTY")
            st.info("ℹ️ Live NSE data unavailable. Using cached sample data.")
        except Exception as e:
            st.error(f"NSE data fetch failed: {e}")
            st.stop()
        if "type" in option_chain.columns:
            option_chain = option_chain[option_chain["type"] == option_type]

    else:
        option_chain = hist_data["Close"].iloc[-20:].reset_index(drop=True)
        if isinstance(option_chain, pd.Series):
            option_chain = option_chain.to_frame(name="price")
        option_chain["strike"] = np.linspace(0.8*S, 1.2*S, len(option_chain))

    if option_type == ["call"]:
        bs = call_price(S, K, T, r, sigma)
    else:
        bs = put_price(S, K, T, r, sigma)
        
    delta = None

    if T > 0 and sigma > 0:
        if option_type == "Call":
            delta = delta_call(S, K, T, r, sigma)
        elif option_type == "Put":
            delta = delta_put(S, K, T, r, sigma)


    iv = implied_volatility(market_price, S, K, T, r, option_type)
    iv_display = "N/A" if np.isnan(iv) else f"{iv:.2%}"

    mc = monte_carlo_price(S, K, T, r, sigma, option_type)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stock Price", f"${S:.2f}")
    col2.metric("BS Price", f"${bs:.2f}")
    col3.metric("Implied Vol", iv_display)
    col4.metric("Monte Carlo", f"${mc:.2f}")

    st.subheader("Risk Metrics")
    if delta is not None and np.isfinite(delta):
        st.write(f"Delta: **{delta:.3f}**")
    else:
        st.write("Delta: **N/A**")

    st.subheader("📉 Price History")
    fig, ax = plt.subplots()
    ax.plot(hist_data.index, hist_data["Close"])
    st.pyplot(fig)

    st.subheader("📊 Backtesting Result")
    pnl = run_backtest(hist_data, K, r, T, sigma)
    fig2, ax2 = plt.subplots()
    ax2.plot(pnl)
    ax2.set_ylabel("Cumulative PnL")
    st.pyplot(fig2)
    
    st.subheader("📈 Volatility Smile")

    # Synthetic option chain for demo (replaced by NSE in section 3)
    option_chain = hist_data["Close"].iloc[-20:].reset_index(drop=True)
    option_chain = ensure_dataframe(option_chain, "price")
    option_chain["strike"] = np.linspace(0.8*S, 1.2*S, len(option_chain))

    strikes, ivs = compute_vol_smile(option_chain, S, T, r, option_type)

    fig, ax = plt.subplots()
    ax.plot(strikes, ivs, marker="o")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Implied Volatility")
    st.pyplot(fig)
    
    st.subheader("📊 Greeks Dashboard")

    g1, g2, g3, g4 = st.columns(4)

    if delta is not None and np.isfinite(delta):
        g1.metric("Delta", f"{delta:.4f}")
    else:
        g1.metric("Delta", "N/A")

    g2.metric("Gamma", f"{gamma(S,K,T,r,sigma):.4f}")
    g3.metric("Vega", f"{vega(S,K,T,r,sigma):.4f}")
    g4.metric("Theta", f"{theta_call(S,K,T,r,sigma):.4f}")



except Exception as e:
    st.error("❌ Model failed to load")
    st.exception(e)

