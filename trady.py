#!/usr/bin/env python
from config import TRADY_CONFIG
CFG = TRADY_CONFIG

def signal_buy_lowBuild(down_streak):
    """
    Buy rule:
    If `down_streak >= 5`, buy using 50% of current cash.
    This rule will `repeatedly` trigger during continuous downward trends,
    resulting in progressively smaller position entries (geometric scaling).
    If you dont like it, use `down_streak == 5`.
    """
    return down_streak == 5

def signal_buy_chasing(up_streak):
    return up_streak == 5

def signal_sell(account, current_price):
    orders = []

    for i, pos in enumerate(account.positions):
        rate = (current_price - pos["entry_price"]) / pos["entry_price"]
        shares_to_sell = 0

        if rate >= (CFG.PROFIT_PCT / 100) or rate <= (CFG.STOP_LOSS_PCT / 100):
            shares_to_sell = pos["shares"]
        elif rate >= (CFG.PARTIAL_PROFIT_PCT):
            # Sell a part of all shares
            shares_to_sell = int(pos["shares"] * CFG.PARTIAL_SHARES_PCT / 100)
            # when only have 1 share, it will become 0, so just sell it
            if shares_to_sell == 0:
                shares_to_sell = 1

        # check if it really wants to sell
        if shares_to_sell > 0:
            # Record the position number and shares to be sold
            orders.append({"position_num": i, "shares_to_sell": shares_to_sell})
    
    return orders
