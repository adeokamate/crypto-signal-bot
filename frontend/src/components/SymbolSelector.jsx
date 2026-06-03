function SymbolSelector({ selectedSymbol, onChange }) {
  return (
    <select
      value={selectedSymbol}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="BTC-USDT">BTC-USDT</option>
      <option value="ETH-USDT">ETH-USDT</option>
      <option value="SOL-USDT">SOL-USDT</option>
    </select>
  );
}

export default SymbolSelector;