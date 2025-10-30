"""Beautiful console output for portfolio management."""

from portfolio import Portfolio
from schemas import RebalanceResult, RebalanceAction


# ANSI Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DIM = '\033[2m'

    # Background colors
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'


def print_header(text: str):
    """Print a styled header."""
    width = 70
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * width}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END} {Colors.BOLD}{text.center(width-4)}{Colors.END} {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * width}{Colors.END}\n")


def print_section(title: str):
    """Print a section title."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}▸ {title}{Colors.END}")
    print(f"{Colors.DIM}{'─' * 68}{Colors.END}")


def log_portfolio(portfolio: Portfolio):
    """Display portfolio information in a beautiful format."""

    # Header
    print_header("🏦 FINTUAL - Portfolio Rebalance Strategy")

    # Current holdings section
    print_section("📊 Current Holdings")

    total_value = 0

    # Table header
    print(f"{Colors.BOLD}{'Symbol':<8} {'Name':<25} {'Price':>10} {'Shares':>8} {'Value':>12}{Colors.END}")
    print(f"{Colors.DIM}{'─' * 68}{Colors.END}")

    # Table rows
    for symbol, stock in portfolio.stocks.items():
        shares = portfolio.holdings[symbol]
        value = shares * stock.price
        total_value += value

        print(f"{Colors.CYAN}{symbol:<8}{Colors.END} "
              f"{stock.name:<25} "
              f"{Colors.YELLOW}${stock.price:>9.2f}{Colors.END} "
              f"{Colors.GREEN}{shares:>8}{Colors.END} "
              f"{Colors.BOLD}${value:>11.2f}{Colors.END}")

    # Total
    print(f"{Colors.DIM}{'─' * 68}{Colors.END}")
    print(f"{Colors.BOLD}{'TOTAL PORTFOLIO VALUE':>54} ${total_value:>11.2f}{Colors.END}")

    # Target allocations section
    print_section("🎯 Target Allocations")

    print(f"{Colors.BOLD}{'Symbol':<8} {'Target %':>12} {'Target Value':>15} {'Current %':>12} {'Difference':>14}{Colors.END}")
    print(f"{Colors.DIM}{'─' * 68}{Colors.END}")

    for symbol in portfolio.stocks.keys():
        if symbol in portfolio.allocations:
            target_pct = portfolio.allocations[symbol] * 100
            target_value = total_value * portfolio.allocations[symbol]
            current_value = portfolio.holdings[symbol] * portfolio.stocks[symbol].price
            current_pct = (current_value / total_value * 100) if total_value > 0 else 0
            diff = current_pct - target_pct

            # Color code the difference
            if abs(diff) < 0.1:
                diff_color = Colors.GREEN
                diff_symbol = "✓"
            elif diff > 0:
                diff_color = Colors.YELLOW
                diff_symbol = "▲"
            else:
                diff_color = Colors.RED
                diff_symbol = "▼"

            print(f"{Colors.CYAN}{symbol:<8}{Colors.END} "
                  f"{Colors.BLUE}{target_pct:>11.1f}%{Colors.END} "
                  f"${target_value:>14.2f} "
                  f"{current_pct:>11.1f}% "
                  f"{diff_color}{diff_symbol} {abs(diff):>6.1f}%{Colors.END}")


def log_rebalance_result(rebalance_result: RebalanceResult):
    """Display rebalance actions in a beautiful format."""

    print_section("⚖️  Rebalance Actions")

    has_actions = len(rebalance_result.to_buy) > 0 or len(rebalance_result.to_sell) > 0

    if not has_actions:
        print(f"\n{Colors.GREEN}{Colors.BOLD}  ✓ Portfolio is already balanced!{Colors.END}\n")
        return

    # Sell actions
    if rebalance_result.to_sell:
        print(f"\n{Colors.RED}{Colors.BOLD}  📉 SELL{Colors.END}")
        print(f"{Colors.DIM}  {'─' * 40}{Colors.END}")

        for action in rebalance_result.to_sell:
            print(f"  {Colors.RED}▼{Colors.END} "
                  f"{Colors.CYAN}{action.symbol:<6}{Colors.END} "
                  f"{Colors.RED}${action.amount:>10.2f}{Colors.END}")

    # Buy actions
    if rebalance_result.to_buy:
        print(f"\n{Colors.GREEN}{Colors.BOLD}  📈 BUY{Colors.END}")
        print(f"{Colors.DIM}  {'─' * 40}{Colors.END}")

        for action in rebalance_result.to_buy:
            print(f"  {Colors.GREEN}▲{Colors.END} "
                  f"{Colors.CYAN}{action.symbol:<6}{Colors.END} "
                  f"{Colors.GREEN}${action.amount:>10.2f}{Colors.END}")

    # Summary
    total_to_sell = sum(a.amount for a in rebalance_result.to_sell)
    total_to_buy = sum(a.amount for a in rebalance_result.to_buy)

    print(f"\n{Colors.DIM}  {'─' * 40}{Colors.END}")
    print(f"  {Colors.BOLD}Total to sell: {Colors.RED}${total_to_sell:>10.2f}{Colors.END}")
    print(f"  {Colors.BOLD}Total to buy:  {Colors.GREEN}${total_to_buy:>10.2f}{Colors.END}")

    # Final separator
    print(f"\n{Colors.CYAN}{'═' * 70}{Colors.END}\n")


def print_success(message: str):
    """Print a success message."""
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ {message}{Colors.END}\n")


def print_error(message: str):
    """Print an error message."""
    print(f"\n{Colors.RED}{Colors.BOLD}✗ {message}{Colors.END}\n")


def print_warning(message: str):
    """Print a warning message."""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ {message}{Colors.END}\n")
