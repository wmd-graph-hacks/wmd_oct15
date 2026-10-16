---
id: math-probability-theory-random-variables-and-distributions
type: subtopic
title: Random variables and distributions
parent_topic: math-probability-theory
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-probability-theory-probability-spaces-and-conditional-probability
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in random variables and distributions
  - apply a standard method from random variables and distributions to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - probability-theory
  - core-to-advanced
---

# Random Variables and Distributions

A random variable X assigns a number to each outcome. Its cumulative distribution function F(x)=P(X≤x) determines its distribution. For a discrete variable, probabilities are given by a probability mass function p(x); for a continuous variable, a density f integrates to probabilities over intervals. A density value is not itself a probability, and a continuous variable has P(X=a)=0.

For a discrete X, E[X]=Σxp(x); for a continuous X, E[X]=∫xf(x)dx when the expectation exists. Transformations use the distribution, not simply an informal substitution: if Y=g(X), then P(Y≤y)=P(g(X)≤y), with inequalities handled according to g’s monotonicity.

**Example.** Let X be uniform on [0,1], so f(x)=1 there. For Y=X², since square is increasing on this domain, F_Y(y)=P(X≤√y)=√y for 0≤y≤1; differentiating gives f_Y(y)=1/(2√y). Its density becomes large near zero but remains integrable, and probabilities are areas under the density.

A distribution model should match the mechanism: Bernoulli for one binary trial, binomial for a fixed number of independent identical binary trials, and Poisson for counts under a rate model. State parameters and support so the model is unambiguous.

**Practice.** For X∼Uniform(0,2), P(X<1/2)=1/4, E[X]=1, Var(X)=1/3. For a discrete variable taking 0,1 with equal probabilities, E[X]=1/2 and Var(X)=1/4.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: random variables and distribution functions

A random variable X assigns a numerical value to each outcome. Its distribution describes probabilities of values or ranges. For discrete X, the probability mass function p(x)=P(X=x) sums to 1. For continuous X, a density f(x) is nonnegative and integrates to 1; P(a≤X≤b)=∫ₐᵇf(x)dx, and a single point has probability zero. The cumulative distribution F(x)=P(X≤x) works for both cases.

Expectation is a probability-weighted average: Σx p(x) for discrete variables and ∫x f(x)dx for continuous variables. Variance E[(X−μ)²] measures spread and equals E[X²]−μ². For aX+b, expectation is aμ+b and variance is a²Var(X). Standardization Z=(X−μ)/σ expresses distance from the mean in standard deviations.

**Worked example.** A fair six-sided die has E[X]=(1+…+6)/6=3.5. E[X²]=91/6, so Var(X)=91/6−(7/2)²=35/12. A die roll is discrete; treating its six outcomes as a continuous uniform density would be a different model.

**Practice with answers.** (1) For a fair coin coded 0/1, mean and variance are both 1/2 and 1/4, respectively. (2) If X has mean 10 and variance 9, then 2X+1 has mean 21 and variance 36. (3) A continuous uniform variable on [0,2] has mean 1 and variance 1/3. (4) Check a proposed pmf by summing probabilities and a density by integrating it over its support.

**Common pitfalls:** confusing density height with probability; forgetting support; assuming expectation must be a possible outcome; and scaling standard deviation like variance.
