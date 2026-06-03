def calculate_portfolio_analytics(portfolio_status):
    trades = portfolio_status["trades"]

    closed_trades = [
        trade for trade in trades
        if "profit" in trade
    ]

    total_trades = len(closed_trades)

    winning_trades = [
        trade for trade in closed_trades
        if trade["profit"] > 0
    ]

    losing_trades = [
        trade for trade in closed_trades
        if trade["profit"] <= 0
    ]

    total_profit = sum(
        trade["profit"] for trade in closed_trades
    )

    if total_trades > 0:
        win_rate = (len(winning_trades) / total_trades) * 100
        best_trade = max(trade["profit"] for trade in closed_trades)
        worst_trade = min(trade["profit"] for trade in closed_trades)
        average_profit = total_profit / total_trades
    else:
        win_rate = 0
        best_trade = 0
        worst_trade = 0
        average_profit = 0

    starting_balance = portfolio_status["starting_balance"]
    total_value = portfolio_status["total_value"]

    net_profit = total_value - starting_balance
    return_percentage = (net_profit / starting_balance) * 100

    return {
        "total_trades": total_trades,
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "win_rate": round(win_rate, 2),
        "total_profit": round(total_profit, 2),
        "best_trade": round(best_trade, 2),
        "worst_trade": round(worst_trade, 2),
        "average_profit": round(average_profit, 2),
        "net_profit": round(net_profit, 2),
        "return_percentage": round(return_percentage, 2)
    }