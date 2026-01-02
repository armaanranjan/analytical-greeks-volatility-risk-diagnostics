# Analytical Greeks, Implied Volatility Surfaces, and Risk Diagnostics in Option Pricing Models

## Overview

This project presents a **computational framework** for analyzing European option pricing models through **analytical Greeks**, **implied volatility inversion**, **volatility smile construction**, **Monte Carlo benchmarking**, and **risk diagnostics**.

Rather than proposing a speculative trading strategy, the project **reframes the Black–Scholes model as a diagnostic baseline** to:
- identify volatility mispricing,
- analyze hedging sensitivities,
- and study the stability of model-implied risk measures.

The system integrates **theoretical finance**, **numerical methods**, and **computational diagnostics** with an interactive **Streamlit-based interface**.

---

## Motivation and Problem Statement

### Why Black–Scholes Still Matters

Despite its simplifying assumptions, the Black–Scholes model remains:
- a benchmark in academic finance,
- a baseline for implied volatility quoting,
- and a reference point for hedging risk.

However, **Black–Scholes is often misused as a predictive trading model**, which leads to flawed conclusions.

### Core Problem Addressed

> **How can classical option pricing models be repurposed as diagnostic tools rather than predictive mechanisms?**

This project addresses:
- volatility mispricing diagnostics,
- sensitivity analysis via Greeks,
- and model breakdown under realistic market conditions.

---

## Mathematical Framework

### 1. Underlying Asset Dynamics

The asset price \( S_t \) is assumed to follow geometric Brownian motion:

\[
dS_t = \mu S_t \, dt + \sigma S_t \, dW_t
\]

Under the **risk-neutral measure**:

\[
dS_t = r S_t \, dt + \sigma S_t \, dW_t
\]

where:
- \( r \) is the risk-free rate,
- \( \sigma \) is volatility,
- \( W_t \) is a Wiener process.

---

### 2. Black–Scholes Option Pricing

#### Call Option Price

\[
C(S,K,T,r,\sigma) = S N(d_1) - K e^{-rT} N(d_2)
\]

#### Put Option Price

\[
P(S,K,T,r,\sigma) = K e^{-rT} N(-d_2) - S N(-d_1)
\]

where:

\[
d_1 = \frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}
\]

\[
d_2 = d_1 - \sigma\sqrt{T}
\]

and \( N(\cdot) \) is the standard normal CDF.

---

## Analytical Greeks (Risk Sensitivities)

Greeks quantify **how option prices respond to changes in market variables**.

### Delta — Directional Risk

\[
\Delta_{\text{call}} = N(d_1)
\]

\[
\Delta_{\text{put}} = N(d_1) - 1
\]

**Interpretation:**  
Delta measures sensitivity to small changes in the underlying price.

---

### Gamma — Convexity Risk

\[
\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}
\]

**Interpretation:**  
Gamma captures how Delta itself changes — crucial for hedging stability.

---

### Vega — Volatility Risk

\[
\text{Vega} = S N'(d_1)\sqrt{T}
\]

**Interpretation:**  
Vega measures sensitivity to changes in volatility and dominates option risk near-the-money.

---

## Implied Volatility

Market option prices invert the Black–Scholes formula to obtain **implied volatility** \( \sigma_{\text{IV}} \):

\[
C_{\text{BS}}(S,K,T,r,\sigma_{\text{IV}}) = C_{\text{market}}
\]

Numerical root-finding (Brent’s method) is used to solve this nonlinear equation.

---

## Volatility Smile

By computing implied volatility across strikes:

\[
\sigma_{\text{IV}}(K)
\]

we obtain the **volatility smile**, revealing:
- skewness,
- fat-tail expectations,
- deviations from constant volatility assumptions.

This directly exposes **model mispricing** and **risk concentration**.

---

## Monte Carlo Simulation

To benchmark analytical results, terminal prices are simulated as:

\[
S_T = S_0 \exp\left(
(r - \frac{1}{2}\sigma^2)T + \sigma\sqrt{T}Z
\right)
\]

where \( Z \sim \mathcal{N}(0,1) \).

Monte Carlo pricing serves as:
- a numerical validation tool,
- a stress-test for analytical assumptions,
- and a comparison under extreme scenarios.

---

## Backtesting Diagnostics

Rather than claiming profitability, historical data is used to:
- examine the **stability of Greeks**,
- analyze **hedging error behavior**,
- and study **volatility regime sensitivity**.

This approach avoids overfitting and unrealistic performance claims.

---

## Real-World Relevance

This framework mirrors how option pricing models are used in practice:

### Financial Institutions
- Risk management
- Greeks-based hedging
- Model validation

### Exchanges & Market Makers
- Volatility surface construction
- Sensitivity monitoring
- Stress testing

### Research & Academia
- Model diagnostics
- Baseline comparison
- Quantitative finance education

---

## What This Project Is NOT

❌ Not a trading bot  
❌ Not a market prediction engine  
❌ Not a profitability claim  

✔ A **diagnostic and analytical framework**  
✔ A **research-grade implementation**  
✔ A **foundation for advanced models** (Heston, SABR, ML volatility)

---

## Project Structure

- core/ Analytical pricing models and Greeks
- analysis/ Volatility smile construction
- backtesting/ Historical diagnostics
- data/ Market data ingestion and fallback
- app.py Streamlit interface

## References
- Black, F., & Scholes, M. (1973).
  The Pricing of Options and Corporate Liabilities.
  Journal of Political Economy.
- Hull, J. (2021).
  Options, Futures, and Other Derivatives. Pearson.
- Gatheral, J. (2006).
  The Volatility Surface. Wiley.
- Glasserman, P. (2004).
  Monte Carlo Methods in Financial Engineering. Springer
