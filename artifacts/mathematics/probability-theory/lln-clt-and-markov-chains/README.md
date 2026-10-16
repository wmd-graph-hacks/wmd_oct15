---
id: math-probability-theory-lln-clt-and-markov-chains
type: subtopic
title: LLN, CLT, and Markov chains
parent_topic: math-probability-theory
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-probability-theory-named-distributions-and-moment-generating-functions
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in lln, clt, and markov chains
  - apply a standard method from lln, clt, and markov chains to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - probability-theory
  - core-to-advanced
---

# Limit Theorems and Markov Chains

The Law of Large Numbers says averages of repeated observations approach the population mean under suitable independence and moment assumptions. It explains why sample averages stabilize; it does not say every finite sample is close. The Central Limit Theorem says that, after centering and scaling, sums or sample means approach a normal distribution under broad conditions. It supports approximate probabilities and confidence procedures, but the approximation may be poor for small samples or heavy-tailed data.

For iid observations with mean μ and variance σ², the sample mean has mean μ and standard error σ/√n. A CLT approximation uses (X̄−μ)/(σ/√n)≈N(0,1). Increasing n reduces standard error at a square-root rate: quadrupling sample size halves it.

A discrete-time Markov chain has states and transition matrix P, where Pᵢⱼ=P(Xₙ₊₁=j|Xₙ=i), with each row summing to one. The Markov property says the next state depends on the current state, not the full past. A stationary distribution π satisfies πP=π and sums to one. Long-run convergence needs conditions such as irreducibility and aperiodicity in a finite chain.

**Example.** A two-state weather chain has transition matrix [[0.8,0.2],[0.4,0.6]]. Solve π=πP with π₁+π₂=1: 0.2π₁=0.4π₂, giving π=(2/3,1/3). This is the stationary proportion, provided the chain’s long-run conditions hold.

**Practice.** If σ=12 and n=36, standard error is 2. For a chain, check rows sum to one before interpreting transition probabilities.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: long-run averages and state transitions

The Law of Large Numbers says sample averages approach the population mean under suitable independence and moment conditions. It explains why repeated measurements stabilize; it does not say each outcome becomes predictable. The Central Limit Theorem says a suitably standardized sum or sample mean is approximately normal for large samples under common regularity conditions. The approximation improves with sample size but may be poor for heavy tails or strong dependence.

A discrete-time Markov chain has states and transition probabilities; the next state depends on the current state, not the full past. A transition matrix P has nonnegative entries and each row sums to 1 (row-vector convention). State probabilities evolve by multiplying by P. A stationary distribution π satisfies πP=π; it describes a stable long-run distribution when the chain’s structure allows convergence.

**Worked example.** A two-state weather model has transition matrix [[.8,.2],[.4,.6]] for sunny/rainy. If today is sunny, tomorrow’s probabilities are (.8,.2). Two days later they are (.8,.2)P=(.72,.28). Solving πP=π with probabilities summing to 1 gives stationary distribution (2/3,1/3).

**Practice with answers.** (1) LLN concerns convergence of averages; CLT describes their scaled distribution. (2) A transition matrix row must total 1. (3) In the example, rainy today gives tomorrow (.4,.6). (4) A chain with absorbing states may not have a unique stationary distribution.

**Common pitfalls:** claiming the CLT makes raw data normal; confusing convergence of averages with convergence of individual trials; and multiplying a transition matrix using the wrong row/column convention.
