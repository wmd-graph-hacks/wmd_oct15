---
id: math-topology-and-number-theory-fermat-euler-quadratic-reciprocity
type: subtopic
title: Fermat, Euler, quadratic reciprocity
parent_topic: math-topology-and-number-theory
phase: optional-extension
estimated_minutes: 60
prerequisites:
  - id: math-topology-and-number-theory-divisibility-primes-modular-arithmetic
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in fermat, euler, quadratic reciprocity
  - apply a standard method from fermat, euler, quadratic reciprocity to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - topology-and-number-theory
  - optional-extension
---

# Fermat, Euler, and Quadratic Reciprocity

Fermat’s little theorem states that for prime p and p∤a, a^(p−1)≡1 (mod p). Euler’s theorem generalizes this: if gcd(a,n)=1, then a^φ(n)≡1 (mod n), where φ(n) counts residues coprime to n. These results reduce large modular powers by reducing exponents.

Quadratic residues ask whether x²≡a (mod p) has a solution. The Legendre symbol (a/p) is 1 for a nonzero square mod p, −1 for a nonsquare, and 0 when p|a. Quadratic reciprocity relates whether p is a square modulo q to whether q is a square modulo p, with a sign determined by residues mod 4.

**Example.** Compute 3¹⁰⁰ mod 7. Since 3⁶≡1 mod 7, reduce exponent 100 mod 6 to 4; 3¹⁰⁰≡3⁴=81≡4 mod 7.

These theorems require coprimality/prime conditions exactly as stated. They provide arithmetic structure, not a shortcut that works for arbitrary modulus and non-coprime bases.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: modular power theorems

Fermat’s Little Theorem says if p is prime and p∤a, then a^(p−1)≡1 (mod p). Euler’s theorem generalizes this: if gcd(a,n)=1, then a^φ(n)≡1 (mod n), where φ(n) counts residues relatively prime to n. These results reduce large exponents but require the coprimality assumptions.

Quadratic reciprocity answers whether a prime p is a square modulo another odd prime q. The Legendre symbol (a/p) is 1 if a is a nonzero square mod p, −1 if a is a nonsquare, and 0 if p divides a. Reciprocity relates (p/q) and (q/p), with a sign determined by residues modulo 4. It is a theorem about quadratic solvability, not ordinary real square roots.

**Worked example.** Compute 3¹⁰ mod 7. Since 3⁶≡1 (mod 7), reduce exponent 10 to 4: 3¹⁰≡3⁴=81≡4. The base 3 is coprime to prime 7, so Fermat applies.

**Practice with answers.** (1) 2⁶≡1 mod 7. (2) φ(9)=6. (3) Euler’s theorem applies to a=2,n=9 and gives 2⁶≡1 mod 9. (4) It does not directly apply to a=3,n=9 because they are not coprime.

**Common pitfalls:** applying Fermat with composite modulus; forgetting gcd conditions; and mixing the Legendre symbol’s sign rule with a claim about integer divisibility.
