---
id: math-abstract-algebra-fields-extensions-galois-introduction
type: subtopic
title: Fields, extensions, Galois introduction
parent_topic: math-abstract-algebra
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-abstract-algebra-domains-pids-ufds-polynomial-rings
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in fields, extensions, galois introduction
  - apply a standard method from fields, extensions, galois introduction to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - abstract-algebra
  - advanced-core
---

# Fields, Extensions, and Galois Theory

A field permits addition, subtraction, multiplication, and division by nonzero elements. A field extension K/F is a larger field containing F. Its degree [K:F] is the dimension of K as a vector space over F. If α is algebraic over F, it satisfies a nonzero polynomial; its minimal polynomial is the monic irreducible polynomial of least degree that α satisfies.

**Example.** ℚ(√2)={a+b√2:a,b∈ℚ} has basis {1,√2} over ℚ, degree 2, because √2 satisfies x²−2. Its ℚ-automorphisms fix rationals and send √2 to either root ±√2. These symmetries form a group of order 2.

Galois theory studies the relationship between field extensions and groups of automorphisms that fix the base field. In a suitable finite Galois extension, intermediate fields correspond to subgroups of the Galois group, reversing inclusion. This connects polynomial solvability to group structure. The introductory goal is to understand roots, splitting fields, automorphisms, and why symmetries reveal algebraic structure—not to memorize the full theorem without examples.

Distinguish an extension field from its degree, and distinguish roots in an algebraic closure from roots already in the base field.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: extend a field and study its symmetries

A field extension K/F contains F as a subfield. Its degree [K:F] is the dimension of K as a vector space over F. For α algebraic over F, adjoining it gives F(α); its degree equals the degree of α’s minimal polynomial. Tower law multiplies degrees through nested finite extensions.

Galois theory studies automorphisms of extensions that fix the base field. For a finite Galois extension, the number of automorphisms equals the degree, and subgroups of the Galois group correspond to intermediate fields in reverse inclusion. The roots of a polynomial are permuted by these symmetries. This explains why some polynomial equations can be solved by radicals and why general degree-five equations cannot.

**Worked example.** ℚ(√2) consists of a+b√2 with rational a,b and has basis {1,√2}, so degree 2. Its two automorphisms fixing ℚ are identity and the map √2↦−√2. Their fixed elements are exactly ℚ.

**Practice with answers.** (1) [ℚ(√2):ℚ]=2. (2) The minimal polynomial of √2 over ℚ is x²−2. (3) The tower law gives [K:F]=[K:E][E:F] for F⊆E⊆K finite. (4) An automorphism preserves addition, multiplication, and identity.

**Common pitfalls:** confusing an extension’s elements with its degree; choosing a polynomial that is not minimal; and assuming every extension is Galois or every root permutation is allowed.
