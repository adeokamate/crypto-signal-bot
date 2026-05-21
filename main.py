import ccxt
import pandas as pd
import logging
import time
import csv
import os
from utils.charting import plot_chart

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

from strategy.indicators import (
    calculate_rsi,
    calculate_sma
)

from strategy.signals import generate_signal


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
    plot_chart(df, symbol)

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