---
id: math-real-analysis-compactness-connectedness-baire-category
type: subtopic
title: Compactness, connectedness, Baire category
parent_topic: math-real-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-real-analysis-metric-spaces
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in compactness, connectedness, baire category
  - apply a standard method from compactness, connectedness, baire category to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - real-analysis
  - advanced-core
---

# Compactness, Connectedness, and Baire Category

Compactness generalizes “closed and bounded” in ℝⁿ. The open-cover definition says every open cover has a finite subcover. In metric spaces, compactness is equivalent to every sequence having a convergent subsequence whose limit remains in the space. Continuous images of compact sets are compact; real-valued continuous functions on compact sets are bounded and attain extrema.

Connectedness means a space cannot be split into two disjoint nonempty relatively open pieces. Intervals are connected; removing an interior point disconnects one. Path-connectedness (any two points joined by a continuous path) implies connectedness, but the converse need not hold in general.

Baire’s category theorem says a complete metric space cannot be expressed as a countable union of nowhere-dense sets. Intuitively, countably many “small” closed sets cannot fill a complete space. It underlies existence results in functional analysis; at an introductory level, understand the completeness hypothesis and the contrast between countable and finite unions.

**Example.** [0,1] is compact. Any continuous f:[0,1]→ℝ has a maximum and minimum. The open cover {(-1,1−1/n): n≥2} does not cover 1, illustrating that an apparent infinite family must actually cover the set before compactness applies.

Compactness is not merely boundedness: (0,1) is bounded but not compact. Check closedness/limit inclusion in Euclidean settings.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: compactness, connectedness, and Baire’s theorem

In ℝ, a set is compact exactly when it is closed and bounded. Compactness allows finite subcovers and yields powerful consequences: continuous functions attain maxima/minima, and continuous images of compact sets remain compact. Connected sets cannot be separated into two disjoint nonempty relatively open pieces; intervals are connected, while a set with a gap is not.

The Baire category theorem says a complete metric space cannot be a countable union of nowhere-dense sets (sets whose closure has empty interior). Equivalently, countable intersections of open dense sets are dense. It is a structural existence result, used in functional analysis to prove the uniform boundedness and open mapping theorems. “Generic” in this setting means belonging to a dense intersection of open sets, not necessarily having probability one.

**Worked example.** The interval [0,1] is compact and connected. Removing 1/2 splits it into [0,1/2) and (1/2,1], which form a separation in the subspace, so the punctured interval is disconnected. The closed interval’s compactness also ensures a continuous function such as x(1−x) attains its maximum 1/4.

**Practice with answers.** (1) (0,1) is bounded but not compact in ℝ because it is not closed. (2) [0,1] is connected; {0,1} is disconnected. (3) A complete metric space cannot be countably covered by closed sets all with empty interior. (4) Compactness in general topology is defined by open covers, not simply closed and bounded.

**Common pitfalls:** extending Heine–Borel beyond ℝⁿ without conditions; confusing connectedness with path-connectedness in all spaces; and interpreting Baire category as a probability statement.
