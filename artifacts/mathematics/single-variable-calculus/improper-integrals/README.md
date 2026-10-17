---
id: math-single-variable-calculus-improper-integrals
type: subtopic
title: Improper integrals
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-integration-techniques
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in improper integrals
  - apply a standard method from improper integrals to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Improper Integrals

An integral is improper when an interval is infinite or the integrand becomes unbounded. Define it as a limit of proper integrals; convergence means that limit is finite. Never substitute an infinite endpoint directly into an antiderivative without taking the limit.

**Infinite interval example.** ∫₁∞ x^(−p)dx means lim_{R→∞}∫₁ᴿx^(−p)dx. For p≠1 this is lim [R^(1−p)−1]/(1−p). If p>1, R^(1−p)→0 and the result is 1/(p−1); if p<1, it diverges. For p=1, the integral is lim ln R=∞. Therefore the p-integral converges exactly when p>1.

**Unbounded integrand example.** ∫₀¹ 1/√x dx=lim_{ε→0+}∫ε¹x^(−1/2)dx=lim(2−2√ε)=2. The integrand grows without bound at 0, yet the total area is finite. Compare with ∫₀¹1/x dx=lim(−ln ε)=∞.

Comparison tests help avoid exact integration. For nonnegative functions, if 0≤f≤g and ∫g converges, then ∫f converges; if f≥g and ∫g diverges, then ∫f diverges. For sign-changing functions, absolute convergence (∫|f| finite) guarantees convergence; conditional convergence requires separate tests.

**Practice with answers.** (1) ∫₂∞ x⁻³dx=1/8. (2) ∫₁∞1/x dx diverges. (3) ∫₀¹x^(−2/3)dx=3. (4) Decide ∫₁∞1/(x²+1)dx: it converges by comparison with 1/x² and equals π/4. Split at every singular point and take one-sided limits separately.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: integrals with infinite limits or unbounded integrands

An improper integral is defined as a limit of proper integrals. For an infinite interval, ∫ₐ∞ f(x)dx means lim_{b→∞}∫ₐᵇ f(x)dx. For a vertical asymptote at c, split at c and take the one-sided limits separately. The integral converges only if every required limit exists and is finite. If one side diverges, the whole integral diverges; cancellation in a principal value does not establish ordinary convergence.

**Benchmark p-integrals.** ∫₁∞ x^(−p)dx converges exactly when p>1, and ∫₀¹ x^(−p)dx converges exactly when p<1. The location of the improper endpoint changes the condition. Comparison tests transfer convergence: if 0≤f≤g and ∫g converges, then ∫f converges; if f≥g≥0 and ∫g diverges, then ∫f diverges.

**Worked example.** ∫₁∞ 1/x² dx=lim_{b→∞}[−1/x]₁ᵇ=1, so it converges. By contrast ∫₁∞1/x dx=lim ln b diverges. At zero, ∫₀¹1/√x dx=lim_{a→0+}2(1−√a)=2, which converges despite the integrand becoming unbounded.

**Practice with answers.** (1) ∫₀∞e^(−x)dx=1. (2) ∫₁∞1/√x dx diverges. (3) Does ∫₀²1/(x−1)dx converge as an ordinary improper integral? No; split at 1, and both one-sided pieces diverge. (4) In a comparison, verify nonnegativity and the inequality on the entire tail or neighborhood being compared.

**Common pitfalls:** substituting infinity as if it were a number; failing to split at every singularity; deciding convergence from the antiderivative alone; and assuming an unbounded function must have infinite integral. A small neighborhood can have finite accumulated area even when heights grow without bound.
