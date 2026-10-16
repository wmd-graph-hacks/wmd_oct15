---
id: math-multivariable-calculus-vectors-and-geometry-in
type: subtopic
title: Vectors and geometry in ℝⁿ
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus
    target_type: topic
    strength: recommended
  - id: math-linear-algebra
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in vectors and geometry in ℝⁿ
  - apply a standard method from vectors and geometry in ℝⁿ to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Vectors in Euclidean Space

A vector in ℝⁿ is an ordered list of n real coordinates. Addition and scalar multiplication are coordinatewise. The dot product x·y=Σxᵢyᵢ gives length ||x||=√(x·x), and x·y=0 means orthogonality. The Cauchy–Schwarz inequality |x·y|≤||x||||y|| ensures the angle formula cosθ=(x·y)/(||x||||y||) is meaningful.

A line through p in direction v is x(t)=p+tv. A plane in ℝ³ with normal n through p satisfies n·(x−p)=0. This normal-vector form is often easier than solving for z. Projection onto a nonzero vector v is projᵥu=((u·v)/(v·v))v; the residual u−projᵥu is perpendicular to v.

**Example.** Find the plane through (1,0,2) with normal (2,−1,3). Its equation is 2(x−1)−y+3(z−2)=0, or 2x−y+3z=8. A point lies on the plane exactly when its displacement from the given point has zero dot product with the normal.

**Practice.** (1) Distance between (1,2) and (4,6) is 5. (2) A direction vector for the intersection of planes with normals n₁,n₂ is perpendicular to both; in ℝ³ use n₁×n₂ when nonzero.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: vectors, lines, planes, and geometry

A vector in ℝⁿ records magnitude and direction. The dot product u·v=Σuᵢvᵢ gives ‖u‖²=u·u and u·v=‖u‖‖v‖cosθ. The cross product in ℝ³ is perpendicular to both inputs and has magnitude equal to parallelogram area. A line through p with direction v is r(t)=p+tv. A plane through p with normal n satisfies n·(r−p)=0.

**Worked example.** The line through (1,0,2) parallel to (2,−1,3) is (1+2t,−t,2+3t). The plane through (1,0,2) with normal (2,−1,3) is 2(x−1)−y+3(z−2)=0, or 2x−y+3z=8. A direction lies parallel to the plane exactly when its dot product with the normal is zero.

**Practice with answers.** (1) Distance from (1,2,2) to the origin is 3. (2) (1,2,0)·(2,−1,4)=0, so the vectors are orthogonal. (3) A normal to the plane spanned by (1,0,0),(0,1,0) is (0,0,1). (4) The angle between nonzero vectors follows from inverse cosine of the normalized dot product.

**Common pitfalls:** treating a point as a direction vector; using a plane’s direction vector as its normal; and forgetting that a line parameter ranges over all real numbers unless restricted.
