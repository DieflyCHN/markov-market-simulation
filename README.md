# Markov Regime-Switching Market Simulator

A minimal simulation framework for studying how trading strategies interact with stochastic market structures under controlled assumptions.

---

## 1. Objective

This project investigates a central question:

> **How does strategy performance depend on the structural properties of the market?**

Rather than relying on historical data, the system constructs a **synthetic, fully controllable environment**, enabling:

* Explicit manipulation of market regimes
* Isolation of structural effects (trend persistence, volatility, path dependence)
* Mechanistic understanding of strategy behavior

The emphasis is on **model transparency and causal interpretation**, not predictive accuracy.

---

## 2. Model Overview

The system is organized into three layers:

### 2.1 Environment (Market)

* Hidden **Markov regime process** with three states:

  * `bull` — positive drift
  * `bear` — negative drift
  * `fluc` — high volatility, near-zero drift

* State evolution:

  ```
  S_t → S_{t+1}  via transition matrix P(S_{t+1} | S_t)
  ```

* Price dynamics:

  ```
  P_{t+1} = P_t · (1 + r_t)
  ```

  where ( r_t ) is sampled from a state-dependent distribution.

* Key property:

  * **Temporal persistence** (via Markov transitions)
  * No intrinsic mean reversion in price level

---

### 2.2 Strategy (Trady)

Rule-based decision functions operating on **observable variables only**:

* Price
* Up/down streaks (trend proxy)

Supported archetypes:

* **Momentum**: buy after consecutive increases
* **Mean reversion**: buy after consecutive decreases

Sell logic (position-level):

* Take-profit
* Stop-loss
* Partial profit-taking

---

### 2.3 Execution (Account)

* Tracks:

  * Cash
  * Multiple independent positions
  * Mark-to-market equity

* Each position maintains:

  * Entry price
  * Share count

* Portfolio valuation:

  ```
  Equity = Cash + Σ(position_i_value)
  ```

* Execution is **order-driven**, decoupled from signal generation.

---

## 3. Simulation Timing Convention

At each step:

1. Observe current state ((P_t, \text{streak}_t))
2. Generate trading decisions
3. Execute trades at (P_t)
4. Update equity
5. Advance market to (P_{t+1})

This implies:

> Strategies react to **completed price information**, not intra-step changes.

---

## 4. Key Observations

Empirical behaviors observed under typical configurations:

### 4.1 Mean Reversion

* Exhibits **negative convexity**
* Accumulates risk during persistent downtrends
* Recovers slowly due to multiplicative losses

---

### 4.2 Momentum

* Benefits from regime persistence
* Displays **positive convexity**
* Performance highly sensitive to transition matrix

---

### 4.3 Path Dependence

* Outcomes strongly depend on trajectory, not just distribution
* Identical parameters can yield divergent equity curves

---

### 4.4 Irreversibility of Drawdowns

Due to multiplicative dynamics:

* A −50% loss requires +100% recovery
* Large drawdowns are structurally difficult to recover from

---

### 4.5 Role of Stop-Loss

* Functions as **path-risk control**
* Reduces tail risk rather than increasing expected return

---

## 5. Limitations

This is a deliberately simplified model:

* No transaction costs or slippage
* Uniform return distributions (no heavy tails)
* Manually specified transition probabilities
* No statistical validation (single-path runs)
* No liquidity or market impact modeling

---

## 6. Design Philosophy

The system prioritizes:

* **Clarity over realism**
* **Mechanisms over data-fitting**
* **Interpretability over performance**

It is best viewed as a **conceptual laboratory**, not a trading tool.

---

## 7. Future Directions

* Monte Carlo simulation (distribution-level analysis)
* Parameter calibration using empirical data
* Transaction cost and slippage modeling
* Risk-aware position sizing
* Extension to POMDP / reinforcement learning agents

---

## 8. Authorship Note

All core components (market model, strategy logic, execution engine) were implemented manually within a short prototyping cycle (<24 hours).

External assistance was limited to:

* Plotting utilities (`plot.py`)
* Documentation refinement

---

## 9. Summary

This project demonstrates that:

> **Strategy performance is not intrinsic — it is conditional on the structure of the environment.**

Understanding that interaction is more valuable than optimizing any single strategy in isolation.
