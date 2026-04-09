import matplotlib.pyplot as plt

def plot_result(price_history, book_value_history):
    fig, ax = plt.subplots()

    ax.plot(price_history, color="red", label="Price")
    ax.plot(book_value_history, color="green", label="Book Value")

    ax.set_xlabel("Tick")
    ax.set_ylabel("Value (log scale)")
    # Dont use linear anymore, log is better when dealing with two "y"
    # Just think about percentage instead of difference
    ax.set_yscale("log")

    ax.grid(True, which="both")
    ax.legend(loc="upper left")

    plt.title("Price vs Account Value (Log Scale)")
    plt.tight_layout()
    plt.show()
