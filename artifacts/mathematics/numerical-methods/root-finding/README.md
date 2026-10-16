---
id: math-numerical-methods-root-finding
type: subtopic
title: Root finding
parent_topic: math-numerical-methods
phase: applied-core
estimated_minutes: 60
prerequisites:
  - id: math-numerical-methods-floating-point-error-conditioning-stability
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in root finding
  - apply a standard method from root finding to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - numerical-methods
  - applied-core
---

# Numerical Root Finding

Bisection starts with [a,b] where continuous f has opposite signs. At each step, evaluate midpoint and retain the half interval with sign change. The root remains bracketed, and after n steps interval width is (b−a)/2ⁿ. It is reliable but converges linearly.

Newton’s method uses tangent-line approximation: xₙ₊₁=xₙ−f(xₙ)/f′(xₙ). Near a simple root with a good starting value, convergence is often quadratic. It can fail if derivative is small/zero, iterates leave the region, or converge to an unintended root. Safeguarded Newton combines Newton steps with a bracket.

**Example.** For f(x)=x²−2, start x₀=1. Newton gives x₁=1.5, x₂≈1.41667, x₃≈1.41422, approaching √2 rapidly. Bisection on [1,2] guarantees an error below 2⁻ⁿ after n steps.

Stop based on residual and step/bracket size, not an arbitrary iteration count alone. A small |f(x)| implies a nearby root only under suitable slope behavior.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: bracket a root or iterate toward one

Bisection starts with [a,b] where f is continuous and f(a),f(b) have opposite signs. The Intermediate Value Theorem guarantees a root in the interval. Each step halves the bracket; after n steps its width is (b−a)/2ⁿ. It is reliable but converges linearly. Newton’s method uses tangent steps xₙ₊₁=xₙ−f(xₙ)/f′(xₙ), often converging quadratically near a simple root with a good starting point, but it can fail if the derivative is small or the iterate leaves the useful region.

**Worked example.** Find √2 using f(x)=x²−2. Starting x₀=1.5, Newton gives x₁=1.5−(0.25/3)=1.4167; next gives about 1.4142. Bisection on [1,2] always retains a bracket but needs more steps for the same accuracy.

Use both residual |f(x)| and step/bracket size as stopping criteria. A small residual alone may not imply a close root when the function is flat. Safeguarded Newton methods fall back to bisection if an iterate exits the bracket.

**Practice with answers.** (1) After 5 bisection steps on [0,1], width is 1/32. (2) For f=x²−9 and x₀=2, one Newton step gives 3.25. (3) Bisection requires opposite endpoint signs and continuity. (4) Newton can converge to a different root or diverge depending on its start.

**Common pitfalls:** using Newton when f′=0; dropping a valid bracket; and claiming convergence without checking assumptions or a stopping error bound.
