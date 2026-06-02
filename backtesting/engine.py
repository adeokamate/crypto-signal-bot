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

    for i in range(len(df)):
        row = df.iloc[i]

        price = float(row["close"])
        rsi = float(row["rsi"])
        sma_short = float(row["sma_short"])
        sma_long = float(row["sma_long"])

        # BUY using full available cash balance
        if rsi < 30 and sma_short > sma_long and position is None:
            quantity = cash_balance / price
            entry_price = price
            cash_balance = 0
            position = "BUY"

            trades.append({
                "type": "BUY",
                "price": round(price, 2),
                "quantity": round(quantity, 6)
            })

        # SELL current holding
        elif rsi > 70 and sma_short < sma_long and position == "BUY":
            exit_value = quantity * price
            entry_value = quantity * entry_price
            profit = exit_value - entry_value

            cash_balance = exit_value
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

    # If still holding, estimate current portfolio value
    if position == "BUY":
        last_price = float(df.iloc[-1]["close"])
        holding_value = quantity * last_price
        final_balance = holding_value
    else:
        final_balance = cash_balance

    total_profit = final_balance - starting_balance
    profit_percentage = (total_profit / starting_balance) * 100

    if completed_trades > 0:
        win_rate = (winning_trades / completed_trades) * 100
    else:
        win_rate = 0

    return {
        "starting_balance": starting_balance,
        "final_balance": round(final_balance, 2),
        "total_profit": round(total_profit, 2),
        "profit_percentage": round(profit_percentage, 2),
        "completed_trades": completed_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(win_rate, 2),
        "open_position": position,
        "open_quantity": round(quantity, 6),
        "trades": trades
    }