---
id: math-single-variable-calculus-power-and-taylor-series
type: subtopic
title: Power and Taylor series
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-sequences-and-series
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in power and taylor series
  - apply a standard method from power and taylor series to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Power and Taylor Series

A power series centered at a is Σcₙ(x−a)ⁿ. It converges for |x−a|<R, diverges for |x−a|>R, and each endpoint must be tested separately. The radius R can be found by the ratio or root test. Inside the radius, power series can be differentiated and integrated term by term; the radius remains the same, though endpoint behavior may change.

The Taylor series of f at a is Σ f⁽ⁿ⁾(a)(x−a)ⁿ/n!. It represents f only where the series converges to the function. Familiar expansions include 1/(1−x)=Σxⁿ for |x|<1, eˣ=Σxⁿ/n! for all x, and sin x=Σ(−1)ⁿx^(2n+1)/(2n+1)! for all x. Substitution and algebra can create expansions, but the interval of validity must be carried along.

**Worked example.** Find the series for 1/(1+x²). Use the geometric series with u=−x²: 1/(1−u)=Σuⁿ, so 1/(1+x²)=1−x²+x⁴−x⁶+… for |x|<1. At x=1, the resulting 1−1+1−1+… does not converge, while the original function is defined. At x=−1 it also diverges. Therefore interval is (−1,1), despite the function being defined at both endpoints.

Taylor polynomials approximate locally. Taylor’s theorem gives a remainder bound; for the alternating sine series, the error is no larger than the first omitted term. Do not assume a Taylor series equals a function merely because derivatives match formally; establish or cite a theorem that controls the remainder.

**Practice with answers.** (1) Radius for Σxⁿ/3ⁿ is 3; test endpoints: x=3 gives Σ1 diverges, x=−3 gives alternating ±1, also diverges. (2) First four nonzero terms of eˣ: 1+x+x²/2+x³/6. (3) Integrate geometric series to obtain −ln(1−x)=Σxⁿ/n for |x|<1; endpoint tests give convergence at x=−1 and divergence at x=1.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: power series and local polynomial models

A power series centered at a is Σcₙ(x−a)ⁿ. The ratio or root test usually finds a radius R: it converges absolutely for |x−a|<R and diverges for |x−a|>R. Test the two endpoints separately; behavior at one endpoint does not determine the other. Inside the interval of convergence, power series can be differentiated and integrated term by term, with the same radius of convergence.

The Taylor polynomial of degree n for f at a is Tₙ(x)=Σ_{k=0}ⁿ f⁽ᵏ⁾(a)(x−a)ᵏ/k!. It matches the function’s first n derivatives at a and can approximate nearby values. Familiar series include eˣ=Σxⁿ/n!, sin x=Σ(−1)ⁿx^(2n+1)/(2n+1)!, and 1/(1−x)=Σxⁿ for |x|<1. A series representation is an equality only within its convergence interval.

**Worked example.** Approximate e^0.1 using degree 2: 1+0.1+(0.1)²/2=1.105. Since all omitted terms are positive, this is an underestimate. The next term is 0.1³/6≈0.000167; the remaining tail is small, so the approximation is about 1.10517. The approximation point is close to the center 0, where the series converges.

Taylor’s theorem supplies a remainder bound when derivative information is known. For an alternating series with decreasing terms, the first omitted term bounds the error. Always distinguish the polynomial (finite approximation) from the infinite series and specify its center, degree, and interval of validity.

**Practice with answers.** (1) The first three nonzero terms of sin x are x−x³/6+x⁵/120. (2) The geometric series for 1/(1+x) is Σ(−1)ⁿxⁿ for |x|<1. (3) The Taylor polynomial of degree 2 for cos x at 0 is 1−x²/2. (4) For Σxⁿ/n!, the ratio test gives convergence for every real x.

**Common pitfalls:** forgetting to test endpoints; using a Taylor series far outside its convergence region; mixing Maclaurin (a=0) with a general Taylor center; and quoting an approximation without an error discussion when accuracy matters.
