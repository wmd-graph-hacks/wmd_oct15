---
id: math-ordinary-differential-equations-linear-odes-and-systems
type: subtopic
title: Linear ODEs and systems
parent_topic: math-ordinary-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-ordinary-differential-equations-first-order-methods
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in linear odes and systems
  - apply a standard method from linear odes and systems to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - ordinary-differential-equations
  - advanced-core
---

# Linear ODEs and Systems

A linear nth-order ODE has the form aₙy⁽ⁿ⁾+…+a₀y=g(x). For constant coefficients, solve the homogeneous equation using the characteristic polynomial; repeated roots produce factors x^k e^{rx}, and complex roots yield damped oscillations. Add a particular solution for forcing and use initial conditions to determine constants.

A system x′=Ax can be solved with eigenvectors and matrix exponentials. If A diagonalizes as PDP⁻¹, then e^{tA}=Pe^{tD}P⁻¹. For repeated or complex eigenvalues, generalized eigenvectors or real sine/cosine forms may be needed. The initial-value solution is x(t)=e^{tA}x(0).

**Example.** For x′=diag(2,−1)x with x(0)=(a,b), components decouple: x₁=ae^{2t}, x₂=be^{−t}. One mode grows, one decays. Eigenvalues reveal this behavior directly.

Convert a scalar nth-order equation to a first-order system by introducing variables for y,y′,… . This makes matrix methods available and clarifies state dimension. Verify units and initial vector ordering.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: solve linear equations and systems

A linear nth-order ODE has the unknown function and its derivatives only to the first power, with coefficients depending on the independent variable. For constant coefficients, try y=e^{rt}; the characteristic polynomial gives exponential solutions for real roots and combinations e^{αt}(C cos βt+D sin βt) for complex roots. Repeated roots add factors t,t²,… . For a forced equation, combine a homogeneous solution with a particular solution.

A first-order system x′=Ax has solution x(t)=e^{At}x(0). If A diagonalizes as PDP⁻¹, then e^{At}=Pe^{Dt}P⁻¹; Jordan form handles defective cases. Eigenvalues determine modes and stability: negative real parts decay, positive ones grow, and imaginary parts produce oscillations.

**Worked example.** Solve y″−3y′+2y=0. Characteristic equation r²−3r+2=(r−1)(r−2)=0, so y=C₁eᵗ+C₂e²ᵗ. Given y(0)=1,y′(0)=0 gives C₁+C₂=1 and C₁+2C₂=0, hence C₁=2,C₂=−1.

**Practice with answers.** (1) y″+4y=0 gives C₁cos2t+C₂sin2t. (2) Repeated root r=−1 twice gives (C₁+C₂t)e^(−t). (3) For x′=diag(−1,2)x, one component decays and one grows. (4) Initial data determines constants for a well-posed linear IVP.

**Common pitfalls:** omitting a t factor for repeated roots; confusing a forced solution with the homogeneous family; and reading stability from determinant alone rather than eigenvalues.
