from fastapi import APIRouter

from api.signals import analyze_symbol
from api.state import paper_engine


router = APIRouter()


@router.get("/portfolio/{symbol}")
def get_portfolio(symbol: str):
    symbol = symbol.upper().replace("-", "/")

    analysis = analyze_symbol(symbol)

    paper_engine.update(
        symbol=symbol,
        price=analysis["price"],
        signal=analysis["signal"]
    )

    status = paper_engine.get_status(
        symbol=symbol,
        current_price=analysis["price"]
    )

    return {
        "symbol": symbol,
        "signal": analysis,
        "portfolio": status
    }