---
id: math-discrete-mathematics-and-combinatorics-recurrences-and-generating-functions
type: subtopic
title: Recurrences and generating functions
parent_topic: math-discrete-mathematics-and-combinatorics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-discrete-mathematics-and-combinatorics-counting-principles-and-binomial-theorem
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in recurrences and generating functions
  - apply a standard method from recurrences and generating functions to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - discrete-mathematics-and-combinatorics
  - core-to-advanced
---

# Recurrences and Generating Functions

A recurrence defines a sequence from earlier terms plus initial conditions. The recurrence alone is not enough to determine a unique sequence without enough starting values. For a linear constant-coefficient recurrence, try solutions rⁿ; the resulting characteristic equation determines the form. Repeated roots introduce polynomial factors such as nrⁿ.

**Example.** Fibonacci numbers satisfy Fₙ=Fₙ₋₁+Fₙ₋₂, F₀=0,F₁=1. Trying Fₙ=rⁿ yields r²−r−1=0, roots φ=(1+√5)/2 and ψ=(1−√5)/2. Therefore Fₙ=(φⁿ−ψⁿ)/√5. Initial values verify constants; substitution verifies the recurrence.

A generating function packages a sequence as G(x)=Σaₙxⁿ. Recurrences become algebraic equations for G, allowing coefficient extraction. For Fibonacci, index shifts turn the recurrence into G(x)=x/(1−x−x²). Generating functions are formal power series; convergence is not required for algebraic manipulation, though analytic convergence can also be studied.

Use generating functions for counting compositions, partitions, and recurrence solutions. Keep track of indexing: whether a sequence begins at n=0 or n=1 changes the algebra.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: recurrences and generating functions

A recurrence defines terms using earlier terms plus initial conditions. For aₙ=raₙ₋₁ the solution is geometric; for aₙ=aₙ₋₁+d it is arithmetic. Linear recurrences with constant coefficients can be solved with a characteristic equation. The recurrence is incomplete without enough starting values.

A generating function A(x)=Σₙ≥0aₙxⁿ packages a sequence into a power series. Shifting and multiplying series encode recurrence operations; coefficients of products count ways to split a total. Fibonacci numbers satisfy Fₙ=Fₙ₋₁+Fₙ₋₂ with F₀=0,F₁=1 and have generating function x/(1−x−x²).

**Worked example.** Let a₀=1 and aₙ=2aₙ₋₁. Then a₁=2, a₂=4, and induction gives aₙ=2ⁿ. Its generating function is Σ(2x)ⁿ=1/(1−2x) for |x|<1/2. Expanding recovers the sequence coefficients.

**Practice with answers.** (1) a₀=3, aₙ=aₙ₋₁+4 gives aₙ=3+4n. (2) Fibonacci values F₂,F₃,F₄ are 1,2,3. (3) The sequence 1,1,1,… has generating function 1/(1−x). (4) Verify a recurrence solution by checking initial values and substituting into the recurrence.

**Common pitfalls:** missing initial conditions; shifting indices incorrectly; and confusing the recurrence with its closed form.
