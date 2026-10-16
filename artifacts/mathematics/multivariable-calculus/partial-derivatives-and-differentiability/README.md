---
id: math-multivariable-calculus-partial-derivatives-and-differentiability
type: subtopic
title: Partial derivatives and differentiability
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-vectors-and-geometry-in
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in partial derivatives and differentiability
  - apply a standard method from partial derivatives and differentiability to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Partial Derivatives and Differentiability

For f(x,y), the partial derivative fₓ measures change in x while holding y fixed; fᵧ does the reverse. They describe coordinate-direction slopes, but a function has many directions of approach. Differentiability is stronger: near (a,b), the change in f is approximated by one linear map, f(a+h,b+k)≈f(a,b)+fₓ(a,b)h+fᵧ(a,b)k, with error small compared with √(h²+k²).

**Example.** For f(x,y)=x²y, fₓ=2xy and fᵧ=x². At (1,2), f=2 and the linear approximation is L(x,y)=2+4(x−1)+(y−2). Estimate f(1.02,1.1)≈2+4(0.02)−0.9=1.18. The exact value is 1.02²·1.1≈1.14444; the discrepancy is small for a nearby input.

Continuous partial derivatives near a point guarantee differentiability there, but merely having partial derivatives at the point does not. For example, f(x,y)=xy/(x²+y²) away from zero with f(0,0)=0 has directional behavior that prevents continuity at the origin. Always distinguish partial derivatives from a total linear approximation.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: partial derivatives and the total differential

For f(x,y), the partial derivative fₓ measures change in x while y is held fixed. Geometrically it is a tangent slope in a coordinate slice. A function is differentiable at a point when one linear map approximates its full change with error small relative to the step size; existence of partial derivatives alone does not guarantee differentiability. Continuous partial derivatives near a point are a useful sufficient condition.

**Worked example.** For f(x,y)=x²y+sin y, fₓ=2xy and fᵧ=x²+cos y. At (1,0), the linear approximation is f(1,0)+2(x−1)+2(y−0)=2(x−1)+2y. For a small displacement (h,k), the predicted change is approximately 2h+2k. Check the approximation against the exact expression when h and k are small.

Second partials describe curvature. Under suitable continuity conditions, mixed partials agree (Clairaut’s theorem). Level curves f(x,y)=c help visualize change without drawing the full surface.

**Practice with answers.** (1) For x²+3xy+y², fₓ=2x+3y and fᵧ=3x+2y. (2) At (1,1), both partials equal 5. (3) The tangent plane at (a,b) is z≈f(a,b)+fₓ(a,b)(x−a)+fᵧ(a,b)(y−b). (4) A cusp or discontinuity can defeat differentiability even if some partial derivatives exist.

**Common pitfalls:** varying more than one variable in a partial derivative; assuming partial derivatives imply a good linear approximation; and confusing a level curve with a cross-section.
