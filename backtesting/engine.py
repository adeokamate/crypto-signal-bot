def run_backtest(df):

    starting_balance = 1000

    balance = starting_balance

    position = None

    entry_price = 0

    trades = []

    for i in range(len(df)):

        row = df.iloc[i]

        price = row["close"]

        rsi = row["rsi"]

        sma_short = row["sma_short"]

        sma_long = row["sma_long"]

        # BUY
        if (
            rsi < 30
            and sma_short > sma_long
            and position is None
        ):

            position = "BUY"

            entry_price = price

            trades.append({
                "type": "BUY",
                "price": price
            })

        # SELL
        elif (
            rsi > 70
            and sma_short < sma_long
            and position == "BUY"
        ):

            profit = price - entry_price

            balance += profit

            trades.append({
                "type": "SELL",
                "price": price,
                "profit": round(profit, 2)
            })

            position = None

    total_profit = balance - starting_balance

    return {
        "starting_balance": starting_balance,
        "final_balance": round(balance, 2),
        "total_profit": round(total_profit, 2),
        "total_trades": len(trades),
        "trades": trades
    }