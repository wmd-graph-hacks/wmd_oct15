---
id: math-single-variable-calculus-riemann-integral-and-ftc
type: subtopic
title: Riemann integral and FTC
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-mean-value-theorem
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in riemann integral and ftc
  - apply a standard method from riemann integral and ftc to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Riemann Integral and Fundamental Theorem

The definite integral ∫ₐᵇ f(x)dx measures signed accumulation. Positive regions contribute positively; regions below the axis contribute negatively. Divide [a,b] into small intervals, choose a sample point in each, multiply function value by interval width, and add. If these Riemann sums approach one common limit as the partition widths shrink, that limit is the integral. Continuous functions on closed bounded intervals are Riemann integrable.

The Fundamental Theorem of Calculus has two parts. Part I: if f is continuous, F(x)=∫ₐˣ f(t)dt satisfies F′(x)=f(x). Accumulation differentiates back to its rate. Part II: if F′=f, then ∫ₐᵇ f(x)dx=F(b)−F(a). This turns area computation into finding an antiderivative.

**Worked example.** Evaluate ∫₁³ 2x dx. An antiderivative is F(x)=x², so the integral is F(3)−F(1)=9−1=8. Interpret this as the area under y=2x from 1 to 3; the trapezoid has parallel sides 2 and 6 and width 2, area 8. Agreement between calculus and geometry is a useful check.

For variable limits, use the chain rule: d/dx ∫ₐ^{g(x)} f(t)dt=f(g(x))g′(x). If both limits vary, differentiate upper accumulation minus lower accumulation. Do not confuse a definite integral (a number) with an indefinite integral (a family of antiderivatives plus C).

**Practice with answers.** (1) ∫₀² (3x²+1)dx=[x³+x]₀²=10. (2) d/dx ∫₂^{x²} cos(t)dt=2x cos(x²). (3) If G(x)=∫₀ˣ (t²−1)dt, then G′(x)=x²−1 and G(2)=2/3. (4) ∫₀² (x−1)dx=0: signed area cancels, even though geometric area is 1.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: accumulation, area, and the Fundamental Theorem

The definite integral ∫ₐᵇ f(x)dx is the limit of Riemann sums Σ f(xᵢ*)Δxᵢ as the partition width approaches zero, when the limit exists. A rectangle’s signed contribution is height times width. Values below the axis contribute negatively, so a definite integral is net accumulation, not necessarily geometric area. Geometric area is computed with absolute value or by splitting where f changes sign.

If F′=f, the Fundamental Theorem of Calculus gives ∫ₐᵇ f(x)dx=F(b)−F(a). The accumulation function G(x)=∫ₐˣ f(t)dt satisfies G′(x)=f(x) when f is continuous. These two parts connect accumulation and instantaneous change. In an applied problem, identify the quantity being accumulated, its rate, interval, and units before integrating.

**Worked example.** If a particle has velocity v(t)=3t²−2t metres per second, its displacement from 1 to 3 seconds is ∫₁³(3t²−2t)dt=[t³−t²]₁³=18 metres. If it changes direction during the interval, total distance requires splitting at each zero of v and integrating |v|.

**Approximation.** Left, right, and midpoint Riemann sums approximate an integral from sampled values. More rectangles usually improve accuracy for a well-behaved function, but an error estimate requires additional information such as monotonicity or a derivative bound. The trapezoidal rule averages endpoint heights on each subinterval and is exact for linear functions.

**Practice with answers.** (1) ∫₀² x dx=2; it is the triangular area under y=x. (2) ∫₀²(x−1)dx=0, although the geometric area is 1: positive and negative signed areas cancel. (3) If F(x)=∫₂ˣ cos(t²)dt, then F′(x)=cos(x²), by the first FTC part and chain-free variable endpoint. (4) If a rate is in litres/minute and time in minutes, its integral is in litres.

**Common pitfalls:** dropping the lower endpoint in F(b)−F(a); confusing displacement and distance; interpreting signed integral as total area; and forgetting that an integral inherits units from integrand times input.
