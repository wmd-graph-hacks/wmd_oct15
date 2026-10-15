# Study planner — product requirements

**Status:** Draft for hackathon MVP  
**Owner:** Nimesh Maslekar  
**Target:** A working, explainable demo built during the Graph Hacks hackathon  
**Primary track:** Agents That Act on Connected Data  
**Secondary fit:** Agent Memory and Coordination, through persistent learner progress

## 1. Product summary

I want to build a study planner that helps a student decide what to study next, based on their exam date, available study time, course topics, prerequisite relationships, and recent quiz results. It should make a small plan the student can act on, then update that plan when the student records new progress.

The product is not another calendar that divides chapters into equal blocks. Its key behavior is to notice when a learner's gap in one topic affects a later topic, recommend a useful next step, and show the evidence behind that recommendation. FalkorDB stores the course and learner knowledge graph and supports the traversals that drive the plan.

## 2. Problem and opportunity

Students commonly have deadlines and study materials but still have to make three decisions themselves: what to study first, how much time to spend, and whether they are ready to move on. A flat task list treats every topic as independent. A generic AI timetable can look personalized without using real evidence about the learner.

The MVP should solve one narrow, verifiable problem: **help a student choose the next high-value study session and explain why it comes next.** A recommendation must follow the course's prerequisite links and the learner's recorded assessment evidence. It must change when that evidence changes.

## 3. Target user

### Primary user

A student preparing for a specific exam who has a syllabus, a limited amount of study time, and uneven confidence across topics.

### User needs

- See a manageable plan for the next few study sessions.
- Start with a foundational gap when it blocks progress on a later topic.
- Know which course resource or practice activity to use next.
- Understand why the planner chose that task.
- Update progress quickly and have the plan respond.

## 4. Goals and non-goals

### Goals for the hackathon MVP

1. Demonstrate one end-to-end student flow using a small course graph.
2. Use FalkorDB as the primary store for topics, prerequisite edges, resources, learner evidence, and study plans.
3. Generate a plan whose topic order is affected by graph relationships and recorded learner results.
4. Persist learner progress across page reloads or a new session.
5. Show the supporting evidence and graph path for each recommendation.
6. Keep setup and demo repeatable with seeded sample data and a reset option.

### Non-goals for the hackathon MVP

- Supporting every subject, school curriculum, or learning style.
- Automatically importing content from arbitrary websites or learning platforms.
- Claiming to measure mastery from a single quiz result.
- Building a full learning management system, calendar integration, or social study network.
- Training a machine-learning model or using an LLM to determine whether a student has mastered a topic.
- Supporting production multi-tenant accounts, payments, or high availability.

## 5. MVP experience

### 5.1 Start a study plan

The student selects a seeded course, enters an exam date and the number of minutes available on a typical study day, and records a short baseline check for a few topics. For the hackathon demo, this course and its learning materials are curated and labeled as sample content.

### 5.2 Get the next study sessions

The planner proposes a short list of sessions, with a topic, estimated duration, a linked resource or practice activity, and a plain-language reason. The first recommendation prioritizes prerequisite gaps that block an important downstream topic, while also considering exam proximity and time available.

Example: “Review fractions for 20 minutes before ratios. Ratios depend on fractions, and your latest fractions check was 2/5. Try the linked practice set, then retake the short check.”

### 5.3 Record progress and adapt

After studying, the student marks the session complete and can enter a short quiz score. The application stores that result with its date and assessment source. On refresh or a new visit, the next plan reflects the new evidence. The UI makes it clear that scores are signals, not a definitive judgment of ability.

### 5.4 Inspect the explanation

For every recommendation, the student can open “Why this?” and see the graph-derived chain: target topic → prerequisite topic → assessment attempt → selected resource. Where there is no assessment evidence, the interface must say that the planner is using course structure only.

## 6. Functional requirements

### P0 — required for demo

