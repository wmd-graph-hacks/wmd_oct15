---
id: math-numerical-methods-numerical-differentiation-and-integration
type: subtopic
title: Numerical differentiation and integration
parent_topic: math-numerical-methods
phase: applied-core
estimated_minutes: 60
prerequisites:
  - id: math-numerical-methods-interpolation-and-splines
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in numerical differentiation and integration
  - apply a standard method from numerical differentiation and integration to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - numerical-methods
  - applied-core
---

# Numerical Differentiation and Integration

Finite differences approximate derivatives. Forward difference [f(x+h)−f(x)]/h has truncation error O(h); central difference [f(x+h)−f(x−h)]/(2h) has O(h²) for smooth functions. Making h smaller reduces truncation error but increases roundoff/cancellation, so there is an optimal scale.

Quadrature approximates integrals by weighted function samples. Midpoint and trapezoidal rules are simple; Simpson’s rule fits parabolas and has higher order for smooth functions. Composite rules subdivide the interval. Error depends on derivatives and mesh width; adaptive quadrature refines where behavior is difficult.

**Example.** Approximate ∫₀¹x²dx using Simpson with h=1/2: (h/3)[f(0)+4f(1/2)+f(1)]=(1/6)[0+1+1]=1/3, exact for this quadratic. The exactness is a property of the rule, not a coincidence.

Compare approximations at successively refined meshes and use an error estimate. Oscillation, singularities, and discontinuities may invalidate standard smooth-function bounds.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: approximate slopes and areas

Finite differences estimate derivatives from sampled values. The forward difference [f(x+h)−f(x)]/h has truncation error of order h for smooth f; the centered difference [f(x+h)−f(x−h)]/(2h) typically has order h². Making h smaller reduces truncation error but increases roundoff and measurement noise, so there is a practical best step size.

For integrals, the trapezoidal rule joins adjacent samples with straight segments; Simpson’s rule fits parabolas over pairs of subintervals and is more accurate for smooth functions. Composite rules refine the partition. Error bounds depend on derivatives, so a numerical answer should include a method and tolerance or an error estimate.

**Worked example.** Estimate f′(1) for f(x)=x² with h=.1. Forward difference is (1.21−1)/.1=2.1; centered difference is (1.21−.81)/.2=2, exact. The centered method cancels the leading error for this smooth function.

**Practice with answers.** (1) Trapezoid estimate for ∫₀¹x dx with one panel is 1/2, exact. (2) For a smooth function, halving h in a second-order difference reduces truncation error roughly by 4 before roundoff dominates. (3) Simpson’s rule requires an even number of equal subintervals in its composite form. (4) More samples do not guarantee better answers if data are noisy.

**Common pitfalls:** choosing a step so tiny that subtraction destroys accuracy; applying an error order without smoothness assumptions; and reporting numerical precision unsupported by the input data.
