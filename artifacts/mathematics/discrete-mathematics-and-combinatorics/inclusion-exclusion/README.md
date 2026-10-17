---
id: math-discrete-mathematics-and-combinatorics-inclusion-exclusion
type: subtopic
title: Inclusion-exclusion
parent_topic: math-discrete-mathematics-and-combinatorics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-discrete-mathematics-and-combinatorics-recurrences-and-generating-functions
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in inclusion-exclusion
  - apply a standard method from inclusion-exclusion to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - discrete-mathematics-and-combinatorics
  - core-to-advanced
---

# Inclusion–Exclusion

When sets overlap, adding their sizes counts shared elements multiple times. For two finite sets, |A∪B|=|A|+|B|−|A∩B|. For three sets, add the individual sizes, subtract pairwise intersections, then add the triple intersection. The alternating pattern continues for finitely many sets.

**Example.** Among integers 1 through 100, count multiples of 3 or 5. There are 33 multiples of 3 and 20 of 5, while 6 are multiples of 15. Thus the count is 33+20−6=47. Adding 33+20 without subtracting overlap would count multiples of 15 twice.

The same principle counts objects avoiding forbidden properties: count all objects, subtract those violating at least one condition, add back double-counted intersections, and continue. For many conditions, organize intersections systematically; the formula has 2ⁿ terms for n sets, so symmetry or recurrences may simplify.

**Practice.** From 1 to 60, multiples of 4 or 6: 15+10−5=20. To count strings avoiding any forbidden pattern, define each event “pattern i occurs” and apply inclusion–exclusion if intersections can be counted.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: correct overlapping counts

For two finite sets, |A∪B|=|A|+|B|−|A∩B|: overlap was counted twice, so subtract once. For three sets, add the singles, subtract pairwise intersections, then add the triple intersection. In general, alternate signs over nonempty intersections. This also counts objects avoiding forbidden properties by correcting overlaps.

**Worked example.** In a class of 40, 22 study algebra, 18 geometry, and 8 both. At least one: 22+18−8=32. Neither: 40−32=8. Check the partition: algebra only 14, geometry only 10, both 8, neither 8; total 40.

In derangements or restricted assignments, intersection counts may depend only on how many restrictions are imposed. Define the universe and each “bad” set clearly before calculating.

**Practice with answers.** (1) If |A|=12, |B|=9, |A∩B|=4, then |A∪B|=17. (2) Three sets have sizes 10 each, pair intersections 3 each, triple intersection 1: union size 30−9+1=22. (3) The triple overlap is added back because it was subtracted three times after being added once.

**Common pitfalls:** ignoring triple and higher intersections; confusing “at least one” with “exactly one”; and failing to compare the answer with universe size.
