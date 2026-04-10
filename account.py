#!/usr/bin/env python
from config import ACCOUNT_CONFIG, A_SHARE
CFG = ACCOUNT_CONFIG

class Account:
    def __init__(self):
        self.cash = CFG.START_CASH
        self.positions = []
        # Book value: cash + stock value
        self.book_value = self.cash
        self.book_value_history = [self.book_value]
        self.fees_sum = 0.0
    
    def update_book_value(self, current_price):
        self.book_value = self.cash
        for pos in self.positions:
            self.book_value += pos["shares"] * current_price
        self.book_value_history.append(self.book_value)
        # print(f"Book value: ${self.book_value:.2f}")

    def buy(self, current_price, shares_to_buy):
        if shares_to_buy < 1 or current_price <= 0:
            return False

        amount = shares_to_buy * current_price
        fees = self.trading_fees_Ashare(amount, "buy")

        if amount > self.cash:
            print("You don't have enough cash to buy that many shares!")
            return False
        
        if amount + fees > self.cash:
            print("You don't have enough cash to cover the fees!")
            return False
        
        total_cost = amount + fees
        self.cash -= total_cost
        self.fees_sum += fees
        self.positions.append({"shares": shares_to_buy, "entry_price": current_price})
        print(f"Buy {shares_to_buy} share(s) at price ${current_price:.2f}. Fees: ${fees:.2f}")
        print(f"Cash now: {self.cash:.2f}")
        return True

    def sell(self, current_price, position_num, shares_to_sell):
        if not self.positions:
            return False
        if position_num < 0 or position_num >= len(self.positions):
            return False
        
        this_position = self.positions[position_num]
        if shares_to_sell > this_position["shares"] or shares_to_sell <= 0 or current_price <= 0:
            return False
        
        amount = shares_to_sell * current_price
        fees = self.trading_fees_Ashare(amount, "sell")
        self.cash += amount - fees
        self.fees_sum += fees
        
        this_position["shares"] -= shares_to_sell
        print(f"Sold shares: {shares_to_sell} at price ${current_price}")
        
        return True                        
    
    def update_position(self):
        # To prevent the "0" share position from continuing to exist
        self.positions = [pos for pos in self.positions if pos["shares"] > 0]

    def has_position(self):
        return len(self.positions) > 0
    
    def trading_fees_Ashare(self, amount, usage):
        """
        amount : Amount of buying/selling
        usage : "buy" / "sell"
        """
        a = A_SHARE

        fees = 0.0
        commission = amount * a.BROKERAGE_COMM
        if commission < a.BROKERAGE_COMM_MIN:
            commission = a.BROKERAGE_COMM_MIN

        fees += commission
        fees += amount * a.TRANSFER_FEE

        if usage == "sell":
            fees +=  amount * a.STAMP_DUTY
        elif usage == "buy":
            pass

        return fees

    