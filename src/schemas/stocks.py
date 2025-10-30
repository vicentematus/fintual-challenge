from typing import Literal
from pydantic import BaseModel

StockSymbol = Literal["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META"]


class Stock(BaseModel):
    symbol: StockSymbol
    name: str
    price: float


# Stocks in Plural
Stocks = dict[StockSymbol, Stock]
