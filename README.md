# Markov Regime-Switching Market Simulator

**Version: v0.4.0-alpha**

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

## 2. What is New in v0.4.0-alpha

Compared with earlier rule-only versions, the framework now includes several important structural extensions:

* **Belief layer over hidden market regimes**

  Strategies no longer react only to visible streaks. They now maintain a lightweight belief over latent market states (`bull`, `bear`, `fluc`) and can use this belief for decision-making.

* **Belief-driven position sizing**

  The system supports a continuous exposure-control style:

  ```
  observation -> belief -> position size
  ```

  This is a meaningful step beyond sparse binary triggers such as “buy / not buy”.

* **State-dependent capped return model**

  In addition to uniform and truncated-normal style return generators, the simulator now supports a **capped normal distribution** designed to mimic markets with explicit price-limit rules (e.g. A-share style daily limits).

* **Transaction-cost-aware execution**

  The account layer explicitly includes:

  * brokerage commission
  * transfer fee
  * stamp duty on sell side

* **Clear timing semantics in the main loop**

  The simulation now explicitly adopts an **end-of-period belief update convention**: the trader observes the completed result of the current step, then updates belief for the next step.

---

## 3. Model Overview

The system is organized into three layers:

### 3.1 Environment (Market)

The market is modeled as a **hidden Markov regime process** with three latent states:

* `bull` — positive drift
* `bear` — negative drift
* `fluc` — high volatility, near-zero drift

The hidden state evolves according to a transition matrix:

```
S_t -> S_{t+1}  via P(S_{t+1} | S_t)
```

Given the current hidden state, the next return is sampled from a state-dependent distribution, and price evolves as:

```
P_{t+1} = P_t * (1 + r_t)
```

#### Environment properties

* **Temporal persistence** via first-order Markov memory
* **State-dependent drift / volatility structure**
* No built-in price-level mean reversion
* Synthetic and fully controllable dynamics

#### Supported return-generation modes

The price engine is modular and can support multiple return models:

* **Uniform sampling**

  Easy to understand, but stylized and unrealistic.

* **Truncated normal sampling**

  Controls outliers by rejecting samples outside a bounded interval.

* **Capped normal sampling**

  Samples from a normal distribution first, then clips returns to an upper/lower bound.
  This produces boundary accumulation and better reflects markets with **hard price limits**.

The capped model is currently the main mode used for A-share-like simulations.

---

### 3.2 Strategy Layer (Trady)

Strategies operate on **partially observable information**, not on the hidden regime directly.

Observable inputs include:

* current price
* up/down streaks
* latent belief over hidden regimes

#### Belief Layer

A lightweight belief system approximates the hidden market structure:

```
observation -> belief -> action
```

This is **not** a full Bayesian filter. Instead, it is a heuristic inference layer that:

* shifts confidence toward `bull` after sufficiently strong upward streaks
* shifts confidence toward `bear` after sufficiently strong downward streaks
* preserves some probability mass for `fluc` to reflect consolidation / instability

This makes the framework **POMDP-like** in spirit, even though the inference rule remains deliberately simple.

#### Supported decision styles

##### Rule-based strategies

* Momentum / trend-following
* Mean reversion / low-build after declines
* Sparse route-style rules based on dominant inferred state

##### Belief-driven strategy

Belief can directly determine desired cash exposure:

```
belief -> target buy fraction
```

This allows position sizing to become continuous rather than purely event-triggered.

#### Sell logic

Sell decisions are evaluated at the **position level**, not only at the portfolio level.

Supported rules include:

* take-profit
* stop-loss
* partial profit-taking

Each position is treated independently using its own entry price.

---

### 3.3 Execution Layer (Account)

The account system tracks:

* available cash
* multiple independent positions
* mark-to-market equity
* cumulative transaction fees

Each position stores:

* entry price
* share count

Portfolio equity is evaluated as:

```
Equity = Cash + sum(position_i_value)
```

Execution is **order-driven** and currently assumes immediate fills at the observed market price.

#### Transaction costs

The current A-share-style fee model includes:

* brokerage commission
* minimum commission floor
* transfer fee
* stamp duty on sell side

This makes the simulator more structurally meaningful than a zero-friction toy model, while remaining intentionally simplified.

---

## 4. Simulation Timing Convention

This is one of the most important modeling choices in the project.

Two interpretations are possible when updating belief in a discrete-time trading simulator:

### (A) End-of-period update **(adopted in v0.4)**

Each tick represents a **completed observation window** (for example, one trading day).

The logic is:

