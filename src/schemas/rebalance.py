from enum import Enum
from pydantic import BaseModel
from .stocks import StockSymbol, Stock


class RebalanceAction(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class Rebalance(BaseModel):
    action: RebalanceAction
    symbol: StockSymbol
    amount: float


class RebalanceResult(BaseModel):
    to_buy: list[Rebalance]
    to_sell: list[Rebalance]
