from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Portfolio(Base):
    __tablename__="portfolios"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    assets=relationship("Asset",back_populates="portfolio")

class Asset(Base):
    __tablename__="assets"
    id=Column(Integer,primary_key=True,index=True)
    ticker=Column(String)
    weight=Column(Float)
    portfolio_id=Column(Integer,ForeignKey("portfolios.id"))

    portfolio=relationship("Portfolio",back_populates="assets")