from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models,schemas
from Risk_engine.dataloader import fetch_price_data,calculate_returns
from Risk_engine.portfolio import Portfolio as RiskPortfolio
from Risk_engine.risk_metrics import historical_var,monte_carlo_var,calculate_beta

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/portfolio")
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    db_portfolio = models.Portfolio(name=portfolio.name)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)

    for asset in portfolio.assets:
        db_asset = models.Asset(
            ticker=asset.ticker,
            weight=asset.weight,
            portfolio_id=db_portfolio.id
        )
        db.add(db_asset)

    db.commit()
    return {"portfolio_id": db_portfolio.id}


@router.get("/risk/{portfolio_id}", response_model=schemas.RiskResponse)
def calculate_risk(portfolio_id: int, db: Session = Depends(get_db)):

    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    assets = portfolio.assets

    tickers = [a.ticker for a in assets]
    weights = [a.weight for a in assets]

    price_data = fetch_price_data(tickers)
    returns = calculate_returns(price_data)

    market_data = fetch_price_data(["^GSPC"])
    market_returns = calculate_returns(market_data)

    risk_portfolio = RiskPortfolio(tickers, weights)
    portfolio_returns = risk_portfolio.portfolio_returns(returns)

    volatility = risk_portfolio.annualized_volatility(portfolio_returns)
    var_95 = historical_var(portfolio_returns)
    var_mc = monte_carlo_var(portfolio_returns)
    beta = calculate_beta(portfolio_returns, market_returns.squeeze())

    return {
        "volatility": round(volatility, 4),
        "var_95": round(var_95, 4),
        
        "monte_carlo_var": round(var_mc, 4),
        "beta": round(beta, 4)
    }