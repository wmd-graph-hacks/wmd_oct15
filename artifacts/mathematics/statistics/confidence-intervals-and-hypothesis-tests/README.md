---
id: math-statistics-confidence-intervals-and-hypothesis-tests
type: subtopic
title: Confidence intervals and hypothesis tests
parent_topic: math-statistics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-statistics-point-estimation-and-maximum-likelihood
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in confidence intervals and hypothesis tests
  - apply a standard method from confidence intervals and hypothesis tests to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - statistics
  - core-to-advanced
---

# Confidence Intervals and Hypothesis Tests

A confidence interval is produced by a procedure that, under repeated sampling assumptions, covers the fixed parameter at a stated long-run rate. A 95% confidence procedure does not mean there is a 95% probability that this particular fixed parameter lies in the already computed interval. Bayesian credible intervals have a different probability interpretation.

A hypothesis test specifies null H₀ and alternative H₁, a statistic, and a rule for evidence. The p-value is the probability under H₀ of results at least as extreme as observed. It is not the probability H₀ is true, nor the probability results occurred “by chance.” A small p-value indicates incompatibility with H₀ under the model; effect size and study design still matter.

Type I error rejects a true null; Type II error fails to reject a false null. Power is the chance to reject under a particular alternative. Larger samples often increase power but can make tiny, unimportant effects statistically significant.

**Example.** A 95% interval for a mean is 12±2, or [10,14]. If a two-sided test of μ=0 uses the corresponding model and interval procedure, 0 is outside the interval, so the test rejects at 5%. This duality depends on matching assumptions and test construction.

Report estimate, uncertainty interval, test, assumptions, and practical interpretation. Avoid “accept H₀”; say “fail to reject” because absence of strong evidence is not proof of no effect.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: quantify uncertainty and test a claim

A confidence interval is produced by a procedure that, over repeated samples under its assumptions, covers the fixed parameter at a stated rate. A 95% confidence level describes the procedure, not a 95% probability that a fixed parameter lies in this already computed interval. A hypothesis test starts with a null model H₀ and measures how unusual the observed statistic (or more extreme data) would be if H₀ and the model assumptions held.

The p-value is that tail probability under H₀; it is not the probability that H₀ is true or the chance results occurred “by luck.” A small p-value is evidence against H₀, not a measure of effect size. Statistical significance and practical importance are different. Type I error rejects a true null; Type II error fails to reject a false null. Larger samples can detect smaller effects.

**Worked example.** Suppose a mean estimate is 12 with standard error 1. For a large-sample normal approximation, a 95% interval is 12±1.96=[10.04,13.96]. Testing H₀:μ=10 at two-sided 5% is equivalent under matching methods to checking whether 10 lies outside the interval; it does, so reject H₀. Interpret this only if the sampling and model assumptions are reasonable.

**Practice with answers.** (1) p=.03 means data this extreme or more are estimated at 3% under H₀ and the model. (2) It does not mean a 3% chance H₀ is true. (3) If an interval includes the null value, the corresponding two-sided test generally fails to reject at the matching level. (4) Report effect estimate and interval, not only the p-value.

**Common pitfalls:** “accepting” the null; interpreting confidence as a probability about a fixed parameter; omitting assumptions; and treating significance as practical importance or causality.
