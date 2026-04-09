#!/usr/bin/env python
from config import ACCOUNT_CONFIG
CFG = ACCOUNT_CONFIG

class Account:
    def __init__(self):
        self.cash = CFG.START_CASH
        self.positions = []
        # Book value: cash + stock value
        self.book_value = self.cash
        self.book_value_history = [self.book_value]
    
    def update_book_value(self, current_price):
        self.book_value = self.cash
        for pos in self.positions:
            self.book_value += pos["shares"] * current_price
        self.book_value_history.append(self.book_value)
        # print(f"Book value: ${self.book_value:.2f}")

    def buy(self, current_price):
        amount = self.cash * CFG.BUY_PCT / 100
        shares = int(amount / current_price)
        if shares < 1:
            return False
        else:
            self.positions.append({"shares": shares, "entry_price": current_price})
            self.cash -= shares * current_price
            print(f"Buy {shares} share(s) at price ${current_price}.")
            print(f"Cash now: {self.cash:.2f}")
            return True

    def sell(self, current_price, position_num, shares_to_sell):
        if not self.positions:
            return False
        if position_num < 0 or position_num >= len(self.positions):
            return False
        
        this_position = self.positions[position_num]
        self.cash += shares_to_sell * current_price
        
        if shares_to_sell <= this_position["shares"]:
            this_position["shares"] -= shares_to_sell

        print(f"Sold shares: {shares_to_sell} at price ${current_price}")
        
        return shares_to_sell > 0                        
    
    def update_position(self):
        # To prevent the "0" share position from continuing to exist
        self.positions = [pos for pos in self.positions if pos["shares"] > 0]

    def has_position(self):
        return len(self.positions) > 0
