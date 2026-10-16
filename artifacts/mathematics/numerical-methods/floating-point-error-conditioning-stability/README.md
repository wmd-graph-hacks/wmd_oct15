---
id: math-numerical-methods-floating-point-error-conditioning-stability
type: subtopic
title: Floating-point error, conditioning, stability
parent_topic: math-numerical-methods
phase: applied-core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-sequences-and-series
    target_type: subtopic
    strength: recommended
  - id: math-linear-algebra-vector-spaces-subspaces-basis
    target_type: subtopic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in floating-point error, conditioning, stability
  - apply a standard method from floating-point error, conditioning, stability to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - numerical-methods
  - applied-core
---

# Floating-Point Error, Conditioning, and Stability

Computers store a finite set of numbers, so arithmetic is rounded. Roundoff error comes from representation and operations; truncation error comes from approximating an infinite process by a finite one. A problem is ill-conditioned if small input changes can cause large output changes. An algorithm is unstable if it amplifies errors unnecessarily. A stable algorithm cannot fix an intrinsically ill-conditioned problem, but it avoids adding avoidable error.

**Example.** To compute √(x+1)−√x for large x, direct subtraction loses significant digits. Rationalize: 1/[√(x+1)+√x], which is algebraically equal but numerically more stable. The issue is cancellation of nearly equal quantities.

Condition number measures sensitivity. For a linear system Ax=b, a large cond(A) means small relative perturbations in data may cause large relative solution changes. Residual ||b−Ax̂|| measures equation mismatch, while forward error ||x−x̂|| measures solution error; a small residual alone may be misleading when A is ill-conditioned.

Report appropriate significant digits, scale variables, and prefer stable factorizations. Do not present machine output as exact mathematics.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: roundoff, conditioning, and algorithm stability

Computers store a finite set of numbers, so many real values are rounded. Floating-point arithmetic approximates each operation with a small relative error in normal ranges, but errors can accumulate or become severe when subtracting nearly equal values. Absolute error is |x−x̂|; relative error divides by |x| and is meaningful when x is not near zero.

Conditioning describes sensitivity of the mathematical problem: a well-conditioned input produces a modest output change. Stability describes whether an algorithm controls the effects of its own rounding errors. An unstable algorithm can give poor results for a well-conditioned problem; a stable algorithm cannot remove inherent ill-conditioning. The condition number of a matrix A in a norm is ‖A‖‖A⁻¹‖ and estimates worst-case relative amplification for solving Ax=b.

**Worked example.** Compute √(x+1)−√x for large x. Direct subtraction loses significant digits because both roots are close. Rationalize: √(x+1)−√x=1/(√(x+1)+√x), which is numerically more stable. The expression’s exact value is small, so relative accuracy is especially sensitive to cancellation.

**Practice with answers.** (1) If input relative error is 10⁻⁶ and condition number is about 10⁴, worst-case output relative error may reach about 10⁻². (2) More precision reduces rounding but does not fix a poorly conditioned problem. (3) Rewriting an equivalent formula can improve stability. (4) Report scale and error, not just many digits.

**Common pitfalls:** equating precision with accuracy; blaming the algorithm when the problem itself is sensitive; and treating a small residual as proof that the solution is accurate for an ill-conditioned system.
