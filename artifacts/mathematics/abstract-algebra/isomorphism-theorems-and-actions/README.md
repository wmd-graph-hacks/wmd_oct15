---
id: math-abstract-algebra-isomorphism-theorems-and-actions
type: subtopic
title: Isomorphism theorems and actions
parent_topic: math-abstract-algebra
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-abstract-algebra-normal-subgroups-and-quotients
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in isomorphism theorems and actions
  - apply a standard method from isomorphism theorems and actions to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - abstract-algebra
  - advanced-core
---

# Isomorphism Theorems and Group Actions

An isomorphism is a bijective homomorphism: it says two groups have the same operation structure under different names. The first isomorphism theorem identifies a quotient by a kernel with an image. The second relates a subgroup H and normal subgroup N: H/(H∩N)≅HN/N. The third describes nested normal subgroups and quotienting in stages.

A group action assigns each group element a permutation of a set, compatibly with multiplication. It models symmetry. The orbit of x is {g·x:g∈G}; the stabilizer is {g:g·x=x}. For finite groups, orbit-stabilizer states |orbit(x)|·|stabilizer(x)|=|G|.

**Example.** Rotations of a square act on its four vertices. The orbit of a chosen vertex has size 4; its stabilizer contains only the identity rotation, size 1; group size is 4. If reflections are included (dihedral group size 8), the stabilizer of a vertex has size 2, again 4·2=8.

Actions convert symmetry into counting and can produce homomorphisms into permutation groups. To use orbit-stabilizer, verify the action and identify both the orbit and stabilizer, not just the group order.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: homomorphisms, isomorphisms, and actions

A group homomorphism φ:G→H preserves the operation: φ(ab)=φ(a)φ(b). Its kernel is a normal subgroup and its image is a subgroup. The first isomorphism theorem says G/kerφ is isomorphic to imφ: after collapsing exactly the elements mapped to identity, no information relevant to the image is lost. An isomorphism is a bijective homomorphism, expressing identical group structure under different labels.

A group action describes symmetries of a set: each group element permutes the set compatibly with multiplication. The orbit of x is all reachable points; the stabilizer fixes x. Orbit-stabilizer says |G|=|Orb(x)||Stab(x)| for finite groups. Actions turn abstract group facts into counting tools and permutation representations.

**Worked example.** Map φ:ℤ→ℤ₆ by φ(k)=k mod 6. It is a homomorphism with kernel 6ℤ and image ℤ₆. Hence ℤ/6ℤ is isomorphic to ℤ₆, directly illustrating the first isomorphism theorem.

**Practice with answers.** (1) Kernel contains identity and is normal. (2) For a transitive action of a group of order 12 with stabilizer size 3, orbit size is 4. (3) A bijection that fails operation preservation is not an isomorphism. (4) Check a proposed homomorphism on arbitrary products, not only sample elements.

**Common pitfalls:** forgetting operation preservation; confusing image and codomain; and using orbit-stabilizer without a genuine action.
