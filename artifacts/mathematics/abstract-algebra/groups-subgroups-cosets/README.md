---
id: math-abstract-algebra-groups-subgroups-cosets
type: subtopic
title: Groups, subgroups, cosets
parent_topic: math-abstract-algebra
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-foundations-of-mathematics
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in groups, subgroups, cosets
  - apply a standard method from groups, subgroups, cosets to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - abstract-algebra
  - advanced-core
---

# Groups, Subgroups, and Cosets

A group is a set G with an associative operation, identity e, and inverses. Examples include integers under addition, nonzero real numbers under multiplication, and permutations under composition. The operation need not be commutative; permutation composition is generally not. A subgroup H⊆G is itself a group under the inherited operation. A convenient test: H is nonempty and ab⁻¹∈H for every a,b∈H.

Left cosets gH={gh:h∈H} partition G into equal-size pieces. For finite G, this proves Lagrange’s theorem: |H| divides |G|. Therefore element orders divide group order. The converse is false: a group may have a divisor d of its order but no subgroup of order d.

**Example.** In ℤ under addition, subgroup 3ℤ={…,−6,−3,0,3,6,…} has cosets 3ℤ, 1+3ℤ, 2+3ℤ, corresponding to residues mod 3. They partition ℤ. The quotient has three elements.

Cosets are equal or disjoint; gH=kH exactly when k⁻¹g∈H. For finite groups, the number of left cosets is the index [G:H], and |G|=|H|[G:H]. Do not assume a coset is a subgroup; generally only the identity coset H is.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: groups, subgroups, and cosets

A group is a set with an associative operation, identity, and inverses. The operation need not be commutative. A subset H is a subgroup if it contains identity and is closed under products and inverses; a useful test is that H is nonempty and ab⁻¹∈H for all a,b∈H. Examples include integers under addition and nonzero residues under multiplication when inverses exist.

Left cosets gH={gh:h∈H} partition a group into equal-sized blocks. Lagrange’s theorem says a subgroup’s order divides the finite group’s order, because cosets partition its elements. It implies the order of any element divides |G|. The converse “every divisor gives a subgroup” is false in general.

**Worked example.** In ℤ under addition, H=3ℤ is a subgroup. Its cosets are 3ℤ, 1+3ℤ, and 2+3ℤ, corresponding to residues mod 3. They partition the integers without overlap. In a finite group of order 12, any subgroup order must divide 12.

**Practice with answers.** (1) The even integers form a subgroup of (ℤ,+). (2) The positive integers do not form a subgroup because additive inverses are missing. (3) A subgroup of a group of order 10 can have order 1,2,5,10. (4) Cosets are either equal or disjoint.

**Common pitfalls:** assuming groups are commutative; checking closure but not inverses; and assuming Lagrange’s divisibility condition guarantees a subgroup of every divisor order.
