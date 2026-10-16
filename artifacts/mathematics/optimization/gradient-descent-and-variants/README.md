---
id: math-optimization-gradient-descent-and-variants
type: subtopic
title: Gradient descent and variants
parent_topic: math-optimization
phase: applied-advanced
estimated_minutes: 60
prerequisites:
  - id: math-optimization-kkt-and-constrained-optimization
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in gradient descent and variants
  - apply a standard method from gradient descent and variants to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - optimization
  - applied-advanced
---

# Gradient Descent and Its Variants

Gradient descent updates xₖ₊₁=xₖ−ηₖ∇f(xₖ), moving opposite the steepest local increase. Step size η matters: too small means slow progress; too large can overshoot or diverge. For an L-smooth convex function, step size at most 1/L yields standard descent guarantees. Feature scaling can dramatically affect convergence.

Momentum combines current gradient with a moving velocity to reduce zigzagging. Stochastic gradient descent uses mini-batch estimates of the gradient, useful for large datasets but noisy. Adaptive methods rescale coordinates based on past gradients. These methods change optimization behavior and generalization; they do not remove the need for validation.

**Example.** Minimize f(x)=x². Gradient is 2x, so xₖ₊₁=(1−2η)xₖ. Convergence to zero requires |1−2η|<1, i.e. 0<η<1. At η=1, iterates alternate without shrinking; at η>1 they diverge.

Monitor objective, gradient norm, and constraints. A small gradient does not guarantee a global optimum in a nonconvex problem.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: iterative minimization with gradients

Gradient descent updates xₖ₊₁=xₖ−η∇f(xₖ), where η>0 is the learning rate. The negative gradient is locally the direction of fastest decrease. If η is too large, iterates can overshoot or diverge; too small makes progress slow. For smooth strongly convex quadratics, suitable step sizes yield convergence, with rate tied to conditioning.

Momentum combines current gradient with previous direction; stochastic gradient descent estimates the gradient from a sample or mini-batch; adaptive methods scale coordinates using past gradients. These variants trade speed, noise, and tuning requirements. Monitor objective, gradient norm, and validation behavior when optimizing a fitted model; optimization success does not guarantee a meaningful model.

**Worked example.** Minimize f(x)=(x−3)². The gradient is 2(x−3). Starting x₀=0 with η=1/4 gives x₁=1.5, x₂=2.25, x₃=2.625; the error halves each step because xₖ₊₁−3=(1−2η)(xₖ−3). With η=1, the iteration oscillates between 0 and 6 and does not converge.

**Practice with answers.** (1) At a differentiable interior minimum, gradient is zero. (2) A zero gradient can also be a saddle or maximum. (3) Momentum can accelerate progress along consistent directions but overshoot. (4) Feature scaling can improve conditioning and convergence.

**Common pitfalls:** selecting learning rate by one successful step; stopping solely because objective changes little; confusing optimization convergence with statistical validity; and ignoring constraints or non-differentiability.
