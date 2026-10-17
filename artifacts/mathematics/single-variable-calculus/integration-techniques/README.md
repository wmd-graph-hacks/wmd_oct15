---
id: math-single-variable-calculus-integration-techniques
type: subtopic
title: Integration techniques
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-riemann-integral-and-ftc
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in integration techniques
  - apply a standard method from integration techniques to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Integration Techniques

Integration reverses differentiation, but there is no single rule that handles every expression. Choose a technique by recognizing structure, then verify by differentiating the result.

**Substitution** reverses the chain rule. If an integrand contains a function and its derivative, set u equal to the inner function. Example: ∫2x cos(x²)dx; let u=x², du=2x dx, giving ∫cos u du=sin(x²)+C. For definite integrals, either transform the bounds or substitute back before evaluating.

**Integration by parts** reverses the product rule: ∫u dv=uv−∫v du. Choose u to become simpler when differentiated. For ∫x eˣdx, let u=x and dv=eˣdx. Then x eˣ−∫eˣdx=eˣ(x−1)+C.

**Partial fractions** decompose rational functions into simpler terms after polynomial division when needed. Since 1/[x(x+1)]=1/x−1/(x+1), its integral is ln|x|−ln|x+1|+C on intervals avoiding poles. **Trigonometric substitution** can simplify radicals such as √(a²−x²) using x=a sin θ; always track the interval and convert back carefully. Trig identities can also reduce powers.

**Strategy.** First simplify algebraically. Look for an inner derivative (substitution); a product where one factor simplifies (parts); a rational function (partial fractions); or a radical matching a geometric identity (trig substitution). If an elementary antiderivative does not exist, use a defined special function or numerical approximation rather than forcing a false formula.

**Practice with answers.** (1) ∫x(x²+1)^4 dx: u=x²+1 gives (x²+1)^5/10+C. (2) ∫ln x dx=x ln x−x+C by parts. (3) ∫1/[x(x+2)]dx=(1/2)ln|x|−(1/2)ln|x+2|+C. (4) Differentiate each answer to check it reproduces the integrand.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: choose an antiderivative method

Integration reverses differentiation, but products and quotients do not have simple reverse rules. Choose a method by inspecting the integrand and asking which derivative pattern it resembles. First simplify algebra and split sums. Always differentiate the proposed antiderivative to check it.

**Substitution** reverses the chain rule: choose u=g(x) when g′(x) appears as a factor. Example: ∫2x cos(x²)dx, let u=x² and du=2x dx, giving sin(x²)+C. For a definite integral either transform both limits to u-values or substitute back before applying the original limits; do not mix the two approaches.

**Integration by parts** reverses the product rule: ∫u dv=uv−∫v du. Choose u so that du is simpler. For ∫x eˣ dx, take u=x, dv=eˣdx; result xeˣ−eˣ+C. For rational functions, **partial fractions** decompose the integrand after factoring the denominator; for example 1/[x(x+1)]=1/x−1/(x+1), so the integral is ln|x|−ln|x+1|+C on intervals avoiding the poles.

Trigonometric integrals use identities and substitution patterns, while trigonometric substitution can simplify radicals such as √(a²−x²). These techniques require practice with domains and absolute values. A table or software result is not a substitute for checking the derivative and stating intervals where the antiderivative is valid.

**Practice with answers.** (1) ∫3x²eˣ³dx=eˣ³+C. (2) ∫x cos x dx=x sin x+cos x+C. (3) ∫1/(x²−1)dx=(1/2)ln|(x−1)/(x+1)|+C. (4) Why include +C for indefinite integrals? Differentiation erases constants, so all antiderivatives differ by a constant on a connected interval.

**Common pitfalls:** selecting u=the more complicated expression in parts; forgetting the Jacobian factor du in substitution; applying logarithm rules across points where the integrand is undefined; and failing to differentiate-check the final expression.
