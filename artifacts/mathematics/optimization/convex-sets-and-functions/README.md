---
id: math-optimization-convex-sets-and-functions
type: subtopic
title: Convex sets and functions
parent_topic: math-optimization
phase: applied-advanced
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus-vectors-and-geometry-in
    target_type: subtopic
    strength: recommended
  - id: math-linear-algebra-vector-spaces-subspaces-basis
    target_type: subtopic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in convex sets and functions
  - apply a standard method from convex sets and functions to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - optimization
  - applied-advanced
---

# Convex Sets and Functions

A set C is convex if the segment between any two points in C remains in C: θx+(1−θ)y∈C for θ∈[0,1]. A function f is convex if f(θx+(1−θ)y)≤θf(x)+(1−θ)f(y). For twice differentiable one-variable functions, f″≥0 implies convexity; in multiple dimensions, a positive semidefinite Hessian is sufficient on a convex domain.

Convexity is valuable because every local minimum is global. For differentiable convex f, f(y)≥f(x)+∇f(x)·(y−x), the tangent plane supports the graph. Strict convexity gives at most one minimizer.

**Example.** f(x)=x² has f″=2>0, so it is strictly convex; its unique minimum is x=0. The feasible set [−1,1] is convex. A set with two separated points but missing their midpoint is not convex.

Convexity of the objective and feasible set makes optimization tractable, but nonconvex problems may still have global solutions. Verify domain convexity and Hessian conditions rather than inferring convexity from a graph.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: convex combinations and global minima

A set C is convex if the segment between any two points in C stays in C: λx+(1−λ)y∈C for 0≤λ≤1. A function f is convex if f(λx+(1−λ)y)≤λf(x)+(1−λ)f(y). For twice-differentiable functions on a convex domain, a positive semidefinite Hessian is a sufficient convexity condition. A local minimum of a convex function is global; strict convexity gives at most one minimizer.

Examples of convex sets include intervals, half-spaces, balls, and intersections of convex sets. The epigraph {(x,t):t≥f(x)} is convex exactly when f is convex. These facts let us identify optimization problems with reliable structure and understand why linear programs are tractable.

**Worked example.** f(x)=x² is convex because f″=2>0. On [−1,2], its global minimum is at x=0, value 0. A stationary point of a strictly convex differentiable function is the unique global minimum.

**Practice with answers.** (1) A line segment is convex. (2) The union of two disjoint convex sets need not be convex. (3) f(x)=−x² is concave, not convex. (4) Any local minimum of a convex function on its convex domain is global.

**Common pitfalls:** assuming a convex function must be strictly convex; checking only one coordinate direction of the Hessian; and treating a nonconvex feasible region as convex because the objective is convex.
