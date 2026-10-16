---
id: math-foundations-of-mathematics-functions-and-cardinality
type: subtopic
title: Functions and cardinality
parent_topic: math-foundations-of-mathematics
phase: foundation
estimated_minutes: 45
prerequisites:
  - id: math-foundations-of-mathematics-relations-and-equivalence
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in functions and cardinality
  - apply a standard method from functions and cardinality to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - foundations-of-mathematics
  - foundation
---

# Functions and Cardinality

A function f:A→B assigns each input a∈A exactly one output f(a)∈B. A is the domain; B is the codomain; the image (range) is {f(a):a∈A}, which may be smaller than B. Two functions are equal only if they have the same domain, codomain, and output for every input. Composition is (g∘f)(x)=g(f(x)) and is defined when outputs of f lie in the domain of g.

A function is injective (one-to-one) if f(x)=f(y) forces x=y. It is surjective (onto B) if every b∈B is hit. It is bijective if both, and then it has an inverse function f⁻¹:B→A. To prove injectivity, start by assuming equal outputs. To prove surjectivity, take an arbitrary target b and solve f(x)=b, checking the solution lies in the domain.

**Worked example.** Let f:ℝ→ℝ, f(x)=x². It is not injective because f(2)=f(−2), and not surjective because no real x maps to −1. But f:[0,∞)→[0,∞), f(x)=x² is bijective: x²=y² with x,y≥0 implies x=y, and any target t≥0 is reached by x=√t. Its inverse is √t.

For finite sets, cardinality is the number of elements. For infinite sets, define two sets to have the same cardinality if a bijection exists between them. This explains the surprising fact that ℕ={1,2,…} and the even positive integers have equal size: n↦2n is a bijection. A proper subset can therefore have the same cardinality as an infinite set. The rational numbers are countable; the real numbers are uncountable (Cantor’s diagonal argument proves no list can contain all reals in an interval).

**Practice with answers.** (1) Is f:ℝ→ℝ, f(x)=x+4 bijective? Yes; inverse y↦y−4. (2) Is f:ℝ→[0,∞), f(x)=x² onto? Yes, but not injective. (3) Is n↦n+1 from nonnegative integers to positive integers bijective? Yes. (4) Why must the codomain be stated? “Onto” is defined relative to the codomain; x² is onto [0,∞) but not onto ℝ.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: functions, inverses, and size of sets

A function f:A→B assigns each input a∈A exactly one output f(a)∈B. A is the domain and B the codomain; the image/range is the set of outputs actually achieved. Injective means distinct inputs have distinct outputs (equivalently, f(a)=f(b) implies a=b). Surjective means every codomain element is achieved. Bijective means both and therefore has an inverse function B→A.

To prove injectivity, start with f(a)=f(b) and derive a=b. To disprove it, find two different inputs with the same output. To prove surjectivity, take arbitrary y in the codomain and solve f(x)=y, checking the solution belongs to the domain. Composition requires the first function’s outputs to fit the next function’s domain.

For finite sets, a bijection is a perfect pairing, so two sets have equal cardinality exactly when a bijection exists. The pigeonhole principle says a map from a larger finite set to a smaller one cannot be injective. For infinite sets, cardinality is defined by bijection: the even integers and all integers have the same size via n↦2n, even though the evens are a proper subset. The rationals are countable; the real numbers are uncountable, a deeper result.

**Worked example.** f:ℝ→ℝ given by f(x)=2x+3 is bijective. If 2a+3=2b+3, then a=b, so it is injective. Given y∈ℝ, choose x=(y−3)/2; then f(x)=y, so it is surjective. The inverse is f⁻¹(y)=(y−3)/2. By contrast, x²:ℝ→ℝ is neither injective (1 and −1 share an output) nor surjective (no real input maps to −1).

**Practice with answers.** (1) Is x²:[0,∞)→[0,∞) bijective? Yes, inverse √y. (2) Is x²:ℝ→[0,∞) injective? No, though it is surjective. (3) A function from a 5-element set to a 4-element set cannot be injective by pigeonhole. (4) Why does a bijection establish equal size? Every element of one set pairs with exactly one element of the other, with no leftovers.

**Common pitfalls:** confusing codomain with image; claiming an inverse exists without bijectivity; proving injectivity with a few values; and assuming an infinite set cannot match a proper subset.
