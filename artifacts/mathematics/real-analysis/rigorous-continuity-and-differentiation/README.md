---
id: math-real-analysis-rigorous-continuity-and-differentiation
type: subtopic
title: Rigorous continuity and differentiation
parent_topic: math-real-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-real-analysis-function-sequences-and-uniform-convergence
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in rigorous continuity and differentiation
  - apply a standard method from rigorous continuity and differentiation to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - real-analysis
  - advanced-core
---

# Rigorous Continuity and Differentiability

Continuity at a means: for every ε>0 there exists δ>0 such that |x−a|<δ implies |f(x)−f(a)|<ε. Differentiability means the difference quotient has a finite limit; equivalently f(a+h)=f(a)+f′(a)h+o(h). The remainder divided by h tends to zero, expressing first-order linear approximation.

Differentiability implies continuity, but continuity does not imply differentiability: |x| is continuous at 0 but has unequal one-sided slopes. A derivative may itself be discontinuous. For example f(x)=x²sin(1/x²) for x≠0 and f(0)=0 is differentiable at 0 with derivative 0, while its derivative oscillates unboundedly nearby.

The Mean Value Theorem supplies powerful consequences. If f′=0 throughout an interval, f is constant; if |f′|≤M, then |f(x)−f(y)|≤M|x−y|. The latter is a Lipschitz bound and implies uniform continuity. On a compact interval, every continuous function is uniformly continuous; on noncompact domains this can fail, e.g. f(x)=x² on ℝ.

For a sequence of differentiable functions, do not infer that the pointwise limit is differentiable. State the convergence conditions and use a theorem designed for exchanging limits and derivatives.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: epsilon-delta continuity and derivative proofs

Continuity of f at a means: for every ε>0 there is δ>0 such that |x−a|<δ implies |f(x)−f(a)|<ε. Unlike a limit definition, x=a is included, though the condition is automatic there. To prove it, bound output change in terms of input change and choose δ to force the desired inequality. Sequentially, continuity means xₙ→a implies f(xₙ)→f(a).

Differentiability at a means the difference quotient has a finite limit. Differentiability implies continuity, but continuity does not imply differentiability; |x| is continuous at 0 with a corner. The derivative is a linear approximation in one dimension: f(a+h)=f(a)+f′(a)h+o(h). This remainder condition is stronger than merely having a plausible tangent line.

**Worked example.** For f(x)=3x+1, |f(x)−f(a)|=3|x−a|. Given ε choose δ=ε/3; then |x−a|<δ implies output difference <ε. The derivative from the quotient is 3, agreeing with the linear slope.

**Practice with answers.** (1) x² is differentiable at every real point, derivative 2x. (2) |x| is not differentiable at zero because left and right slopes differ. (3) If f′(a) exists, f is continuous at a. (4) Continuity alone does not guarantee a derivative.

**Common pitfalls:** choosing δ before controlling all factors; proving a limit but forgetting the function value; and reversing the implication “differentiable implies continuous.”
