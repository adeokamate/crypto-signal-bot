function SignalCard({ signal, reason }) {

  let signalColor = "#ffffff";

  if (signal.includes("BUY")) {
    signalColor = "#22c55e";
  }

  if (signal.includes("SELL")) {
    signalColor = "#ef4444";
  }

  return (
    <div className="signal-card">
      <h3>Signal</h3>

      <h2 style={{ color: signalColor }}>
        {signal}
      </h2>

      <p>{reason}</p>
    </div>
  );
}

export default SignalCard;