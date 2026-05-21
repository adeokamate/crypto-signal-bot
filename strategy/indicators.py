from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

from config.settings import (
    RSI_PERIOD,
    SMA_SHORT_WINDOW,
    SMA_LONG_WINDOW
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