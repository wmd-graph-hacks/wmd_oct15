---
id: math-ordinary-differential-equations-matrix-exponentials-and-laplace-transforms
type: subtopic
title: Matrix exponentials and Laplace transforms
parent_topic: math-ordinary-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-ordinary-differential-equations-linear-odes-and-systems
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in matrix exponentials and laplace transforms
  - apply a standard method from matrix exponentials and laplace transforms to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - ordinary-differential-equations
  - advanced-core
---

# Matrix Exponentials and Laplace Transforms

The matrix exponential e^{tA}=I+tA+t²A²/2!+… is defined by a convergent power series and solves X′=AX with X(0)=I. It propagates initial states: x(t)=e^{tA}x₀. Diagonalization simplifies powers; Jordan form handles defective matrices, producing polynomial factors times exponentials.

The Laplace transform L{f}=∫₀∞e^(−st)f(t)dt converts derivatives into algebraic expressions: L{y′}=sY−y(0). It is useful for linear ODEs with initial values, step inputs, and impulses. Solve for Y(s), decompose into known transforms, and invert; always keep initial conditions in the transformed equation.

**Example.** Solve y′+y=1, y(0)=0. Transform: sY+Y=1/s, so Y=1/[s(s+1)]=1/s−1/(s+1). Thus y=1−e^(−t). Direct substitution confirms the result.

Transforms require convergence conditions and can encode piecewise functions via Heaviside shifts. Partial fraction signs and initial-value terms are frequent error sources.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: transform time derivatives into algebra

The matrix exponential e^{At}=I+At+(At)²/2!+… solves x′=Ax with initial vector x(0). It is always defined for finite matrices. Laplace transform L{f}(s)=∫₀∞e^(−st)f(t)dt converts derivatives using L{f′}=sF(s)−f(0), embedding initial conditions into an algebraic equation. Partial fractions and inverse transforms recover the time response.

Laplace methods are especially useful for piecewise forcing, impulses, and coupled linear systems. The transform exists only in a suitable half-plane depending on growth. Heaviside step functions encode switched inputs; delta distributions model idealized instantaneous impulses.

**Worked example.** Solve y′+y=1, y(0)=0. Taking transforms gives sY−0+Y=1/s, so Y=1/[s(s+1)]=1/s−1/(s+1). Invert: y(t)=1−e^(−t). The solution starts at zero and tends to the steady state 1.

**Practice with answers.** (1) L{1}=1/s. (2) L{e^{at}}=1/(s−a) for s>a. (3) L{sin bt}=b/(s²+b²). (4) L{f′} includes the initial value term; dropping it solves a different problem.

**Common pitfalls:** forgetting initial data in the derivative transform; using transform formulas outside convergence conditions; and mishandling step shifts in piecewise forcing.
