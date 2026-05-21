import ccxt
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import logging
import time
import csv
import os

logging.basicConfig(
    filename="logs/signals.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

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

def calculate_sma(df):

    sma20 = SMAIndicator(close=df["close"], window=20)
    sma50 = SMAIndicator(close=df["close"], window=50)

    df["sma20"] = sma20.sma_indicator()
    df["sma50"] = sma50.sma_indicator()

    return df


def generate_signal(df):
    latest = df.iloc[-1]

    price = latest["close"]
    rsi = latest["rsi"]
    sma20 = latest["sma20"]
    sma50 = latest["sma50"]

    if rsi < 30 and sma20 > sma50:
        signal = "STRONG BUY"
        reason = "RSI is oversold and SMA20 is above SMA50, showing bullish trend confirmation"

    elif rsi > 70 and sma20 < sma50:
        signal = "STRONG SELL"
        reason = "RSI is overbought and SMA20 is below SMA50, showing bearish trend confirmation"

    elif sma20 > sma50:
        signal = "HOLD"
        reason = "Trend is bullish, but RSI has not reached a strong buy zone"

    elif sma20 < sma50:
        signal = "HOLD"
        reason = "Trend is bearish, but RSI has not reached a strong sell zone"

    else:
        signal = "HOLD"
        reason = "No clear signal"

    return price, rsi, sma20, sma50, signal, reason

def save_signal_to_csv(symbol, price, rsi, sma20, sma50, signal, reason):
    file_path = "logs/signals.csv"

    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "symbol",
                "price",
                "rsi",
                "sma20",
                "sma50",
                "signal",
                "reason"
            ])

        writer.writerow([
            pd.Timestamp.now(),
            symbol,
            price,
            round(rsi, 2),
            round(sma20, 2),
            round(sma50, 2),
            signal,
            reason
        ])


def main(symbol="BTC/USDT"):
    df = fetch_candle_data(symbol=symbol)
    df = calculate_rsi(df)
    df = calculate_sma(df)

    price, rsi, sma20, sma50, signal, reason = generate_signal(df)

    print("===== CRYPTO SIGNAL BOT =====")
    print(f"Pair: {symbol}")
    print(f"Latest Price: {price}")
    print(f"RSI: {round(rsi, 2)}")
    print(f"SMA20: {round(sma20, 2)}")
    print(f"SMA50: {round(sma50, 2)}")
    print(f"Signal: {signal}")
    print(f"Reason: {reason}")
    print("=============================\n")
    

    logging.info(
    f"{symbol} | Price: {price} | RSI: {round(rsi,2)} | "
    f"SMA20: {round(sma20,2)} | SMA50: {round(sma50,2)} | "
    f"Signal: {signal}"
)
    save_signal_to_csv(symbol, price, rsi, sma20, sma50, signal, reason)

if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            main(symbol=symbol)
        print("\nWaiting 60 seconds before next check...\n")
        time.sleep(60)