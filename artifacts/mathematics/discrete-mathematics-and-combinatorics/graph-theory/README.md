---
id: math-discrete-mathematics-and-combinatorics-graph-theory
type: subtopic
title: Graph theory
parent_topic: math-discrete-mathematics-and-combinatorics
phase: core-to-advanced
estimated_minutes: 60
prerequisites:
  - id: math-discrete-mathematics-and-combinatorics-inclusion-exclusion
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in graph theory
  - apply a standard method from graph theory to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - discrete-mathematics-and-combinatorics
  - core-to-advanced
---

# Graph Theory

A graph consists of vertices and edges. In an undirected graph, degree counts incident edges (a loop contributes two); the handshaking lemma says the sum of degrees is 2|E|. A path connects vertices; a graph is connected if every pair has a path. A tree is connected and acyclic; equivalently, a tree with n vertices has n−1 edges, and adding any edge creates a cycle.

Euler trails use every edge once; a connected graph has an Euler circuit exactly when every vertex has even degree, and an Euler trail with distinct endpoints exactly when two vertices have odd degree. Hamiltonian paths visit every vertex once; unlike Euler criteria, no simple degree test characterizes all Hamiltonian graphs.

Planar graphs can be drawn without crossing edges. For connected planar simple graphs with at least 3 vertices, V−E+F=2; this yields bounds such as E≤3V−6. A proper coloring assigns different colors to adjacent vertices. A matching is a set of pairwise nonincident edges; network flow sends quantities through a directed capacitated graph while conserving flow at intermediate vertices.

**Example.** A connected graph with degrees 2,2,2,4 has all degrees even, so it has an Euler circuit. If exactly two degrees were odd, it would have an Euler trail but no circuit. Always check connectedness of non-isolated vertices.

Model choices matter: define whether edges are directed, weighted, or repeated, then translate the real problem precisely.

## Study sequence

Reproduce each derivation without looking, then solve a new instance with changed data. For each answer, write the assumptions and explain why the selected method applies. Revisit the questions after a delay to check durable recall.

## Lesson: vertices, paths, trees, and networks

A graph G=(V,E) has vertices and edges. It is connected when every pair of vertices has a path between them. Degree counts incident edges (a loop contributes two). The handshaking lemma Σdeg(v)=2|E| follows because each edge has two ends. A tree is connected and acyclic; with n vertices it has n−1 edges and a unique path between every pair.

Euler trails use every edge once; a connected graph has an Euler circuit exactly when all degrees are even, and an Euler trail when exactly two degrees are odd. Hamilton paths visit every vertex once; unlike Euler trails, no simple degree test solves all cases. Planarity concerns crossing-free drawings. Coloring assigns adjacent vertices different colors; matchings pair vertices by disjoint edges. Network flow adds capacities and conservation at intermediate vertices.

**Worked example.** A connected graph has degrees 2,2,3,3. Exactly two vertices have odd degree, so it has an Euler trail from one odd vertex to the other, but no Euler circuit. Degree sum 10 confirms 5 edges.

**Practice with answers.** (1) A tree on 8 vertices has 7 edges. (2) Cycle C₅ has an Euler circuit because every degree is 2. (3) Complete graph K₄ has 6 edges and degree 3 at each vertex. (4) A matching cannot include two edges sharing a vertex.

**Common pitfalls:** confusing Euler and Hamilton paths; forgetting connectedness in Euler criteria; and assuming a graph is nonplanar because one drawing has crossings.
