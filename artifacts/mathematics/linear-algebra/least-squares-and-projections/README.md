---
id: math-linear-algebra-least-squares-and-projections
type: subtopic
title: Least squares and projections
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-inner-products-and-orthogonality
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in least squares and projections
  - apply a standard method from least squares and projections to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Least Squares and Orthogonal Projection

When Ax=b has no exact solution, least squares chooses x minimizing ||Ax−b||₂. The vector Ax lies in the column space of A, so the best approximation is the orthogonal projection of b onto that space. Therefore the residual r=b−Ax is orthogonal to every column: Aᵀr=0, yielding the normal equations AᵀAx=Aᵀb.

If columns of A are independent, the minimizer is unique. Directly solving normal equations can worsen conditioning because cond(AᵀA) is roughly cond(A)². QR factorization A=QR gives R x=Qᵀb and is generally more stable. For rank-deficient systems, use SVD or a pseudoinverse and state which solution criterion is chosen (often minimum norm).

**Example.** Fit y≈c to data 1 and 3. The least-squares constant minimizes (c−1)²+(c−3)². Differentiate to get 4c−8=0, so c=2, the mean. Residuals are −1 and 1 and sum to zero: they are orthogonal to the constant column (1,1).

In regression, a small residual does not prove a good model. Check residual patterns, assumptions, data quality, and uncertainty. Least squares optimizes a specific error measure; outliers can strongly influence squared error.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: fitting data by projection

An overdetermined system Ax≈b may have no exact solution. Least squares chooses x minimizing ‖Ax−b‖². At the minimum, the residual r=b−Ax is orthogonal to every column of A; therefore AᵀAx=Aᵀb, the normal equations. If A has full column rank, AᵀA is invertible. In computation, QR factorization is usually more stable than explicitly forming AᵀA.

Geometrically, Ax is the projection of b onto the column space of A. The error vector is perpendicular to that space. This interpretation explains why least squares is useful for regression, calibration, and noisy measurements. Scaling columns and inspecting residuals can reveal poor conditioning or a model that misses structure.

**Worked example.** Fit y≈c to observations 1, 2, and 4. The model matrix is a column of ones, and the least-squares constant is the mean c=(1+2+4)/3=7/3. Residuals are −4/3, −1/3, and 5/3; they sum to zero, so the residual is orthogonal to the constant column. The fitted value minimizes total squared error.

**Practice with answers.** (1) The least-squares constant for 2, 2, 8 is 4. (2) What does a zero residual mean? An exact solution exists. (3) If columns of A are dependent, the fitted vector may still be unique as a projection, while coefficient vectors may not be unique. (4) Why inspect residuals? Patterns indicate model mismatch; random scatter is more consistent with the model assumptions.

**Common pitfalls:** minimizing absolute errors while using squared-error equations; interpreting correlation as causation; solving normal equations with a singular matrix without checking rank; and forgetting that a good fit does not establish a good causal model.
