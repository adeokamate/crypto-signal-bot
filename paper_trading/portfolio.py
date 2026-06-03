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
    

    def get_analytics(self, current_price):
            status = self.get_status(current_price)

            completed_trades = [
                trade for trade in self.trades
                if trade["type"] == "SELL"
            ]

            profits = [
                trade.get("profit", 0)
                for trade in completed_trades
            ]

            winning_trades = [
                profit for profit in profits
                if profit > 0
            ]

            losing_trades = [
                profit for profit in profits
                if profit <= 0
            ]

            total_trades = len(completed_trades)
            total_profit = sum(profits)
            net_profit = status["total_value"] - self.starting_balance

            if total_trades > 0:
                win_rate = (len(winning_trades) / total_trades) * 100
                average_profit = total_profit / total_trades
            else:
                win_rate = 0
                average_profit = 0

            best_trade = max(profits) if profits else 0
            worst_trade = min(profits) if profits else 0

            return {
                "symbol": self.symbol,
                "total_trades": total_trades,
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate": round(win_rate, 2),
                "total_profit": round(total_profit, 2),
                "best_trade": round(best_trade, 2),
                "worst_trade": round(worst_trade, 2),
                "average_profit": round(average_profit, 2),
                "net_profit": round(net_profit, 2),
                "return_percentage": round(
                    (net_profit / self.starting_balance) * 100,
                    2
                )
            }