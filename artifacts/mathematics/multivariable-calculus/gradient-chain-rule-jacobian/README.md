---
id: math-multivariable-calculus-gradient-chain-rule-jacobian
type: subtopic
title: Gradient, chain rule, Jacobian
parent_topic: math-multivariable-calculus
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-partial-derivatives-and-differentiability
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in gradient, chain rule, jacobian
  - apply a standard method from gradient, chain rule, jacobian to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - multivariable-calculus
  - advanced-core
---

# Gradient, Directional Derivatives, and the Chain Rule

The gradient ∇f=(fₓ,fᵧ,… ) collects partial derivatives. For differentiable f, the directional derivative in unit direction u is Dᵤf=∇f·u. Thus the gradient points toward steepest increase, and its magnitude is the maximal directional rate. At a regular level surface f=c, ∇f is perpendicular to the surface because moving tangent to the level set does not change f to first order.

For a map F:ℝⁿ→ℝᵐ, the Jacobian J_F is the m×n matrix of first partial derivatives. The chain rule for G∘F is J_(G∘F)(x)=J_G(F(x))J_F(x). Matrix dimensions provide a useful check. For a coordinate change, |det J| is the local volume scaling factor; absolute value is needed for integration because volume is nonnegative.

**Example.** Let f(x,y)=x²+y² and take unit direction u=(3/5,4/5). At (1,2), ∇f=(2,4), so Dᵤf=2·3/5+4·4/5=22/5. Along the curve r(t)=(cos t,sin t), the chain rule gives d/dt f(r(t))=∇f(r(t))·r′(t)=0, consistent with f=1 along the circle.

## Study sequence

1. Work each example yourself, line by line.
2. Solve the practice prompts in the course notebook and explain the method aloud or in writing.
3. Return after a day and solve a similar problem with changed values or assumptions.

## Lesson: gradient, directional derivative, and Jacobian

The gradient ∇f=(fₓ,fᵧ,…) points in the direction of greatest instantaneous increase; its magnitude is the maximum directional rate. For a unit vector u, Dᵤf=∇f·u. For a vector-valued map F:ℝⁿ→ℝᵐ, the Jacobian J has entry ∂Fᵢ/∂xⱼ and describes the best local linear transformation. The multivariable chain rule multiplies Jacobians in the order maps are applied.

**Worked example.** Let f(x,y)=x²+y². At (1,2), ∇f=(2,4). The rate toward u=(3/5,4/5) is (2,4)·u=22/5. The maximum rate is ‖∇f‖=√20, in direction (1,2)/√5.

For a coordinate change x=x(u,v), y=y(u,v), the Jacobian determinant measures local area scaling. The change-of-variables integral includes its absolute value; orientation may change sign, area does not. In a composition z=f(x,y), x=x(t), y=y(t), dz/dt=fₓ dx/dt+fᵧ dy/dt.

**Practice with answers.** (1) ∇(xy)=(y,x). (2) The derivative of F(x,y)=(x²+y,xy) has Jacobian [[2x,1],[y,x]]. (3) If x=2u and y=3v, the area scale is 6. (4) A directional derivative needs a unit direction to represent rate per unit distance.

**Common pitfalls:** using a nonunit direction without accounting for its length; forgetting the absolute Jacobian determinant in area integrals; and reversing Jacobian multiplication order.
