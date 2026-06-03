from fastapi import APIRouter

from config.settings import TIMEFRAME, CANDLE_LIMIT
from services.market_data import fetch_candle_data
from strategy.indicators import calculate_rsi, calculate_sma, calculate_macd
from backtesting.engine import run_backtest


router = APIRouter()


@router.get("/backtest/{symbol}")
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

    return {
        "symbol": symbol,
        "backtest": run_backtest(df)
    }