---
id: math-topology-and-number-theory-divisibility-primes-modular-arithmetic
type: subtopic
title: Divisibility, primes, modular arithmetic
parent_topic: math-topology-and-number-theory
phase: optional-extension
estimated_minutes: 60
prerequisites:
  - id: math-topology-and-number-theory-connectedness-and-fundamental-group
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in divisibility, primes, modular arithmetic
  - apply a standard method from divisibility, primes, modular arithmetic to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - topology-and-number-theory
  - optional-extension
---

# Divisibility, Primes, and Modular Arithmetic

For integers a,b, a divides b (a|b) if b=ak for some integer k. The Euclidean algorithm repeatedly divides with remainder and computes gcd(a,b); reversing the steps yields Bézout coefficients u,v with ua+vb=gcd(a,b). A prime has exactly two positive divisors, 1 and itself; every integer greater than 1 factors uniquely into primes up to order.

Congruence a≡b (mod n) means n|(a−b). Addition and multiplication preserve congruence, enabling arithmetic with residue classes. A multiplicative inverse of a modulo n exists exactly when gcd(a,n)=1. Solve linear congruences using gcd conditions and Bézout’s identity.

**Example.** Solve 14x≡8 (mod 30). gcd(14,30)=2 divides 8, so solutions exist. Divide by 2: 7x≡4 (mod 15). Since 7⁻¹≡13 mod 15 (7·13=91≡1), x≡52≡7 (mod 15). Modulo 30 there are two residue solutions, 7 and 22.

Always reduce modulo n after operations and check whether division is legal: cancellation requires an invertible factor modulo n.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: divisibility and arithmetic modulo n

For integers a,b with a≠0, a divides b if b=ak for some integer k. The Euclidean algorithm repeatedly writes a=bq+r with 0≤r<|b|; the last nonzero remainder is gcd(a,b). Back-substitution expresses the gcd as a linear combination of a and b (Bézout’s identity). A prime has exactly two positive divisors and is the basic multiplicative building block by unique factorization.

Congruence a≡b (mod n) means n divides a−b. Addition and multiplication preserve congruence, so calculations can be reduced to residues 0,…,n−1. Division is allowed only by a residue coprime to n, which then has a modular inverse found by the extended Euclidean algorithm. Composite moduli may have nonzero residues without inverses.

**Worked example.** Find inverse of 3 mod 7. Euclidean algorithm gives 7=2·3+1, hence 1=7−2·3, so −2 is an inverse and 3⁻¹≡5 mod 7. Check 3·5=15≡1. Solve 3x≡2 mod 7 by multiplying by 5: x≡10≡3.

**Practice with answers.** (1) gcd(48,18)=6. (2) 17≡2 (mod 5). (3) 2 has no inverse mod 6 because gcd(2,6)≠1. (4) A linear congruence ax≡b mod n has a solution iff gcd(a,n) divides b.

**Common pitfalls:** dividing a congruence by a nonunit; confusing prime with coprime; and forgetting to reduce the final residue to a chosen representative.
