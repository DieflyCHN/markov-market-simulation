#!/usr/bin/env python
import random
from config import MARKET_STATE_CONFIG, A_SHARE
CFG = MARKET_STATE_CONFIG
ASHARE_CFG = A_SHARE
import math_tools as mymath

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
        Keep the original interface;
        you can now change the price simulation method here
        by modifying the `return` statement.
        """
        return self.next_price_capped_normal(current_price)

    def next_price_uniform(self, current_price):
        """   
        This function will draw samples with equal probability within
        a given interval, resulting in poor realism, but it is easier
        to understand.

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

        # Magic if/else, No meaning!
        if round (new_price, 2) == 0:
            return 0.01
        else:
            return round (new_price, 2)
    
    def _get_state_dist_params(self, config):
        if self.state == "bull":
            return {
                "mu": config.BULL_MU,
                "sigma": config.BULL_SIGMA,
                "lower": config.BULL_LOWER,
                "upper": config.BULL_UPPER
            }
        elif self.state == "bear":
            return {
                "mu": config.BEAR_MU,
                "sigma": config.BEAR_SIGMA,
                "lower": config.BEAR_LOWER,
                "upper": config.BEAR_UPPER
            }
        elif self.state == "fluc":
            return {
                "mu": config.FLUC_MU,
                "sigma": config.FLUC_SIGMA,
                "lower": config.FLUC_LOWER,
                "upper": config.FLUC_UPPER
            }
        else:
            raise ValueError(f"Unknown market state: {self.state}")

    def next_price_normal(self, current_price):
        params = self._get_state_dist_params(CFG)
        pct = mymath.sample_normal(params["mu"], params["sigma"])
        new_price = current_price * (1 + pct)
        return round(new_price, 2)

    def next_price_truncated_normal(self, current_price):
        """
        Uses a truncated normal distribution to generate returns.

        Compared to a standard normal distribution:
        - prevents extreme outliers
        - keeps returns within a controlled range

        More realistic than uniform sampling.
        """
        params = self._get_state_dist_params(CFG)
        pct = mymath.sample_truncated_normal(
            params["mu"], params["sigma"],
            params["lower"], params["upper"])
        new_price = current_price * (1 + pct)
        return round(new_price, 2)

    def next_price_capped_normal(self, current_price):
        """
        Suitable for simulating markets with price limit systems,
        such as the A-share market.
        """
        params = self._get_state_dist_params(ASHARE_CFG)
        pct = mymath.sample_capped_normal(
            params["mu"], params["sigma"],
            params["lower"], params["upper"])
        new_price = current_price * (1 + pct)
        return round(new_price, 2)
        