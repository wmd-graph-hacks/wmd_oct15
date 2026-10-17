---
id: math-single-variable-calculus-mean-value-theorem
type: subtopic
title: Mean Value Theorem
parent_topic: math-single-variable-calculus
phase: core
estimated_minutes: 60
prerequisites:
  - id: math-single-variable-calculus-derivatives-and-applications
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in mean value theorem
  - apply a standard method from mean value theorem to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - single-variable-calculus
  - core
---

# Mean Value Theorem

The Mean Value Theorem (MVT) connects average change over an interval with instantaneous change at some point. If f is continuous on [a,b] and differentiable on (a,b), then there exists c∈(a,b) such that f′(c)=[f(b)−f(a)]/(b−a). Geometrically, somewhere the tangent line is parallel to the secant through the endpoints. Rolle’s theorem is the special case f(a)=f(b), giving a point where f′(c)=0.

**Worked example.** For f(x)=x² on [1,3], average slope is (9−1)/(3−1)=4. Since f′(x)=2x, the MVT point solves 2c=4, hence c=2, which lies in (1,3). The theorem guarantees at least one such c; it does not say there is exactly one.

A powerful consequence is a change bound. If |f′(x)|≤M throughout an interval, then |f(b)−f(a)|≤M|b−a|. More generally, if f′(x)>0 throughout an interval, f is strictly increasing there. If f′=0 throughout, f is constant. These claims follow by applying MVT to any two points in the interval.

Hypotheses matter. Continuity is needed on the closed interval and differentiability on the open interval. For f(x)=|x| on [−1,1], endpoint values agree, but there is no point with derivative zero; the conclusion of Rolle’s theorem fails because f is not differentiable at 0. A graph alone cannot establish the theorem’s assumptions.

**Practice with answers.** (1) For f(x)=x³ on [0,2], MVT gives c with 3c²=4, so c=2/√3. (2) If f′≤−2 on [1,4], then f(4)−f(1)≤−6. (3) If f′=0 everywhere on an interval, MVT applied to any x<y gives f(y)−f(x)=0, so f is constant. (4) Is Rolle applicable to x²−1 on [−1,1]? Yes; c=0 works.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: what the Mean Value Theorem guarantees

If f is continuous on [a,b] and differentiable on (a,b), then some c∈(a,b) satisfies f′(c)=[f(b)−f(a)]/(b−a). The right side is the average rate across the interval; the theorem guarantees an interior instant with that same instantaneous rate. Rolle’s theorem is the special case f(a)=f(b), which guarantees a horizontal tangent somewhere inside.

The hypotheses are part of the conclusion. Continuity on the closed interval rules out a break at an endpoint or inside. Differentiability on the open interval rules out a corner or cusp inside. Failure of a hypothesis does not prove the conclusion false; it means this theorem cannot guarantee it.

**Worked example.** Let f(x)=x² on [1,3]. It is continuous and differentiable, and its average slope is (9−1)/(3−1)=4. Since f′(x)=2x, setting f′(c)=4 gives c=2, which is in (1,3). The theorem predicted existence; the derivative equation finds the point.

**Useful consequences.** If f′(x)=0 throughout an interval, the MVT shows f is constant there. If f′>0 throughout an interval, then for x₁<x₂ the MVT gives f(x₂)−f(x₁)=f′(c)(x₂−x₁)>0, so f is increasing. If |f′|≤M, then |f(b)−f(a)|≤M|b−a|; this bounds how fast a function can change.

**Practice with answers.** (1) For f(x)=x³ on [0,2], average slope is 4; solve 3c²=4 to get c=2/√3. (2) Does f(x)=|x| satisfy MVT on [−1,1]? No, it is not differentiable at 0. (3) If f′≥2 on [a,b], show f(b)−f(a)≥2(b−a): apply MVT and use its positive interval length.

**Common pitfalls:** asserting an exact c before checking hypotheses; confusing average slope with the slope at every point; and assuming the theorem finds a point uniquely. It guarantees at least one point, often without identifying it.