- **Course selection:** Load one seeded course with roughly 12–20 topics, prerequisite links, a small set of resources, and short checks.
- **Plan setup:** Capture an exam date, available study minutes per day, and learner identity for the demo.
- **Baseline evidence:** Record a score or confidence response for selected topics.
- **Graph-backed prioritization:** Use FalkorDB queries to identify weak prerequisites on paths to exam-relevant topics; do not derive topic relationships solely from an LLM response.
- **Plan creation:** Return up to three upcoming sessions, each with topic, duration, resource/check, and reason.
- **Progress update:** Mark a session complete and optionally attach a new assessment score.
- **Persistent state:** Retain learner attempts and completed sessions between visits.
- **Explainability:** Expose relevant prerequisite path, latest learner evidence, and resource source for recommendations.
- **Demo reset:** Restore the seeded learner and course to a known starting state.
- **Error handling:** If there are no results, no resources, or an invalid graph path, tell the user what is missing and offer a safe next step; do not fabricate content.

### P1 — include only if P0 is stable

- Add a short natural-language prompt such as “What should I study next and why?”
- Allow the learner to mark a recommendation as not useful and record a reason.
- Show a simple course concept graph view with learner evidence highlighted.
- Let a user add a topic or resource manually for the demo course.

## 7. Graph and data requirements

### Core node types

- `Learner`: demo learner identifier and preferences.
- `Course`: title and source/provenance.
- `Topic`: title, course order, estimated effort, exam relevance, and optional description.
- `Resource`: title, type, URL or local demo reference, and source.
- `Assessment`: prompt/check metadata and topic coverage.
- `Attempt`: score or confidence, timestamp, and assessment reference.
- `StudySession`: planned/completed state, duration, and timestamps.

### Core relationships

- `(Course)-[:CONTAINS]->(Topic)`
- `(Topic)-[:PREREQUISITE_OF]->(Topic)`
- `(Resource)-[:TEACHES]->(Topic)`
- `(Assessment)-[:CHECKS]->(Topic)`
- `(Learner)-[:MADE_ATTEMPT]->(Attempt)-[:ABOUT]->(Topic)`
- `(Learner)-[:HAS_SESSION]->(StudySession)-[:FOCUSES_ON]->(Topic)`
- `(StudySession)-[:USES]->(Resource)`

Edges and evidence should preserve source and time where relevant. Do not store packet-like or oversized content in the graph; keep the graph focused on relationships and queryable learning state. Seed data should be small and hand-reviewable.

### Recommendation logic

For the MVP, use an understandable, deterministic scoring/ranking approach backed by graph queries:

1. Find topics relevant to the selected course/exam.
2. Traverse their prerequisite paths.
3. Rank a prerequisite lower in readiness when the latest valid attempt is below a configurable threshold or no attempt exists.
4. Prefer unresolved prerequisites that block one or more higher-priority topics.
5. Select a resource linked to the chosen topic and fit the session duration to the learner's available time.
6. Return the evidence path and reason together with the recommendation.

An LLM may rewrite retrieved facts into clear language, but it must not invent topic dependencies, scores, citations, or resources. Keep the raw structured recommendation available so a reviewer can inspect what the model received.

## 8. User stories and acceptance criteria

### Story A: create a plan

As a student preparing for an exam, I want a short plan based on my time and course structure, so that I know what to do next.

**Acceptance criteria:**

- I can choose the sample course, provide exam date and daily time, and submit baseline results.
- The planner returns no more than three next sessions with duration, topic, and linked resource/check.
- At least one recommendation is justified by a prerequisite relationship or recorded assessment evidence.
- If available learning evidence is absent, the reason explicitly says so.

### Story B: see why a topic comes first

As a student, I want to understand a recommendation, so that I can trust or challenge it.

**Acceptance criteria:**

- “Why this?” shows the prerequisite chain and latest supporting assessment when present.
- The displayed score and resource correspond to records in FalkorDB.
- No unsupported claim such as “you have mastered this” is shown from a single score.

### Story C: update my progress

As a student, I want my plan to respond after I finish a session or retake a check, so that it remains useful.

**Acceptance criteria:**

- I can complete a session and record a new result.
- The update persists after refresh.
- When the new evidence changes readiness, the next plan changes accordingly and explains the change.

### Story D: replay the demo

As a reviewer, I want to reset the demo to a known state, so that I can see the before-and-after behavior.

**Acceptance criteria:**

- A reset restores course and learner seed state.
- The same demo steps consistently reproduce the expected recommendation change.
- The demo can run with documented local setup or a live deployment and has a short fallback video.

