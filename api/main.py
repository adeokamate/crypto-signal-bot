from fastapi import FastAPI

from config.settings import SYMBOLS, TIMEFRAME, CANDLE_LIMIT
from services.market_data import fetch_candle_data
from strategy.indicators import calculate_rsi, calculate_sma, calculate_macd
from strategy.signals import generate_signal
from backtesting.engine import run_backtest


app = FastAPI(
    title="Crypto Signal Bot API",
    description="API backend for crypto signal analysis, backtesting and trading analytics",
    version="1.0.0"
)


def analyze_symbol(symbol):
    df = fetch_candle_data(
        symbol=symbol,
        timeframe=TIMEFRAME,
        limit=CANDLE_LIMIT
    )

    df = calculate_rsi(df)
    df = calculate_sma(df)
    df = calculate_macd(df)

    price, rsi, sma_short, sma_long, macd, macd_signal, signal, reason = generate_signal(df)

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "rsi": round(rsi, 2),
        "sma_short": round(sma_short, 2),
        "sma_long": round(sma_long, 2),
        "macd": round(macd, 4),
        "macd_signal": round(macd_signal, 4),
        "signal": signal,
        "reason": reason
    }


@app.get("/")
def home():
    return {
        "message": "Crypto Signal Bot API is running"
    }


@app.get("/symbols")
def get_symbols():
    return {
        "symbols": SYMBOLS
    }


@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    symbol = symbol.upper().replace("-", "/")
    return analyze_symbol(symbol)


@app.get("/signals")
def get_all_signals():
    return {
        "signals": [
            analyze_symbol(symbol)
            for symbol in SYMBOLS
        ]
    }


@app.get("/backtest/{symbol}")
def backtest(symbol: str):
    symbol = symbol.upper().replace("-", "/")

    df = fetch_candle_data(
        symbol=symbol,
        timeframe=TIMEFRAME,
        limit=CANDLE_LIMIT
    )

    df = calculate_rsi(df)
    df = calculate_sma(df)
    df = calculate_macd(df)

    results = run_backtest(df)

    return {
        "symbol": symbol,
        "backtest": results
    }