---
id: math-foundations-of-mathematics-mathematical-induction
type: subtopic
title: Mathematical induction
parent_topic: math-foundations-of-mathematics
phase: foundation
estimated_minutes: 45
prerequisites:
  - id: math-foundations-of-mathematics-proof-techniques
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in mathematical induction
  - apply a standard method from mathematical induction to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - foundations-of-mathematics
  - foundation
---

# Mathematical Induction

Induction proves an infinite sequence of statements P(n), usually for integers n≥n₀, using a domino principle. First prove the base case P(n₀). Then prove the inductive step: for an arbitrary k≥n₀, assume P(k) and derive P(k+1). Together these show P(n) for every n≥n₀. The inductive assumption is temporary and may be used only in the step.

**Worked example.** Prove 1+2+…+n=n(n+1)/2 for all n≥1. Base case n=1: both sides equal 1. Inductive step: assume 1+…+k=k(k+1)/2. Then
1+…+k+(k+1)=k(k+1)/2+(k+1)=(k+1)(k+2)/2,
which is precisely the formula with n=k+1. Therefore the statement holds for every positive integer.

A frequent mistake is to check several values and conclude the pattern is proven. Checking n=1,2,3 is useful for discovering a conjecture, but infinitely many later values remain. Another mistake is to write “assume the result for n and prove it for n” rather than explicitly proving the next case. State the starting index: a recurrence may be true only from n=2 onward.

**Strong induction** assumes P(n₀),…,P(k) to prove P(k+1). It is useful when the next case is built from more than the immediately preceding case. For example, every integer n≥2 is a product of primes: if n is prime, done; otherwise n=ab with 1<a,b<n. By strong induction, a and b each factor into primes, so n does too. The induction hypothesis covers both smaller factors.

**Structural induction** applies the same idea to recursively built objects such as strings, trees, or formulas: prove a base object has the property, then show each construction rule preserves it.

**Practice with answers.** (1) Prove 1+3+…+(2n−1)=n²: in the step add 2k+1 to k² to obtain (k+1)². (2) Why is checking n=1 through 100 insufficient? A claim about all n has infinitely many cases; a proof must explain the general transition. (3) What is wrong with using P(k) to prove P(k+2) without a base case for k+1? The chain has a gap; establish bases for both parity classes or use a valid induction step.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: induction as a proof method

Mathematical induction proves a statement P(n) for every integer n≥n₀. First prove the base case P(n₀). Then assume P(k) for an arbitrary k≥n₀ (the induction hypothesis) and prove P(k+1). The base case anchors the process; the inductive step passes truth from one integer to the next. Both are essential. Strong induction assumes all cases from n₀ through k to prove P(k+1), useful when the next case depends on several earlier cases.

**Worked example.** Prove 1+2+…+n=n(n+1)/2 for n≥1. Base case n=1: both sides equal 1. Assume 1+…+k=k(k+1)/2. Then 1+…+k+(k+1)=k(k+1)/2+(k+1)=(k+1)(k+2)/2, which is the claimed formula at k+1. Therefore it holds for all n≥1.

The induction hypothesis is an assumption inside the proof, not a statement already proved for every k in isolation. In the inductive step, explicitly show how it transforms the target at k+1. Strong induction proves every integer n≥2 is a product of primes: if n is prime it is done; otherwise n=ab with 1<a,b<n, and the induction hypothesis factors a and b into primes.

**Practice with answers.** (1) Prove 2ⁿ≥n+1 for n≥0: base n=0; if 2ᵏ≥k+1, then 2ᵏ⁺¹≥2k+2≥k+2. (2) Why is checking n=1,2,3 not a proof for all n? No finite set of examples establishes infinitely many cases. (3) For induction starting at n=4, what base case is needed? P(4); the induction then covers all n≥4.

**Common pitfalls:** omitting the base case; assuming P(k+1) while trying to prove it; using the induction hypothesis without identifying it; and proving the step only for a specific numerical k.
