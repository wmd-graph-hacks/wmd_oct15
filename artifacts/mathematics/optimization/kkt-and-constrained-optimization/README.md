---
id: math-optimization-kkt-and-constrained-optimization
type: subtopic
title: KKT and constrained optimization
parent_topic: math-optimization
phase: applied-advanced
estimated_minutes: 60
prerequisites:
  - id: math-optimization-linear-programming-simplex-duality
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in kkt and constrained optimization
  - apply a standard method from kkt and constrained optimization to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - optimization
  - applied-advanced
---

# KKT Conditions and Constrained Optimization

For minimize f(x) subject to gᵢ(x)≤0 and hⱼ(x)=0, define a Lagrangian L=f+Σλᵢgᵢ+Σνⱼhⱼ. KKT conditions include stationarity ∇ₓL=0, primal feasibility, dual feasibility λᵢ≥0, and complementary slackness λᵢgᵢ=0. Active constraints can have positive multipliers; inactive constraints must have zero multiplier.

KKT conditions are necessary for local optima under constraint qualifications (regularity assumptions). For convex objectives and constraints, they are sufficient for global optimality. Without these assumptions, a KKT point may not be optimal, and an optimum may fail a standard qualification.

**Example.** Minimize x² subject to x≥1, written g(x)=1−x≤0. L=x²+λ(1−x). Stationarity 2x−λ=0; feasibility x≥1, λ≥0; complementarity λ(1−x)=0. Candidate x=1 gives λ=2 and satisfies conditions; convexity confirms global minimum.

Multipliers quantify marginal value of relaxing constraints in regular settings. Keep sign conventions consistent: writing constraints as g≤0 versus g≥0 changes multiplier signs.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: KKT conditions and active constraints

For differentiable optimization with constraints, Karush–Kuhn–Tucker conditions extend Lagrange multipliers. They combine stationarity, primal feasibility, dual feasibility (sign restrictions), and complementary slackness. Complementary slackness says an inactive inequality constraint has zero multiplier; a positive multiplier can occur only on an active boundary. Under convexity and regularity conditions, KKT conditions are sufficient for a global optimum; otherwise they are generally necessary candidates only.

**Worked example.** Minimize (x−3)² subject to x≤1. The unconstrained minimizer x=3 is infeasible, so the constrained optimum is the boundary x=1. The constraint is active and moving into the feasible region increases objective. This simple case illustrates why unconstrained critical points cannot settle constrained problems.

In larger problems, write every constraint consistently (for example g(x)≤0), define multiplier signs according to that convention, then check all conditions. Constraint qualifications ensure the gradient equations meaningfully describe the feasible boundary; degenerate constraints may violate them.

**Practice with answers.** (1) Minimize x² subject to x≥1: optimum x=1. (2) If an inequality has slack at the optimum, its KKT multiplier is zero. (3) Convex objective plus convex feasible set and KKT regularity makes a KKT point globally optimal. (4) Always verify the candidate against the original constraints.

**Common pitfalls:** inconsistent inequality signs; ignoring complementary slackness; treating necessary KKT conditions as sufficient for nonconvex problems; and failing to check constraint qualifications.
