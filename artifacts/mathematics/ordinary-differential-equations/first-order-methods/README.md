---
id: math-ordinary-differential-equations-first-order-methods
type: subtopic
title: First-order methods
parent_topic: math-ordinary-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-sequences-and-series
    target_type: subtopic
    strength: recommended
  - id: math-linear-algebra-vector-spaces-subspaces-basis
    target_type: subtopic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in first-order methods
  - apply a standard method from first-order methods to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - ordinary-differential-equations
  - advanced-core
---

# First-Order ODE Methods

A first-order ODE relates y and y′. A solution is a function satisfying the equation on an interval and meeting any initial condition. Separable equations y′=g(x)h(y) can be rearranged and integrated, while noting constant solutions lost by division. Linear equations y′+p(x)y=q(x) use an integrating factor μ=e^{∫p dx}, giving (μy)′=μq.

**Example.** Solve y′+2y=eˣ, y(0)=0. The integrating factor is e^{2x}; then (e^{2x}y)′=e^{3x}. Integrate: e^{2x}y=e^{3x}/3+C, so y=eˣ/3+Ce^(−2x). Initial condition gives C=−1/3. Check by substitution.

Autonomous equations y′=f(y) have equilibria where f(y)=0. A sign chart indicates whether solutions move up or down and whether equilibria attract nearby solutions. Exact equations M dx+N dy=0 arise when a potential function exists; check Mᵧ=Nₓ on a suitable simply connected domain.

Separation can divide by zero or cross singularities; solve equilibria separately and state intervals of validity. Initial conditions select one member from a family of solutions.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: separate, linear, and exact first-order equations

For separable y′=g(t)h(y), rearrange dy/h(y)=g(t)dt and integrate, then apply the initial condition. For a linear equation y′+p(t)y=q(t), multiply by integrating factor μ=e^{∫p dt}; then (μy)′=μq. Keep the interval where coefficients and divisions are valid. Exact equations M(t,y)dt+N(t,y)dy=0 arise when M_y=N_t and can be integrated as a potential function.

**Worked example.** Solve y′=ty with y(0)=2. Separate: dy/y=t dt, so ln|y|=t²/2+C and y=Ce^{t²/2}. Initial data gives C=2, hence y=2e^{t²/2}. The solution remains positive; division by y did not lose this initial-value solution.

For y′+2y=e^(−t), integrating factor e^(2t) gives (e^(2t)y)′=eᵗ; integrate to obtain y=e^(−t)+Ce^(−2t). Verify by substitution. The homogeneous part describes natural decay; the particular part is driven by the input.

**Practice with answers.** (1) y′=3y gives y=Ce^{3t}. (2) y′+y=1 gives y=1+Ce^(−t). (3) In y′=y², division by y² omits y=0; check it separately. (4) Initial conditions determine constants after the general solution is found.

**Common pitfalls:** dividing by an expression that could be zero; losing absolute values in logarithms; forgetting the integrating factor multiplies every term; and not checking the initial condition.
