import pytest
from portfolio import Portfolio
from schemas import Stock, StockSymbol, RebalanceAction, RebalanceResult, Rebalance


def test_rebalance_returns_correct_buy_and_sell_actions_for_40_60_allocation():
    """
    Given a portfolio with $10,000 total value:
    - Currently holding: $5,000 META and $5,000 AAPL
    - Target allocation: 40% META and 60% AAPL

    When rebalancing

    Then it should return:
    - Sell $1,000 of META
    - Buy $1,000 of AAPL
    """
    # Given
    portfolio = Portfolio()

    meta_stock = Stock(symbol="META", name="Meta Platforms", price=100.0)
    aapl_stock = Stock(symbol="AAPL", name="Apple Inc.", price=100.0)

    portfolio.add_stock(meta_stock, shares=50)  # 50 * $100 = $5,000
    portfolio.add_stock(aapl_stock, shares=50)  # 50 * $100 = $5,000

    portfolio.add_allocation("META", 0.40)  # 40%
    portfolio.add_allocation("AAPL", 0.60)  # 60%

    # When
    rebalance_result = portfolio.rebalance()

    # Then
    assert rebalance_result.to_sell == [
        Rebalance(action=RebalanceAction.SELL, symbol="META", amount=1000.0)
    ]

    assert rebalance_result.to_buy == [
        Rebalance(action=RebalanceAction.BUY, symbol="AAPL", amount=1000.0)
    ]


def test_rebalance_three_stocks_with_unequal_allocation():
    """
    Given a portfolio with $15,000 total value:
    - Currently holding: $5,000 META, $5,000 AAPL, $5,000 GOOGL (equal 33.33% each)
    - Target allocation: 30% META, 50% AAPL, and 20% GOOGL

    When rebalancing

    Then it should return:
    - Sell $500 of META (from $5,000 to $4,500 = 30% of $15,000)
    - Buy $2,500 of AAPL (from $5,000 to $7,500 = 50% of $15,000)
    - Sell $2,000 of GOOGL (from $5,000 to $3,000 = 20% of $15,000)
    """
    # Given
    portfolio = Portfolio()

    meta_stock = Stock(symbol="META", name="Meta Platforms", price=100.0)
    aapl_stock = Stock(symbol="AAPL", name="Apple Inc.", price=100.0)
    googl_stock = Stock(symbol="GOOGL", name="Alphabet Inc.", price=100.0)

    portfolio.add_stock(meta_stock, shares=50)  # 50 * $100 = $5,000
    portfolio.add_stock(aapl_stock, shares=50)  # 50 * $100 = $5,000
    portfolio.add_stock(googl_stock, shares=50)  # 50 * $100 = $5,000

    portfolio.add_allocation("META", 0.30)  # 30%
    portfolio.add_allocation("AAPL", 0.50)  # 50%
    portfolio.add_allocation("GOOGL", 0.20)  # 20%

    # When
    rebalance_result = portfolio.rebalance()

    # Then
    assert rebalance_result.to_sell == [
        Rebalance(action=RebalanceAction.SELL, symbol="META", amount=500.0),
        Rebalance(action=RebalanceAction.SELL, symbol="GOOGL", amount=2000.0),
    ]

    assert rebalance_result.to_buy == [
        Rebalance(action=RebalanceAction.BUY, symbol="AAPL", amount=2500.0)
    ]


def test_rebalance_extreme_imbalance_to_70_30():
    """
    Given a portfolio with $10,000 total value:
    - Currently holding: $9,000 META and $1,000 AAPL (90/10 split)
    - Target allocation: 70% META and 30% AAPL

    When rebalancing

    Then it should return:
    - Sell $2,000 of META (from $9,000 to $7,000 = 70%)
    - Buy $2,000 of AAPL (from $1,000 to $3,000 = 30%)
    """
    # Given
    portfolio = Portfolio()

    meta_stock = Stock(symbol="META", name="Meta Platforms", price=100.0)
    aapl_stock = Stock(symbol="AAPL", name="Apple Inc.", price=100.0)

    portfolio.add_stock(meta_stock, shares=90)  # 90 * $100 = $9,000
    portfolio.add_stock(aapl_stock, shares=10)  # 10 * $100 = $1,000

    portfolio.add_allocation("META", 0.70)  # 70%
    portfolio.add_allocation("AAPL", 0.30)  # 30%

    # When
    rebalance_result = portfolio.rebalance()

    # Then
    assert rebalance_result.to_sell == [
        Rebalance(action=RebalanceAction.SELL, symbol="META", amount=2000.0)
    ]

    assert rebalance_result.to_buy == [
        Rebalance(action=RebalanceAction.BUY, symbol="AAPL", amount=2000.0)
    ]


