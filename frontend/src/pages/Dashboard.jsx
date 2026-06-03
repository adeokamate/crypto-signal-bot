import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";

function Dashboard() {
    const [data, setData] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    async function loadData() {
        try {
            const result = await getDashboard("BTC-USDT");
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

            <p>Price: {data.signal.price}</p>

            <p>Signal: {data.signal.signal}</p>

            <p>RSI: {data.signal.rsi}</p>

            <p>MACD: {data.signal.macd}</p>
        </div>
    );
}

export default Dashboard;