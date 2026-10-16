---
id: math-optimization-linear-programming-simplex-duality
type: subtopic
title: Linear programming, simplex, duality
parent_topic: math-optimization
phase: applied-advanced
estimated_minutes: 60
prerequisites:
  - id: math-optimization-convex-sets-and-functions
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in linear programming, simplex, duality
  - apply a standard method from linear programming, simplex, duality to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - optimization
  - applied-advanced
---

# Linear Programming, Simplex, and Duality

A linear program optimizes cᵀx subject to linear inequalities and equalities. The feasible region is a polyhedron. If an optimum exists and the region has a vertex, a linear objective has an optimum at a vertex. The simplex method moves between adjacent basic feasible solutions, improving the objective until no improving pivot exists; degeneracy can cause repeated vertices without careful rules.

Every primal LP has a dual LP. Dual variables assign values to constraints and can be interpreted as shadow prices. Weak duality says a dual-feasible value bounds the primal optimum; when both are feasible and bounded, strong duality gives equal optimal values. Complementary slackness links positive variables to tight constraints.

**Example.** Maximize 3x+2y subject to x+y≤4, x≤2, y≤3, x,y≥0. Check vertices: (0,0),(2,0),(2,2),(1,3),(0,3). Objective values are 0,6,10,9,6; optimum is 10 at (2,2). The vertex check is small and transparent.

Always distinguish infeasible, unbounded, and finite-optimum cases. Scaling and units help interpret constraint values and dual prices.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: feasible corners and dual values

A linear program optimizes a linear objective subject to linear equalities/inequalities. The feasible region is a polyhedron. If an optimum exists and the region has suitable boundedness, an optimum occurs at an extreme point, which motivates the simplex method’s movement between corners. Before solving, graph small two-variable cases, test feasibility, and distinguish infeasible, unbounded, and finite-optimum cases.

Every linear program has a dual problem. For a maximization problem with ≤ constraints and nonnegative variables, dual variables assign prices to constraints. Weak duality says every feasible dual value bounds every feasible primal value; equality at optimality is strong duality under standard feasibility conditions. A binding constraint can have a nonzero shadow price, measuring local objective improvement from relaxing it.

**Worked example.** Maximize 3x+2y subject to x+y≤4, x≤2, x,y≥0. The corner values at (0,0),(2,0),(2,2),(0,4) are 0,6,10,8, so optimum is 10 at (2,2). The constraints identify resource limits; changing a bound may change which corner is optimal.

**Practice with answers.** (1) x≥2 and x≤1 is infeasible. (2) Maximize x subject only to x≥0 is unbounded. (3) A feasible dual solution provides an upper bound on a primal maximization. (4) Simplex traverses vertices using objective-improving pivots.

**Common pitfalls:** overlooking infeasibility or unboundedness; interpreting shadow prices far outside the local range; and forgetting sign conventions when writing the dual.
