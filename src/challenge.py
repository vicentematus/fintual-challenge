from log import log_portfolio, log_rebalance_result
from portfolio import Portfolio
from schemas import Stock


def main():
    portfolio = Portfolio()

    META_STOCK = Stock(symbol="META", name="Meta Platforms, Inc.", price=100)
    AAPL_STOCK = Stock(symbol="AAPL", name="Apple Inc.", price=100)

    portfolio.add_stock(META_STOCK, shares=5)
    portfolio.add_stock(AAPL_STOCK, shares=5)

    portfolio.add_allocation("META", 0.4)
    portfolio.add_allocation("AAPL", 0.6)

    log_portfolio(portfolio)

    rebalance_result = portfolio.rebalance()
    log_rebalance_result(rebalance_result)


if __name__ == "__main__":
    main()
