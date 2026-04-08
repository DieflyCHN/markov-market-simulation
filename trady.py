#!/usr/bin/env python

def signal_buy_lowBuild(down_streak):
    """
    Buy rule:
    If `down_streak >= 5`, buy using 50% of current cash.
    This rule will repeatedly trigger during continuous downward trends,
    resulting in progressively smaller position entries (geometric scaling).
    If you dont like it, use `down_streak == 5`.
    """
    return down_streak >= 5

def signal_buy_chasing(up_streak):
    return up_streak >= 5

def signal_sell(account, current_price):
    half_candidate = None

    for i, pos in enumerate(account.positions):
        rate = (current_price - pos["entry_price"]) / pos["entry_price"]
        
        if rate >= 0.1 or rate <= -0.05:
            return "full", i
        elif rate >= 0.05 and half_candidate is None:
            half_candidate = i
        
    if half_candidate is not None:
        return "half", half_candidate
    
    return False, None
    
