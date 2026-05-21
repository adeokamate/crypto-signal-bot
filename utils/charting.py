import matplotlib.pyplot as plt


def plot_chart(df, symbol):

    plt.figure(figsize=(12, 6))

    plt.plot(
        df["timestamp"],
        df["close"],
        label="Close Price"
    )

    plt.plot(
        df["timestamp"],
        df["sma_short"],
        label="SMA Short"
    )

    plt.plot(
        df["timestamp"],
        df["sma_long"],
        label="SMA Long"
    )

    plt.title(f"{symbol} Price Chart")

    plt.xlabel("Time")
    plt.ylabel("Price")

    plt.legend()

    plt.grid(True)

    file_name = symbol.replace("/", "_")

    plt.savefig(f"charts/{file_name}.png")

    plt.close()