---
id: math-foundations-of-mathematics-relations-and-equivalence
type: subtopic
title: Relations and equivalence
parent_topic: math-foundations-of-mathematics
phase: foundation
estimated_minutes: 45
prerequisites:
  - id: math-foundations-of-mathematics-sets-and-operations
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in relations and equivalence
  - apply a standard method from relations and equivalence to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - foundations-of-mathematics
  - foundation
---

# Relations and Equivalence

A binary relation R on a set A is a set of ordered pairs from A×A. We write aRb when (a,b)∈R. Relations model comparison, divisibility, connectivity, and sameness. Four properties are especially useful: reflexive (aRa for all a), symmetric (aRb implies bRa), antisymmetric (aRb and bRa imply a=b), and transitive (aRb and bRc imply aRc).

An **equivalence relation** is reflexive, symmetric, and transitive. It groups elements that count as equivalent under some chosen criterion. The equivalence class [a]={x∈A:xRa} contains all elements equivalent to a. Equivalence classes either coincide or are disjoint, so they partition A.

**Worked example: congruence.** For integers a,b and positive n, define a≡b (mod n) when n divides a−b. Reflexive because n divides 0; symmetric because n divides b−a=−(a−b); transitive because if n divides a−b and b−c, it divides their sum a−c. Modulo 5, the class of 2 is …,−8,−3,2,7,12,…; each member leaves remainder 2 on division by 5. The five classes are represented by 0,1,2,3,4.

A **partial order** is reflexive, antisymmetric, and transitive. For example, ⊆ orders subsets of a set, but two subsets need not be comparable. A **total order** additionally requires every pair to be comparable; ≤ on real numbers is total. Do not confuse symmetric with antisymmetric: symmetric allows two-way related distinct elements, while antisymmetric rules that out.

**Practice with answers.** (1) On integers, “x≤y” is reflexive, antisymmetric, and transitive, but not symmetric. (2) “x−y is divisible by 3” is an equivalence relation. (3) “x divides y” on positive integers is a partial order: if x|y and y|x, positivity forces x=y. (4) Why do equivalence classes partition A? Every a lies in [a] by reflexivity; if two classes overlap, symmetry and transitivity show their representatives are equivalent, so the classes are equal.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: relations, equivalence, and order

A relation from A to B is any subset of A×B. A relation R on a set A can be tested for properties: reflexive means aRa for every a; symmetric means aRb implies bRa; antisymmetric means aRb and bRa together imply a=b; transitive means aRb and bRc imply aRc. These are independent properties, so check each from its definition.

An equivalence relation is reflexive, symmetric, and transitive. It partitions a set into equivalence classes [a]={x∈A:xRa}; two classes are either equal or disjoint. Congruence modulo n is a standard example: a≡b (mod n) exactly when n divides a−b. The equivalence classes modulo 3 are the numbers with remainders 0, 1, and 2.

A partial order is reflexive, antisymmetric, and transitive. It need not compare every pair. Set inclusion ⊆ is a partial order: neither {1}⊆{2} nor {2}⊆{1}, so the sets are incomparable. A total order adds comparability of every pair, as ≤ does on real numbers. A Hasse diagram can display a finite partial order by omitting transitive edges.

**Worked example.** On integers define aRb when a−b is divisible by 5. Reflexivity follows because a−a=0 is divisible by 5. Symmetry follows because b−a=−(a−b) is divisible by 5. If a−b and b−c are divisible by 5, their sum a−c is divisible by 5, proving transitivity. Thus R is an equivalence relation, with five residue classes.

**Practice with answers.** (1) “a is the same age as b” is an equivalence relation if age is defined consistently. (2) “a≤b” on integers is a total order. (3) “a divides b” on positive integers is a partial order, not symmetric. (4) Equality of absolute values on integers is an equivalence relation; the class of 3 is {−3,3}.

**Common pitfalls:** checking only some axioms; mistaking antisymmetric for “not symmetric”; assuming an equivalence class contains just one representative; and assuming every partial order is total.
