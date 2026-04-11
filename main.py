#!/usr/bin/env python
from plot import plot_result

from account import Account
from market_simulation.market_simulator import MarketIndex
from belief import init_belief, update_belief
from trady import signal_buy_belief, signal_sell
from config import MAIN_CONFIG
CFG = MAIN_CONFIG

mode = input("""Please select your stock market beginning status:
    (U): bUll market
    (R): beaR market
    (F): high Fluctuation market      
    :""").strip().upper()

while mode not in ["U", "R", "F"]:
    mode = input ("INCORRECT mode selection, please select again:").upper()

market_index = MarketIndex(mode)    # obserable Index (for trader)
account = Account()
belief = init_belief()

while market_index.tick < CFG.MAX_TICKS:
    current_price = market_index.current_price
  
    # Selling Strategy
    orders = signal_sell(account, current_price)
    for order in sorted(orders, key=lambda x: x["position_num"], reverse=True):
        account.sell(current_price, order["position_num"], order["shares_to_sell"])

    # Buying Strategy
    # Future: `signal_buy_xxx` will determine how many shares to buy; currently in a transitional state.
    cash_to_buy_pct = signal_buy_belief(belief)
    if cash_to_buy_pct > 0:
        amount_to_buy = account.cash * cash_to_buy_pct
        shares_to_buy = int(amount_to_buy / current_price)
        if shares_to_buy != 0:
            account.buy(current_price, shares_to_buy)

    # Update account informations
    account.update_position()
    account.update_book_value(current_price)

    # === Temporal semantics of belief update ===
    #
    # There are two valid interpretations of when belief should be updated:
    #
    # (A) End-of-period update (current implementation)
    #     - Each tick represents a completed observation window (e.g., one trading day).
    #     - The trader makes decisions at the beginning of tick t using belief from t-1.
    #     - The market then evolves during tick t (price update + streak update).
    #     - After observing the outcome of tick t, belief is updated,
    #       and will be used for decisions at tick t+1.
    #
    #     Timeline:
    #         decision(t) -> market evolves(t) -> observe -> update belief -> decision(t+1)
    #
    #     This matches typical low-frequency trading intuition:
    #     "After seeing today's close, decide what to do tomorrow."
    #
    # (B) Online / lagged update
    #     - The trader can only use fully completed past information.
    #     - Current tick outcome is not yet observable when making decisions.
    #     - Belief is therefore always one tick behind the latest market move.
    #
    #     Timeline:
    #         decision(t) -> update belief(t-1 info) -> market evolves(t)
    #
    #     This resembles high-frequency / streaming settings where
    #     the current period is still unfolding and not fully known.
    #
    # We adopt (A) here for clearer economic interpretation and consistency
    # with streak-based signals and regime learning.
    market_index.next_tick()
    belief = update_belief(belief, market_index.up_streak, market_index.down_streak)

print(account.book_value)
plot_result(market_index.price_history, account.book_value_history)
