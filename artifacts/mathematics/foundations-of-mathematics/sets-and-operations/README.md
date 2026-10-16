---
id: math-foundations-of-mathematics-sets-and-operations
type: subtopic
title: Sets and operations
parent_topic: math-foundations-of-mathematics
phase: foundation
estimated_minutes: 45
prerequisites:
  - id: math-foundations-of-mathematics-mathematical-induction
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in sets and operations
  - apply a standard method from sets and operations to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - foundations-of-mathematics
  - foundation
---

# Sets and Operations

A set is a collection of distinct objects. The notation x∈A means x is an element; A⊆B means every element of A is also in B. Two sets are equal exactly when they have the same elements, which is often proved by showing A⊆B and B⊆A. The empty set ∅ has no elements. The power set P(A) is the set of all subsets of A; if A has n elements, P(A) has 2ⁿ elements.

Union collects elements in either set: A∪B={x:x∈A or x∈B}. Intersection collects elements in both: A∩B={x:x∈A and x∈B}. A\B contains elements in A but not B. A complement Aᶜ depends on a fixed universal set U and contains elements of U outside A. Cartesian product A×B consists of ordered pairs (a,b), so generally A×B≠B×A.

**Worked example.** Let U={1,2,3,4,5,6}, A={1,2,3,4}, B={3,4,5}. Then A∩B={3,4}, A∪B={1,2,3,4,5}, A\B={1,2}, and Aᶜ={5,6}. Check De Morgan’s law (A∪B)ᶜ=Aᶜ∩Bᶜ: both sides equal {6}. The law is not a trick to memorize; membership gives a proof. x is outside A∪B exactly when x is outside A and outside B.

Set-builder notation describes a set by a condition, such as {n∈ℤ: n is even}. Be precise about the domain and whether endpoints are included. An interval [a,b] includes endpoints; (a,b) does not. In proofs involving set identities, begin with “Let x be arbitrary” and translate membership into logical conditions.

**Practice with answers.** Let A={a,b,c} and B={b,c,d}. (1) A∩B={b,c}. (2) A\B={a}. (3) A∪B={a,b,c,d}. (4) P({0,1})={∅,{0},{1},{0,1}}. (5) Is {1,2} an element of P({1,2,3})? Yes, because it is a subset. (6) Prove A∩(B∪C)=(A∩B)∪(A∩C): an element belongs to the left exactly when it is in A and (in B or in C), equivalent to (in A and B) or (in A and C).

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Deeper lesson: proving set identities

Set identities are most reliably proved from definitions. To prove A=B, show both inclusions. For A⊆B, let x be arbitrary and assume x∈A; translate this membership into its defining conditions and derive x∈B. Repeat with the roles reversed. This method works for finite and infinite sets, unlike checking a few examples.

**Worked example.** Prove A\(B∪C)=(A\B)∩(A\C). Take arbitrary x. Membership in the left means x∈A and x∉B∪C. The latter means x∉B and x∉C. Thus x∈A\B and x∈A\C, so x belongs to the right. Reversing these equivalences proves the reverse inclusion. This is an instance of De Morgan’s laws combined with set difference.

For finite sets, the power set P(A) is the set of all subsets of A. If |A|=n, then |P(A)|=2ⁿ because each element is either included or excluded from a chosen subset. A×B records ordered choices; if the sets are finite, |A×B|=|A||B|. These facts connect sets to counting and Cartesian products to relations and functions.

**Practice with answers.** (1) If A has 4 elements, |P(A)|=16. (2) If |A|=3 and |B|=5, |A×B|=15. (3) Is A∩B⊆A always true? Yes, since membership in the intersection includes membership in A. (4) Is A⊆A∪B always true? Yes. (5) For U={1,2,3,4}, A={1,3}, find Aᶜ={2,4}. Then check A∪Aᶜ=U and A∩Aᶜ=∅.

**Common pitfalls:** using “or” to mean exclusive-or without saying so; forgetting that a complement changes when U changes; confusing ∈ with ⊆; and proving only one inclusion when asked to prove equality.
