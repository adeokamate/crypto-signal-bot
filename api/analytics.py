from fastapi import APIRouter

from api.signals import analyze_symbol
from api.state import paper_engine


router = APIRouter()


@router.get("/analytics/{symbol}")
def get_analytics(symbol: str):
    symbol = symbol.upper().replace("-", "/")

    analysis = analyze_symbol(symbol)

    paper_engine.update(
        symbol=symbol,
        price=analysis["price"],
        signal=analysis["signal"]
    )

    analytics = paper_engine.get_analytics(
        symbol=symbol,
        current_price=analysis["price"]
    )

    return {
        "symbol": symbol,
        "signal": analysis,
        "analytics": analytics
    }