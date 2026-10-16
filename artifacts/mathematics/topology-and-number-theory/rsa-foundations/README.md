---
id: math-topology-and-number-theory-rsa-foundations
type: subtopic
title: RSA foundations
parent_topic: math-topology-and-number-theory
phase: optional-extension
estimated_minutes: 60
prerequisites:
  - id: math-topology-and-number-theory-fermat-euler-quadratic-reciprocity
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in rsa foundations
  - apply a standard method from rsa foundations to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - topology-and-number-theory
  - optional-extension
---

# RSA Foundations

RSA illustrates how modular arithmetic can support public-key encryption. Choose distinct large primes p,q; set n=pq and φ(n)=(p−1)(q−1). Choose e coprime to φ(n), then find d with ed≡1 mod φ(n). Public key is (n,e); private key includes d. Encryption maps message m to c≡mᵉ mod n; decryption computes cᵈ mod n.

Why does it work? ed=1+kφ(n). For m coprime to n, Euler’s theorem gives m^{φ(n)}≡1 mod n, so m^{ed}≡m mod n. A fuller argument handles messages divisible by p or q using congruences and the Chinese remainder theorem.

**Small example (not secure).** Let p=5,q=11, n=55, φ=40. Choose e=3 and d=27 because 3·27=81≡1 mod 40. Message m=2 encrypts to 2³=8 mod 55; decrypt 8²⁷ mod 55 by repeated squaring to recover 2. Tiny primes demonstrate arithmetic only; they can be factored immediately.

Real RSA requires cryptographically secure primes, padding such as OAEP, careful implementation, and key management. Raw textbook RSA is deterministic and insecure. The number-theory lesson is modular exponentiation and inverses, not a production cryptography recipe.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: public-key arithmetic with RSA

RSA chooses distinct primes p,q, sets n=pq and φ(n)=(p−1)(q−1), then chooses e coprime to φ(n). The private exponent d satisfies ed≡1 (mod φ(n)). A message represented by an integer m with 0≤m<n is encrypted as c=mᵉ mod n and decrypted as cᵈ mod n. Euler/Fermat structure explains why decryption recovers m for valid parameters.

**Worked example (toy only).** Let p=5,q=11, so n=55 and φ(n)=40. Choose e=3; its inverse modulo 40 is d=27 because 3·27=81≡1. Encrypt m=7: c=7³ mod55=13. Decrypt 13²⁷ mod55 by repeated squaring and obtain 7. These tiny values are easy to factor and are not secure.

Real RSA requires very large random primes, padding schemes, secure key generation, and vetted implementations. Raw RSA is deterministic and insecure. Security depends on factoring difficulty and correct engineering; classroom arithmetic illustrates the number theory, not a production cryptosystem.

**Practice with answers.** (1) For p=3,q=7, n=21 and φ(n)=12. (2) e=5 is coprime to 12 and inverse d=5. (3) Why require gcd(e,φ(n))=1? So e has a modular inverse. (4) Why is raw RSA unsuitable? It is deterministic and reveals structure.

**Common pitfalls:** using small primes in real systems; choosing e without checking coprimality; encrypting messages outside 0≤m<n; and treating toy RSA as secure practice.
