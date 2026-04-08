#!/usr/bin/env python
class Account:
    def __init__(self):
        self.cash = 10000
        self.positions = []
        self.book_value = self.cash
        self.book_value_history = [self.book_value]
    
    def update_book_value(self, current_price):
        self.book_value = self.cash
        for pos in self.positions:
            self.book_value += pos["shares"] * current_price
        self.book_value_history.append(self.book_value)
        # print(f"Book value: ${self.book_value:.2f}")

    def buy(self, current_price):
        amount = self.cash * 0.5
        shares = int(amount / current_price)
        if shares < 1:
            return False
        else:
            self.positions.append({"shares": shares, "entry_price": current_price})
            self.cash -= shares * current_price
            print(f"Buy {shares} share(s) at price ${current_price}.")
            print(f"Cash now: {self.cash:.2f}")
            return True

    def sell(self, current_price, position_num, strategy):
        if not self.positions:
            return False
        if position_num < 0 or position_num >= len(self.positions):
            return False
        
        this_position = self.positions[position_num]
        sell_count = 0
        if strategy == "full":
            sell_shares = this_position["shares"]

            self.cash += sell_shares * current_price
            sell_count += sell_shares
            this_position["shares"] = 0

        elif strategy == "half":
            sell_shares = int(this_position["shares"] * 0.5)
            # When only have 1 share, just sell it.
            if sell_shares == 0:
                sell_shares = 1

            self.cash += sell_shares * current_price
            this_position["shares"] -= sell_shares
            sell_count += sell_shares
        else:
            return False
        
        self.positions = [pos for pos in self.positions if pos["shares"] > 0]

        print(f"Sold shares: {sell_count} at price ${current_price}")
        
        return sell_count > 0
    
    def has_position(self):
        len(self.positions) > 0