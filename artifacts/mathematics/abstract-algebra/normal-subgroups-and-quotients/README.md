---
id: math-abstract-algebra-normal-subgroups-and-quotients
type: subtopic
title: Normal subgroups and quotients
parent_topic: math-abstract-algebra
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-abstract-algebra-groups-subgroups-cosets
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in normal subgroups and quotients
  - apply a standard method from normal subgroups and quotients to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - abstract-algebra
  - advanced-core
---

# Normal Subgroups and Quotient Groups

A subgroup N is normal if gN=Ng for every g, equivalently gNg⁻¹=N. Normality is the condition that makes coset multiplication well-defined: (aN)(bN)=abN. The quotient group G/N treats all elements in a coset as equivalent.

Every group homomorphism φ:G→K preserves the operation: φ(ab)=φ(a)φ(b). Its kernel kerφ={g:φ(g)=e} is always a normal subgroup. The image is a subgroup of K. The first isomorphism theorem states G/kerφ is isomorphic to imφ: once the kernel is collapsed, no further information is lost.

**Example.** φ:ℤ→ℤ₆ given by φ(n)=n mod 6 is a homomorphism. Kernel is 6ℤ, image is ℤ₆, so ℤ/6ℤ≅ℤ₆. The quotient identifies integers differing by a multiple of six.

To show a subgroup is normal, use conjugation or exploit commutativity (all subgroups of an abelian group are normal). A quotient construction requires normality; arbitrary cosets do not automatically form a group.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: normality makes quotient operations well-defined

A subgroup N is normal if gN=Ng for every g, equivalently gNg⁻¹=N. Every subgroup of an abelian group is normal; kernels of homomorphisms are always normal. Normality is exactly what makes multiplication of cosets independent of representatives: (aN)(bN)=abN.

The quotient group G/N consists of cosets, with this induced operation. The quotient map sends g to gN. Its kernel is N. Quotients collapse the normal subgroup to the identity and preserve the remaining algebraic structure. In ℤ modulo n, the quotient ℤ/nℤ is a finite additive group of residue classes.

**Worked example.** In ℤ, N=3ℤ is normal because the group is abelian. The quotient has three elements [0],[1],[2], with [2]+[2]=[1]. Choosing different representatives gives the same class: 2+2=4≡1 mod 3, and 5+5=10≡1 mod 3.

**Practice with answers.** (1) Every kernel is normal. (2) A nonnormal subgroup cannot generally be used to form a quotient group. (3) The quotient ℤ/2ℤ has two classes. (4) In an abelian group all subgroups are normal.

**Common pitfalls:** multiplying cosets before checking normality; assuming every subgroup is normal in a nonabelian group; and confusing a coset with a quotient element’s representative.
