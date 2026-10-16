---
id: math-real-analysis-function-sequences-and-uniform-convergence
type: subtopic
title: Function sequences and uniform convergence
parent_topic: math-real-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-real-analysis-completeness-of
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in function sequences and uniform convergence
  - apply a standard method from function sequences and uniform convergence to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - real-analysis
  - advanced-core
---

# Sequences of Functions and Uniform Convergence

A sequence of functions fₙ converges pointwise to f if, for each fixed x, the number fₙ(x) approaches f(x). The speed may depend on x. Uniform convergence requires one index N to work for all x at once: for every ε>0, there is N such that n≥N implies |fₙ(x)−f(x)|<ε for every x in the domain. Equivalently, supₓ|fₙ(x)−f(x)|→0.

**Example.** On [0,1], fₙ(x)=xⁿ converges pointwise to f(x)=0 for x<1 and f(1)=1. The limit is discontinuous. Convergence is not uniform: for any n, values near 1 remain close to 1 while f(x)=0, so the supremum error is 1. On [0,r] with r<1, however, sup xⁿ=rⁿ→0 uniformly.

Uniform convergence preserves continuity when each fₙ is continuous. It also allows limits to pass through integrals on suitable finite intervals. Differentiating a limit is more delicate: uniform convergence of fₙ alone does not justify convergence of derivatives; one needs additional hypotheses such as uniform convergence of derivatives plus convergence at one point.

To prove uniform convergence, seek a bound |fₙ(x)−f(x)|≤aₙ independent of x with aₙ→0. To disprove it, choose xₙ depending on n where the error stays bounded away from zero.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: pointwise versus uniform convergence

Functions fₙ converge pointwise to f on E if for each fixed x and ε>0, eventually |fₙ(x)−f(x)|<ε. The required index N may depend on x. Convergence is uniform if one N works for every x∈E. In quantifiers, pointwise has ∀x∀ε∃N∀n≥N; uniform has ∀ε∃N∀x∀n≥N. The order change is the key distinction.

**Worked example.** fₙ(x)=xⁿ on [0,1] converges pointwise to f(x)=0 for x<1 and f(1)=1. It is not uniform: near 1, xⁿ stays close to 1 for any fixed n, so supₓ|fₙ−f|=1. On [0,a] with a<1, the supremum is aⁿ→0, so convergence is uniform.

Uniform limits preserve continuity: if every fₙ is continuous and convergence is uniform, the limit is continuous. Uniform convergence also permits exchanging limit and integral under standard hypotheses; termwise differentiation requires stronger conditions. The Weierstrass M-test gives uniform convergence when |fₙ(x)|≤Mₙ and ΣMₙ converges.

**Practice with answers.** (1) fₙ(x)=x/n converges uniformly to zero on [0,10] since sup error=10/n. (2) The same sequence is not uniform on ℝ. (3) A uniform limit of continuous functions cannot have a jump. (4) To disprove uniform convergence, find points xₙ where the error stays bounded below.

**Common pitfalls:** moving quantifiers in the wrong order; checking pointwise values only; assuming every pointwise limit preserves continuity; and using a convergence theorem without its uniformity conditions.
