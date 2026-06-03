from fastapi import APIRouter

from config.settings import TIMEFRAME, CANDLE_LIMIT
from services.market_data import fetch_candle_data
from strategy.indicators import calculate_rsi, calculate_sma, calculate_macd
from backtesting.engine import run_backtest
from api.signals import analyze_symbol
from api.state import paper_engine


router = APIRouter()


@router.get("/dashboard/{symbol}")
def get_dashboard(symbol: str):
    symbol = symbol.upper().replace("-", "/")

    signal_data = analyze_symbol(symbol)

    df = fetch_candle_data(
        symbol=symbol,
        timeframe=TIMEFRAME,
        limit=CANDLE_LIMIT
    )

    df = calculate_rsi(df)
    df = calculate_sma(df)
    df = calculate_macd(df)

    backtest_results = run_backtest(df)

    paper_engine.update(
        symbol=symbol,
        price=signal_data["price"],
        signal=signal_data["signal"]
    )

    portfolio_status = paper_engine.get_status(
        symbol=symbol,
        current_price=signal_data["price"]
    )

    portfolio_analytics = paper_engine.get_analytics(
        symbol=symbol,
        current_price=signal_data["price"]
    )

    return {
        "symbol": symbol,
        "signal": signal_data,
        "backtest": backtest_results,
        "portfolio": portfolio_status,
        "analytics": portfolio_analytics
    }