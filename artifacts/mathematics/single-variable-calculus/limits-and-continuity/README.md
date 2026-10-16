---
id: math-single-variable-calculus-limits-and-continuity
type: subtopic
title: Limits and continuity
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-foundations-of-mathematics
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in limits and continuity
  - apply a standard method from limits and continuity to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Limits and Continuity

A limit describes the value a function approaches near a point, not necessarily the value at the point. We write limₓ→a f(x)=L when f(x) can be made arbitrarily close to L by requiring x sufficiently close—but unequal—to a. The ε–δ definition makes this precise: for every ε>0 there is δ>0 such that 0<|x−a|<δ implies |f(x)−L|<ε.

**Worked example.** Prove limₓ→2 x²=4. Given ε>0, factor |x²−4|=|x−2||x+2|. Restrict first to |x−2|<1, so 1<x<3 and |x+2|<5. Choose δ=min(1,ε/5). Then 0<|x−2|<δ gives |x²−4|<5δ≤ε. This is the basic proof pattern: factor the target error, bound the awkward factor near the point, and choose δ to control the remaining factor.

Limits obey sum, product, and quotient laws when component limits exist and the denominator limit is nonzero. When direct substitution gives 0/0, simplify, factor, rationalize, or use a squeeze argument; 0/0 is an indeterminate form, not an answer. One-sided limits matter at endpoints and jumps. A two-sided limit exists exactly when the left and right limits agree.

A function is continuous at a if f(a) is defined, the limit exists, and the limit equals f(a). Polynomials are continuous everywhere; rational functions are continuous where denominators are nonzero. A removable discontinuity occurs when the limit exists but the function is missing or has the wrong value at the point. The Intermediate Value Theorem says a continuous function on [a,b] takes every value between f(a) and f(b); it can prove existence of roots, but does not locate them exactly.

**Practice with answers.** (1) limₓ→3 (x²−9)/(x−3)=lim(x+3)=6 for x≠3. (2) f(x)=sin x/x has a removable hole at 0 if left undefined; defining f(0)=1 makes it continuous. (3) If f is continuous, f(0)=−1 and f(2)=3, some c∈(0,2) has f(c)=0 by IVT. (4) Check continuity of 1/(x−1): continuous for x≠1, undefined at 1.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: limits, continuity, and existence

The limit limₓ→a f(x)=L describes nearby inputs. The value f(a) may differ from L or may be undefined. In an epsilon-delta proof, ε is the allowed output error; choose δ so that an input within δ guarantees output error below ε. For f(x)=x² at a=2, |x²−4|=|x−2||x+2|. If |x−2|<1, then |x+2|<5; taking δ=min(1,ε/5) proves the limit.

For computation, try direct substitution first. If it produces 0/0, factor and cancel a common factor only for x≠a, rationalize radicals, combine fractions, or use a known limit. For a piecewise function, compute left and right limits separately. A two-sided limit exists only if they match. At endpoints, continuity is one-sided. A function is continuous at a when it is defined there, its limit exists, and that limit equals its value.

**Theorems in use.** The Intermediate Value Theorem (IVT) requires continuity on a closed interval [a,b]. If f(a)<0<f(b), it guarantees some root c∈(a,b); it does not identify c or guarantee only one root. The Extreme Value Theorem guarantees a maximum and minimum for a continuous function on a closed bounded interval. Check both endpoint values and interior critical points when finding extrema.

**Worked example.** Show f(x)=x³+x−1 has a root in (0,1). It is continuous because it is a polynomial. f(0)=−1 and f(1)=1, so IVT gives c∈(0,1) with f(c)=0. Also f′(x)=3x²+1>0, so f is strictly increasing and the root is unique. The first argument proves existence; the derivative supplies uniqueness.

**Practice with answers.** (1) limₓ→2 (x²−4)/(x−2)=4. (2) For f(x)=x+1 when x<1 and f(x)=3 when x≥1, the left limit at 1 is 2 and right limit is 3; no two-sided limit. (3) A continuous f with f(−2)=4 and f(3)=−1 has a zero between −2 and 3 by IVT. (4) Can IVT alone say the zero is unique? No; for example a curve may cross the axis more than once.

**Common pitfalls:** substituting into an indeterminate form as if 0/0 were a value; canceling a factor and forgetting the original function’s domain; applying a closed-interval theorem to a discontinuous function or an open interval; and claiming uniqueness from existence alone.
