---
id: math-multivariable-calculus-multiple-integrals-and-change-of-variables
type: subtopic
title: Multiple integrals and change of variables
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-optimization-and-lagrange-multipliers
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in multiple integrals and change of variables
  - apply a standard method from multiple integrals and change of variables to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Multiple Integrals and Change of Variables

A double integral ∬ᴰf(x,y)dA accumulates a density over a region. Compute it as an iterated integral by describing the region with bounds; changing order can simplify the bounds or integrand. Sketching the region before writing limits prevents many errors. For nonnegative f, the integral is volume under the surface; for signed f, it is net accumulation.

A coordinate substitution transforms both integrand and area element. If (x,y)=T(u,v), then dA=|det J_T|du dv. The Jacobian accounts for local stretching. Polar coordinates x=r cosθ, y=r sinθ have determinant r, so dA=r dr dθ. Omitting r is a common serious error.

**Example.** Find the area of a disk radius R: ∬ᴰ1dA=∫₀²π∫₀ᴿ r dr dθ=(R²/2)(2π)=πR². For a density ρ(x,y)=x²+y² on the same disk, polar form is ρ=r²; integral is ∫₀²π∫₀ᴿ r³drdθ=πR⁴/2.

For triple integrals, cylindrical coordinates use dV=r dr dθ dz; spherical coordinates use ρ²sinφ dρ dφ dθ (with φ measured down from the positive z-axis). Bounds must match the region and coordinate convention. Fubini’s theorem permits switching order under standard integrability conditions.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: double integrals and coordinate changes

A double integral ∬ᴿ f(x,y)dA accumulates density or signed height over a region. For a rectangle it can be evaluated as an iterated integral; for nonrectangular regions, describe the bounds carefully and choose an order that simplifies them. Sketch the region before writing limits. Fubini’s theorem permits changing order when the function is suitably integrable.

Under (x,y)=T(u,v), area transforms as dA=|∂(x,y)/∂(u,v)| dudv. The determinant accounts for local stretching. Polar coordinates x=r cosθ, y=r sinθ have Jacobian r, so dA=r dr dθ. The factor r is essential.

**Worked example.** Integrate 1 over the disk x²+y²≤a². In polar coordinates, 0≤r≤a and 0≤θ≤2π, so area=∫₀²π∫₀ᵃ r dr dθ=πa². Omitting r would give the wrong area.

Triple integrals accumulate over volumes; cylindrical and spherical coordinates extend the method. For density ρ, mass=∫ρ dV. Units provide a useful check: surface density times area gives mass.

**Practice with answers.** (1) Area of a radius-3 disk is 9π. (2) For 0≤x≤1, 0≤y≤x, area is ∫₀¹x dx=1/2. (3) Use the absolute determinant for ordinary volume. (4) Reversed bounds must describe the same region.

**Common pitfalls:** omitting the Jacobian; changing coordinates without transforming the region; and reversing order without redrawing bounds.
