---
id: math-linear-algebra-determinants-and-invertibility
type: subtopic
title: Determinants and invertibility
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-linear-maps-and-rank-nullity
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in determinants and invertibility
  - apply a standard method from determinants and invertibility to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Determinants and Invertibility

The determinant det(A) is a scalar that measures oriented volume scaling of the linear map x↦Ax. In ℝ², |det A| is the area scale; in ℝ³ it is the volume scale. A negative determinant reverses orientation. A matrix is invertible exactly when its determinant is nonzero, equivalently when its columns are independent, its kernel is {0}, and its linear system has a unique solution for every right-hand side.

For 2×2 matrices, det[[a,b],[c,d]]=ad−bc. Determinants are multiplicative: det(AB)=det(A)det(B). Swapping rows changes sign; scaling a row scales the determinant; adding a multiple of one row to another leaves it unchanged. These rules support efficient computation. Cofactor expansion is useful for small matrices or matrices with many zeros, but is inefficient for large dense matrices.

**Example.** A=[[2,1],[3,2]] has determinant 4−3=1, so it is invertible. Its inverse is [[2,−1],[−3,2]]. Verify by multiplication. The parallelogram spanned by its columns has area 1, although the columns are not unit or perpendicular.

Do not compute a large determinant to solve a numerical system; use factorizations. Determinants can be mathematically informative but numerically misleading due to scale and roundoff.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: determinant as an invertibility test

For a 2×2 matrix [[a,b],[c,d]], det=ad−bc. A square matrix is invertible exactly when its determinant is nonzero. Geometrically, the absolute determinant is the area or volume scaling factor of the associated linear map; a zero determinant means the map collapses dimension. Swapping two rows changes the sign, multiplying a row by k scales the determinant by k, and adding a multiple of one row to another leaves it unchanged.

For larger matrices, cofactor expansion is useful when a row or column has many zeros; elimination is often more efficient for numerical computation. A triangular matrix has determinant equal to the product of its diagonal entries. Row swaps and row scaling must be tracked during elimination. Cramer’s rule gives formulas for a unique solution when det(A)≠0, but it is generally inefficient for large systems.

**Worked example.** For A=[[2,1],[5,3]], det(A)=6−5=1, so A is invertible and A⁻¹=[[3,−1],[−5,2]]. Check by multiplying A A⁻¹=I. If the second row were twice the first, the determinant would be zero; the rows would be dependent and the system would not have a unique solution for every right-hand side.

**Practice with answers.** (1) det([[1,2],[3,4]])=−2. (2) A 3×3 triangular matrix with diagonal 2,−1,4 has determinant −8. (3) If det(A)=5 for a 3×3 matrix, det(2A)=2³·5=40. (4) If two rows are identical, determinant is 0.

**Common pitfalls:** using the 2×2 shortcut for larger matrices; forgetting cofactor signs alternate; treating a zero determinant as proof the system has no solutions (it may have infinitely many); and ignoring row-swap sign changes.
