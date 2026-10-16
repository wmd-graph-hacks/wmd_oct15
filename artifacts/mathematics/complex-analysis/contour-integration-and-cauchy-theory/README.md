---
id: math-complex-analysis-contour-integration-and-cauchy-theory
type: subtopic
title: Contour integration and Cauchy theory
parent_topic: math-complex-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-complex-analysis-holomorphic-functions-and-cauchy-riemann
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in contour integration and cauchy theory
  - apply a standard method from contour integration and cauchy theory to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - complex-analysis
  - advanced-core
---

# Contour Integrals and Cauchy’s Theorems

A contour is a piecewise smooth oriented curve z(t). Its integral is ∫C f(z)dz=∫ f(z(t))z′(t)dt. Orientation matters: reversing a contour changes the sign. Complex line integrals differ from real arc-length integrals because dz carries direction.

Cauchy’s theorem says that if f is holomorphic on a suitable simply connected region, its integral around a closed contour is zero. Cauchy’s integral formula states f(a)=(1/2πi)∮C f(z)/(z−a) dz when a is inside a positively oriented simple contour. It expresses interior values using boundary values and implies strong derivative formulas.

**Example.** For |a|<R, ∮_|z|=R dz/(z−a)=2πi. Parameterize circle or apply the formula to constant f=1. If |a|>R, the pole is outside and the integral is 0 by Cauchy’s theorem. Location relative to the contour changes the answer.

Check that the function is holomorphic on and inside the contour except for explicitly handled singularities, and respect orientation. Cauchy’s theorem cannot be applied across a pole or hole.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: integrate around a contour

For a parametrized curve z(t), a contour integral is ∫ f(z(t))z′(t)dt. Orientation matters: reversing a contour changes the sign. Cauchy’s theorem says the integral of a holomorphic function around a closed contour is zero under suitable domain conditions, such as a simply connected region. Cauchy’s integral formula recovers interior values: f(a)=(1/2πi)∮ f(z)/(z−a) dz.

These results imply strong consequences: holomorphic functions have derivatives of all orders, and values inside a contour are controlled by boundary values. If a region has holes or singularities inside, check the hypotheses carefully; a contour integral may not vanish.

**Worked example.** Evaluate ∮|z|=2 dz/z counterclockwise. Parametrize z=2e^{it}, dz=2ie^{it}dt; dz/z=i dt. Integrating t=0 to 2π gives 2πi. The integrand has a singularity at 0 inside the contour, so Cauchy’s theorem does not imply zero.

**Practice with answers.** (1) ∮|z|=1 z² dz=0. (2) ∮|z|=1 dz/z=2πi. (3) Reversing orientation negates the integral. (4) Cauchy’s integral formula requires the point to lie inside and f holomorphic on/inside the contour (with suitable neighborhood conditions).

**Common pitfalls:** ignoring contour orientation; applying Cauchy’s theorem across a singularity or hole; and forgetting dz’s factor in parametrization.
