---
id: math-complex-analysis-taylor-and-laurent-series
type: subtopic
title: Taylor and Laurent series
parent_topic: math-complex-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-complex-analysis-contour-integration-and-cauchy-theory
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in taylor and laurent series
  - apply a standard method from taylor and laurent series to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - complex-analysis
  - advanced-core
---

# Taylor and Laurent Series

Holomorphic functions admit local Taylor expansions. If f is holomorphic near a, f(z)=Σ f⁽ⁿ⁾(a)(z−a)ⁿ/n! within its convergence disk. Laurent series generalize this to an annulus and allow negative powers: Σₙ∈ℤ cₙ(z−a)ⁿ. The principal part (negative powers) identifies an isolated singularity.

A removable singularity has no nonzero principal part after redefining the function. A pole has finitely many negative-power terms. An essential singularity has infinitely many. The same expression may have different Laurent expansions on different annuli because convergence regions differ.

**Example.** For 1/[z(z−1)], in |z|<1, write −1/[z(1−z)]=−(1/z)(1+z+z²+…)=−1/z−1−z−…, valid 0<|z|<1. In |z|>1, expand 1/[z²(1−1/z)]=1/z²+1/z³+…, valid |z|>1. State the annulus with every expansion.

Termwise differentiation and integration are valid inside the annulus of convergence. Do not substitute a boundary point without checking convergence there.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: analytic series and isolated singularities

Holomorphic functions have Taylor series inside disks up to the nearest singularity. A Laurent series allows negative powers on an annulus and separates behavior near an isolated singularity. If all negative-power coefficients vanish, the singularity is removable. A finite principal part gives a pole; infinitely many negative powers give an essential singularity.

The coefficient of (z−a)⁻¹ is the residue. Laurent coefficients can be computed by contour integrals or algebraic expansion. Radius and annulus of convergence are determined by singularity locations; test the actual domain, not just a formal series.

**Worked example.** For 1/[z(z−1)] near z=0, write −1/z·1/(1−z)=−1/z−1−z−z²−… for 0<|z|<1. The coefficient of 1/z is −1, so the residue at zero is −1. Near z=1, use a different expansion centered there.

**Practice with answers.** (1) eᶻ has Taylor series Σzⁿ/n! with infinite radius. (2) sin z/z has a removable singularity at zero because its series is 1−z²/3!+…. (3) 1/z³ has a pole of order 3. (4) Essential singularity example: e^(1/z) at zero.

**Common pitfalls:** using a Taylor series where the function is not holomorphic; forgetting an annulus may exclude the center; and confusing pole order with residue.
