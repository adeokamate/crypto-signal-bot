from config.settings import (
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT
)


def run_backtest(df):
    starting_balance = 1000
    cash_balance = starting_balance

    position = None
    entry_price = 0
    quantity = 0

    trades = []
    completed_trades = 0
    winning_trades = 0
    losing_trades = 0

    realized_profit = 0
    unrealized_profit = 0

    for i in range(len(df)):
        row = df.iloc[i]

        price = float(row["close"])
        rsi = float(row["rsi"])
        sma_short = float(row["sma_short"])
        sma_long = float(row["sma_long"])
        macd = float(row["macd"])
        macd_signal = float(row["macd_signal"])

        if position == "BUY":
            stop_loss_price = entry_price * (1 - STOP_LOSS_PERCENT / 100)
            take_profit_price = entry_price * (1 + TAKE_PROFIT_PERCENT / 100)

            if price <= stop_loss_price:
                exit_value = quantity * price
                entry_value = quantity * entry_price
                profit = exit_value - entry_value

                cash_balance = exit_value
                realized_profit += profit
                completed_trades += 1
                losing_trades += 1

                trades.append({
                    "type": "STOP LOSS",
                    "price": round(price, 2),
                    "quantity": round(quantity, 6),
                    "profit": round(profit, 2)
                })

                position = None
                entry_price = 0
                quantity = 0

            elif price >= take_profit_price:
                exit_value = quantity * price
                entry_value = quantity * entry_price
                profit = exit_value - entry_value

                cash_balance = exit_value
                realized_profit += profit
                completed_trades += 1
                winning_trades += 1

                trades.append({
                    "type": "TAKE PROFIT",
                    "price": round(price, 2),
                    "quantity": round(quantity, 6),
                    "profit": round(profit, 2)
                })

                position = None
                entry_price = 0
                quantity = 0

        if rsi < 30 and sma_short > sma_long and macd > macd_signal and position is None:
            quantity = cash_balance / price
            entry_price = price
            cash_balance = 0
            position = "BUY"

            trades.append({
                "type": "BUY",
                "price": round(price, 2),
                "quantity": round(quantity, 6)
            })

        elif rsi > 70 and sma_short < sma_long and macd < macd_signal and position == "BUY":
            exit_value = quantity * price
            entry_value = quantity * entry_price
            profit = exit_value - entry_value

            cash_balance = exit_value
            realized_profit += profit
            completed_trades += 1

            if profit > 0:
                winning_trades += 1
            else:
                losing_trades += 1

            trades.append({
                "type": "SELL",
                "price": round(price, 2),
                "quantity": round(quantity, 6),
                "profit": round(profit, 2)
            })

            position = None
            entry_price = 0
            quantity = 0

    if position == "BUY":
        last_price = float(df.iloc[-1]["close"])
        current_value = quantity * last_price
        entry_value = quantity * entry_price
        unrealized_profit = current_value - entry_value
        final_balance = current_value
    else:
        final_balance = cash_balance

    net_profit = final_balance - starting_balance
    profit_percentage = (net_profit / starting_balance) * 100

    if completed_trades > 0:
        win_rate = (winning_trades / completed_trades) * 100
    else:
        win_rate = 0

    return {
        "starting_balance": starting_balance,
        "final_balance": round(final_balance, 2),
        "realized_profit": round(realized_profit, 2),
        "unrealized_profit": round(unrealized_profit, 2),
        "net_profit": round(net_profit, 2),
        "profit_percentage": round(profit_percentage, 2),
        "completed_trades": completed_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(win_rate, 2),
        "open_position": position,
        "open_quantity": round(quantity, 6),
        "trades": trades
    }