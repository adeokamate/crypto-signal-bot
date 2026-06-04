function AnalyticsCard({ analytics }) {
  return (
    <div className="analytics-card">
      <h3>Portfolio Analytics</h3>

      <p>Total Trades: {analytics.total_trades}</p>
      <p>Winning Trades: {analytics.winning_trades}</p>
      <p>Losing Trades: {analytics.losing_trades}</p>
      <p>Win Rate: {analytics.win_rate}%</p>
      <p>Net Profit: ${analytics.net_profit}</p>
      <p>Return: {analytics.return_percentage}%</p>
      <p>Best Trade: ${analytics.best_trade}</p>
      <p>Worst Trade: ${analytics.worst_trade}</p>
    </div>
  );
}

export default AnalyticsCard;