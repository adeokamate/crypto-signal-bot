function SignalCard({ signal, reason }) {
  return (
    <div className="signal-card">
      <h3>Signal</h3>
      <h2>{signal}</h2>
      <p>{reason}</p>
    </div>
  );
}

export default SignalCard;