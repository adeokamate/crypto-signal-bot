const API_BASE_URL = "http://127.0.0.1:8000";

export async function getDashboard(symbol) {
    const response = await fetch(
        `${API_BASE_URL}/dashboard/${symbol}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch dashboard data");
    }

    return await response.json();
}