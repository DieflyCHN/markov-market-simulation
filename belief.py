#!/usr/bin/env python
from config import BELIEF
CFG = BELIEF

def init_belief():
    return {"bull": CFG.BULL_BELIEF_START, "bear": CFG.BEAR_BELIEF_START, "fluc": CFG.FLUC_BELIEF_START}

def normalize_belief(belief):
    total = sum(belief.values())
    if total <= 0:
        return init_belief()
    return {k: v / total for k, v in belief.items()}

def update_belief(belief: dict, up_streak, down_streak):
    # Heuristic belief update:
    # When a strong trend is detected (up/down streak),
    # we increase confidence in the corresponding regime (bull/bear),
    # while also slightly increasing "fluc" to reflect potential
    # consolidation or volatility around extreme price levels.
    #
    # This models scenarios like:
    # - high-level consolidation after a strong rally
    # - bottom formation after a prolonged decline
    new_belief = belief.copy()
    if up_streak >= CFG.UP_STREAK_CONDITION:
        new_belief["bull"] += CFG.UP_BULL_CHANGE_PCT / 100
        new_belief["bear"] -= CFG.UP_BEAR_CHANGE_PCT / 100
        new_belief["fluc"] += CFG.UP_FLUC_CHANGE_PCT / 100
    elif down_streak >= CFG.DOWN_STREAK_CONDITION:
        new_belief["bull"] -= CFG.DOWN_BULL_CHANGE_PCT / 100
        new_belief["bear"] += CFG.DOWN_BEAR_CHANGE_PCT / 100
        new_belief["fluc"] += CFG.DOWN_FLUC_CHANGE_PCT / 100

    for k in new_belief:
        new_belief[k] = max(0.0, new_belief[k])
    return normalize_belief(new_belief)