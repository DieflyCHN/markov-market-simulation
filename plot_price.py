import matplotlib.pyplot as plt

# Standalone utility for quick price-only visualization (not used by main.py)
def draw_history(price_history):
    plt.plot(price_history)
    plt.title("Price Simulation")
    plt.xlabel("Step")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()