#!/usr/bin/env python
import random

class MarketState:
    """
    Represents the hidden market regime.

    The regime evolves as a Markov chain, introducing temporal structure
    into the environment. This allows the model to capture persistence
    in market conditions (e.g., trends and volatility clustering).
    """
    def __init__(self):
        self.state = "fluc"
        self.transition = {
            "bull":    {"bull": 0.8, "bear": 0.1, "fluc":0.1},
            "bear":    {"bull": 0.1, "bear": 0.8, "fluc":0.1},
            "fluc":    {"bull": 0.3, "bear": 0.3, "fluc":0.4},
        }

    def next_state(self):
        """
        Transition the market to the next state.

        The next state is sampled according to a Markov transition matrix,
        where the probability depends only on the current state.

        This implements a first-order Markov process:
            P(s_{t+1} | s_t)
        """
        prob = self.transition[self.state]
        states = list(prob.keys())
        weights = list(prob.values())
        self.state = random.choices(states, weights = weights, k=1)[0]

    def next_price(self, current_price):
        """
        Generate the next price based on the current market state.

        The price change is stochastic but conditioned on the current regime:
            - bull: positive drift
            - bear: negative drift
            - fluc: high volatility, no clear drift

        Returns:
            new_price: updated price
            state: the state used to generate this price change
        """
        if self.state == "bull":
            pct = random.uniform(0.1, 0.51)
        elif self.state == "bear":
            pct = random.uniform(-0.5, -0.1)
        else:   # Fluctuation
            pct = random.uniform(-0.8, 0.8)
        
        new_price = current_price * (1 + pct / 100)
        #return round (new_price, 2), self.state    # market "hidden" state
        return round (new_price, 2)

# Before learning Markov chain. No Using.
# # Simply Random Mode 
# def simulate_random(current_price):
#     # Just like in the Chinese stock market, the daily price (percentage) limit is 20%.
#     pct = random.uniform(-0.2, 0.2)

#     new_price = current_price * (1 + pct / 100)
#     return round(new_price, 2)

# # Trend Mode 
# def simulate_trend(current_price, last_price):
#     difference = current_price - last_price
#     # The effects or impacts of the `trend` can be adjusted.
#     if difference > 0:
#         trend = random.uniform(-0.03, 0.5)
#     elif difference < 0:
#         trend = random.uniform(-0.5, 0.03)
#     elif difference == 0:
#         trend = 0
#     pct = trend + random.uniform(-0.2, 0.2)
#     new_price = current_price * (1 + pct / 100)
#     return round(new_price, 2)

# # Fluctuation Mode
# def simulate_fluc(current_price):
#     # A random for "strong or weak" fluctuation
#     if random.random() > 0.5:
#         fluc = random.uniform(-0.5, 0.5)
#     else:
#         fluc = random.uniform(-0.1, 0.1)

#     pct = fluc + random.uniform(-0.2, 0.2)
#     new_price = current_price * (1 + pct / 100)
#     return round(new_price, 2)
