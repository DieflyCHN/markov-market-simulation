#!/usr/bin/env python
from config import TRADY_CONFIG
CFG = TRADY_CONFIG

def signal_buy_lowBuild(down_streak):
    return CFG.LOW_BUILD_MAP.get(down_streak, 0)

def signal_buy_chasing(up_streak):
    return CFG.CHASING_MAP.get(up_streak, 0)

def signal_buy_random():
    import random
    if random.uniform(0, 1) > 0.5:
        return 0.5
    else:
        return 0

def signal_buy_belief(belief:dict):
    """
    Convert regime belief directly into desired cash allocation.

    bull -> stronger long bias
    bear -> suppress long exposure
    fluc -> allow small exploratory positions
    """
    # These `magic numbers` are worth discussing and adjusting.
    pct = belief["bull"] * 0.3 + belief["fluc"] * 0.05 - belief["bear"] * 0.3
    return max(0, min(pct, 1))

def signal_buy_belief_route(belief: dict, up_streak, down_streak):
    # This Route strategy results in very sparse final decisions, 
    # making it almost impossible to trigger purchase conditions. 
    state = max(belief, key=belief.get)

    if state == "bull":
        return signal_buy_chasing(up_streak)
    elif state == "bear":
        return signal_buy_lowBuild(down_streak)
    else:
        return signal_buy_random()

def signal_sell(account, current_price):
    orders = []

    for i, pos in enumerate(account.positions):
        rate = (current_price - pos["entry_price"]) / pos["entry_price"]
        shares_to_sell = 0

        # This includes both profit-taking and stop-loss decisions.
        if rate >= (CFG.PROFIT_PCT / 100) or rate <= (CFG.STOP_LOSS_PCT / 100):
            shares_to_sell = pos["shares"]
        elif rate >= (CFG.PARTIAL_PROFIT_PCT / 100):
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