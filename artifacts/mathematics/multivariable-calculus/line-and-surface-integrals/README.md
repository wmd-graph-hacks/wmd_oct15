---
id: math-multivariable-calculus-line-and-surface-integrals
type: subtopic
title: Line and surface integrals
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-multiple-integrals-and-change-of-variables
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in line and surface integrals
  - apply a standard method from line and surface integrals to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Line and Surface Integrals

A scalar line integral ∫C f ds sums a scalar quantity along a curve and does not depend on orientation. Parameterize C by r(t), a≤t≤b; then ds=||r′(t)||dt and the integral is ∫ f(r(t))||r′(t)||dt. A vector line integral ∫C F·dr measures work along an oriented path and equals ∫F(r(t))·r′(t)dt; reversing direction changes its sign.

A surface integral ∬S f dS accumulates a scalar over surface area. A flux integral ∬S F·n dS measures flow through an oriented surface; for parameterization r(u,v), the oriented area vector is rᵤ×rᵥ dudv. Reverse the cross-product order to reverse orientation.

**Example.** Work by F=(−y,x) around the unit circle counterclockwise: r(t)=(cos t,sin t), 0≤t≤2π. Then F(r)=(-sin t,cos t)=r′(t), so F·r′=1 and work is ∫₀²π1dt=2π. The direction is part of the problem.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: integrating along curves and surfaces

A scalar line integral ∫C f ds accumulates along arc length; for r(t), ds=‖r′(t)‖dt. A vector line integral ∫C F·dr measures work along an oriented path and becomes ∫F(r(t))·r′(t)dt. Reversing the path changes the sign of the vector integral but not a scalar ds integral.

A surface integral ∬S f dS accumulates over area. For z=g(x,y), dS=√(1+gₓ²+gᵧ²)dA. Flux of F through an oriented surface is ∬S F·n dS; the normal orientation matters. Closed surfaces conventionally use outward orientation.

**Worked example.** Let F(x,y)=(−y,x) and parametrize the unit circle counterclockwise by r(t)=(cos t,sin t), 0≤t≤2π. Then F(r(t))=r′(t), so ∮C F·dr=∫₀²π1dt=2π. The sign matches the field’s direction around the curve.

**Practice with answers.** (1) The length of r(t)=(t,t), 0≤t≤1, is √2. (2) The scalar integral of 1 over a curve is its length. (3) Reverse the circle orientation: the vector integral is −2π. (4) Flux needs a specified normal direction.

**Common pitfalls:** confusing ds with dr; omitting speed in scalar line integrals; failing to include orientation; and tracing only part of a curve.
