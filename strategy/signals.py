from config.settings import (
    RSI_BUY_THRESHOLD,
    RSI_SELL_THRESHOLD
)


def generate_signal(df):

    latest = df.iloc[-1]

    price = latest["close"]

    rsi = latest["rsi"]

    sma_short = latest["sma_short"]

    sma_long = latest["sma_long"]

    if rsi < RSI_BUY_THRESHOLD and sma_short > sma_long:

        signal = "STRONG BUY"

        reason = (
            "RSI is oversold and short SMA is above long SMA"
        )

    elif rsi > RSI_SELL_THRESHOLD and sma_short < sma_long:

        signal = "STRONG SELL"

        reason = (
            "RSI is overbought and short SMA is below long SMA"
        )

    elif sma_short > sma_long:

        signal = "HOLD"

        reason = (
            "Trend is bullish, but RSI has not reached buy zone"
        )

    elif sma_short < sma_long:

        signal = "HOLD"

        reason = (
            "Trend is bearish, but RSI has not reached sell zone"
        )

    else:

        signal = "HOLD"

        reason = "No clear signal"

    return (
        price,
        rsi,
        sma_short,
        sma_long,
        signal,
        reason
    )