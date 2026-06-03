from fastapi import APIRouter

from config.settings import SYMBOLS, TIMEFRAME, CANDLE_LIMIT
from services.market_data import fetch_candle_data
from strategy.indicators import calculate_rsi, calculate_sma, calculate_macd
from strategy.signals import generate_signal


router = APIRouter()


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


@router.get("/symbols")
def get_symbols():
    return {"symbols": SYMBOLS}


@router.get("/signal/{symbol}")
def get_signal(symbol: str):
    symbol = symbol.upper().replace("-", "/")
    return analyze_symbol(symbol)


@router.get("/signals")
def get_all_signals():
    return {
        "signals": [
            analyze_symbol(symbol)
            for symbol in SYMBOLS
        ]
    }