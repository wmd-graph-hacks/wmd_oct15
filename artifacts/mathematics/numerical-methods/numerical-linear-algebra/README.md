---
id: math-numerical-methods-numerical-linear-algebra
type: subtopic
title: Numerical linear algebra
parent_topic: math-numerical-methods
phase: applied-core
estimated_minutes: 60
prerequisites:
  - id: math-numerical-methods-numerical-differentiation-and-integration
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in numerical linear algebra
  - apply a standard method from numerical linear algebra to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - numerical-methods
  - applied-core
---

# Numerical Linear Algebra

LU factorization writes A=LU (with pivoting, PA=LU) and supports repeated solves. QR writes A=QR with orthogonal Q and triangular R; it is central to stable least squares. For large sparse problems, iterative methods such as conjugate gradients (symmetric positive definite A) can be more efficient than dense factorization.

Conditioning governs sensitivity; algorithmic stability governs computed error. Pivoting avoids dividing by tiny pivots. Orthogonal transformations preserve Euclidean norms, which helps explain QR stability. Iterative solvers stop based on residual norms, but preconditioning may be needed to accelerate convergence.

**Example.** Solve [[2,1],[1,3]]x=(1,2). Elimination gives x₁=1/5, x₂=3/5. Substitution checks the residual is zero exactly. In floating point, examine a scaled residual and conditioning rather than expecting exact zeros.

For symmetric positive definite matrices, Cholesky is efficient. Choose a method based on matrix size, sparsity, symmetry, and whether multiple right-hand sides will be solved.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: factor a system and solve efficiently

Gaussian elimination transforms Ax=b into an equivalent triangular system. LU factorization A=LU stores elimination work and is useful when solving repeatedly with the same matrix. Pivoting swaps rows to avoid dividing by a tiny pivot and improves numerical stability. QR factorization A=QR uses orthogonal transformations and is preferred for least squares because it preserves lengths and avoids squaring the condition number as normal equations do.

For very large sparse systems, iterative methods such as Jacobi, Gauss–Seidel, and conjugate gradient can be faster and use less memory. Convergence depends on matrix properties and the method; monitor residuals and stopping criteria. Preconditioning transforms a system to improve conditioning while preserving its solution.

**Worked example.** Solve 2x+y=5 and x+3y=6. Eliminate x: twice the second equation is 2x+6y=12; subtract the first to get 5y=7, y=1.4, then x=1.8. Substitution verifies both equations. For larger systems, factorization automates these same steps while pivoting guards against unstable divisions.

**Practice with answers.** (1) The solution to x+y=3, x−y=1 is (2,1). (2) QR’s Q has orthonormal columns. (3) LU is useful for multiple right-hand sides with one A. (4) A small residual is useful but should be interpreted alongside conditioning.

**Common pitfalls:** explicitly computing A⁻¹ to solve a system; ignoring pivoting; using iterative methods without checking convergence; and mistaking residual size for forward solution error.
