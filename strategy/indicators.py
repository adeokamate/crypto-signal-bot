from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from ta.trend import SMAIndicator, MACD

from config.settings import (
    RSI_PERIOD,
    SMA_SHORT_WINDOW,
    SMA_LONG_WINDOW,
    MACD_FAST_WINDOW,
    MACD_SLOW_WINDOW,
    MACD_SIGNAL_WINDOW
)


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

def calculate_macd(df):
    macd = MACD(
        close=df["close"],
        window_fast=MACD_FAST_WINDOW,
        window_slow=MACD_SLOW_WINDOW,
        window_sign=MACD_SIGNAL_WINDOW
    )

    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_histogram"] = macd.macd_diff()

    return df