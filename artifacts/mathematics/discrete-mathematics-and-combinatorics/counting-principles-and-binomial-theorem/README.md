---
id: math-discrete-mathematics-and-combinatorics-counting-principles-and-binomial-theorem
type: subtopic
title: Counting principles and binomial theorem
parent_topic: math-discrete-mathematics-and-combinatorics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-foundations-of-mathematics-sets-and-operations
    target_type: subtopic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in counting principles and binomial theorem
  - apply a standard method from counting principles and binomial theorem to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - discrete-mathematics-and-combinatorics
  - core-to-advanced
---

# Counting Principles and the Binomial Theorem

The product rule counts sequential choices: if one stage has m options and another n options, there are mn combined choices. The sum rule adds disjoint alternatives. For ordered selections of k objects from n, use n!/(n−k)!; for unordered selections use C(n,k)=n!/[k!(n−k)!]. Decide whether order matters and whether repetition is allowed before choosing a formula.

The binomial theorem expands (x+y)ⁿ=Σₖ C(n,k)x^(n−k)yᵏ. The coefficient counts which k of n factors contribute y. Pascal’s identity C(n,k)=C(n−1,k)+C(n−1,k−1) follows by splitting selections according to whether a particular element is included.

**Example.** How many 4-digit codes use distinct digits 0–9? The first position has 10 choices, then 9, 8, 7, giving 10·9·8·7=5040. If leading zero is forbidden, the first position has 9 choices, then 9,8,7: 4536. State what a code allows; wording changes the count.

**Practice.** Choose 3 students from 10: C(10,3)=120. Arrange 3 of 10 in roles: 10·9·8=720. Coefficient of x²y³ in (x+y)⁵ is C(5,3)=10.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: systematic counting

The addition principle counts disjoint alternatives; the multiplication principle counts sequential choices. If r choices are made from n distinct objects, order matters for permutations P(n,r)=n!/(n−r)!, while unordered selections use combinations C(n,r)=n!/[r!(n−r)!]. Repetition changes the model: ordered length-r strings from n symbols allow nʳ outcomes. State whether order and repetition matter before choosing a formula.

The binomial theorem expands (x+y)ⁿ=ΣₖC(n,k)xⁿ⁻ᵏyᵏ. Coefficients count choices of which k factors contribute y. Pascal’s identity C(n,k)=C(n−1,k−1)+C(n−1,k) follows by asking whether a chosen k-set contains a fixed element.

**Worked example.** A 4-digit code uses digits 0–9 with repetition allowed: 10⁴ codes. If digits cannot repeat, 10·9·8·7. If it is a 4-digit number with a nonzero first digit and no repetition, 9·9·8·7. The first-position restriction changes the count.

**Practice with answers.** (1) Choose 3 of 8 books: C(8,3)=56. (2) Arrange 3 of 8 books: 8·7·6=336. (3) Coefficient of x²y³ in (x+y)⁵ is C(5,3)=10. (4) A 6-element set has 2⁶=64 subsets.

**Common pitfalls:** multiplying overlapping cases; using combinations when order matters; forgetting leading-zero restrictions; and counting the same arrangement more than once.
