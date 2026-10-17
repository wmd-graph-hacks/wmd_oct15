---
id: math-linear-algebra-linear-maps-and-rank-nullity
type: subtopic
title: Linear maps and rank-nullity
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-vector-spaces-subspaces-basis
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in linear maps and rank-nullity
  - apply a standard method from linear maps and rank-nullity to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Linear Maps and Rank–Nullity

A map T:V→W is linear when T(u+v)=T(u)+T(v) and T(cv)=cT(v). Once bases are chosen, T is represented by a matrix A; applying T becomes matrix multiplication. The kernel ker(T) consists of inputs sent to zero; the image im(T) consists of outputs attained. The kernel describes lost directions, while the image describes reachable directions.

The rank–nullity theorem states dim(V)=dim ker(T)+dim im(T) for finite-dimensional V. It explains why solving Ax=b depends on rank: if the nullity is positive, a consistent system has infinitely many solutions; if full column rank, a consistent solution is unique.

**Example.** T:ℝ³→ℝ² defined by T(x,y,z)=(x+y,y+z) has matrix [[1,1,0],[0,1,1]]. Solving T(x,y,z)=0 gives x=−y and z=−y, so kernel is span{(−1,1,−1)}, dimension 1. The rank is 2, and 3=1+2 confirms rank-nullity. Since rank equals the output dimension, T is onto.

A matrix’s columns are images of domain basis vectors. Changing bases changes the matrix but not the underlying map. For an endomorphism (same domain and codomain), similar matrices represent the same map in different bases.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: transformations, matrices, and rank-nullity

A linear map T:V→W preserves addition and scalar multiplication: T(au+bv)=aT(u)+bT(v). Once bases are chosen, T is represented by a matrix. Its columns are the coordinate vectors of the images of the domain basis vectors. Composition of maps corresponds to matrix multiplication, and the order matters: applying S then T gives matrix [T][S].

The kernel ker(T)={v:T(v)=0} measures inputs collapsed to zero; the image im(T)={T(v):v∈V} is the set of reachable outputs. Rank-nullity for finite-dimensional V says dim(V)=dim ker(T)+dim im(T). Thus a map from ℝⁿ to ℝᵐ cannot have rank exceeding either dimension. For a square matrix, injective, surjective, invertible, and full rank are equivalent.

**Worked example.** T:ℝ³→ℝ² with T(x,y,z)=(x+y,y+z). Its matrix is [[1,1,0],[0,1,1]]. Solving T(x,y,z)=0 gives x=−y and z=−y, so ker(T)=span{(−1,1,−1)} has dimension 1. The two rows are independent, so rank is 2. Rank-nullity checks: 3=1+2.

**Practice with answers.** (1) The derivative map from polynomials of degree ≤3 to degree ≤2 has kernel equal to constant polynomials (dimension 1) and image all degree ≤2 polynomials (dimension 3). (2) If T:ℝ⁵→ℝ³ has nullity 2, its rank is 3. (3) The matrix [[1,2],[2,4]] is not invertible; its rank is 1 and kernel dimension is 1. (4) To compute a matrix of T, apply T to each basis vector and place those outputs as columns.

**Common pitfalls:** mixing coordinate bases when multiplying matrices; confusing the kernel with the image; and interpreting rank as the number of nonzero entries instead of pivot columns.
