#!/usr/bin/env python
import random
from config import MARKET_STATE_CONFIG
CFG = MARKET_STATE_CONFIG

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
            "bull":    {"bull": CFG.BULL_TO_BULL, "bear": CFG.BULL_TO_BEAR, "fluc":CFG.BULL_TO_FLUC},
            "bear":    {"bull": CFG.BEAR_TO_BULL, "bear": CFG.BEAR_TO_BEAR, "fluc":CFG.BEAR_TO_FLUC},
            "fluc":    {"bull": CFG.FLUC_TO_BULL, "bear": CFG.FLUC_TO_BEAR, "fluc":CFG.FLUC_TO_FLUC},
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
        """
        if self.state == "bull":
            pct = random.uniform(CFG.BULL_PCT_LOWER, CFG.BULL_PCT_UPPER) / 100
        elif self.state == "bear":
            pct = random.uniform(CFG.BEAR_PCT_LOWER, CFG.BEAR_PCT_UPPER) / 100
        else:   # Fluctuation
            pct = random.uniform(CFG.FLUC_PCT_LOWER, CFG.FLUC_PCT_UPPER) / 100
        
        new_price = current_price * (1 + pct)

        if round (new_price, 2) == 0:
            return 0.01
        else:
            return round (new_price, 2)