---
id: math-statistics-point-estimation-and-maximum-likelihood
type: subtopic
title: Point estimation and maximum likelihood
parent_topic: math-statistics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-probability-theory
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in point estimation and maximum likelihood
  - apply a standard method from point estimation and maximum likelihood to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - statistics
  - core-to-advanced
---

# Point Estimation and Maximum Likelihood

An estimator is a rule mapping sample data to a parameter estimate. Its sampling distribution describes how it varies across repeated samples. Bias is E[θ̂]−θ; variance measures spread; mean squared error equals variance plus squared bias. Unbiasedness alone does not guarantee usefulness—a high-variance estimator can be poor. Consistency means estimates converge to the true parameter as sample size grows under stated assumptions.

Maximum likelihood chooses the parameter that makes observed data most probable under a model. For independent observations, likelihood is the product of individual probabilities or densities; log-likelihood converts products to sums and is easier to optimize. Likelihood is a function of the parameter with data held fixed; it is not automatically a probability distribution over parameters.

**Example.** For Bernoulli observations xᵢ∈{0,1}, likelihood is p^(Σxᵢ)(1−p)^(n−Σxᵢ). Log-likelihood derivative is (Σxᵢ)/p−(n−Σxᵢ)/(1−p). Setting it to zero yields p̂=Σxᵢ/n, the sample proportion. Boundary cases with all zeros or ones give estimates 0 or 1.

Check model assumptions, parameter constraints, and whether an optimum is interior or on a boundary. A numerical estimate without an uncertainty statement can convey false precision.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: estimate a parameter from a sample

A statistic is a quantity computed from observed data; an estimator is a rule for estimating a population parameter. The sample mean estimates a population mean, and the sample proportion estimates a population proportion. Bias is the difference between an estimator’s expected value and the target. Variability describes how estimates change across repeated samples. Mean squared error combines variance and squared bias.

Maximum likelihood chooses the parameter value that makes the observed data most likely under a model. For independent observations, likelihoods multiply; log-likelihoods add and are easier to optimize. Check parameter bounds and whether the maximum occurs at an interior point or boundary. A point estimate alone does not capture sampling uncertainty.

**Worked example.** For 5 Bernoulli trials with 4 successes, L(p)=p⁴(1−p). The log likelihood is 4ln p+ln(1−p). Setting its derivative 4/p−1/(1−p)=0 gives p̂=4/5. This matches the sample proportion. If all observations are successes, the MLE is the boundary p̂=1.

**Practice with answers.** (1) For 20 trials with 7 successes, p̂=0.35. (2) The sample mean of 2,4,9 is 5. (3) Why take logs? Log is increasing, so it preserves the maximizing parameter while turning products into sums. (4) Repeated samples, not repeated measurements of one fixed sample, describe estimator sampling variability.

**Common pitfalls:** confusing a parameter with its estimate; assuming unbiased means always close; maximizing likelihood without considering boundaries; and reporting many decimal places unsupported by sample size.
