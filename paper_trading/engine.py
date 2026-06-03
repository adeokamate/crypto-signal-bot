class PaperTradingEngine:
    def __init__(self, starting_balance=1000):
        self.starting_balance = starting_balance
        self.cash_balance = starting_balance
        self.position = None
        self.entry_price = 0
        self.quantity = 0
        self.trades = []

    def buy(self, symbol, price):
        if self.position is not None:
            return

        self.quantity = self.cash_balance / price
        self.entry_price = price
        self.cash_balance = 0
        self.position = "BUY"

        self.trades.append({
            "symbol": symbol,
            "type": "BUY",
            "price": round(price, 2),
            "quantity": round(self.quantity, 6)
        })

    def sell(self, symbol, price):
        if self.position != "BUY":
            return

        exit_value = self.quantity * price
        entry_value = self.quantity * self.entry_price
        profit = exit_value - entry_value

        self.cash_balance = exit_value
        self.position = None

        self.trades.append({
            "symbol": symbol,
            "type": "SELL",
            "price": round(price, 2),
            "quantity": round(self.quantity, 6),
            "profit": round(profit, 2)
        })

        self.entry_price = 0
        self.quantity = 0

    def update(self, symbol, price, signal):
        if signal == "STRONG BUY":
            self.buy(symbol, price)

        elif signal == "STRONG SELL":
            self.sell(symbol, price)

    def get_status(self, current_price=None):
        if self.position == "BUY" and current_price is not None:
            current_value = self.quantity * current_price
            unrealized_profit = current_value - (
                self.quantity * self.entry_price
            )
            total_value = current_value
        else:
            unrealized_profit = 0
            total_value = self.cash_balance

        return {
            "starting_balance": self.starting_balance,
            "cash_balance": round(self.cash_balance, 2),
            "position": self.position,
            "entry_price": round(self.entry_price, 2),
            "quantity": round(self.quantity, 6),
            "unrealized_profit": round(unrealized_profit, 2),
            "total_value": round(total_value, 2),
            "trades": self.trades
        }