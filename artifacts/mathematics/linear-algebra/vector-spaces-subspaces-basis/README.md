---
id: math-linear-algebra-vector-spaces-subspaces-basis
type: subtopic
title: Vector spaces, subspaces, basis
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-foundations-of-mathematics
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in vector spaces, subspaces, basis
  - apply a standard method from vector spaces, subspaces, basis to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Vector Spaces, Subspaces, and Bases

A vector space over a field is a set with addition and scalar multiplication satisfying familiar algebraic rules. Examples include ℝⁿ, polynomials of degree at most n, and continuous functions on an interval. A subset W is a subspace if it contains zero and is closed under linear combinations: au+bv∈W whenever u,v∈W and scalars a,b are allowed.

A span is the set of all linear combinations of given vectors. Vectors are linearly independent when the only combination equal to zero uses all zero coefficients. A basis is an independent spanning set. Coordinates relative to a basis are unique; dimension is the number of vectors in any basis.

**Example.** W={(x,y,z):x+y+z=0} is a subspace of ℝ³. Solve z=−x−y, so (x,y,z)=x(1,0,−1)+y(0,1,−1). These two vectors span W and are independent, hence form a basis and dim W=2. By contrast, {(x,y):x+y=1} is not a subspace because it does not contain (0,0).

For a matrix, pivot columns identify independent directions, but the basis for the column space uses the corresponding columns of the original matrix. Row reduction preserves solution information and rank, but not the actual column vectors. That distinction prevents a common basis error.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: spanning, independence, and dimension

A vector space V over a field F supports addition and scalar multiplication with the familiar rules. Common examples are ℝⁿ, polynomials, and functions. A subspace W must contain zero and be closed under every linear combination: if u,v∈W and a,b∈F, then au+bv∈W. A set defined by homogeneous linear equations is a subspace; a shifted line such as x+y=1 is not because it misses zero.

The span of vectors v₁,…,vₖ is every combination c₁v₁+…+cₖvₖ. They are linearly independent if the only solution of c₁v₁+…+cₖvₖ=0 is all cᵢ=0. A basis is an independent spanning set. In a finite-dimensional space every basis has the same number of vectors; this number is the dimension. Coordinates relative to a chosen basis are unique.

**Worked example.** Solve x+y+z=0. Set x=s and y=t, so z=−s−t. Then (x,y,z)=s(1,0,−1)+t(0,1,−1). These vectors span the solution plane. If a(1,0,−1)+b(0,1,−1)=0, the first and second coordinates force a=b=0, so they are independent and form a basis. The plane has dimension 2.

For matrix calculations, pivot positions reveal rank and independent columns. To form a basis for the column space, use pivot columns from the original matrix, not the row-reduced matrix; row operations preserve dependence relations but change the actual column vectors. A homogeneous system Ax=0 gives the null space, while Ax=b may be empty or an affine translate rather than a subspace.

**Practice with answers.** (1) Is {(x,y):x=2y} a subspace? Yes; it is span{(2,1)}. (2) Is {(x,y):x=2y+1} a subspace? No; it omits zero. (3) Do (1,0) and (2,0) form a basis of ℝ²? No; they are dependent and do not span ℝ². (4) A basis of the polynomials of degree ≤2 is {1,x,x²}, so dimension is 3.

**Common pitfalls:** checking closure under addition but forgetting scalar multiplication; calling a spanning set a basis without independence; confusing row-space and column-space bases; and assuming a solution set to an inhomogeneous system is a vector subspace.
