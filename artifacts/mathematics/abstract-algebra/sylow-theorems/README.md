---
id: math-abstract-algebra-sylow-theorems
type: subtopic
title: Sylow theorems
parent_topic: math-abstract-algebra
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-abstract-algebra-isomorphism-theorems-and-actions
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in sylow theorems
  - apply a standard method from sylow theorems to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - abstract-algebra
  - advanced-core
---

# Sylow Theorems

Let |G|=pᵃm, where p is prime and p does not divide m. A Sylow p-subgroup has order pᵃ, the largest power of p dividing |G|. Sylow’s theorems say such subgroups exist; every p-subgroup lies in a conjugate of one; and the number nₚ of Sylow p-subgroups divides m and satisfies nₚ≡1 (mod p).

These arithmetic restrictions often force normality. If nₚ=1, the unique Sylow subgroup is normal because conjugation must send it to another Sylow subgroup, and there is only one.

**Example.** A group of order 15 has p=5 part 5 and complementary m=3. Thus n₅ divides 3 and is 1 mod 5; only n₅=1 works. The subgroup of order 5 is normal. For p=3, n₃ divides 5 and is 1 mod 3, so n₃ can be 1 or 4.

Sylow counting is a constraint method, not a complete classification by itself. Combine it with subgroup intersections, conjugacy, and known group structures. Keep straight the prime-power subgroup order pᵃ and the number nₚ of such subgroups.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: count subgroups of prime-power order

Write a finite group order as |G|=pⁿm with p∤m. Sylow’s theorems state that p-subgroups exist of order pⁿ; every p-subgroup lies in a conjugate of a Sylow p-subgroup; and the number nₚ of Sylow p-subgroups divides m and is congruent to 1 mod p. These constraints often determine nₚ and reveal normality: a unique Sylow subgroup is normal.

**Worked example.** If |G|=15=3·5, the number n₅ divides 3 and is 1 mod 5. Only n₅=1 works, so the subgroup of order 5 is unique and normal. For n₃, it divides 5 and is 1 mod 3, so n₃ is 1 or 4. The theorem narrows possibilities but may not decide uniquely.

To use Sylow effectively, first identify the prime-power part, list divisors of the remaining factor, then retain values congruent to 1 modulo p. Do not confuse “a subgroup exists” with “it is unique.”

**Practice with answers.** (1) For group order 21, n₇ divides 3 and is 1 mod 7, so n₇=1. (2) For order 12, n₃ divides 4 and is 1 mod 3: n₃=1 or 4. (3) Unique Sylow subgroup is normal. (4) Conjugate Sylow subgroups have equal order.

**Common pitfalls:** using the wrong complementary factor m; forgetting both divisibility and congruence; and concluding normality when more than one subgroup may exist.
