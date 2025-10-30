from exceptions import AllocationError, StockInvalidError
from schemas import (
    Allocation,
    Holding,
    RebalanceAction,
    RebalanceResult,
    Rebalance,
    Stock,
    StockSymbol,
    Stocks,
)


class Portfolio:
    stocks: Stocks
    allocations: Allocation
    holdings: Holding

    def __init__(self):
        self.stocks = Stocks()
        self.allocations = Allocation()
        self.holdings = Holding()

    def add_allocation(self, stock: StockSymbol, allocation: float):
        if allocation <= 0.0 or allocation > 1.0:
            raise AllocationError(
                f"Allocation must be between 0% and 100%, got {allocation * 100}%!"
            )

        if stock not in self.allocations:
            self.allocations[stock] = allocation
        else:
            self.allocations[stock] += allocation

        self._validate_allocations()

    def add_stock(self, stock: Stock, shares: int):
        if shares <= 0:
            raise StockInvalidError("Shares can't be zero or negative!")

        if stock.symbol in self.holdings:
            self.holdings[stock.symbol] += shares
        else:
            self.holdings[stock.symbol] = shares

        self.stocks[stock.symbol] = stock

    def _validate_allocations(self):
        total = sum(self.allocations.values())
        if total > 1.0 or total < 0.0:
            raise AllocationError("Allocations must sum to 100%.")

    def _get_total_stocks(self) -> float:
        """
        Get the total amount of stocks you own based on the shares you have.
        """
        total = 0
        for stock_symbol, shares in self.holdings.items():
            stock = self.stocks[stock_symbol]
            price = stock.price * shares
            total += price

        return total

    def _calculate_current_stock(self, stock_symbol: StockSymbol) -> float:
        shares = self.holdings[stock_symbol]
        stock = self.stocks[stock_symbol]
        price = stock.price * shares
        return price

    def _calculate_rebalance(self) -> list[Rebalance]:
        total_stocks = self._get_total_stocks()
        reallocations: list[Rebalance] = []
        for stock_symbol, shares in self.holdings.items():
            current_value = shares * self.stocks[stock_symbol].price
            allocation_percentage = self.allocations[stock_symbol]
            target_value = total_stocks * allocation_percentage

            has_to_sell = target_value < current_value
            has_to_buy = target_value > current_value
            has_to_hold = target_value == current_value

            if has_to_sell:
                reallocations.append(
                    Rebalance(
                        action=RebalanceAction.SELL,
                        symbol=stock_symbol,
                        amount=current_value - target_value,
                    )
                )
            elif has_to_buy:
                reallocations.append(
                    Rebalance(
                        action=RebalanceAction.BUY,
                        symbol=stock_symbol,
                        amount=target_value - current_value,
                    )
                )
            elif has_to_hold:
                reallocations.append(
                    Rebalance(
                        action=RebalanceAction.HOLD, symbol=stock_symbol, amount=0.0
                    )
                )

        return reallocations

    def rebalance(self) -> RebalanceResult:
        actions = self._calculate_rebalance()
        to_buy = [a for a in actions if a.action == RebalanceAction.BUY]
        to_sell = [a for a in actions if a.action == RebalanceAction.SELL]
        return RebalanceResult(to_buy=to_buy, to_sell=to_sell)
