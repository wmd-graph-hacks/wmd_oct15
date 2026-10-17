---
id: math-probability-theory-joint-distributions-expectation-variance
type: subtopic
title: Joint distributions, expectation, variance
parent_topic: math-probability-theory
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-probability-theory-random-variables-and-distributions
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in joint distributions, expectation, variance
  - apply a standard method from joint distributions, expectation, variance to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - probability-theory
  - core-to-advanced
---

# Joint Distributions, Expectation, and Variance

For random variables X,Y, a joint distribution describes probabilities of pairs. Marginal distributions are obtained by summing or integrating over the other coordinate. Conditional distributions describe one variable after the other is observed. Independence means the joint distribution factors into the product of marginals.

Linearity of expectation always holds when expectations exist: E[aX+bY]=aE[X]+bE[Y], even without independence. Variance Var(X)=E[(X−E[X])²]=E[X²]−E[X]². For a sum, Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y), where Cov(X,Y)=E[XY]−E[X]E[Y]. Independence implies zero covariance when moments exist, but zero covariance does not generally imply independence.

**Example.** Two fair dice have independent values X,Y, each with mean 3.5 and variance 35/12. Their sum S has mean 7 and variance 35/6. If instead Y=X, then S=2X, variance is 4·35/12=35/3; dependence changes the spread even though the marginal distributions are unchanged.

For a transformation g(X), use E[g(X)]=Σg(x)p(x) or ∫g(x)f(x)dx. Do not substitute g(E[X]) for E[g(X)] unless special conditions justify it; generally these differ.

**Practice.** If E[X]=2 and E[Y]=−1, E[3X−2Y]=8. If Var(X)=4, Var(2X+1)=16. If X,Y independent with variances 4 and 9, Var(X−Y)=13.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: joint behavior and dependence

A joint distribution describes two or more random variables together. For discrete variables, joint probabilities sum to 1 over pairs; marginal distributions sum over the other variable. Conditional distributions divide joint probabilities by the conditioning marginal when it is positive. For continuous variables, integrate a joint density over regions and integrate out coordinates to get marginals.

Covariance Cov(X,Y)=E[(X−μX)(Y−μY)]=E[XY]−E[X]E[Y] indicates whether variables tend to vary together. Correlation divides covariance by σXσY to obtain a unit-free value in [−1,1]. Independence implies zero covariance when moments exist, but zero covariance does not generally imply independence. For sums, Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y); independence removes the covariance term.

**Worked example.** Let X and Y be independent fair 0/1 variables. E[X]=E[Y]=1/2, E[XY]=1/4, so covariance is 0. For S=X+Y, variance is 1/4+1/4=1/2. If instead Y=X, covariance is 1/4 and variance of X+Y=4Var(X)=1, showing why dependence matters.

**Practice with answers.** (1) For a joint table, obtain P(X=x) by summing the row/column over all y. (2) If X,Y are independent, E[XY]=E[X]E[Y]. (3) Cov(X,X)=Var(X). (4) If Cov=0, one may conclude no linear association, but not necessarily independence.

**Common pitfalls:** summing a joint table incorrectly; assuming zero correlation proves independence; and omitting covariance when finding the variance of a dependent sum.
