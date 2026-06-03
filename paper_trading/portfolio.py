from config.settings import (
    BUY_POSITION_PERCENT,
    STRONG_BUY_POSITION_PERCENT
)


class Portfolio:
    def __init__(self, symbol, starting_balance=1000):
        self.symbol = symbol
        self.starting_balance = starting_balance
        self.cash_balance = starting_balance
        self.position = None
        self.entry_price = 0
        self.quantity = 0
        self.trades = []

    def buy(self, price, position_percent):
        if self.position is not None:
            return

        amount_to_invest = self.cash_balance * (position_percent / 100)

        self.quantity = amount_to_invest / price
        self.entry_price = price
        self.cash_balance -= amount_to_invest
        self.position = "BUY"

        self.trades.append({
            "symbol": self.symbol,
            "type": "BUY",
            "price": round(price, 2),
            "quantity": round(self.quantity, 6),
            "amount_invested": round(amount_to_invest, 2)
    })

    def sell(self, price):
        if self.position != "BUY":
            return

        exit_value = self.quantity * price
        entry_value = self.quantity * self.entry_price
        profit = exit_value - entry_value

        self.cash_balance = exit_value

        self.trades.append({
            "symbol": self.symbol,
            "type": "SELL",
            "price": round(price, 2),
            "quantity": round(self.quantity, 6),
            "profit": round(profit, 2)
        })

        self.position = None
        self.entry_price = 0
        self.quantity = 0

    def update(self, price, signal):
        if signal == "STRONG BUY":
            self.buy(price, STRONG_BUY_POSITION_PERCENT)

        elif signal == "BUY":
            self.buy(price, BUY_POSITION_PERCENT)

        elif signal in ["SELL", "STRONG SELL"]:
            self.sell(price)

    def get_status(self, current_price):
        if self.position == "BUY":
            current_value = self.quantity * current_price
            unrealized_profit = current_value - (
                self.quantity * self.entry_price
            )
            total_value = current_value
        else:
            unrealized_profit = 0
            total_value = self.cash_balance

        return {
            "symbol": self.symbol,
            "starting_balance": self.starting_balance,
            "cash_balance": round(self.cash_balance, 2),
            "position": self.position,
            "entry_price": round(self.entry_price, 2),
            "quantity": round(self.quantity, 6),
            "unrealized_profit": round(unrealized_profit, 2),
            "total_value": round(total_value, 2),
            "trades": self.trades
        }