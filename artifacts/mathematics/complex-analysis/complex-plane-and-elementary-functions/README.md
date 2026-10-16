---
id: math-complex-analysis-complex-plane-and-elementary-functions
type: subtopic
title: Complex plane and elementary functions
parent_topic: math-complex-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-sequences-and-series
    target_type: subtopic
    strength: recommended
  - id: math-foundations-of-mathematics-sets-and-operations
    target_type: subtopic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in complex plane and elementary functions
  - apply a standard method from complex plane and elementary functions to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - complex-analysis
  - advanced-core
---

# Complex Numbers and Elementary Functions

A complex number z=x+iy has real part x, imaginary part y, conjugate x−iy, and modulus |z|=√(x²+y²). The plane view makes addition vector addition. In polar form z=re^{iθ}; multiplication multiplies magnitudes and adds arguments, while division divides magnitudes and subtracts arguments. Arguments are defined modulo 2π.

Euler’s formula e^{iθ}=cosθ+i sinθ links exponential and trigonometric forms. The complex exponential is periodic: e^{z+2πi}=e^z. The complex logarithm is multivalued because z=re^{iθ} has arguments θ+2πk; a branch chooses a continuous argument on a restricted domain.

**Example.** Compute (1+i)⁴. Since 1+i=√2 e^{iπ/4}, its fourth power is 4e^{iπ}=−4. Polar form avoids repeated expansion. For n-th roots of re^{iθ}, roots are r^(1/n)e^{i(θ+2πk)/n}, k=0,…,n−1; they are equally spaced on a circle.

Complex arithmetic is algebraically familiar, but ordering is unavailable: there is no compatible total order on ℂ. Interpret geometric statements through modulus and angle, not inequalities like z>0.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: complex arithmetic and polar form

A complex number z=x+iy has real part x, imaginary part y, conjugate x−iy, and modulus |z|=√(x²+y²). Multiplication by e^{iθ}=cosθ+i sinθ rotates by θ; polar form z=re^{iθ} makes multiplication and powers geometric. De Moivre’s formula (re^{iθ})ⁿ=rⁿe^{inθ} helps find powers and roots. Every nonzero complex number has n distinct nth roots spaced evenly around a circle.

The complex exponential eᶻ=eˣ(cos y+i sin y) is periodic in the imaginary direction. A logarithm is multivalued: log z=ln|z|+i(arg z+2πk). Choosing a principal argument creates a branch cut and discontinuity; always specify the branch when using complex logarithms or powers.

**Worked example.** Write 1+i in polar form: modulus √2 and angle π/4, so 1+i=√2e^{iπ/4}. Its cube is 2√2e^{i3π/4}=−2+2i. Direct multiplication confirms the result.

**Practice with answers.** (1) |3−4i|=5. (2) (1+i)²=2i. (3) Cube roots of 1 have angles 0,2π/3,4π/3. (4) There is no order relation on ℂ compatible with ordinary field operations.

**Common pitfalls:** forgetting arguments are defined modulo 2π; using one logarithm value without choosing a branch; and confusing i²=−1 with a positive real square root.
