---
id: math-complex-analysis-holomorphic-functions-and-cauchy-riemann
type: subtopic
title: Holomorphic functions and Cauchy–Riemann
parent_topic: math-complex-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-complex-analysis-complex-plane-and-elementary-functions
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in holomorphic functions and cauchy–riemann
  - apply a standard method from holomorphic functions and cauchy–riemann to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - complex-analysis
  - advanced-core
---

# Holomorphic Functions and Cauchy–Riemann Equations

A function f is complex differentiable at z₀ if [f(z₀+h)−f(z₀)]/h has the same limit as complex h approaches zero from every direction. This is more restrictive than ordinary two-variable differentiability. A function holomorphic on an open set is complex differentiable at every point there; holomorphic functions are infinitely differentiable and locally represented by power series.

Write f=u+iv with real-valued u(x,y),v(x,y). If first partials are continuous, complex differentiability requires Cauchy–Riemann equations uₓ=vᵧ and uᵧ=−vₓ. They are necessary in general; with continuous partial derivatives they are sufficient locally.

**Example.** f(z)=z²=(x²−y²)+i(2xy), so uₓ=2x=vᵧ and uᵧ=−2y=−vₓ. It is holomorphic everywhere. For f(z)=conjugate z=x−iy, uₓ=1 but vᵧ=−1, so CR fails and the function is not complex differentiable.

Do not assume satisfying CR at one point proves holomorphicity nearby. Verify the regularity conditions or establish differentiability directly. Holomorphicity is a strong global constraint with consequences far beyond the local derivative.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: complex differentiability is restrictive

For f(z), the complex derivative is lim_{h→0}[f(z+h)−f(z)]/h, where h may approach from any direction in the plane. Write f=u+iv. If u,v have continuous first partial derivatives nearby, complex differentiability requires the Cauchy–Riemann equations uₓ=vᵧ and uᵧ=−vₓ. With suitable regularity these conditions are also sufficient. A holomorphic function is complex differentiable throughout an open region.

**Worked example.** f(z)=z² gives u=x²−y² and v=2xy. Then uₓ=2x=vᵧ and uᵧ=−2y=−vₓ, so it is holomorphic, with f′(z)=2z. For f(z)=conjugate(z)=x−iy, u=x,v=−y; uₓ=1 but vᵧ=−1, so the equations fail and the function is not complex differentiable.

Holomorphicity implies a convergent power series locally and infinitely many derivatives. Harmonic functions arise as real or imaginary parts because uₓₓ+uᵧᵧ=0. This rigidity is much stronger than ordinary real differentiability.

**Practice with answers.** (1) eᶻ is holomorphic everywhere and derivative eᶻ. (2) z̄ is not holomorphic. (3) If f is holomorphic, its real and imaginary parts are harmonic. (4) Checking CR at one point alone does not prove holomorphicity in a region.

**Common pitfalls:** treating CR equations as sufficient without regularity; checking only one partial relation; and assuming every smooth function of x,y is holomorphic.
