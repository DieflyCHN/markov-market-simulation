# All name with PCT (percentage) should without "%"
# Like 90 (90%)
class MAIN_CONFIG:
    MAX_TICKS = 10000

class MARKET_STATE_CONFIG:
    # Markov state space

    # Uniform:
    # Each type should sum as 1
    # BULL
    BULL_TO_BULL = 0.6
    BULL_TO_BEAR = 0.2
    BULL_TO_FLUC = 0.2
    # BEAR
    BEAR_TO_BULL = 0.2
    BEAR_TO_BEAR = 0.6
    BEAR_TO_FLUC = 0.2
    # FLUCTUATION
    FLUC_TO_BULL = 0.3
    FLUC_TO_BEAR = 0.3
    FLUC_TO_FLUC = 0.4

    # PRICE LIMITS (in Percentage without "%")
    BULL_PCT_LOWER = -1
    BULL_PCT_UPPER = 10
        # Be careful! Negativ should be reversed!
    BEAR_PCT_LOWER = -10
    BEAR_PCT_UPPER = 1
    FLUC_PCT_LOWER = -1
    FLUC_PCT_UPPER = 1

    # (Truncated) normol distribution
    # MU / SIGMA / LOWER / UPPER use decimal return units, e.g. 0.10 means 10%.
    BULL_MU = 0.003
    BULL_SIGMA = 0.015
    BULL_LOWER = -0.03
    BULL_UPPER = 0.1

    BEAR_MU = -0.003
    BEAR_SIGMA = 0.015
    BEAR_LOWER = -0.1
    BEAR_UPPER = 0.03

    FLUC_MU = 0.0
    FLUC_SIGMA = 0.03
    FLUC_LOWER = -0.03
    FLUC_UPPER = 0.03

class MARKET_INDEX_CONFIG:
    START_PRICE = 100

class ACCOUNT_CONFIG:
    START_CASH = 10000

class TRADY_CONFIG:
    PROFIT_PCT = 10 #in Percentage without "%"
    PARTIAL_PROFIT_PCT = 5
    PARTIAL_SHARES_PCT = 50
    STOP_LOSS_PCT = -5  #Stop loss line should be negative!

    LOW_BUILD_MAP = {   # down_streak: cash_to_buy_(pct)
        5: 80 / 100,
        6: 30 / 100,
        7: 0.1/ 100
    }

    CHASING_MAP = {     # dup_streak: cash_to_buy_(pct)
        5: 0.8 / 100,
        6: 0.3 / 100,
        7: 0.1 / 100
    }

class A_SHARE:
    # Stamp duty 印花税, 5 per 10k, Price is fixed nationwide and `non-negotiable`.
    STAMP_DUTY = 5 / 10000
    # Brokerage commissions 券商佣金, usually 2.5 per 10k, min 5, `Editable`
    BROKERAGE_COMM = 2.5 / 10000
    BROKERAGE_COMM_MIN = 5
    # Transfer fee 过户费, 0.1 per 10k
    TRANSFER_FEE = 0.1 / 10000
    # Trading fee 规费, 0.0541 per 10k, already calc in Brokerage comm., no more usage
    # TRADING_FEE = 0.0541 / 10000

    # NOTE:
    # Distribution parameters are duplicated intentionally.
    # MARKET_STATE_CONFIG is for generic normal/truncated simulation.
    # A_SHARE is reserved for capped A-share-specific simulation.
    # Capped distribution function
    # MU / SIGMA / LOWER / UPPER use decimal return units, e.g. 0.10 means 10%.
    BULL_MU = 0.003
    BULL_SIGMA = 0.015
    BULL_LOWER = -0.03
    BULL_UPPER = 0.1

    BEAR_MU = -0.003
    BEAR_SIGMA = 0.015
    BEAR_LOWER = -0.1
    BEAR_UPPER = 0.03

    FLUC_MU = 0.0
    FLUC_SIGMA = 0.03
    FLUC_LOWER = -0.03
    FLUC_UPPER = 0.03

class BELIEF:
    # Belief_start sum = 1
    BULL_BELIEF_START = 1/3
    BEAR_BELIEF_START = 1/3
    FLUC_BELIEF_START = 1/3

    UP_STREAK_CONDITION = 5
    UP_BULL_CHANGE_PCT = 15
    UP_BEAR_CHANGE_PCT = -10
    UP_FLUC_CHANGE_PCT = 5

    DOWN_STREAK_CONDITION = 5
    DOWN_BULL_CHANGE_PCT = -10
    DOWN_BEAR_CHANGE_PCT = 15
    DOWN_FLUC_CHANGE_PCT = 5