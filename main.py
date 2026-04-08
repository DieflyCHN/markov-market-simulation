#!/usr/bin/env python
from market_simulation.market_simulator import MarketIndex
from plot import plot_result
from trady import signal_buy_chasing, signal_buy_lowBuild, signal_sell
from account import Account

mode = input("""Please select your stock market beginning status:
    (U): bUll market
    (R): beaR market
    (F): high Fluctuation market      
    :""").upper()

while mode not in ["U", "R", "F"]:
    mode = input ("INCORRECT mode selection, please select again:").upper()

market_index = MarketIndex(mode)
account = Account()

# Setup simulation ticks (How many cycles?)
while market_index.tick < 10000:
    current_price = market_index.current_price
    
    # if signal_buy_lowBuild(market_index.down_streak):
    if signal_buy_chasing(market_index.up_streak):
        account.buy(current_price)

    strategy, position_num = signal_sell(account, market_index.current_price)
    if strategy is not False:
        account.sell(current_price, position_num, strategy)

    account.update_book_value(market_index.current_price)

    market_index.next_tick()

print(account.book_value)
plot_result(market_index.price_history, account.book_value_history)