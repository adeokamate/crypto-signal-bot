import csv
import os
import logging
import pandas as pd


logging.basicConfig(
    filename="logs/signals.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)


def save_signal_to_csv(symbol, price, rsi, sma_short, sma_long, signal, reason):
    os.makedirs("logs", exist_ok=True)

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


def log_signal(symbol, price, rsi, sma_short, sma_long, signal):
    os.makedirs("logs", exist_ok=True)

    logging.info(
        f"{symbol} | Price: {price} | RSI: {round(rsi, 2)} | "
        f"SMA Short: {round(sma_short, 2)} | "
        f"SMA Long: {round(sma_long, 2)} | "
        f"Signal: {signal}"
    )