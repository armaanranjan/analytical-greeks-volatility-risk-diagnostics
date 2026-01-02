import numpy as np
import pandas as pd
from core.implied_vol import implied_volatility

def compute_vol_smile(option_chain, S, T, r, option_type):
    """
    option_chain: DataFrame indexed by strike, with ONE column = market price
    """

    # 🔒 Ensure DataFrame
    if isinstance(option_chain, pd.Series):
        option_chain = option_chain.to_frame()

    # 🔒 Ensure exactly one column
    price_col = option_chain.columns[0]

    strikes = []
    ivs = []

    for strike, row in option_chain.iterrows():
        market_price = float(row[price_col])

        if market_price <= 0:
            continue

        try:
            iv = implied_volatility(
                market_price,
                S,
                float(strike),
                T,
                r,
                option_type
            )
            strikes.append(float(strike))
            ivs.append(iv)
        except Exception:
            continue

    return np.array(strikes), np.array(ivs)
