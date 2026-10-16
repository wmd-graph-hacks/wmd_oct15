---
id: math-topology-and-number-theory-topological-spaces-and-continuity
type: subtopic
title: Topological spaces and continuity
parent_topic: math-topology-and-number-theory
phase: optional-extension
estimated_minutes: 60
prerequisites:
  - id: math-foundations-of-mathematics
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in topological spaces and continuity
  - apply a standard method from topological spaces and continuity to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - topology-and-number-theory
  - optional-extension
---

# Topological Spaces and Continuity

A topology on X is a collection of subsets called open sets, containing ∅ and X and closed under arbitrary unions and finite intersections. It abstracts which points count as near one another without requiring a distance. Every metric generates a topology through open balls, but different metrics can generate the same topology.

A function f:X→Y is continuous if the preimage of every open set in Y is open in X. This definition generalizes ε–δ continuity and makes composition straightforward. A homeomorphism is a bijective continuous map with continuous inverse; it expresses topological sameness, preserving properties such as connectedness and compactness.

**Example.** On ℝ with the usual topology, f(x)=x² is continuous because inverse images of open sets are open (equivalently use ordinary analysis). On a set with the discrete topology every subset is open, so every map from a discrete space is continuous.

Topology ignores lengths and angles: a circle and an ellipse are homeomorphic, but a circle and a line are not compact-equivalent. Keep the chosen topology explicit; “open” is relative to it.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: open sets define continuity

A topology on X is a collection of open subsets containing ∅ and X, closed under arbitrary unions and finite intersections. A topological space needs no distance; it captures which points count as nearby. A function f:X→Y is continuous if preimages of open sets are open. This generalizes epsilon-delta continuity and makes continuity independent of coordinates.

The discrete topology declares every subset open; every function from a discrete space is continuous. The indiscrete topology has only ∅ and X open; maps into it are automatically continuous. These extremes help test definitions. A homeomorphism is a bijective continuous map with continuous inverse; it expresses topological equivalence, so a coffee mug and a torus are often described as equivalent through a handle-preserving deformation.

**Worked example.** For f:ℝ→ℝ, f(x)=x², continuity can be checked by taking preimages: f⁻¹((a,b))={x:a<x²<b}, a union of open intervals (or empty), hence open. The preimage viewpoint also handles spaces without a metric.

**Practice with answers.** (1) Continuous maps preserve preimages of open sets. (2) A bijection need not be a homeomorphism if its inverse is discontinuous. (3) In the discrete topology every subset is open. (4) A topology must be closed under arbitrary unions but only finite intersections.

**Common pitfalls:** assuming topology is always defined from a metric; confusing images and preimages in the continuity definition; and assuming continuous bijection always has continuous inverse without compactness/Hausdorff conditions.
