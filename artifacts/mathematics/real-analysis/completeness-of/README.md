---
id: math-real-analysis-completeness-of
type: subtopic
title: Completeness of ℝ
parent_topic: math-real-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus
    target_type: topic
    strength: recommended
  - id: math-foundations-of-mathematics
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in completeness of ℝ
  - apply a standard method from completeness of ℝ to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - real-analysis
  - advanced-core
---

# Completeness of the Real Numbers

The completeness property distinguishes ℝ from ℚ: every nonempty subset of ℝ that is bounded above has a least upper bound (supremum). The supremum need not belong to the set. For S={x∈ℚ:x²<2}, viewed as a subset of ℚ it has no rational supremum; in ℝ its supremum is √2. This “no missing limit points” property supports many central theorems of analysis.

A sequence is Cauchy if its terms eventually lie arbitrarily close to one another. Every convergent sequence is Cauchy; completeness says every Cauchy sequence in ℝ converges to a real limit. A nested sequence of nonempty closed bounded intervals whose lengths shrink to zero has exactly one common point. These formulations are equivalent in ℝ and useful in different proofs.

**Example.** Decimal truncations 1, 1.4, 1.41, 1.414,… of √2 form a Cauchy sequence: after enough digits, any two terms differ by at most the remaining tail. Completeness guarantees a real limit. The algebraic argument that √2 is irrational shows why that limit is not in ℚ.

Completeness also underlies the Extreme Value Theorem: a continuous function on a closed bounded interval attains a maximum and minimum. In proofs, identify whether you need boundedness, a supremum, or convergence of a Cauchy sequence; do not use completeness as an unexplained slogan.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: least upper bounds and completeness

The real numbers are complete: every nonempty set of reals that is bounded above has a least upper bound (supremum). A supremum is the smallest upper bound and need not belong to the set; a maximum must belong. This property distinguishes ℝ from ℚ and underlies limit theorems, nested intervals, and convergence of Cauchy sequences.

**Worked example.** Let S={x∈ℝ:x²<2 and x≥0}. The set is nonempty and bounded above by 2, so α=sup S exists. If α²<2, continuity of squaring allows a slightly larger number still in S, contradicting upper-bound status. If α²>2, a slightly smaller number remains an upper bound, contradicting leastness. Therefore α²=2, so α=√2. Completeness guarantees the number exists before the algebra identifies it.

A sequence is Cauchy if its terms eventually lie arbitrarily close to one another. Completeness of ℝ says every Cauchy sequence converges in ℝ. In ℚ, rational decimal approximations to √2 are Cauchy but have no rational limit. Monotone bounded sequences also converge: an increasing bounded sequence tends to its supremum.

**Practice with answers.** (1) A bounded increasing sequence converges. (2) The set (0,1) has supremum 1 but no maximum. (3) The sequence 1−1/n increases to 1. (4) Completeness is a property of the number system, not a claim that every bounded sequence converges.

**Common pitfalls:** confusing supremum with maximum; assuming ℚ has every real limit; and invoking convergence without a completeness or other convergence argument.
