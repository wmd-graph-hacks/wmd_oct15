---
id: math-statistics-anova-and-regression
type: subtopic
title: ANOVA and regression
parent_topic: math-statistics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-statistics-confidence-intervals-and-hypothesis-tests
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in anova and regression
  - apply a standard method from anova and regression to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - statistics
  - core-to-advanced
---

# ANOVA and Regression

Analysis of variance (ANOVA) compares group means by partitioning total variation into between-group and within-group components. The F statistic compares variation explained by group differences with unexplained variation. A significant omnibus test says not all means are equal; it does not identify which groups differ, so planned contrasts or corrected post-hoc comparisons may be needed.

Linear regression models a response as a linear combination of predictors plus error. In simple regression y=β₀+β₁x+ε, β₁ is the expected response change per unit x under the model. Least squares estimates coefficients by minimizing squared residuals. Inspect residual plots for nonlinearity, unequal variance, dependence, and outliers; correlation or regression alone does not establish causation.

Logistic regression models log odds: log[p/(1−p)]=β₀+β₁x. A one-unit increase in x multiplies odds by e^β₁, holding other predictors fixed. Odds are not probabilities; translating back requires the baseline context.

**Example.** If β₁=0.4 in logistic regression, the odds ratio is e^0.4≈1.49: odds are about 49% higher per unit x under the fitted model. The probability change depends on starting probability and is not constant.

Distinguish interpolation from extrapolation. Predictions beyond observed predictor ranges rely on stronger assumptions and may be unreliable.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: compare means and model relationships

ANOVA compares group means by separating between-group variation from within-group variation. The F statistic is a ratio of mean squares; a large value suggests at least one group mean differs under the model. A significant result does not identify which groups differ, so follow-up comparisons need multiplicity control. Standard assumptions include independent observations and an appropriate residual model.

Linear regression models a response as β₀+β₁x plus error. Least squares chooses coefficients minimizing squared residuals. The slope describes the expected response change per unit predictor under the model. Inspect residual plots for nonlinearity, changing spread, outliers, and dependence. Logistic regression models log-odds for binary outcomes; exponentiating a coefficient gives an odds ratio, not a constant probability increase.

**Worked example.** For points (1,2),(2,3),(3,5), x̄=2 and ȳ=10/3. The least-squares slope is Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²=3/2; intercept is 10/3−(3/2)·2=1/3. The fitted line is ŷ=1/3+1.5x. Residuals reveal how the line misses observations.

**Practice with answers.** (1) A slope of −2 means fitted response falls 2 units per predictor unit. (2) An ANOVA rejection means not all means are equal, not that every pair differs. (3) In logistic regression β=0.4 corresponds to odds multiplier e^.4≈1.49. (4) Association alone does not establish causation.

**Common pitfalls:** extrapolating far beyond observed x; reading R² as proof of a valid model; interpreting an odds ratio as risk ratio; and using many pairwise tests without adjustment.
