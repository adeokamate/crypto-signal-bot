from config.settings import (
    RSI_BUY_THRESHOLD,
    RSI_SELL_THRESHOLD
)


def generate_signal(df):

    buy_score = 0
    sell_score = 0

    latest = df.iloc[-1]

    price = latest["close"]

    rsi = latest["rsi"]

    sma_short = latest["sma_short"]

    sma_long = latest["sma_long"]

    macd = latest["macd"]
    macd_signal = latest["macd_signal"]

   # RSI
    if rsi < RSI_BUY_THRESHOLD:
        buy_score += 1

    if rsi > RSI_SELL_THRESHOLD:
        sell_score += 1

    # SMA
    if sma_short > sma_long:
        buy_score += 1

    if sma_short < sma_long:
        sell_score += 1

    # MACD
    if macd > macd_signal:
        buy_score += 1

    if macd < macd_signal:
        sell_score += 1

    if buy_score == 3:
        signal = "STRONG BUY"
        reason = "All indicators confirm bullish setup"

    elif buy_score == 2:
        signal = "BUY"
        reason = "Majority of indicators are bullish"

    elif sell_score == 3:
        signal = "STRONG SELL"
        reason = "All indicators confirm bearish setup"

    elif sell_score == 2:
        signal = "SELL"
        reason = "Majority of indicators are bearish"

    else:
        signal = "HOLD"
        reason = "No strong market consensus"
    return (
        price,
        rsi,
        sma_short,
        sma_long,
        macd,
        macd_signal,
        signal,
        reason
    )