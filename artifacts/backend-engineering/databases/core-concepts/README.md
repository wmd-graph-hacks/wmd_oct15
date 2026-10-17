---
id: backend-engineering-databases-core-concepts
type: subtopic
title: 'Relational: Entity-relationship modeling: foundations — study lesson'
parent_topic: backend-engineering-databases
phase: advanced-core
estimated_minutes: 80
prerequisites:
- id: backend-engineering-software-engineering-practice-on-call-practices
  target_type: subtopic
  strength: recommended
learning_outcomes:
- 'explain the key ideas in Relational: Entity-relationship modeling: foundations
  and how they relate'
- apply an appropriate model or method to a worked example
- state assumptions, check the result, and identify a limitation
tags:
- backend-engineering
- databases
---

# Relational: Entity-relationship modeling: foundations

## Core idea

This lesson narrows **Databases** to a connected set of concepts. The scope terms below come from the subject outline; use them as a map of the model, not as a vocabulary list to memorize in isolation.

Transactions group operations around consistency and isolation guarantees. Indexes can reduce lookup work but add storage and write cost; design around invariants and access patterns. For this unit, focus on **Relational: Entity-relationship modeling** and how it fits the wider model.

- **Relational: Entity-relationship modeling** — define the object or process, name the conditions under which it applies, and connect it to the neighboring concepts in this unit.
- **normalization (1NF through BCNF)** — define the object or process, name the conditions under which it applies, and connect it to the neighboring concepts in this unit.
- **SQL (joins, subqueries, window functions, CTEs)** — define the object or process, name the conditions under which it applies, and connect it to the neighboring concepts in this unit.
- **indexes (B-tree, hash, composite, covering)** — define the object or process, name the conditions under which it applies, and connect it to the neighboring concepts in this unit.

## How to reason through the material

Trace one request from caller to storage and back. Mark trust boundaries, state changes, failure points, and retry behavior; then test the contract at both normal and partial-failure cases.

For each item, make a three-column note: what it describes, what evidence or operation identifies it, and how changing one relevant condition changes the prediction. Then draw arrows between the items to show whether they represent prerequisites, steps in a process, alternative models, or ways of measuring the same system. Do not assume that two adjacent terms have a causal relationship unless the model or evidence supports it.

## Worked study example

Choose **Relational: Entity-relationship modeling** from the list. State a concrete question that can be answered using it; write down the system boundary, observations available, assumptions, and expected result. Work from the definition or governing model to the result, and annotate each step with why it is valid. Change one condition and predict the effect before looking up the answer. If the prediction fails, identify whether the cause is a violated assumption, a measurement issue, or a mistaken link between concepts.

## Check your understanding

1. Explain the difference between the first two concepts in your own words, including one condition that changes how they should be used.
2. Give an example where a learner could recognize the vocabulary but still apply the model incorrectly. State the correction.
3. What observation, calculation, or test would most directly challenge your explanation?

## Retrieval practice

Close the lesson and reconstruct the concept map from memory. Work one example without notes, then explain the assumptions and one limitation. Revisit the hardest step after a delay and solve a changed example.
