from config.settings import SYMBOLS
from paper_trading.engine import PaperTradingEngine


paper_engine = PaperTradingEngine(
    symbols=SYMBOLS,
    starting_balance=1000
)