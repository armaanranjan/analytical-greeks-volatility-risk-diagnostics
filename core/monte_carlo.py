import numpy as np

def monte_carlo_price(S, K, T, r, sigma, option_type="call", sims=10000):
    # Force scalars (safety)
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)

    Z = np.random.standard_normal(sims)

    ST = S * np.exp(
        (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z
    )

    if option_type == "call":
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)

    return float(np.exp(-r * T) * payoff.mean())
