#!/usr/bin/env python
from plot import plot_result
from market_simulation.market_simulator import MarketIndex
from trady import signal_buy_chasing, signal_buy_lowBuild, signal_sell, signal_buy_random
from account import Account
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

while market_index.tick < CFG.MAX_TICKS:
    current_price = market_index.current_price
  
    # Selling Strategy
    orders = signal_sell(account, current_price)
    for order in sorted(orders, key=lambda x: x["position_num"], reverse=True):
        account.sell(current_price, order["position_num"], order["shares_to_sell"])

    # Buying Strategy
    # Future: `signal_buy_xxx` will determine how many shares to buy; currently in a transitional state.
    cash_to_buy_pct = signal_buy_lowBuild(market_index.down_streak)
    if cash_to_buy_pct > 0:
        amount_to_buy = account.cash * cash_to_buy_pct
        shares_to_buy = int(amount_to_buy / current_price)
        if shares_to_buy != 0:
            account.buy(current_price, shares_to_buy)

    # Update account informations
    account.update_position()
    account.update_book_value(current_price)

    market_index.next_tick()

print(account.book_value)
plot_result(market_index.price_history, account.book_value_history)
