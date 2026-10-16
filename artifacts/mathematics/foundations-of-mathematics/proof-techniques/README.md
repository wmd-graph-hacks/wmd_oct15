---
id: math-foundations-of-mathematics-proof-techniques
type: subtopic
title: Proof techniques
parent_topic: math-foundations-of-mathematics
phase: foundation
estimated_minutes: 45
prerequisites:
  - id: math-foundations-of-mathematics-logic-and-quantifiers
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in proof techniques
  - apply a standard method from proof techniques to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - foundations-of-mathematics
  - foundation
---

# Proof Techniques

A proof is a finite chain of justified steps that turns assumptions into the desired conclusion. Before choosing a method, identify the domain, hypotheses, and exact conclusion. Definitions are often the best starting point: “even” means 2k for some integer k; “divides” means an integer multiple; “injective” means equal outputs force equal inputs.

**Direct proof.** Assume the hypotheses and derive the conclusion. To show the sum of two even integers is even, write them as 2a and 2b. Their sum is 2(a+b), and a+b is an integer, so the sum is even. The proof works because it expands the definition and returns to the definition.

**Contrapositive.** To prove P⇒Q, it is enough to prove ¬Q⇒¬P. Use this when the negation of the conclusion has a useful form. Example: if n² is odd, then n is odd. Prove the contrapositive: if n is even, n=2k, so n²=4k²=2(2k²), which is even. Thus an even square cannot be odd, proving the original implication.

**Contradiction.** Assume the claim is false and derive an impossibility. To prove √2 is irrational, suppose √2=a/b in lowest terms, with integers a,b and b≠0. Then a²=2b², so a² is even and therefore a is even. Put a=2k; then 4k²=2b², so b²=2k² and b is also even. Both a and b are divisible by 2, contradicting that the fraction was in lowest terms.

**Proof by cases.** Split the domain into cases that cover every possibility. For any integer n, either n is even or odd. If proving n²−n is even, in the even case n=2k and n(n−1) is a product with an even factor; in the odd case n−1 is even. These cases are exhaustive.

**Existence and uniqueness.** Existence requires producing an object. Uniqueness requires showing any two objects with the property are equal. If an object x satisfies a property and any y satisfying it must equal x, then exactly one object exists. Do not confuse “I found one” with “there is only one.”

**Practice with answers.** (1) Prove the sum of two odd integers is even: (2a+1)+(2b+1)=2(a+b+1). (2) For “if 3n+1 is even, then n is odd,” use parity: if n were even, 3n+1 would be odd; hence n cannot be even. (3) Find the flaw: “All birds fly; penguins are birds; therefore penguins fly.” The inference form is valid, but the first premise is false. A proof must establish or be allowed to assume its premises.

## Study sequence

1. Read the explanations and reproduce the worked example without looking.
2. Solve the practice questions on paper before checking the answers.
3. Write down the definition or theorem used and why its conditions apply.
4. Revisit the material after a delay and solve a changed version of one problem.

## Lesson: choosing a proof strategy

Before writing, unpack the statement: identify the domain, assumptions, conclusion, and definitions involved. For a direct proof of P⇒Q, assume P and build a chain that ends at Q. For a contrapositive proof, assume ¬Q and derive ¬P. Contradiction assumes the negation of the desired claim and derives an impossibility such as 0=1 or an object being both even and odd. Use cases when the cases are exhaustive and do not overlap, or when overlap is harmless.

**Worked example.** Prove the sum of two odd integers is even. Let m and n be arbitrary odd integers. By definition m=2a+1 and n=2b+1 for some integers a,b. Then m+n=2(a+b+1), and a+b+1 is an integer; hence m+n is even. The proof works because it begins with arbitrary objects and uses the definitions of odd and even.

For an existential statement, construct a witness and verify it. For uniqueness, assume x and y both satisfy the property and prove x=y. To disprove “for all x, P(x),” one counterexample is sufficient. Examples can reveal a pattern, but they do not prove a universal claim unless a theorem justifies the generalization.

**Practice with answers.** (1) Prove the product of two even integers is even: (2a)(2b)=2(2ab). (2) Prove if n² is even then n is even: contrapositively, if n is odd, n=2k+1 and n²=2(2k²+2k)+1, odd. (3) Disprove “every prime is odd”: 2 is a counterexample. (4) To prove there is an even prime, exhibit 2 and verify it has exactly two positive divisors.

**Proof editing checklist:** Are variables arbitrary but within the stated domain? Is each inference justified? Did the argument establish the exact conclusion rather than a converse? Is a constructed integer actually an integer? Can a reader identify where each hypothesis was used?
