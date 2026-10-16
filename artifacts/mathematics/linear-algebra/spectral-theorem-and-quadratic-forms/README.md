---
id: math-linear-algebra-spectral-theorem-and-quadratic-forms
type: subtopic
title: Spectral theorem and quadratic forms
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-least-squares-and-projections
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in spectral theorem and quadratic forms
  - apply a standard method from spectral theorem and quadratic forms to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Spectral Theorem and Quadratic Forms

A real symmetric matrix A has an orthonormal basis of eigenvectors: A=QΛQᵀ, where QᵀQ=I and Λ is diagonal with real eigenvalues. This spectral theorem is stronger than ordinary diagonalization because it guarantees an orthogonal change of coordinates. Symmetry is essential.

A quadratic form is q(x)=xᵀAx. With y=Qᵀx, it becomes q=yᵀΛy=Σλᵢyᵢ². If all eigenvalues are positive, q is positive definite; nonnegative eigenvalues give positive semidefinite; mixed signs indicate indefiniteness. These classifications describe curvature and stability.

**Example.** For A=[[2,1],[1,2]], eigenvectors (1,1) and (1,−1) have eigenvalues 3 and 1. In orthonormal eigen-coordinates q=3y₁²+y₂², so q>0 for every nonzero x: A is positive definite. In optimization, a positive definite Hessian at a critical point gives a strict local minimum.

Under a general invertible coordinate change x=Sy, quadratic matrices transform by congruence SᵀAS, not similarity S⁻¹AS. Similarity preserves eigenvalues; congruence preserves inertia (counts of positive, negative, zero directions) under Sylvester’s law.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: symmetric matrices and quadratic forms

The spectral theorem says every real symmetric matrix A has an orthonormal eigenbasis: A=QΛQᵀ with QᵀQ=I. The change of coordinates y=Qᵀx removes cross terms from the quadratic form xᵀAx, giving yᵀΛy=Σλᵢyᵢ². Eigenvalue signs classify the form: all positive means positive definite; all nonnegative means positive semidefinite; mixed signs mean indefinite.

For a quadratic function f(x)=xᵀAx+bᵀx+c with symmetric A, the gradient is 2Ax+b and Hessian is 2A. At a stationary point, positive definite Hessian gives a strict minimum; negative definite gives a strict maximum; an indefinite Hessian gives a saddle. For constrained or nonstationary cases, inspect the domain and boundary too.

**Worked example.** For f(x,y)=x²+4xy+y², the matrix is A=[[1,2],[2,1]]. Its eigenvalues are 3 and −1, so the form is indefinite. Indeed along (1,1) it is positive, while along (1,−1) it is negative. The origin is a saddle for this quadratic function.

**Practice with answers.** (1) x²+2y² is positive definite because its eigenvalues are 1 and 2. (2) x²−y² is indefinite. (3) For a symmetric matrix, eigenvectors from distinct eigenvalues are orthogonal. (4) Diagonalization by an orthogonal Q preserves lengths and angles, which is why it is especially useful in geometry and data analysis.

**Common pitfalls:** applying the real symmetric spectral theorem to arbitrary matrices; classifying using diagonal entries alone; and ignoring the domain or constraints when interpreting a Hessian test.
