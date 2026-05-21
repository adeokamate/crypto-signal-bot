import ccxt
import pandas as pd
import logging
import time
import csv
import os

from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

from config.settings import (
    SYMBOLS,
    TIMEFRAME,
    SCAN_INTERVAL,
    CANDLE_LIMIT,
    RSI_PERIOD,
    RSI_BUY_THRESHOLD,
    RSI_SELL_THRESHOLD,
    SMA_SHORT_WINDOW,
    SMA_LONG_WINDOW,
)


logging.basicConfig(
    filename="logs/signals.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)


def fetch_candle_data(symbol, timeframe, limit):
    exchange = ccxt.binance()

    candles = exchange.fetch_ohlcv(
        symbol,
        timeframe=timeframe,
        limit=limit
    )

    df = pd.DataFrame(
        candles,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def calculate_rsi(df):
    rsi = RSIIndicator(
        close=df["close"],
        window=RSI_PERIOD
    )

    df["rsi"] = rsi.rsi()
    return df


def calculate_sma(df):
    sma_short = SMAIndicator(
        close=df["close"],
        window=SMA_SHORT_WINDOW
    )

    sma_long = SMAIndicator(
        close=df["close"],
        window=SMA_LONG_WINDOW
    )

    df["sma_short"] = sma_short.sma_indicator()
    df["sma_long"] = sma_long.sma_indicator()

    return df


def generate_signal(df):
    latest = df.iloc[-1]

    price = latest["close"]
    rsi = latest["rsi"]
    sma_short = latest["sma_short"]
    sma_long = latest["sma_long"]

    if rsi < RSI_BUY_THRESHOLD and sma_short > sma_long:
        signal = "STRONG BUY"
        reason = "RSI is oversold and short SMA is above long SMA"

    elif rsi > RSI_SELL_THRESHOLD and sma_short < sma_long:
        signal = "STRONG SELL"
        reason = "RSI is overbought and short SMA is below long SMA"

    elif sma_short > sma_long:
        signal = "HOLD"
        reason = "Trend is bullish, but RSI has not reached buy zone"

    elif sma_short < sma_long:
        signal = "HOLD"
        reason = "Trend is bearish, but RSI has not reached sell zone"

    else:
        signal = "HOLD"
        reason = "No clear signal"

    return price, rsi, sma_short, sma_long, signal, reason


def save_signal_to_csv(symbol, price, rsi, sma_short, sma_long, signal, reason):
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
                "sma_short",
                "sma_long",
                "signal",
                "reason"
            ])

        writer.writerow([
            pd.Timestamp.now(),
            symbol,
            price,
            round(rsi, 2),
            round(sma_short, 2),
            round(sma_long, 2),
            signal,
            reason
        ])


def main(symbol):
    df = fetch_candle_data(
        symbol=symbol,
        timeframe=TIMEFRAME,
        limit=CANDLE_LIMIT
    )

    df = calculate_rsi(df)
    df = calculate_sma(df)

    price, rsi, sma_short, sma_long, signal, reason = generate_signal(df)

    print("===== CRYPTO SIGNAL BOT =====")
    print(f"Pair: {symbol}")
    print(f"Latest Price: {price}")
    print(f"RSI: {round(rsi, 2)}")
    print(f"SMA{SMA_SHORT_WINDOW}: {round(sma_short, 2)}")
    print(f"SMA{SMA_LONG_WINDOW}: {round(sma_long, 2)}")
    print(f"Signal: {signal}")
    print(f"Reason: {reason}")
    print("=============================\n")

    logging.info(
        f"{symbol} | Price: {price} | RSI: {round(rsi, 2)} | "
        f"SMA{SMA_SHORT_WINDOW}: {round(sma_short, 2)} | "
        f"SMA{SMA_LONG_WINDOW}: {round(sma_long, 2)} | "
        f"Signal: {signal}"
    )

    save_signal_to_csv(
        symbol,
        price,
        rsi,
        sma_short,
        sma_long,
        signal,
        reason
    )


if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            main(symbol)

        print(f"\nWaiting {SCAN_INTERVAL} seconds before next check...\n")
        time.sleep(SCAN_INTERVAL)