# ADR 005: Current application, hackathon fit, and product readiness

**Status:** Current-state decision, recorded 2026-10-17  
**Related:** [Study planner PRD](adr_002_prd-study-planner.md), [Study planner HLD and LLD](adr_003_study-planner-hld-lld.md), [Checkpoint 1 snapshot](adr_004_ckpt1.md)

## 1. Context

The application has grown from the first Foundational Mathematics planner slice into a multi-subject study agent. The earlier checkpoint describes the initial 12-topic dashboard and predates the current subject picker, study agent, tutor, and expanded curriculum. This record describes the current repository state and the work still needed before the app can be relied on as a useful study planner.

## 2. Decision

Treat the application as a **graph-grounded, multi-subject study planner and study agent prototype**. FalkorDB is the source of truth for curriculum relationships and learner evidence. Deterministic graph tools retrieve and validate study candidates. An optional LLM can help interpret a request, select from retrieved candidates, or explain retrieved lesson material; it does not get to invent graph facts or commit a proposed plan without learner approval.

The nine loaded subjects are Mathematics, AI and Machine Learning, Backend Engineering, Biology, Chemistry, Computer Science Foundations, Cybersecurity, DevOps and Cloud, and Physics. Mathematics has the most mature authored curriculum. The other eight have been expanded beyond their original one-lesson-per-topic state, but their depth and coverage still need subject-matter review before they should be presented as complete courses.

## 3. What the application currently does

- Loads subject-scoped courses, topics, subtopics, prerequisite relationships, lesson chunks, and question banks into FalkorDB. Curriculum loading can target one subject or all subjects and is designed to refresh changed source files.
- Provides a subject picker for the graph map, study agent, quiz, and tutor. Subject identity scopes retrieval and prevents prerequisite links from crossing subjects.
- Shows a graph map with learner progress and whether a subtopic has a quiz. Inferred syllabus-order links are identified as inferred rather than verified prerequisites.
- Lets a learner ask the study agent for help finding topics, prerequisite closure, bottlenecks, critical path, and plan feasibility. The agent can prepare a plan proposal; the learner approves it before it is committed.
- Provides per-subtopic quizzes and stores learner mastery/evidence. The demo learner's seeded mastered topics apply to Mathematics only.
- Answers tutor questions from retrieved lesson chunks, with source citations when the LLM path is enabled. Without that path, the tutor uses extractive lesson content; it can decline questions that the indexed content does not support.
- Supports demo authentication and a Firebase session-authentication path. LLM-backed behavior is optional and has deterministic or extractive fallbacks.

Current catalog figures recorded in the README are 84 Mathematics lessons, 266 lessons across the other eight subjects, 302 authored prerequisite links across those eight, and 858 quiz questions in 283 lesson banks. These are counts of loaded material, not evidence that every subject has equivalent instructional quality.

## 4. How this fits Hackathon Track 01

The project is built for **Track 01: Agents That Act on Connected Data**. Its core demonstration is that an agent acts on connected, persisted learning data:

1. FalkorDB stores connected subject structure and learner evidence: topics, prerequisite edges, lesson chunks, quiz results, and mastery state.
2. The agent calls tools that query this graph to identify a goal, its prerequisites, available learning steps, and feasibility. This makes the connected-data source part of the agent's reasoning path rather than a decorative graph display.
3. Tool results are constrained to the selected subject and existing graph IDs. The backend checks proposed plans against known subtopics and prerequisite order.
4. The agent proposes changes and the learner explicitly approves a plan before the application commits it. Quiz results update learner evidence and can change future recommendations.
5. The application remains useful when the model is unavailable: deterministic tools and graph-backed behavior provide the fallback.

This is a credible track-aligned prototype. A stronger demonstration should show one complete loop live: choose a subject and goal, inspect graph-derived prerequisites and evidence, receive a plan with reasons, approve it, complete a quiz or learning step, and show the updated graph-backed state affecting the next recommendation. The app should label inferred edges and any content-quality limitations during that demonstration.

## 5. Remaining work for a useful study planner

The next work should improve learning usefulness and trust, in this order.

### 5.1 Review and improve the curriculum

- Have knowledgeable reviewers check each subject's topic coverage, subtopic boundaries, lesson accuracy, examples, and quiz answer keys.
- Replace inferred syllabus order with authored prerequisite relationships where a genuine learning dependency exists. Keep sequence-only links visibly distinct from prerequisites.
- Add worked examples, practice of varied difficulty, misconceptions, and explanations for answers. A list of terms or a short overview is not enough for the tutor to teach a concept.
- Attach reliable source references to lessons and questions, including provenance and review date. Make it possible to identify stale or unreviewed content.
- Add a repeatable authoring and review workflow so curriculum changes can be checked before they are loaded.

### 5.2 Make assessment evidence meaningful

- Review whether each quiz tests the stated learning objective, not just recognition of the lesson scope. Improve distractors, feedback, and coverage across each subject.
- Make diagnostics useful at onboarding, and give the learner a clear way to revisit missed skills.
- Track evidence by objective and over time. Revisit the current mastery rules and thresholds using actual learner performance; do not treat the current rules as validated measures of ability.
- Explain uncertainty and distinguish unseen, self-reported, practiced, and demonstrated knowledge.

### 5.3 Turn recommendations into a practical plan

- Ask for a learner goal, current level, deadline, available study time, and preferred session length; use those inputs consistently across subjects.
- Generate a calendar-aware schedule with realistic durations, prerequisite ordering, breaks, and a way to reschedule missed sessions. A feasibility estimate alone is not a day-by-day plan.
- Give each recommended step a clear reason, expected duration, learning resource, and check for completion. After a quiz or session, recalculate the next step from updated evidence.
- Let learners correct goals and progress, and provide useful empty states when a subject lacks reviewed content or quizzes.

### 5.4 Validate the complete learner experience

- Exercise all nine subjects through the browser, including subject switching, graph map, agent proposal and approval, quiz, tutor citations, progress persistence, and error states.
- Add evaluation cases for prerequisite correctness, subject isolation, plan validity, answer-key correctness, tutor grounding, and behavior when content is missing. Include representative non-Mathematics cases.
- Test clean installation, curriculum refresh, and upgrade from an existing graph. Document safe backup/reset behavior before asking users to discard stored graph data.
- Review Firebase configuration, learner-data access boundaries, session protections, secret handling, and deployment settings before real learners or public deployment.
- Measure whether learners can understand and complete the flow, then prioritize changes from that feedback.

## 6. Success criteria for the next useful release

A learner can choose any reviewed subject, state a concrete goal and time budget, complete an appropriate diagnostic, and receive a short schedule whose steps:

- follow reviewed prerequisite relationships;
- cite reviewed lesson or practice material;
- explain why each step was selected and how long it should take;
- reflect the learner's quiz and completion evidence;
- adapt after the learner completes a step or changes availability; and
- clearly disclose when the curriculum or evidence is incomplete.

For the hackathon walkthrough, the same flow should show the graph facts and tool results that led to the recommendation, then show an approved action and its effect on learner state.

## 7. Consequences

- The app's strongest claim is its explainable agent loop over connected curriculum and learner data, not the completeness of all nine curricula.
- Subject counts and generated or inferred structure must not be presented as proof of course quality.
- Curriculum review, assessment quality, and end-to-end learner testing are release work, not optional polish.
- LLM features remain bounded by graph retrieval, source material, validation, and learner approval. They cannot compensate for missing or inaccurate curriculum data.
- This record supplements the earlier checkpoint; update that checkpoint or supersede it when the current implementation is audited again.
