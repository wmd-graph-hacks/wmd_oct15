---
id: math-statistics-experimental-design
type: subtopic
title: Experimental design
parent_topic: math-statistics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-statistics-nonparametric-and-bayesian-methods
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in experimental design
  - apply a standard method from experimental design to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - statistics
  - core-to-advanced
---

# Experimental Design

Good statistical conclusions begin with design. Random assignment balances measured and unmeasured factors in expectation and supports causal interpretation. Random sampling helps generalize to a population. These are distinct: a randomized convenience sample can support a causal comparison in that sample but may generalize poorly.

Replication estimates variability; controls provide a comparison; blinding can reduce expectation effects; blocking groups similar experimental units before random assignment to reduce nuisance variation. In factorial designs, vary multiple factors systematically to estimate main effects and interactions. An interaction means the effect of one factor changes with the level of another.

**Example.** To compare two fertilizers across fields with different soil quality, pair or block plots by field section, then randomly assign fertilizer within each block. The comparison uses within-block differences, reducing noise caused by soil variation. Simply placing all plots of one treatment in one region confounds fertilizer and location.

Predefine outcomes, sample size rationale, exclusions, and analysis where possible. Avoid optional stopping and selective outcome reporting, which can inflate false positive rates. For observational studies, measure likely confounders and state that adjustment cannot guarantee removal of unmeasured confounding.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: design a study that answers its question

Begin with a target population, a precise research question, a response variable, and a plan for sampling or assigning treatments. Random sampling supports generalization to a population; random assignment supports causal comparison by balancing confounders on average. They solve different problems. Observational studies can show association but usually cannot rule out confounding as strongly as a randomized experiment.

Use replication to estimate variability, control groups to create a comparison, and blocking to account for known sources of variation. Blinding reduces measurement and behavior effects. Predefine outcomes and analysis when possible. Sample size affects precision and power; increasing sample size does not fix biased sampling, poor measurement, or a confounded design.

**Worked example.** To test whether a study schedule improves quiz scores, randomly assign eligible students to the new schedule or usual schedule, stratifying by prior score if it is strongly predictive. Use the same quiz conditions and a predefined score outcome. Compare groups while accounting for the blocking variable. If students choose their own schedule, motivation may confound the result.

**Practice with answers.** (1) Random sampling addresses representation; random assignment addresses treatment comparability. (2) A confounder relates to treatment and outcome and can distort their association. (3) Repeated measurements on one person are not independent participants. (4) A larger biased sample can estimate the wrong target very precisely.

**Common pitfalls:** treating correlation as causation; confusing random assignment with random sampling; changing outcomes after seeing results; and ignoring missing data or nonresponse.
