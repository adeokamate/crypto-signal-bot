from paper_trading.portfolio import Portfolio


class PaperTradingEngine:
    def __init__(self, symbols, starting_balance=1000):
        self.portfolios = {
            symbol: Portfolio(
                symbol=symbol,
                starting_balance=starting_balance
            )
            for symbol in symbols
        }

    def update(self, symbol, price, signal):
        portfolio = self.portfolios.get(symbol)

        if portfolio is None:
            return

        portfolio.update(price, signal)

    def get_status(self, symbol, current_price):
        portfolio = self.portfolios.get(symbol)

        if portfolio is None:
            return None

        return portfolio.get_status(current_price)

    def get_all_statuses(self, current_prices):
        statuses = {}

        for symbol, portfolio in self.portfolios.items():
            price = current_prices.get(symbol)

            if price is not None:
                statuses[symbol] = portfolio.get_status(price)

        return statuses
    

    def get_analytics(self, symbol, current_price):
        portfolio = self.portfolios.get(symbol)

        if portfolio is None:
            return None

        return portfolio.get_analytics(current_price)