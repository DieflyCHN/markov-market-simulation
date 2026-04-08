import matplotlib.pyplot as plt

def plot_result(price_history, book_value_history):
    fig, ax1 = plt.subplots()

    # --- Original Point ---
    base_price = price_history[0]
    base_value = book_value_history[0]
    scale = base_value / base_price  # ≈ 100

    # --- Left: Price ---
    ax1.plot(price_history, color="red", label="Price")
    ax1.set_xlabel("Tick")
    ax1.set_ylabel("Price", color="red")
    ax1.tick_params(axis='y', labelcolor="red")
    ax1.grid(True)

    # --- Right: Account ---
    def price_to_value(y):
        return y * scale

    def value_to_price(y):
        return y / scale

    ax2 = ax1.secondary_yaxis('right', functions=(price_to_value, value_to_price))
    ax2.set_ylabel("Book Value", color="green")

    scaled_value = [v / scale for v in book_value_history]
    ax1.plot(scaled_value, color="green", label="Book Value")

    ax1.legend(loc="upper left")

    plt.title("Price vs Account Value (Aligned Scale)")
    plt.tight_layout()
    plt.show()