1. At the beginning of tick `t`, the trader acts using belief formed from past completed information.
2. The market evolves during tick `t`.
3. Price and streak information for tick `t` become observable.
4. Belief is updated **after** observing the completed result.
5. The updated belief is then used for decisions at tick `t+1`.

Timeline:

```
decision(t) -> market evolves(t) -> observe result -> update belief -> decision(t+1)
```

This corresponds to the intuitive low-frequency interpretation:

> “After seeing today’s completed market move, decide what to do tomorrow.”

This is the convention now adopted in the main loop.

### (B) Online / lagged update

An alternative interpretation is that the current tick is still unfolding while the trader is making decisions. In that case, the newest market move is not yet fully observable, so belief must remain one step behind.

Timeline:

```
decision(t) -> market evolves(t) -> update used only at t+1
```

This interpretation is more natural in high-frequency or streaming settings.

### Why v0.4 adopts (A)

The current framework uses:

* streak-based signals
* latent regime belief
* position-level risk logic
* discrete bar-like market evolution

Taken together, these design choices are much closer to a **completed-period decision model** than to microstructure-level high-frequency execution.

Therefore, the simulator now explicitly adopts **end-of-period belief updating** for conceptual clarity and economic interpretability.

---

## 5. Main Loop Semantics

Under the current convention, each simulation step can be summarized as:

1. Read current observable market information
2. Generate sell decisions
3. Generate buy decisions
4. Execute trades at current price
5. Update account equity
6. Advance the market by one step
7. Update belief from the newly completed market result

Conceptually:

```
current observable info -> trade at P_t -> market moves to P_{t+1} -> learn from new result
```

This ensures that strategies react to **completed market information**, not to hypothetical intra-step knowledge.

---

## 6. Key Observations

### 6.1 Mean Reversion

* Exhibits **negative convexity**
* Accumulates risk during persistent downtrends
* Recovers slowly because losses are multiplicative

### 6.2 Momentum

* Benefits from regime persistence
* Displays **positive convexity**
* Performance is highly sensitive to the transition matrix

### 6.3 Belief-Driven Position Sizing

* Converts latent state inference into **continuous exposure decisions**
* Reduces reliance on sparse event triggers
* Allows smoother adaptation across market regimes

### 6.4 Path Dependence

* Outcomes depend strongly on trajectory
* Identical parameters can produce divergent simulation paths

### 6.5 Irreversibility of Drawdowns

Because wealth evolves multiplicatively:

* −50% requires +100% to recover
* Large drawdowns are structurally difficult to reverse

### 6.6 Stop-Loss as Path-Risk Control

* Stop-loss mainly controls adverse path dependence
* It should not be understood as a free source of alpha
* Its primary function is **tail-risk containment**

---

## 7. Limitations

The framework remains intentionally minimal.

Current limitations include:

* no slippage modeling
* no market impact
* stylized transition probabilities set by hand
* simplified return distributions
* heuristic belief update rather than Bayesian filtering
* single-path analysis by default
* no systematic Monte Carlo distribution study yet
* no empirical calibration yet

The simulator should therefore be understood as a **mechanism-oriented research toy**, not as a production-grade trading engine.

---

## 8. Design Philosophy

The project prioritizes:

* **clarity over realism**
* **mechanisms over data fitting**
* **interpretability over predictive performance**
* **controlled structure over noisy historical complexity**

It is best understood as a **conceptual laboratory** for asking structural questions about strategy behavior.

---

## 9. Future Directions

Planned or natural extensions include:

* Monte Carlo simulation and distribution-level analysis
* empirical parameter calibration
* slippage and market impact modeling
* richer transaction-cost structures
* risk-aware / volatility-aware position sizing
* full Bayesian belief updating
* formal POMDP framing
* extension toward reinforcement learning agents
* comparative experiments across market microstructure assumptions

---

## 10. Authorship Note

All core components were implemented manually within a short prototyping cycle.

These include:

* market regime process
* price simulation logic
* strategy layer
* account / execution engine
* belief-based decision framework

External assistance was limited to:

* plotting utilities (`plot.py`)
* documentation refinement
* code review / structural debugging support

---

## 11. Summary

> **Strategy performance is not intrinsic; it is conditional on the structure of the environment.**

The addition of a belief layer further highlights a second point:

> **Decision quality depends not only on observable signals, but also on how hidden structure is inferred and transformed into action.**

In that sense, this project is less about “predicting markets” and more about understanding how **assumptions about market structure, observability, and action timing** jointly shape simulated trading outcomes.
