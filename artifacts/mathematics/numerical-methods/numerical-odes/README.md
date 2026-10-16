---
id: math-numerical-methods-numerical-odes
type: subtopic
title: Numerical ODEs
parent_topic: math-numerical-methods
phase: applied-core
estimated_minutes: 60
prerequisites:
  - id: math-numerical-methods-numerical-linear-algebra
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in numerical odes
  - apply a standard method from numerical odes to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - numerical-methods
  - applied-core
---

# Numerical ODE Solvers

Euler’s method advances y′=f(t,y) by yₙ₊₁=yₙ+h f(tₙ,yₙ). It is easy to understand but has global error O(h) for smooth problems. Runge–Kutta methods combine several slope samples per step; classical RK4 has global error O(h⁴) and is a strong general-purpose method for nonstiff equations.

Stability concerns whether numerical perturbations grow appropriately. For y′=λy, Euler multiplies each step by 1+hλ; stability requires |1+hλ|≤1. Stiff systems may require tiny explicit steps despite slowly varying solutions; implicit methods such as backward Euler can be more stable.

**Example.** For y′=y, y(0)=1 with h=0.1, Euler gives y₁=1.1; exact value is e^0.1≈1.10517. Reducing h improves error, but multiple steps accumulate local error.

Compare step refinements, monitor error estimates, and respect event/boundary behavior. A plotted curve can look smooth while being inaccurate.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: step-by-step numerical solutions of ODEs

For y′=f(t,y), Euler’s method advances yₙ₊₁=yₙ+h f(tₙ,yₙ). It follows the current tangent and has global error typically O(h) on a fixed interval. Improved Euler/Heun averages slopes at the ends of a step. Runge–Kutta methods sample intermediate slopes; classical RK4 has global error O(h⁴) for smooth problems but requires four function evaluations per step.

Step size affects accuracy and stability. For y′=λy with λ<0, explicit Euler multiplies each step by 1+hλ; stability requires |1+hλ|≤1. A stiff equation may require a very small explicit step even when the solution changes slowly. Compare step refinements or use an adaptive solver, and distinguish truncation error from model error.

**Worked example.** Solve approximately y′=y, y(0)=1 with Euler step h=.1. y₁=1+.1(1)=1.1; exact e^.1≈1.10517. A second step gives 1.21 versus e^.2≈1.22140. The error accumulates; reducing h generally improves the approximation for this problem.

**Practice with answers.** (1) Euler step for y′=t+y, y(0)=1, h=.2 gives y₁=1.2. (2) RK4 evaluates four slopes per step. (3) Stability concerns bounded response to perturbations, not just local accuracy. (4) Check units: time step times derivative has units of the dependent variable.

**Common pitfalls:** confusing step size with error order; using a method outside its stability region; and trusting a plotted curve without refinement or error control.
