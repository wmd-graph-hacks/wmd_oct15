---
id: math-foundations-of-mathematics-logic-and-quantifiers
type: subtopic
title: Logic and quantifiers
parent_topic: math-foundations-of-mathematics
phase: foundation
estimated_minutes: 45
prerequisites: []
learning_outcomes:
  - define the central objects and notation in logic and quantifiers
  - apply a standard method from logic and quantifiers to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - foundations-of-mathematics
  - foundation
---

# Logic and Quantifiers

Mathematics begins by making claims precise. A proposition is a statement that is either true or false. “7 is prime” is a proposition; “x is prime” is an open sentence until x is specified or quantified. Logical connectives build larger propositions: ¬P (not P), P∧Q (both), P∨Q (at least one), and P⇒Q (if P then Q). In mathematics, “or” is inclusive unless stated otherwise.

An implication P⇒Q is false only when P is true and Q is false. It is logically equivalent to its contrapositive ¬Q⇒¬P, but generally not to its converse Q⇒P. For example, “if n is divisible by 4, then n is even” is true; its converse is false because 6 is even but not divisible by 4. The biconditional P⇔Q means both implications hold.

Quantifiers specify how broadly a predicate applies. ∀x∈S P(x) means every member of S has property P; ∃x∈S P(x) means at least one does. Order matters: ∀x∃y (y>x) is true over the real numbers, while ∃y∀x (y>x) is false. Negation changes the quantifier and negates the predicate: ¬∀x P(x) is ∃x ¬P(x); ¬∃x P(x) is ∀x ¬P(x).

**Worked example.** Negate “For every real x>0, there is a real y such that y²=x.” Its form is ∀x>0 ∃y∈ℝ (y²=x). Negate one quantifier at a time: ∃x>0 ∀y∈ℝ (y²≠x). This says there is a positive real number that is not the square of any real number. The claim is false because every positive real has a real square root, but the negation is formed correctly.

**How to solve a quantified claim.** To prove a universal statement, take an arbitrary allowed object and prove the predicate. To disprove it, give one counterexample. To prove an existential statement, exhibit a witness and verify it. To disprove it, show every candidate fails. Keep the domain visible: a statement may be true over ℝ and false over ℤ.

**Practice with answers.** (1) Negate “Every integer has a larger integer.” Answer: “There exists an integer n such that no integer is larger than n.” (2) Is “If x²=9, then x=3” true over ℝ? No; x=−3 is a counterexample. (3) Repair it: “If x²=9 and x≥0, then x=3.” This is true. (4) Write “Some student solved every exercise” symbolically. One form is ∃s∈Students ∀e∈Exercises Solved(s,e).

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Deeper lesson: implication, equivalence, and quantifier order

An implication P⇒Q is a promise about cases where P holds. It says nothing about cases where P is false. This explains why a false hypothesis makes an implication true, and why proving the converse requires separate work. To prove P⇒Q, use the hypothesis P and derive Q; alternatively prove the contrapositive ¬Q⇒¬P. To prove P⇔Q, prove both directions, often under separate headings.

Quantifier order expresses dependence. “For every real x, there is a y>x” permits y to depend on x: choose y=x+1. “There is a y greater than every real x” requires a single fixed y and is false: given any candidate y, choose x=y+1. When negating nested quantifiers, switch each quantifier in place and negate the final predicate.

**Worked example.** Negate “For every positive integer n, there exists an integer k such that n=2k.” The negation is: “There exists a positive integer n such that for every integer k, n≠2k.” The witness n=1 proves the negation true. Notice how the negation changes the original claim into a statement about an odd integer, not a claim that no positive integer is even.

**Practice with answers.** (1) Negate “For every x∈ℝ there exists y∈ℝ with y>x”: ∃x∈ℝ such that ∀y∈ℝ, y≤x; false, since x+1 is always larger. (2) Is “x²=1 implies x=1” true over ℝ? No; x=−1 is a counterexample. (3) State the contrapositive of “If n² is divisible by 3, then n is divisible by 3”: if n is not divisible by 3, n² is not divisible by 3.

**Self-check:** underline the domain, circle every quantifier, and test whether a witness may depend on an earlier variable. For a universal claim seek a proof or one counterexample; for an existential claim supply one witness or rule out all candidates.
