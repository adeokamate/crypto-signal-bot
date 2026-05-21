import ccxt
import pandas as pd
from ta.momentum import RSIIndicator


def fetch_candle_data(symbol="BTC/USDT", timeframe="1h", limit=100):
    exchange = ccxt.binance()

    candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    df = pd.DataFrame(
        candles,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df


def calculate_rsi(df, period=14):
    rsi = RSIIndicator(close=df["close"], window=period)
    df["rsi"] = rsi.rsi()
    return df


def generate_signal(df):
    latest = df.iloc[-1]

    price = latest["close"]
    rsi = latest["rsi"]

    if rsi < 30:
        signal = "BUY"
        reason = "RSI is below 30, market may be oversold"
    elif rsi > 70:
        signal = "SELL"
        reason = "RSI is above 70, market may be overbought"
    else:
        signal = "HOLD"
        reason = "RSI is neutral"

    return price, rsi, signal, reason


def main():
    df = fetch_candle_data()
    df = calculate_rsi(df)

    price, rsi, signal, reason = generate_signal(df)

    print("===== CRYPTO SIGNAL BOT =====")
    print(f"Pair: BTC/USDT")
    print(f"Latest Price: {price}")
    print(f"RSI: {round(rsi, 2)}")
    print(f"Signal: {signal}")
    print(f"Reason: {reason}")


if __name__ == "__main__":
    main()