## 9. Success measures

### Hackathon demo success

- A reviewer can understand the student problem and see the recommendation in under one minute.
- The graph is visibly responsible for a recommendation, and the evidence path can be inspected.
- Updating one assessment result changes at least one recommendation for an explainable reason.
- Learner state persists across a refresh.
- The demo can be reset and replayed without editing database records manually.

### Product signals to measure later

- Percentage of recommendations started or completed.
- Percentage of learners who return and update progress.
- Whether students rate recommendations as relevant/useful.
- Whether students can correctly explain why a prerequisite was recommended.

The hackathon MVP should not report learning gains or improved exam scores as proven outcomes; we will not have a valid study to support those claims.

## 10. UX and content principles

- Keep the next action prominent; the graph visualization supports the explanation and should not overwhelm the plan.
- Show “why”, source, and uncertainty next to recommendations.
- Use accessible text, keyboard-friendly controls, and readable contrast.
- Make sample/demo content visibly distinct from a student's own records.
- Use encouraging, non-judgmental wording. Avoid labeling a learner as “bad” or “behind.”
- Offer a concise plan that respects the stated time budget instead of maximizing scheduled minutes.

## 11. Technical constraints and assumptions

- FalkorDB is the system of record for graph relationships and persistent learner state; it must materially affect plan generation.
- The backend owns credentials and issues parameterized Cypher queries. The browser must not connect to FalkorDB directly with privileged credentials.
- Course graph and learner state should be separable so future versions can isolate learner data.
- The hackathon version uses one seeded course and a small sample learner. Multi-user production access control is future work.
- Any sample course/resources must be authored by us or used with clearly recorded, permissible sources.
- Live deployment is preferred by the event; if unavailable, provide working local setup instructions and a demo video.

## 12. Two-day implementation plan

### Day 1 — graph, seed, and first plan

1. Select a narrow subject and author a small syllabus: 12–20 topics, dependency edges, a few resources, and short baseline checks.
2. Start FalkorDB locally and implement idempotent seed/reset scripts.
3. Add parameterized Cypher queries for prerequisite traversal, latest attempts, and topic-linked resources.
4. Build the basic plan setup form and an API endpoint that returns structured graph-backed recommendations.
5. Verify the recommendation and its evidence path using the seeded learner.

### Day 2 — adapt, explain, and demo

1. Build the session list and “Why this?” evidence view.
2. Implement completion and assessment updates, persist them to FalkorDB, and recalculate the plan.
3. Add demo reset, empty/error states, and basic accessibility polish.
4. Deploy if practical; document setup, environment variables, data seed, and reset steps.
5. Rehearse the before/after learning-gap scenario, capture a short fallback video, and make sure the demo still works from a clean reset.

## 13. Demo script

1. Select the sample course, set an exam date and study-time budget, and enter one low score for a foundational topic.
2. Ask for the next study plan. Show the agent placing the prerequisite first and linking the resource.
3. Open “Why this?” and trace the prerequisite path back to the assessment evidence.
4. Complete the session and enter a stronger follow-up score.
5. Refresh or return to the plan. Show that the persistent evidence changed the recommendation and explain what changed.

## 14. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Looks like a generic AI timetable | Make one assessment-driven prerequisite recommendation the central demo; show the graph path. |
| Sample graph feels invented or arbitrary | Pick a familiar subject, keep it small, and cite/label the source for course content and resources. |
| Weak evidence is presented as mastery | Use transparent thresholds and timestamps; phrase results as “latest check suggests” rather than definitive mastery. |
| LLM hallucinates dependencies or citations | Retrieve structured evidence from FalkorDB first; constrain generation and display the underlying records. |
| Too much time goes into visualizing the graph | Prioritize plan + evidence cards; add a graph visualization only after the full update loop works. |
| Two-day scope expands into a full LMS | Keep one course, one learner, manual inputs, three recommendations, and one before/after story. |

## 15. Decisions to confirm during implementation

- Which familiar subject will provide the sample course graph?
- Will quiz scoring be manual entry, a short built-in quiz, or both? Start with manual entry plus one built-in check if time allows.
- Which LLM/provider is available? Keep deterministic graph ranking usable without an LLM.
- What deployment target and environment-variable setup does the team already know?

