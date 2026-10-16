---
id: math-linear-algebra-inner-products-and-orthogonality
type: subtopic
title: Inner products and orthogonality
parent_topic: math-linear-algebra
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-linear-algebra-eigenvalues-diagonalization-jordan-form
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in inner products and orthogonality
  - apply a standard method from inner products and orthogonality to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - linear-algebra
  - core-to-advanced
---

# Inner Products and Orthogonality

An inner product generalizes the dot product: it is bilinear (or conjugate-linear in complex spaces), symmetric/Hermitian, and positive definite. It defines norm ||v||=√⟨v,v⟩ and angle. Vectors are orthogonal when their inner product is zero. Orthogonal vectors are automatically independent when nonzero.

Gram–Schmidt turns an independent list into an orthogonal list spanning the same space. Given v₁,…,vₖ, set u₁=v₁; then uⱼ=vⱼ−Σᵢ<ⱼ proj_{uᵢ}(vⱼ), where projᵤ(v)=⟨v,u⟩/⟨u,u⟩u. Normalize each nonzero uᵢ to obtain an orthonormal basis. In computation, modified Gram–Schmidt is more stable than the classical form.

**Example.** Start with v₁=(1,1), v₂=(1,0). Let u₁=(1,1). Projection of v₂ onto u₁ is (1/2)(1,1). Thus u₂=(1/2,−1/2), orthogonal to u₁. Normalize to q₁=(1,1)/√2 and q₂=(1,−1)/√2.

Orthogonal projection gives the closest point in a subspace under Euclidean distance. The residual is perpendicular to the subspace. This geometric fact drives least squares and Fourier approximation.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: angles, orthogonal decompositions, and Gram–Schmidt

An inner product generalizes the dot product and defines length ‖v‖=√⟨v,v⟩ and angle through cos θ=⟨u,v⟩/(‖u‖‖v‖). Vectors are orthogonal when their inner product is zero. The Cauchy–Schwarz inequality |⟨u,v⟩|≤‖u‖‖v‖ guarantees the cosine lies between −1 and 1. In ℝⁿ with the usual dot product, this recovers familiar geometry.

An orthogonal set of nonzero vectors is automatically independent. An orthonormal basis has mutually perpendicular unit vectors, so coordinates are simple: the coefficient along qᵢ is ⟨v,qᵢ⟩. Gram–Schmidt converts an independent list into an orthogonal list by subtracting projections, then normalizes. Numerical implementations often use modified Gram–Schmidt or QR methods for improved stability.

**Worked example.** Let u=(1,1) and v=(1,0). Project v onto u: projᵤ(v)=[(v·u)/(u·u)]u=(1/2)(1,1). The residual w=v−projᵤ(v)=(1/2,−1/2) is orthogonal to u because w·u=0. Thus {u,w} is an orthogonal basis of ℝ².

**Practice with answers.** (1) Normalize (3,4): (3/5,4/5). (2) Are (1,2) and (−2,1) orthogonal? Yes, dot product 0. (3) Projection of (2,1) onto (1,0) is (2,0). (4) In an orthonormal basis, the squared length is the sum of squared coordinates (Pythagorean theorem).

**Common pitfalls:** projecting onto a vector but forgetting to divide by its squared norm; assuming vectors with dot product zero are unit vectors; and normalizing a zero residual, which signals dependence in Gram–Schmidt.
