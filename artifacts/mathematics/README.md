---
id: math-course
type: course
title: Mathematics
level: foundation-to-advanced-undergraduate
language: en
status: authored-learning-map
---

# Mathematics: course map

This catalog organizes a broad mathematics pathway from proof foundations through advanced undergraduate subjects. It is intentionally broader than a conventional Grade 11–12 syllabus. Use the **Foundation** topics to build proof and notation fluency; **Core** topics establish widely useful calculus, algebra, probability, and discrete mathematics; **Advanced core** topics are proof-heavy undergraduate material; **Optional extension** topics are enrichment. Placement depends on learner preparation.

For a concrete two-year school sequence, use the [Grades 11–12 syllabus](./syllabus.md). It identifies core, enrichment, and later undergraduate extension material, and includes suggested pacing, lesson structure, assessment, and capstone evidence.

## How to read this catalog

Each subtopic is a separate `README.md` with stable identifiers and explicit graph relationships. `PREREQUISITE_OF` is directed from prerequisite to dependent; the frontmatter `target_type` identifies whether a prerequisite ID is a topic or subtopic. A dependency marked `soft` is useful preparation but not an absolute gate. Estimates are suggested focused study hours, not promises of mastery. Assess understanding through proofs, calculations, modeling, and explanation—not completion alone.

## Suggested progression

1. Foundations of Mathematics → single-variable calculus and linear algebra.
2. Discrete mathematics, probability, and statistics can run alongside calculus after foundations.
3. Multivariable calculus and ODEs follow single-variable calculus and linear algebra.
4. Real analysis deepens calculus; abstract algebra deepens structures; complex analysis follows calculus and analysis.
5. PDEs, numerical methods, and optimization apply calculus, linear algebra, and differential equations.
6. Topology and number theory are optional extensions; number theory also supports cryptography.

## Topic index

- [foundations-of-mathematics](./foundations-of-mathematics/README.md) — Foundation; 6 subtopics. Language, structure, and proof habits used throughout mathematics.
- [single-variable-calculus](./single-variable-calculus/README.md) — Core; 8 subtopics. Limits, change, accumulation, and infinite processes for functions of one real variable.
- [multivariable-calculus](./multivariable-calculus/README.md) — Advanced core; 7 subtopics. Calculus of functions on Euclidean spaces, including geometry and integral theorems.
- [linear-algebra](./linear-algebra/README.md) — Core to advanced; 8 subtopics. Linear structure, transformations, spectral methods, and approximation.
- [real-analysis](./real-analysis/README.md) — Advanced core; 6 subtopics. Rigorous foundations for limits, convergence, integration, and metric structure.
- [abstract-algebra](./abstract-algebra/README.md) — Advanced core; 7 subtopics. Symmetry and algebraic operations studied through groups, rings, and fields.
- [complex-analysis](./complex-analysis/README.md) — Advanced core; 5 subtopics. Differentiability over ℂ imposes strong structure on functions and integrals.
- [ordinary-differential-equations](./ordinary-differential-equations/README.md) — Advanced core; 4 subtopics. Models of change expressed through derivatives and initial data.
- [partial-differential-equations](./partial-differential-equations/README.md) — Advanced core; 4 subtopics. Equations involving partial derivatives, boundary conditions, and spatial modes.
- [probability-theory](./probability-theory/README.md) — Core to advanced; 5 subtopics. Axiomatic uncertainty, random variables, distributions, and limit behavior.
- [statistics](./statistics/README.md) — Core to advanced; 5 subtopics. Use data to estimate parameters, quantify uncertainty, test claims, and model relationships.
- [numerical-methods](./numerical-methods/README.md) — Applied core; 6 subtopics. Approximate mathematical solutions while controlling error, stability, and computational cost.
- [discrete-mathematics-and-combinatorics](./discrete-mathematics-and-combinatorics/README.md) — Core to advanced; 4 subtopics. Finite structures, counting, recurrences, and graphs.
- [optimization](./optimization/README.md) — Applied advanced; 4 subtopics. Choose best feasible decisions under linear or nonlinear objectives and constraints.
- [topology-and-number-theory](./topology-and-number-theory/README.md) — Optional extension; 5 subtopics. A bridge to abstract spaces, algebraic topology, and arithmetic structure.

