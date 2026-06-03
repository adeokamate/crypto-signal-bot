import pandas as pd
import time
from utils.charting import plot_chart
from strategy.indicators import calculate_rsi, calculate_sma, calculate_macd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, macd_signal
from paper_trading.engine import PaperTradingEngine
from config.settings import (
    SYMBOLS,
    TIMEFRAME,
    SCAN_INTERVAL,
    CANDLE_LIMIT,
    RSI_PERIOD,
    RSI_BUY_THRESHOLD,
    RSI_SELL_THRESHOLD,
    SMA_SHORT_WINDOW,
    SMA_LONG_WINDOW,
)

from strategy.indicators import (
    calculate_rsi,
    calculate_sma
)

from strategy.signals import generate_signal
from utils.storage import save_signal_to_csv, log_signal
from services.market_data import fetch_candle_data
from backtesting.engine import run_backtest

from config.settings import (
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT
)
paper_engine = PaperTradingEngine(
    symbols=SYMBOLS,
    starting_balance=1000
)

def main(symbol):
    df = fetch_candle_data(
        symbol=symbol,
        timeframe=TIMEFRAME,
        limit=CANDLE_LIMIT
    )

    df = calculate_rsi(df)
    df = calculate_sma(df)
    df = calculate_macd(df)
    backtest_results = run_backtest(df)

    print("===== BACKTEST RESULTS =====")
    print(f"Pair: {symbol}")
    print(f"Starting Balance: {backtest_results['starting_balance']}")
    print(f"Final Balance: {backtest_results['final_balance']}")
    print(f"Realized Profit: {backtest_results['realized_profit']}")
    print(f"Unrealized Profit: {backtest_results['unrealized_profit']}")
    print(f"Net Profit: {backtest_results['net_profit']}")
    print(f"Profit Percentage: {backtest_results['profit_percentage']}%")
    print(f"Completed Trades: {backtest_results['completed_trades']}")
    print(f"Winning Trades: {backtest_results['winning_trades']}")
    print(f"Losing Trades: {backtest_results['losing_trades']}")
    print(f"Win Rate: {backtest_results['win_rate']}%")
    print(f"Open Position: {backtest_results['open_position']}")
    print(f"Open Quantity: {backtest_results['open_quantity']}")
    print("============================")

    for trade in backtest_results["trades"]:
        print(trade)

    plot_chart(df, symbol)

    price, rsi, sma_short, sma_long,macd, macd_signal, signal, reason = generate_signal(df)

    print("\n===== CRYPTO SIGNAL BOT =====")
    print(f"Pair: {symbol}")
    print(f"Latest Price: {price}")
    print(f"RSI: {round(rsi, 2)}")
    print(f"SMA{SMA_SHORT_WINDOW}: {round(sma_short, 2)}")
    print(f"SMA{SMA_LONG_WINDOW}: {round(sma_long, 2)}")
    print(f"MACD: {round(macd, 4)}")
    print(f"MACD Signal: {round(macd_signal, 4)}")
    print(f"Signal: {signal}")
    print(f"Reason: {reason}")
    print("=============================\n")

    log_signal(
        symbol,
        price,
        rsi,
        sma_short,
        sma_long,
        macd,
        macd_signal,
        signal
    )

    save_signal_to_csv(
        symbol,
        price,
        rsi,
        sma_short,
        sma_long,
        macd,
        macd_signal,
        signal,
        reason
    )
    paper_engine.update(symbol, price, signal)

    paper_status = paper_engine.get_status(
    symbol=symbol,
    current_price=price
)

    print("===== PAPER TRADING STATUS =====")
    print(f"Cash Balance: {paper_status['cash_balance']}")
    print(f"Position: {paper_status['position']}")
    print(f"Entry Price: {paper_status['entry_price']}")
    print(f"Quantity: {paper_status['quantity']}")
    print(f"Unrealized Profit: {paper_status['unrealized_profit']}")
    print(f"Total Value: {paper_status['total_value']}")
    print("================================\n")

if __name__ == "__main__":
    while True:
        for symbol in SYMBOLS:
            main(symbol)

        print(f"\nWaiting {SCAN_INTERVAL} seconds before next check...\n")
        time.sleep(SCAN_INTERVAL)