---
id: math-single-variable-calculus-derivatives-and-applications
type: subtopic
title: Derivatives and applications
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-limits-and-continuity
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in derivatives and applications
  - apply a standard method from derivatives and applications to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Derivatives and Applications

The derivative f′(a) is the instantaneous rate of change and the slope of the tangent line. It is defined by the limit f′(a)=limₕ→0 [f(a+h)−f(a)]/h when that limit exists. For f(x)=x², the difference quotient is [(x+h)²−x²]/h=2x+h, so f′(x)=2x. Near a, differentiability means f(a+h)≈f(a)+f′(a)h: the function is locally approximated by a line.

Rules make derivatives efficient. (cf)′=cf′; (f+g)′=f′+g′; (fg)′=f′g+fg′; (f/g)′=(f′g−fg′)/g²; and the chain rule says (f∘g)′(x)=f′(g(x))g′(x). The chain rule is essential for nested functions: d/dx sin(x²)=2x cos(x²).

Derivatives support optimization and qualitative analysis. An interior local maximum or minimum of a differentiable function must occur at a critical point where f′=0 (or where the derivative fails). This is necessary, not sufficient: x³ has derivative 0 at 0 but no extremum. Use a sign chart, second derivative test, or endpoint comparison. If f′>0 on an interval, f increases there; if f′<0, it decreases. For a moving object with position s(t), velocity is s′(t) and acceleration is s″(t).

**Worked optimization example.** A rectangle has perimeter 20, so if one side is x, the other is 10−x and area A(x)=x(10−x), 0≤x≤10. Then A′=10−2x; the only interior critical point is x=5. Since A″=−2<0, this gives a maximum, area 25. Checking endpoints gives area 0, confirming the maximum. The modeling step—expressing the constraint before differentiating—is as important as the derivative.

**Practice with answers.** (1) d/dx (x³−4x)=3x²−4. (2) d/dx e^(x²)=2xe^(x²). (3) For s=t³−6t²+9t, velocity is 3t²−12t+9 and acceleration is 6t−12. (4) Find extrema of x²−4x on [0,5]: critical x=2; values 0,−4,5, so absolute minimum −4 at 2 and maximum 5 at 5.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: derivative as local rate

The derivative f′(a)=limₕ→0 [f(a+h)−f(a)]/h is the limiting slope of secant lines, when the limit exists. It is also the instantaneous rate of change. For position s(t), s′(t) is velocity and s″(t) is acceleration. Keep units: if s is metres and t is seconds, velocity is metres per second.

Use the power rule, product rule, quotient rule, and chain rule. The chain rule is essential for composition: if y=(3x²+1)⁵, then y′=5(3x²+1)⁴·6x. For implicit equations, differentiate both sides with respect to x and remember that y depends on x; d(y²)/dx=2y(dy/dx). A derivative can fail at corners, cusps, vertical tangents, or discontinuities.

**Applications.** Critical numbers occur where f′=0 or f′ is undefined inside the domain. They are candidates, not automatically maxima or minima. A sign chart for f′ identifies increasing and decreasing intervals. A sign change + to − gives a local maximum; − to + gives a local minimum. The second derivative describes concavity where it exists. For a closed interval, compare critical points and both endpoints.

**Worked example.** A rectangle has perimeter 20, so if one side is x, the other is 10−x and area A(x)=x(10−x), 0≤x≤10. Then A′(x)=10−2x, so the interior critical point is x=5. Since A″=−2<0, this is a maximum; the square has area 25. The domain matters: the algebraic critical point must describe an allowed rectangle.

**Practice with answers.** (1) d/dx[(x²+1)³]=6x(x²+1)². (2) If s(t)=t³−6t²+9t, velocity is 3t²−12t+9 and acceleration is 6t−12. (3) For f(x)=x²−4x on [0,5], critical x=2; compare f(0)=0, f(2)=−4, f(5)=5, so absolute minimum −4 and maximum 5. (4) For x²+y²=25, dy/dx=−x/y where y≠0.

**Common pitfalls:** forgetting the chain factor; treating every critical point as an extremum; ignoring endpoints; and reporting a rate without units or its meaning in the model.
