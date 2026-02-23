import numpy as np
class Portfolio:
    def __init__(self,tickers,weights):
        self.tickers=tickers
        self.weights=np.array(weights)
        if not np.isclose(np.sum(self.weights),1):
            raise ValueError("Weights must sum to 1")
        
    def portfolio_returns(self,returns_df):
        return returns_df.dot(self.weights)
    def annualized_volatality(self,portfolio_returns):
        daily_vol=np.std(portfolio_returns)
        return daily_vol*np.sqrt(252)
