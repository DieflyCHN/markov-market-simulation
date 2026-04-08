"""
This module simulates a stochastic stock market environment with regime switching.

The market is modeled as a Markov process over hidden states:
    - bull (upward bias)
    - bear (downward bias)
    - fluctuation (high volatility)

At each time step:
    1. The current market state determines the price movement.
    2. After the price is updated, the market transitions to the next state
       according to a Markov transition matrix.

This design ensures that:
    - price dynamics are state-dependent
    - market regimes exhibit temporal persistence ("memory")
"""

#!/usr/bin/env python
from market_simulation.market_state import MarketState

# # --- Simulation loop ---
# # At each step:
# #   - The current market state generates a price change
# #   - Then the state transitions to the next regime (Markov update)
# step = 1
# prices = []
# while step <= 100000:
#     # Price update driven by current state
#     price, state = market.next_price(price)
#     prices.append(price)
#     print(f"Step {step:2d} | State: {state:9s} | Price: ${price:.2f}")

#     # Transition to next state (Markov chain)
#     market.next_state()

#     # binput("Press Enter for next tick...")
#     step += 1

class MarketIndex:
    def __init__(self, mode):
        self.market = MarketState()
        self.mode = mode
        self.current_price = 100.00
        self.previous_price = None
        self.down_streak = 0
        self.up_streak = 0
        self.tick = 0
        self.price_history = [self.current_price]
        
        # market "hidden" state
        if self.mode == "U":
            self.market.state = "bull"
        elif self.mode == "R":
            self.market.state = "bear"
        elif self.mode == "F":
            self.market.state = "fluc"
        # market "observable" state
        # self.state = self.market.state

        print("=== Market has memory (Markov chain) ===")

    def next_tick(self):
        # Remember previous_price
        self.previous_price = self.current_price
        # Update current_price
        self.current_price = self.market.next_price(self.current_price)
        self.price_history.append(self.current_price)

        # Update streak
        if self.current_price > self.previous_price:
            self.up_streak += 1
            self.down_streak = 0
        elif self.current_price < self.previous_price:
            self.down_streak += 1
            self.up_streak = 0
        else:   # No price change
            self.up_streak = 0
            self.down_streak = 0

        # Output    
        # print(f"Tick {self.tick:3d} | State: {self.state:5s} | Price: ${self.current_price:.2f}")
        print(f"Tick {self.tick:3d} | Price: ${self.current_price:.2f}")
        
        # Transition to next state (Markov chain)
        self.market.next_state()
        self.tick += 1
