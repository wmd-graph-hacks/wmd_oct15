---
id: math-real-analysis-riemann-stieltjes-and-lebesgue-integration
type: subtopic
title: Riemann–Stieltjes and Lebesgue integration
parent_topic: math-real-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-real-analysis-rigorous-continuity-and-differentiation
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in riemann–stieltjes and lebesgue integration
  - apply a standard method from riemann–stieltjes and lebesgue integration to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - real-analysis
  - advanced-core
---

# Riemann–Stieltjes and Lebesgue Integration

The Riemann–Stieltjes integral ∫f dα generalizes ∫f dx by weighting interval increments α(xᵢ)−α(xᵢ₋₁). If α is differentiable, it often equals ∫f(x)α′(x)dx. If α is a step function with a jump at c, the integral captures a weighted value f(c) at that jump. This connects integration to distributions of mass and expectation.

Lebesgue integration organizes contributions by the values a function takes and measures the sizes of their level sets, rather than partitioning only the domain into intervals. It can integrate functions with many discontinuities and supports powerful limit theorems. Constructing it rigorously requires measurable sets and measures; here the key intuition is that “area” can be accumulated over irregular sets.

**Example.** A random variable X with discrete outcomes xᵢ and probabilities pᵢ has expectation E[X]=Σxᵢpᵢ, which is an integral with respect to its probability measure. For a continuous density, E[X]=∫x f(x)dx. Both are the same measure-theoretic idea.

The Monotone Convergence Theorem allows increasing nonnegative functions to pass through a limit inside an integral. Dominated Convergence allows pointwise limits when an integrable bound controls all functions. These hypotheses matter: pointwise convergence alone does not permit exchanging limit and integral.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: weighted accumulation and measure-based integration

The Riemann–Stieltjes integral ∫f dα weights values of f by increments of an increasing function α. When α(x)=x it is the ordinary Riemann integral; when α is a step function, it can encode weighted sums or point masses. The definition uses sums f(ξᵢ)[α(xᵢ)−α(xᵢ₋₁)]. It is useful in probability and integration by parts.

Lebesgue integration measures the size of sets on which a function takes values, then accumulates value across those sets. This handles limits of functions more flexibly than partitioning the domain. A measurable nonnegative function has integral defined by approximation from below with simple functions; signed functions require integrability of absolute value for a finite integral. Monotone and dominated convergence theorems justify exchanging limits and integrals under their conditions.

**Worked example.** If X is a discrete random variable taking values xᵢ with probabilities pᵢ, its expectation is Σxᵢpᵢ. This is a Lebesgue integral with respect to the probability measure: E[X]=∫X dP. The measure assigns mass pᵢ to each outcome/value, so the integral becomes a weighted sum.

**Practice with answers.** (1) For a step α with jump 2 at c, the Stieltjes integral contributes 2f(c), under the usual continuity convention. (2) Dominated convergence requires an integrable dominating function. (3) Pointwise convergence alone does not generally permit taking limits through integrals. (4) The Lebesgue integral agrees with the Riemann integral for bounded Riemann-integrable functions.

**Common pitfalls:** swapping limits and integrals without a theorem; confusing measure with length in every setting; and forgetting absolute integrability for signed functions.
