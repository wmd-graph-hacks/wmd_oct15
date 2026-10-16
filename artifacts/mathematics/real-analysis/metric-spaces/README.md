---
id: math-real-analysis-metric-spaces
type: subtopic
title: Metric spaces
parent_topic: math-real-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-real-analysis-riemann-stieltjes-and-lebesgue-integration
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in metric spaces
  - apply a standard method from metric spaces to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - real-analysis
  - advanced-core
---

# Metric Spaces

A metric d(x,y) measures distance and satisfies nonnegativity, identity of indiscernibles, symmetry, and the triangle inequality. A metric space is a set equipped with such a distance. Open balls B(x,r)={y:d(x,y)<r} define neighborhoods, convergence, continuity, and openness without requiring coordinates.

Examples include Euclidean distance, the discrete metric (distance 1 between distinct points), and sup distance on continuous functions. A sequence converges to x when d(xₙ,x)→0. It is Cauchy when pairwise distances become small. A metric space is complete if every Cauchy sequence converges within the space; ℚ with usual distance is not complete, while ℝ is.

A function between metric spaces is continuous at x if for every ε>0 there is δ>0 such that d_X(x,y)<δ implies d_Y(f(x),f(y))<ε. This is the familiar ε–δ definition with generalized distances.

**Example.** In the discrete metric, a sequence converges to x exactly when it is eventually equal to x: choose ε<1. Thus convergence depends on the chosen metric/topology, not just the underlying set.

Metric spaces let analysis transfer to spaces of functions, sequences, and geometric objects. When proving continuity or completeness, always name the metric being used.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: distance, convergence, and continuity in metric spaces

A metric d assigns distances satisfying nonnegativity, identity of indiscernibles, symmetry, and the triangle inequality. A metric space is a set with such a distance. Open balls B(x,r)={y:d(x,y)<r} define neighborhoods and open sets. A sequence converges to x if d(xₙ,x)→0; it is Cauchy if pairwise distances eventually become small. Completeness means every Cauchy sequence converges within the space.

Continuity at x means inputs close to x map to outputs close to f(x), expressed with ε and δ using the two metrics. A function is uniformly continuous if one δ works everywhere. Compactness generalizes closed bounded intervals: every open cover has a finite subcover. In metric spaces, sequential compactness is equivalent. Compact continuous images are compact, which helps prove boundedness and attainment of extrema.

**Worked example.** On (0,1) with usual distance, xₙ=1/n is Cauchy but converges to 0 outside the space; the space is not complete. On [0,1], the same sequence converges within the space and the interval is complete and compact.

**Practice with answers.** (1) The discrete metric d(x,y)=1 for x≠y is a metric. (2) Every convergent sequence is Cauchy. (3) Every Cauchy sequence need not converge unless the space is complete. (4) A continuous real-valued function on a compact space is bounded and attains its extrema.

**Common pitfalls:** assuming the metric must come from coordinates; confusing closed with compact in arbitrary spaces; and forgetting completeness depends on the chosen space, not just the sequence formula.
