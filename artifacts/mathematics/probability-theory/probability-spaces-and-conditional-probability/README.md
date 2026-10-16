---
id: math-probability-theory-probability-spaces-and-conditional-probability
type: subtopic
title: Probability spaces and conditional probability
parent_topic: math-probability-theory
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-foundations-of-mathematics
    target_type: topic
    strength: recommended
  - id: math-single-variable-calculus
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in probability spaces and conditional probability
  - apply a standard method from probability spaces and conditional probability to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - probability-theory
  - core-to-advanced
---

# Probability Spaces and Conditional Probability

A probability model consists of a sample space Ω, a collection of events, and a probability P assigning each event a value in [0,1]. For finite equally likely outcomes, P(A)=|A|/|Ω|; for general models, probabilities obey P(Ω)=1 and countable additivity. The complement rule is P(Aᶜ)=1−P(A); for two events, P(A∪B)=P(A)+P(B)−P(A∩B).

Conditional probability updates the model after learning B occurred: P(A|B)=P(A∩B)/P(B), provided P(B)>0. Events A and B are independent when P(A∩B)=P(A)P(B), equivalently P(A|B)=P(A) when defined. Independence is not the same as disjointness: disjoint positive-probability events are dependent.

Bayes’ theorem reverses conditioning: P(A|B)=P(B|A)P(A)/P(B). Use the law of total probability to expand P(B) across mutually exclusive cases Aᵢ: P(B)=ΣP(B|Aᵢ)P(Aᵢ).

**Example.** A disease affects 1% of a population. A test is 99% sensitive and has a 5% false-positive rate. For 10,000 people, expect 100 affected, of whom 99 test positive; among 9,900 unaffected, 495 test positive. Thus P(disease|positive)=99/(99+495)=1/6≈16.7%. A highly accurate sounding test can have a modest positive predictive value when the base rate is low.

**Practice.** If a fair die is rolled, A={even}, B={greater than 3}: P(A)=1/2, P(B)=1/2, P(A∩B)=1/3, so they are not independent. Always identify the conditioning event and denominator before calculating.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: model outcomes and update by evidence

A probability space has sample space Ω, event collection, and probability P. Events obey P(A)≥0, P(Ω)=1, and countable additivity for disjoint events. For finite equally likely outcomes, P(A)=|A|/|Ω|; this shortcut is invalid if outcomes have unequal chances. Complements satisfy P(Aᶜ)=1−P(A), and unions use inclusion-exclusion.

Conditional probability P(A|B)=P(A∩B)/P(B) describes a restricted model after B is known, provided P(B)>0. Independence means P(A∩B)=P(A)P(B); it is not the same as disjointness. Bayes’ rule reverses conditioning using a prior and a likelihood. A tree diagram helps track the sequence and multiply probabilities along a branch, then add disjoint branches.

**Worked example.** A factory uses machines A and B for 60% and 40% of output. Their defect rates are 1% and 3%. Overall defect probability is .6(.01)+.4(.03)=.018. Given a defective item, probability it came from B is .4(.03)/.018=2/3. Bayes’ rule uses the base production rates as well as the defect rates.

**Practice with answers.** (1) Roll a fair die; P(even)=1/2. (2) Given a roll is greater than 3, probability it is even is 2/3. (3) Independent events with probabilities .2 and .5 intersect with probability .1. (4) Disjoint events of positive probability cannot be independent.

**Common pitfalls:** using the wrong conditioning denominator; ignoring base rates; assuming independence without evidence; and counting overlapping outcomes twice.
