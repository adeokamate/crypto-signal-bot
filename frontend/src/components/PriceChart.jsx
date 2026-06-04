import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

function PriceChart({ data }) {
  if (!data || data.length === 0) {
    return <p>No chart data available</p>;
  }

  return (
    <div className="chart-card">
      <h3>Price Chart</h3>

      <LineChart width={1000} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" hide />
        <YAxis domain={["auto", "auto"]} />
        <Tooltip />

        <Line
          type="monotone"
          dataKey="close"
          stroke="#22c55e"
          strokeWidth={2}
          dot={false}
        />

        <Line
          type="monotone"
          dataKey="sma_short"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={false}
        />

        <Line
          type="monotone"
          dataKey="sma_long"
          stroke="#f97316"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </div>
  );
}

export default PriceChart;