---
id: math-numerical-methods-interpolation-and-splines
type: subtopic
title: Interpolation and splines
parent_topic: math-numerical-methods
phase: applied-core
estimated_minutes: 60
prerequisites:
  - id: math-numerical-methods-root-finding
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in interpolation and splines
  - apply a standard method from interpolation and splines to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - numerical-methods
  - applied-core
---

# Interpolation and Splines

Interpolation constructs a function matching data points exactly. The degree-(n−1) polynomial through n distinct nodes is unique. Lagrange form builds it from basis polynomials; Newton divided differences make incremental updates convenient. Interpolation differs from regression: interpolation has zero error at sample nodes, while regression balances overall residuals.

High-degree polynomial interpolation can oscillate badly, especially near interval ends with equally spaced nodes (Runge phenomenon). Piecewise cubic splines fit local polynomials while enforcing continuity of value, slope, and often curvature at knots. Natural cubic splines set second derivatives to zero at endpoints; other boundary conditions are possible.

**Example.** Linear interpolation between (0,1) and (2,5) gives slope 2 and p(x)=1+2x, so p(1)=3. This is exact if the underlying relationship is linear; otherwise it is an approximation whose error depends on curvature and spacing.

Use nodes that cover the domain, avoid unsupported extrapolation, and distinguish exact data fit from model truth.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: interpolate data without overfitting

Interpolation constructs a function passing through given data. A degree-n polynomial uniquely interpolates n+1 distinct x-values, but high-degree polynomials can oscillate badly near endpoints (Runge phenomenon). Piecewise polynomial splines use lower-degree pieces joined with continuity conditions; cubic splines often enforce continuous first and second derivatives and produce smooth curves.

Lagrange form makes the interpolating polynomial explicit; Newton divided differences allow efficient updates when points are added. Interpolation estimates between data points, while extrapolation outside the range is less constrained and often unreliable. If observations contain noise, a regression or smoothing spline is generally more appropriate than forcing an exact fit.

**Worked example.** Points (0,1) and (2,5) determine the line through them: slope 2, so p(x)=1+2x. At x=1 the interpolated value is 3. This exact fit says nothing about whether the true underlying function is linear; more data or a model assumption is needed.

**Practice with answers.** (1) n+1 distinct points determine one polynomial of degree at most n. (2) A spline can reduce global oscillation by using local pieces. (3) Predicting at x=10 from data only at 0 and 2 is extrapolation. (4) Duplicate x-values with different y-values cannot both be interpolated by a function.

**Common pitfalls:** confusing interpolation with causal modeling; ignoring noise; extrapolating a polynomial far outside the data; and overlooking duplicate abscissas or continuity constraints.
