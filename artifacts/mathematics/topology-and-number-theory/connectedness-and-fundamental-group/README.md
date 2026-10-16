---
id: math-topology-and-number-theory-connectedness-and-fundamental-group
type: subtopic
title: Connectedness and fundamental group
parent_topic: math-topology-and-number-theory
phase: optional-extension
estimated_minutes: 60
prerequisites:
  - id: math-topology-and-number-theory-topological-spaces-and-continuity
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in connectedness and fundamental group
  - apply a standard method from connectedness and fundamental group to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - topology-and-number-theory
  - optional-extension
---

# Connectedness and the Fundamental Group

A space is connected if it cannot be partitioned into two disjoint nonempty open subsets. Path-connectedness means every two points can be joined by a continuous path and implies connectedness. A loop based at x is a path starting and ending at x. Two loops are equivalent if one can be continuously deformed into the other while keeping the base point fixed.

The fundamental group π₁(X,x) consists of loop-equivalence classes, with product given by concatenation. It captures holes that obstruct shrinking loops to a point. A simply connected space is path-connected and has trivial fundamental group.

**Example.** In the plane, any loop can shrink to a point, so π₁(ℝ²) is trivial. On a circle, loops have integer winding number; going around once, twice, or in reverse gives classes in ℤ. This explains π₁(S¹)≅ℤ.

The fundamental group depends on base point in definition, though path-connected spaces have isomorphic groups up to choice. Introductory computations focus on circles, graphs, and simple deformations; rigorous invariance requires algebraic topology tools.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: loops and holes

A space is path-connected if any two points can be joined by a continuous path. A loop starts and ends at a base point. Two loops are homotopic if one can be continuously deformed into the other while keeping the base point fixed. Homotopy classes of loops form the fundamental group π₁(X), with concatenation as the operation. It is a topological invariant up to suitable basepoint conventions.

The circle has fundamental group isomorphic to the integers: a loop’s winding number counts signed turns. The plane is simply connected because every loop contracts to a point. The punctured plane is not: a loop winding once around the missing point cannot contract without crossing it. This gives an algebraic way to detect a hole.

**Worked example.** A loop making two counterclockwise turns around the origin represents 2∈ℤ; a clockwise turn represents −1; a loop followed by its reverse represents 0 and contracts. Winding numbers add under loop concatenation.

**Practice with answers.** (1) Every loop in ℝ² contracts, so π₁(ℝ²) is trivial. (2) The circle’s fundamental group is ℤ. (3) A path-connected space is connected, but the converse can fail in general. (4) Homotopies must preserve the base point for based loops.

**Common pitfalls:** assuming a visible loop always detects a distinct hole; confusing path-connectedness with connectedness; and forgetting basepoint and orientation conventions.
