---
id: math-linear-algebra-singular-value-decomposition
type: subtopic
title: Singular Value Decomposition
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-spectral-theorem-and-quadratic-forms
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in singular value decomposition
  - apply a standard method from singular value decomposition to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Singular Value Decomposition

Every real m×n matrix has an SVD A=UΣVᵀ, where U and V are orthogonal and Σ has nonnegative singular values σ₁≥σ₂≥…. The columns of V are input directions; A maps them to orthogonal output directions U scaled by σᵢ. Singular values are square roots of eigenvalues of AᵀA.

SVD works for rectangular and rank-deficient matrices. It reveals rank (number of nonzero singular values), operator norm (σ₁), and condition number (σ₁/σᵣ for nonzero values). The pseudoinverse replaces each nonzero σᵢ with 1/σᵢ and gives least-squares solutions; very small singular values amplify noise, so truncated SVD can regularize.

**Example.** If A=diag(3,1), its singular values are 3 and 1. For any unit vector x, ||Ax|| lies between 1 and 3. Truncating to rank 1 gives diag(3,0), the closest rank-1 matrix to A in both spectral and Frobenius norms (Eckart–Young theorem).

Applications include data compression, denoising, principal component analysis, and solving ill-conditioned systems. The mathematics identifies a best low-rank approximation; choosing how many components to retain remains a modeling decision.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: singular values as stretch factors

Every real m×n matrix A has a singular value decomposition A=UΣVᵀ, where U and V are orthogonal and Σ is diagonal-shaped with nonnegative singular values σ₁≥σ₂≥…. The right singular vectors in V are input directions; A maps each vᵢ to σᵢuᵢ. Singular values measure stretch, rank is the number of positive singular values, and the condition number σ₁/σᵣ (for nonzero smallest σᵣ) measures sensitivity on the row space.

SVD exists for rectangular and rank-deficient matrices, unlike eigenvalue diagonalization. It gives the best rank-k approximation: keeping the k largest singular values minimizes both spectral-norm and Frobenius-norm error among rank-k matrices. This supports compression, denoising, and principal component analysis. Small singular values also explain why some inverse problems amplify noise.

**Worked example.** For A=diag(3,1), singular values are 3 and 1; the coordinate directions are already singular vectors. The matrix stretches the first coordinate by 3 and the second by 1. Its 2-norm condition number is 3. If the second diagonal entry were 0.001, the condition number would be 3000, so small data errors could cause much larger solution errors.

**Practice with answers.** (1) Rank equals the number of nonzero singular values. (2) For an orthogonal matrix, all singular values are 1. (3) The best rank-1 approximation to diag(5,2) is diag(5,0). (4) Why are singular values nonnegative? They are square roots of the nonnegative eigenvalues of AᵀA.

**Common pitfalls:** confusing singular values with eigenvalues; assuming A is square; treating a tiny singular value as exactly zero without a tolerance policy; and claiming truncation preserves all information.
