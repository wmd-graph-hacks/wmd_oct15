---
id: math-linear-algebra-eigenvalues-diagonalization-jordan-form
type: subtopic
title: Eigenvalues, diagonalization, Jordan form
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-determinants-and-invertibility
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in eigenvalues, diagonalization, jordan form
  - apply a standard method from eigenvalues, diagonalization, jordan form to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Eigenvalues, Diagonalization, and Jordan Form

An eigenvector v≠0 of A satisfies Av=λv; λ is an eigenvalue. Solve det(A−λI)=0 for eigenvalues, then solve (A−λI)v=0 for eigenvectors. Eigenvectors identify directions whose direction is preserved by the transformation, though their scale may change or reverse.

A matrix is diagonalizable if it has a basis of eigenvectors. Then A=PDP⁻¹, making powers easy: Aⁿ=PDⁿP⁻¹. Distinct eigenvalues guarantee independent eigenvectors, but repeated eigenvalues require checking geometric multiplicity (eigenspace dimension). If there are too few eigenvectors, Jordan form uses generalized eigenvectors to organize the remaining structure.

**Example.** A=[[2,1],[0,2]] has characteristic polynomial (2−λ)² and only eigenvalue 2. Solving (A−2I)v=0 gives y=0, so eigenspace has dimension 1. It is not diagonalizable. The matrix is already a Jordan block; its powers are [[2ⁿ,n2ⁿ⁻¹],[0,2ⁿ]]. This shows why repeated eigenvalues alone do not imply diagonalization.

For a system x′=Ax, eigenvalues also describe exponential modes e^{λt}; real parts govern growth or decay. Complex eigenvalues produce oscillatory components. Always distinguish algebraic multiplicity (root multiplicity) from geometric multiplicity (dimension of eigenspace).

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: eigenvectors and repeated action

An eigenvector v≠0 of A satisfies Av=λv; the scalar λ is its eigenvalue. Solve det(A−λI)=0 for eigenvalues, then find the null space of A−λI for eigenvectors. Eigenvectors describe directions whose span is preserved by the transformation. A matrix is diagonalizable when it has a basis of eigenvectors, so A=PDP⁻¹ and Aⁿ=PDⁿP⁻¹. This makes repeated transformations and linear recurrences easier to analyze.

For an n×n matrix, eigenvalues are roots of the characteristic polynomial, counted with algebraic multiplicity. Each eigenspace dimension is its geometric multiplicity and cannot exceed algebraic multiplicity. Distinct eigenvalues have independent eigenvectors; repeated eigenvalues may or may not supply enough eigenvectors. If they do not, Jordan form organizes generalized eigenvectors and reveals polynomial factors multiplying λⁿ in powers of A.

**Worked example.** For A=[[2,1],[0,3]], eigenvalues are 2 and 3. For λ=2, solving (A−2I)v=0 gives v=(1,0). For λ=3, v=(1,1). These are independent, so P=[[1,1],[0,1]], D=diag(2,3), and A=PDP⁻¹. Therefore powers can be computed from the simple diagonal entries.

**Practice with answers.** (1) For diag(4,−1), the standard basis vectors are eigenvectors with eigenvalues 4 and −1. (2) A 2×2 matrix with two distinct eigenvalues is diagonalizable. (3) Is [[1,1],[0,1]] diagonalizable? No: eigenvalue 1 has only one independent eigenvector. (4) Why exclude v=0 from eigenvectors? It satisfies Av=λv for every λ and conveys no invariant direction.

**Common pitfalls:** reporting zero as an eigenvector; computing eigenvectors before solving the characteristic equation; assuming every matrix is diagonalizable; and confusing similar matrices with equal entries (similarity means the same linear map in different bases).
