---
id: math-multivariable-calculus-green-stokes-and-divergence-theorems
type: subtopic
title: Green, Stokes, and Divergence theorems
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-line-and-surface-integrals
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in green, stokes, and divergence theorems
  - apply a standard method from green, stokes, and divergence theorems to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Green, Stokes, and Divergence Theorems

These theorems turn boundary measurements into interior derivative measurements. Green’s theorem in the plane says ∮C(P dx+Q dy)=∬D(Qₓ−Pᵧ)dA for a positively oriented simple boundary. It converts circulation around a boundary to total scalar curl inside. Stokes’ theorem is its three-dimensional surface analogue: ∮∂S F·dr= ∬S (curl F)·n dS. The Divergence theorem says ∬∂V F·n dS=∭V div F dV, converting outward flux to total source strength inside.

**Example using Green.** For F=(-y,x) around the unit circle, Qₓ−Pᵧ=1−(−1)=2. Green gives circulation ∬disk 2dA=2π, matching direct parameterization. This agreement is both a check and a demonstration of why the theorem is useful: the easier side can replace the harder one.

Before applying a theorem, verify the boundary is appropriately closed, the field has the required derivatives, and orientations agree. Positive planar orientation is counterclockwise; a closed surface uses outward normals. If the surface has a hole, include every boundary component with induced orientation.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: relate derivatives to boundary integrals

Green’s theorem relates circulation around a positively oriented simple closed curve to integrated planar curl: ∮C(P dx+Q dy)= ∬R(Qₓ−Pᵧ)dA. Stokes’ theorem generalizes this to a surface: circulation around its oriented boundary equals surface integral of curl. The Divergence theorem relates outward flux through a closed surface to volume integral of divergence: ∬S F·n dS=∭E div F dV. Each converts an integral into an equivalent one over a boundary or interior.

Check smoothness, closure, and orientation before applying a theorem. Positive orientation in Green’s theorem is counterclockwise. Stokes’ boundary orientation follows the right-hand rule. Divergence uses outward normals.

**Worked example.** For F=(x,y,z), div F=3. Outward flux through a sphere of radius a is ∭ball 3 dV=3(4πa³/3)=4πa³. Directly, F=a n on the sphere, giving a times its area 4πa², the same result.

**Practice with answers.** (1) For F=(−y,x), planar curl Qₓ−Pᵧ=2, so circulation around radius-a disk is 2πa². (2) A constant field has zero net flux through a closed surface. (3) Reversing boundary orientation reverses circulation sign. (4) A consistently oriented surface is required for Stokes.

**Common pitfalls:** applying a theorem when closure assumptions fail; using inward instead of outward normal; and confusing curl with divergence.