def test_rebalance_already_balanced_portfolio():
    """
    Given a portfolio with $10,000 total value:
    - Currently holding: $6,000 META and $4,000 AAPL (60/40 split)
    - Target allocation: 60% META and 40% AAPL

    When rebalancing

    Then it should return:
    - No buy actions
    - No sell actions
    """
    # Given
    portfolio = Portfolio()

    meta_stock = Stock(symbol="META", name="Meta Platforms", price=100.0)
    aapl_stock = Stock(symbol="AAPL", name="Apple Inc.", price=100.0)

    portfolio.add_stock(meta_stock, shares=60)  # 60 * $100 = $6,000
    portfolio.add_stock(aapl_stock, shares=40)  # 40 * $100 = $4,000

    portfolio.add_allocation("META", 0.60)  # 60%
    portfolio.add_allocation("AAPL", 0.40)  # 40%

    # When
    rebalance_result = portfolio.rebalance()

    # Then
    assert rebalance_result.to_sell == []
    assert rebalance_result.to_buy == []


def test_rebalance_four_stocks_complex_allocation():
    """
    Given a portfolio with $20,000 total value:
    - Currently holding: $5,000 each of META, AAPL, GOOGL, MSFT (25% each)
    - Target allocation: 40% META, 30% AAPL, 20% GOOGL, 10% MSFT

    When rebalancing

    Then it should return:
    - Buy $3,000 of META (from $5,000 to $8,000 = 40%)
    - Buy $1,000 of AAPL (from $5,000 to $6,000 = 30%)
    - Sell $1,000 of GOOGL (from $5,000 to $4,000 = 20%)
    - Sell $3,000 of MSFT (from $5,000 to $2,000 = 10%)
    """
    # Given
    portfolio = Portfolio()

    meta_stock = Stock(symbol="META", name="Meta Platforms", price=100.0)
    aapl_stock = Stock(symbol="AAPL", name="Apple Inc.", price=100.0)
    googl_stock = Stock(symbol="GOOGL", name="Alphabet Inc.", price=100.0)
    msft_stock = Stock(symbol="MSFT", name="Microsoft Corp.", price=100.0)

    portfolio.add_stock(meta_stock, shares=50)  # 50 * $100 = $5,000
    portfolio.add_stock(aapl_stock, shares=50)  # 50 * $100 = $5,000
    portfolio.add_stock(googl_stock, shares=50)  # 50 * $100 = $5,000
    portfolio.add_stock(msft_stock, shares=50)  # 50 * $100 = $5,000

    portfolio.add_allocation("META", 0.40)  # 40%
    portfolio.add_allocation("AAPL", 0.30)  # 30%
    portfolio.add_allocation("GOOGL", 0.20)  # 20%
    portfolio.add_allocation("MSFT", 0.10)  # 10%

    # When
    rebalance_result = portfolio.rebalance()

    # Then
    assert rebalance_result.to_sell == [
        Rebalance(action=RebalanceAction.SELL, symbol="GOOGL", amount=1000.0),
        Rebalance(action=RebalanceAction.SELL, symbol="MSFT", amount=3000.0),
    ]

    assert rebalance_result.to_buy == [
        Rebalance(action=RebalanceAction.BUY, symbol="META", amount=3000.0),
        Rebalance(action=RebalanceAction.BUY, symbol="AAPL", amount=1000.0),
    ]
