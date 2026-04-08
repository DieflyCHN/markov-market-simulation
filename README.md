# Markov Market Simulation

A lightweight simulation framework to explore how different trading strategies behave under regime-switching stochastic environments.

## Motivation

This project was developed as a rapid prototype (<24 hours) to explore a core question:

**How does the effectiveness of a trading strategy depend on the underlying market structure?**

Instead of focusing on real-world data, the goal is to construct a controllable environment where:

- Market regimes (bull / bear / fluctuation) are explicitly modeled
- Strategies can be tested under different structural assumptions
- Emergent behaviors (e.g., drawdown, convexity, path dependence) can be observed

The emphasis is on **understanding mechanisms**, not building a production trading system.

## Core Idea

The system consists of three layers:

1. **Environment (Market)**
   - Regime-switching process (Markov chain)
   - Each regime produces different price dynamics

2. **Strategy (Trady)**
   - Rule-based decision functions (e.g., mean reversion, momentum)
   - Operates only on observable variables

3. **Execution (Account)**
   - Position-level management
   - Cash, holdings, and mark-to-market valuation

## Features

- Markovian regime-switching market model
- Position-level portfolio tracking
- Support for multiple strategies:
  - Mean-reversion (buy after consecutive drops)
  - Momentum (buy after consecutive rises)
- Visualization of:
  - Price dynamics
  - Account equity curve
- Experiments on:
  - Strategy robustness
  - Path dependence
  - Risk asymmetry

## Example Findings

- Mean-reversion strategies exhibit **negative convexity**:
  - Risk increases during downturns
  - Gains are truncated during recoveries

- Momentum strategies outperform in persistent regimes:
  - Positive convexity
  - Better alignment with regime persistence

- Severe drawdowns are often **irrecoverable** due to multiplicative dynamics

- Stop-loss mechanisms act as **path-risk control**, not profit enhancers

## Limitations

- No transaction costs or slippage
- Simplified return distributions (uniform sampling)
- Manually specified transition probabilities (not data-driven)
- No statistical validation (single-path simulation)

This project is intended as a **conceptual exploration tool**, not a realistic market model.

## Future Work

- Introduce transaction costs and market impact
- Calibrate model parameters using real data
- Monte Carlo simulations for statistical robustness
- Risk-aware position sizing
- Extension toward POMDP / RL-based agents

This project prioritizes **clarity of mechanisms over realism**, aiming to build intuition about how strategies interact with stochastic environments.

## Note on Code Authorship

All core components of this project (market model, strategy logic, and account system) were implemented manually within a short prototyping timeframe (<24 hours).

External assistance was only used for minor utilities such as plotting (`plot.py`) and this `README`.  
The focus of this project is on **model construction and conceptual clarity**, rather than code generation.
