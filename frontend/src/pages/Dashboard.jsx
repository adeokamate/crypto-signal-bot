import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";
import MetricCard from "../components/MetricCard";
import SignalCard from "../components/SignalCard";
import SymbolSelector from "../components/SymbolSelector";
function Dashboard() {
  const [data, setData] = useState(null);
    const [symbol, setSymbol] = useState("BTC-USDT");
  useEffect(() => {
    loadData();
  }, [symbol]);

  async function loadData() {
    try {
      const result = await getDashboard(symbol);
      console.log(result);
      setData(result);
    } catch (error) {
      console.error(error);
    }
  }

  if (!data) {
    return <h2>Loading...</h2>;
  }

  return (
    <div>
      <h1>Crypto Signal Bot Dashboard</h1>
      
      <h2>{data.symbol}</h2>

      <div className="dashboard-grid">
        <MetricCard title="Price" value={`$${data.signal.price}`} />
        <MetricCard title="RSI" value={data.signal.rsi} />
        <MetricCard title="SMA Short" value={data.signal.sma_short} />
        <MetricCard title="SMA Long" value={data.signal.sma_long} />
        <MetricCard title="MACD" value={data.signal.macd} />
        <MetricCard title="MACD Signal" value={data.signal.macd_signal} />

        <SignalCard
          signal={data.signal.signal}
          reason={data.signal.reason}
        />
      </div>
    </div>
  );
}

export default Dashboard;