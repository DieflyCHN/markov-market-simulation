# All name with PCT (percentage) should without "%"
# Like 90 (90%)
class MAIN_CONFIG:
    MAX_TICKS = 10000

class MARKET_STATE_CONFIG:
    # Markov state space
    # Each type should sum as 1
    # BULL
    BULL_TO_BULL = 0.8
    BULL_TO_BEAR = 0.1
    BULL_TO_FLUC = 0.1
    # BEAR
    BEAR_TO_BULL = 0.1
    BEAR_TO_BEAR = 0.8
    BEAR_TO_FLUC = 0.1
    # FLUCTUATION
    FLUC_TO_BULL = 0.25
    FLUC_TO_BEAR = 0.25
    FLUC_TO_FLUC = 0.5

    # PRICE LIMITS (in Percentage without "%")
    BULL_PCT_LOWER = -1
    BULL_PCT_UPPER = 10
        # Be careful! Negativ should be reversed!
    BEAR_PCT_LOWER = -10
    BEAR_PCT_UPPER = 1
    FLUC_PCT_LOWER = -3
    FLUC_PCT_UPPER = 3

class MARKET_INDEX_CONFIG:
    START_PRICE = 100

class ACCOUNT_CONFIG:
    START_CASH = 10000
    BUY_PCT = 50    #in Percentage without "%"

class TRADY_CONFIG:
    PROFIT_PCT = 10 #in Percentage without "%"
    PARTIAL_PROFIT_PCT = 5
    PARTIAL_SHARES_PCT = 50
    STOP_LOSS_PCT = 5
    
