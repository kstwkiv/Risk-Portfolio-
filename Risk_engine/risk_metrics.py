import numpy as np
def monte_carlo_var(portfolio_returns,confidence=0.95,simulations=10000):
    mean=np.mean(portfolio_returns)
    std=np.std(portfolio_returns)
    simulated_returns=np.random.normal(mean,std,simulations)
    percentile=(1-confidence)*100
    return np.percentile(simulated_returns,percentile)

def historical_var(portfolio_returns,confidence=0.95):
    percentile=(1-confidence)*100
    return np.percentile(portfolio_returns,percentile)

def calculate_beta(portfolio_returns, market_returns):
    # Align both series to avoid index mismatch chaos
    aligned = portfolio_returns.align(market_returns, join="inner")
    rp, rm = aligned[0], aligned[1]

    if len(rp) < 2:
        raise ValueError("Not enough data points to compute beta.")

    market_variance = np.var(rm, ddof=1)

    if np.isclose(market_variance, 0):
        raise ValueError("Market variance is zero. Cannot compute beta.")

    covariance = np.cov(rp, rm, ddof=1)[0, 1]

    return covariance / market_variance