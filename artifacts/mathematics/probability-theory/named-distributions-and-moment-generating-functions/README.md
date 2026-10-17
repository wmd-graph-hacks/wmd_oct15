---
id: math-probability-theory-named-distributions-and-moment-generating-functions
type: subtopic
title: Named distributions and moment generating functions
parent_topic: math-probability-theory
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-probability-theory-joint-distributions-expectation-variance
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in named distributions and moment generating functions
  - apply a standard method from named distributions and moment generating functions to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - probability-theory
  - core-to-advanced
---

# Common Distributions and Moment Generating Functions

Choose a distribution from the random mechanism. Bernoulli(p) models one success/failure trial; Binomial(n,p) counts successes across n independent trials; Geometric(p) counts trials to first success; Poisson(λ) models event counts under a constant-rate approximation. Uniform(a,b) has constant density; Exponential(λ) models waiting times; Normal(μ,σ²) models symmetric variation and appears in limit approximations.

For Binomial, E[X]=np and Var(X)=np(1−p). For Poisson, both mean and variance are λ. For Exponential(λ), mean is 1/λ and the memoryless property says the remaining wait distribution does not depend on elapsed time. Verify support and parameterization: some texts define geometric counts beginning at zero, others at one.

A moment-generating function M_X(t)=E[e^{tX}], when finite near zero, encodes moments: M′(0)=E[X], M″(0)=E[X²]. Independent sums multiply MGFs, making them useful for identifying sum distributions. Existence is not guaranteed for every distribution.

**Example.** If X∼Binomial(10,0.2), mean is 2 and variance is 1.6. The probability of exactly two successes is C(10,2)(0.2)²(0.8)⁸≈0.302. The formula follows by choosing which two trials succeed and multiplying independent trial probabilities.

**Practice.** Poisson(4): P(X=0)=e⁻⁴ and E[X]=Var(X)=4. Exponential rate 2 has mean 1/2 and P(X>1)=e⁻². A normal model must specify both center μ and spread σ (or variance σ²).

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: choose a distribution from its mechanism

Bernoulli(p) models one binary trial. Binomial(n,p) counts successes in n independent, identically distributed trials. Geometric(p) counts trials up to the first success. Poisson(λ) models counts over a fixed exposure under a constant-rate independent-event approximation. Uniform(a,b) has constant density; exponential(λ) models waiting time with a memoryless property; normal(μ,σ²) models continuous variation with a symmetric bell shape. State the support and parameters.

Moment generating functions M_X(t)=E[eᵗˣ], when they exist near zero, encode moments: M′(0)=E[X], M″(0)=E[X²]. For independent variables, M_{X+Y}=M_XM_Y. This can identify sums and derive moments, but existence is not guaranteed for every distribution.

**Worked example.** If 10 independent components each fail with probability .02, the number of failures X is Binomial(10,.02). P(X=0)=.98¹⁰≈.817. Its mean is np=.2 and variance np(1−p)=.196. A Poisson(.2) approximation is reasonable for rare events and gives e^(−.2)≈.819, close but not exact.

**Practice with answers.** (1) One coin toss is Bernoulli; 20 tosses counted is binomial. (2) Poisson mean and variance are both λ. (3) Normal standardization maps X to (X−μ)/σ. (4) An exponential waiting time with rate λ has mean 1/λ.

**Common pitfalls:** choosing a named distribution by superficial resemblance; confusing rate with mean; using binomial without independence/equal probabilities; and treating an approximation as an identity.
