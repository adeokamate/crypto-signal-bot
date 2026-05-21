def run_backtest(df):

    balance = 1000
    position = None
    entry_price = 0

    trades = []

    for i in range(len(df)):

        row = df.iloc[i]

        price = row["close"]

        rsi = row["rsi"]

        sma_short = row["sma_short"]

        sma_long = row["sma_long"]

        # BUY CONDITION
        if (
            rsi < 30
            and sma_short > sma_long
            and position is None
        ):

            position = "BUY"

            entry_price = price

            trades.append(
                f"BUY at {price}"
            )

        # SELL CONDITION
        elif (
            rsi > 70
            and sma_short < sma_long
            and position == "BUY"
        ):

            profit = price - entry_price

            balance += profit

            trades.append(
                f"SELL at {price} | Profit: {round(profit, 2)}"
            )

            position = None

    return balance, trades