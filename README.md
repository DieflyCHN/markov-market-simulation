# Markov Regime-Switching Market Simulator

**Version: v0.3.0-alpha**

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

  where `r_t` is sampled from a state-dependent distribution.

* Key properties:

  * **Temporal persistence** (Markov memory)
  * No intrinsic mean reversion in price level

---

### 2.2 Strategy (Trady)

Strategies now operate on **partially observable information**:

* Price
* Up/down streaks (trend proxy)
* **Latent belief over hidden regimes (bull / bear / fluc)**

#### Belief Layer (new in v0.3)

A lightweight belief system approximates the hidden market state:

```
observation → belief → action
```

* Belief is updated heuristically based on streak dynamics
* Not a full Bayesian filter, but captures **state inference behavior**
* Represents a **POMDP-like extension** of the original framework

#### Decision Modes

The framework now supports two paradigms:

* **Rule-based strategies**

  * Momentum (buy after consecutive rises)
  * Mean reversion (buy after consecutive drops)

* **Belief-driven strategies (new)**

  * Belief directly controls **position sizing**
  * Transitions from binary decisions (“buy / not buy”) to **continuous exposure control**

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

* Execution is **order-driven** and includes:

  * Transaction costs (brokerage, transfer fee, stamp duty)

---

## 3. Simulation Timing Convention

At each step:

1. Observe current state `(P_t, streak_t)`
2. Update belief (latent inference)
3. Generate trading decisions
4. Execute trades at `P_t`
5. Update equity
6. Advance market to `P_{t+1}`

> Strategies react to **completed price information**, not intra-step changes.

---

## 4. Key Observations

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

### 4.3 Belief-Driven Control (new)

* Converts latent state inference into **position sizing decisions**
* Reduces reliance on sparse trigger conditions
* Enables smoother adaptation across regimes

---

### 4.4 Path Dependence

* Outcomes depend strongly on trajectory
* Identical parameters can yield divergent results

---

### 4.5 Irreversibility of Drawdowns

Due to multiplicative dynamics:

* −50% loss requires +100% recovery
* Large drawdowns are structurally difficult to recover

---

### 4.6 Role of Stop-Loss

* Acts as **path-risk control**
* Reduces tail risk rather than increasing expected return

---

## 5. Limitations

* No slippage or market impact
* Simplified return distributions (uniform sampling)
* Manually specified transition probabilities
* Belief update is **heuristic (non-Bayesian)**
* No statistical validation (single-path simulation)

---

## 6. Design Philosophy

The system prioritizes:

* **Clarity over realism**
* **Mechanisms over data-fitting**
* **Interpretability over performance**

It is best viewed as a **conceptual laboratory**, not a trading system.

---

## 7. Future Directions

* Monte Carlo simulation (distribution-level analysis)
* Parameter calibration using empirical data
* Slippage and market impact modeling
* Risk-aware position sizing
* Full Bayesian belief update (true POMDP formulation)
* Extension toward reinforcement learning agents

---

## 8. Authorship Note

All core components (market model, strategy logic, execution engine) were implemented manually within a short prototyping cycle (<24 hours).

External assistance was limited to:

* Plotting utilities (`plot.py`)
* Documentation refinement

---

## 9. Summary

> **Strategy performance is not intrinsic — it is conditional on the structure of the environment.**

The introduction of a belief layer further demonstrates that:

> **Decision quality depends not only on observable signals, but on how hidden structure is inferred and acted upon.**
