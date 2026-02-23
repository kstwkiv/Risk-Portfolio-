from dataloader import fetch_price_data,calculate_returns
from portfolio import Portfolio
from risk_metrics import monte_carlo_var,historical_var,calculate_beta

tickers=["AAPL","MSFT","GOOGL"]
weights=[0.4,0.4,0.2]

price_data=fetch_price_data(tickers)
returns=calculate_returns(price_data)
market_data=fetch_price_data(["^GSPC"])
market_returns=calculate_returns(market_data)

portfolio=Portfolio(tickers,weights)
portfolio_returns=portfolio.portfolio_returns(returns)

volatility=portfolio.annualized_volatality(portfolio_returns)
var_hist=historical_var(portfolio_returns)
var_mc=monte_carlo_var(portfolio_returns)
beta=calculate_beta(portfolio_returns,market_returns.squeeze())

print("Annualized Volatility:", round(volatility, 4))
print("Historical VaR (95%):", round(var_hist, 4))
print("Monte Carlo VaR (95%):", round(var_mc, 4))
print("Beta vs S&P 500:", round(beta, 4))