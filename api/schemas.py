from pydantic import BaseModel
from typing import List

class AssetCreate(BaseModel):
    ticket:str
    weight:float

class PortfolioCreate(BaseModel):
    name:str
    assets:List[AssetCreate]

class RiskResponse(BaseModel):
    volatility:float
    var_95:float
    monte_carlo_var:float
    beta:float
    