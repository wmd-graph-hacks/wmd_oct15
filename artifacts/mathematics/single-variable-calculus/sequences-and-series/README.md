---
id: math-single-variable-calculus-sequences-and-series
type: subtopic
title: Sequences and series
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-improper-integrals
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in sequences and series
  - apply a standard method from sequences and series to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Sequences and Series

A sequence (aₙ) converges to L if its terms eventually become arbitrarily close to L. A series Σaₙ is defined through partial sums s_N=Σ_{n=1}^N aₙ; the series converges when s_N has a finite limit. A necessary condition is aₙ→0, but it is not sufficient: the harmonic series Σ1/n diverges.

Use tests matched to the structure. **Geometric series** Σarⁿ converges when |r|<1, with sum a/(1−r) under the usual indexing. **Comparison** applies to nonnegative terms bounded by a known series. **Ratio/root tests** are effective for factorials and exponentials: if lim |aₙ₊₁/aₙ|=L<1, absolute convergence; if L>1, divergence; L=1 is inconclusive. **Alternating series** with decreasing magnitudes tending to zero converges, and the error after N terms is at most the next term.

**Worked example.** Σ(−1)^{n+1}/n converges by the alternating test: 1/n decreases to zero. But it does not converge absolutely, since Σ|(-1)^{n+1}/n|=Σ1/n diverges. Thus it is conditionally convergent. Rearranging terms of a conditionally convergent series can change its sum, so order matters.

For positive decreasing f, the integral test compares Σf(n) and ∫f(x)dx. For p-series Σ1/nᵖ, convergence occurs exactly for p>1. Distinguish absolute convergence, conditional convergence, and divergence. A test that gives no conclusion is not evidence of convergence; choose a different test.

**Practice with answers.** (1) Σ(1/3)ⁿ from n=0 sums to 3/2. (2) Σ1/n² converges (p=2). (3) Σ1/√n diverges (p=1/2). (4) Σn/2ⁿ converges by ratio test (limit 1/2). (5) Σ(−1)ⁿ/√n converges conditionally by alternating test, but not absolutely.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: sequences, infinite sums, and convergence tests

A sequence (aₙ) converges to L if its terms approach L; formally, for each ε>0 all sufficiently large n satisfy |aₙ−L|<ε. A series Σaₙ is the limit of partial sums S_N=Σ_{n=1}^N aₙ. The terms must tend to zero for a series to converge, but this condition alone is not sufficient: the harmonic series Σ1/n diverges.

The geometric series Σ arⁿ converges when |r|<1 and sums to a/(1−r) when it starts at n=0. For positive terms, comparison, limit comparison, integral, ratio, and root tests can establish convergence. For alternating terms with decreasing magnitudes tending to zero, the alternating-series test gives convergence and bounds the error by the first omitted term. Absolute convergence (Σ|aₙ| converges) implies convergence; conditional convergence means the original converges but its absolute-value series does not.

**Worked example.** For Σ n/3ⁿ, use the ratio test: aₙ₊₁/aₙ=[(n+1)/3ⁿ⁺¹]/[n/3ⁿ]=(n+1)/(3n)→1/3<1, so the series converges absolutely. For Σ(−1)ⁿ/n, terms decrease to zero, so it converges; its absolute values form the divergent harmonic series, hence convergence is conditional.

**How to choose a test.** Factorials or powers suggest ratio/root tests. A rational expression in n may invite comparison or limit comparison with 1/nᵖ. Monotone expressions resembling an area may use the integral test. Alternating signs suggest checking both decreasing magnitudes and zero limit. State the test’s hypotheses before applying its conclusion.

**Practice with answers.** (1) Σ(1/2)ⁿ converges to 2 if n begins at 0. (2) Σ1/n² converges by p-series (p=2). (3) Σ1/n diverges (p=1). (4) Σ(−1)ⁿ/√n converges conditionally by the alternating test, since 1/√n decreases to zero while Σ1/√n diverges. (5) If aₙ↛0, Σaₙ diverges by the nth-term test.

**Common pitfalls:** treating aₙ→0 as sufficient; using a test outside its hypotheses; forgetting absolute versus conditional convergence; and applying the alternating test when magnitudes do not decrease.
