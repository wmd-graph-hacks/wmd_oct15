---
id: math-multivariable-calculus-optimization-and-lagrange-multipliers
type: subtopic
title: Optimization and Lagrange multipliers
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-gradient-chain-rule-jacobian
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in optimization and lagrange multipliers
  - apply a standard method from optimization and lagrange multipliers to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Optimization and Lagrange Multipliers

For an unconstrained differentiable function, an interior local extremum must have zero gradient. In two variables, solve fₓ=fᵧ=0, then classify candidates using the Hessian or compare values on a closed bounded domain. A critical point may be a saddle, so solving the equations is only the candidate-finding step.

For a constraint g(x,y)=c, the Lagrange multiplier condition ∇f=λ∇g says that at a constrained extremum the gradients are parallel: the objective has no first-order change along feasible tangent directions. Solve this equation together with the constraint, then evaluate f at every candidate. The regularity condition ∇g≠0 is important; singular constraint points need separate checking.

**Example.** Maximize xy subject to x²+y²=1. Lagrange equations are (y,x)=λ(2x,2y). If x,y are nonzero, these imply x²=y². Candidates include (±1/√2,±1/√2); products are ±1/2, so the maximum is 1/2 and minimum −1/2. Check cases x=0 or y=0 as well; they yield product 0.

For inequality constraints, KKT conditions extend the Lagrange method with nonnegative multipliers and complementary slackness. They are necessary under constraint qualifications and sufficient for convex problems. Do not claim a local candidate is globally optimal without convexity or a full comparison.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: critical points and constrained extrema

For an unconstrained differentiable function, an interior local extremum must satisfy ∇f=0. This condition is necessary, not sufficient: classify with second derivatives/Hessian or compare values and inspect the domain boundary. For a constraint g(x,y)=c with nonzero gradient, a constrained extremum occurs where ∇f=λ∇g. The gradients are parallel because allowable tangent directions have zero first-order change in g.

**Worked example.** Maximize f(x,y)=xy subject to x²+y²=1. The multiplier equations (y,x)=λ(2x,2y), together with the constraint, give x=±y. Same-sign points yield f=1/2 and opposite-sign points yield −1/2. Thus max is 1/2 and min −1/2. The circle is compact, so extrema exist.

For inequalities, boundary cases matter. At corners or active boundaries the gradient equation alone may miss candidates; KKT conditions extend the method with multipliers and complementary slackness.

**Practice with answers.** (1) Extrema of x+y on x²+y²=1 are ±√2. (2) Minimize x²+y² subject to x+y=1: at x=y=1/2, minimum 1/2. (3) Why test a disk’s boundary? An extremum can occur there even when ∇f≠0.

**Common pitfalls:** forgetting the constraint equation; treating ∇f=0 as sufficient; omitting boundary components; and using a multiplier equation where the constraint gradient vanishes.