## Suggested semester plan

This is a flexible 4-year-equivalent sequence, not a fixed school timetable. A focused semester typically contains 12–15 teaching weeks plus review and assessment. For a Grade 11–12 learner, begin with the foundation layer and select age-appropriate parts of single-variable calculus, linear algebra, discrete mathematics, probability, and statistics; defer proof-heavy advanced topics until prerequisites are secure.

| Stage | Suggested focus | Evidence of readiness |
|---|---|---|
| A | Foundations; functions and algebra review (prerequisite knowledge); introductory limits and derivatives | Translate claims, write short proofs, manipulate functions, explain derivative as rate |
| B | Integral calculus; sequences and series; vectors and introductory linear algebra | Set up integrals, test basic convergence, solve linear systems and explain geometric meaning |
| C | Multivariable calculus; probability; statistics; discrete mathematics | Model multivariate change, compute conditional probabilities, interpret data and count structures |
| D | Real analysis; abstract algebra; ODEs; numerical methods; optimization | Prove convergence claims, reason with structures, analyze models and numerical error |
| E | Complex analysis; PDEs; advanced probability/statistics; graph theory applications | Synthesize theorems and methods in an extended project |
| Extension | Topology and number theory | Explore abstraction and proof beyond the core pathway |

## Recommended instructional rhythm

For each subtopic, use a cycle of retrieval (5–10 minutes), explicit teaching and worked examples (20–30 minutes), guided practice (20–30 minutes), independent transfer problem (15–25 minutes), and a brief reflection. Revisit key definitions after 1, 3, 7, and 21 days. Maintain a proof notebook and an error log: record the mistaken assumption or step, the correction, and a new example that tests the correction.

## Assessment blueprint

- **Diagnostic:** prerequisite fluency and notation; use results to choose a starting point, not to label ability.
- **Formative:** low-stakes retrieval, one proof/explanation, and one application per study block.
- **Topic checkpoint:** mix routine procedures with conceptual interpretation and a problem that changes representation.
- **Cumulative assessment:** integrate material across earlier topics; permit a formula sheet only when the goal is modeling and reasoning rather than recall.
- **Mastery evidence:** require repeated, spaced success on varied problems plus explanation of assumptions. One quiz score is a signal, not a definitive mastery claim.

## Capstone options

1. **Model and analyze motion:** derive an ODE from assumptions, solve or approximate it, and compare the model with data.
2. **Least-squares investigation:** collect or use a small dataset, fit a linear model, inspect residuals, and discuss uncertainty and conditioning.
3. **Graph and counting project:** model a real network, prove a structural claim, and compare algorithms or counting strategies.
4. **Optimization project:** formulate a constrained decision problem, solve a small instance, and interpret dual or sensitivity information.
5. **Proof portfolio:** select results from analysis or algebra and present definitions, lemmas, proofs, examples, and counterexamples.

## Scope and level note

The catalog follows the subject list supplied for this project. It is an enriched pathway reaching introductory graduate-adjacent ideas in a few places (for example, Lebesgue integration, Baire category, and Galois theory), rather than a jurisdiction-specific school examination syllabus. Before using it for a formal Grade 11–12 course, align topic selection, notation, and depth with the applicable board standards.


## Resource graph representation

Each folder `README.md` describes a `Topic`; each nested subtopic `README.md` is a `Subtopic` teaching resource. Use `CONTAINS` from topic to subtopic. Resolve prerequisite metadata by ID and `target_type`; for subtopic prerequisites, create a directed `PREREQUISITE_OF` edge from the referenced node to the current node and retain its `strength`. The Markdown body is the learner-facing resource content. Keep course structure and learner assessment evidence as separate graph data.
