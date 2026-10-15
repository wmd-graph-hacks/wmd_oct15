# Checkpoint 1: Current application behavior

**Status:** Current-state snapshot (2026-10-15)  
**Related:** [Study planner PRD](adr_002_prd-study-planner.md), [Study planner HLD and LLD](adr_003_study-planner-hld-lld.md)

> This document records what is implemented in the repository now. It is not a statement that every product requirement is complete. Where the running application differs from the intended product, the difference is called out below.

## 1. Product intent

The intended product is a personalized study planner that uses a knowledge graph to answer:

1. What should this learner study next?
2. Which prerequisite topics do they need first?
3. Which source material should they use?
4. What evidence supports the plan, and how should the plan change as they learn?

For Hackathon Track 01, **Agents That Act on Connected Data**, the key demonstration is that FalkorDB stores connected course and learner facts, the application retrieves relevant graph context, and an AI component can make a constrained choice using that context. The graph remains authoritative for topics, prerequisites, learner evidence, and references.

## 2. What the application does when run

1. Start FalkorDB using Docker Compose and run the FastAPI application.
2. Sign in using the local demo learner when `AUTH_MODE=demo`, or use the configured Firebase sign-in flow when `AUTH_MODE=firebase`.
3. The application idempotently seeds a hand-authored Foundational Mathematics course into FalkorDB. It contains 12 topics, prerequisite relationships, a small set of Khan Academy resource links, and hand-authored diagnostic questions.
4. The learner can choose an exam goal, target date, and daily study-time budget. These preferences are saved on the learner record.
5. The dashboard traverses the graph from the selected goal, gathers its prerequisite topics, and shows up to three candidates that are not considered mastered. A running average of recorded scores at or above 70% is treated as mastered for this prototype.
6. For each recommendation, the dashboard can open its linked resource, accept a manually entered score out of five, or record the session as complete. Attempts and sessions are stored in the learner graph and can influence later recommendations.

The current dashboard is server-rendered Jinja HTML. Its forms post to FastAPI routes. It does not currently call the JSON API from browser JavaScript.

## 3. Implemented components

### API and application services

The versioned API is mounted under `/api/v1` and uses the signed-in learner from the same session cookie as the UI. It currently provides:

- Health and seeded course retrieval.
- Roadmap preview (`GET /api/v1/plan`).
- Roadmap generation and persistence (`POST /api/v1/plan/generate`).
- Saved-plan retrieval.
- Learner preference updates.
- Attempts, diagnostic assessment retrieval/submission, and completed study sessions.

Graph queries are kept in `app/graph/repository.py` and use parameterized Cypher values. API routes and server-rendered UI are separated into `app/api/` and `app/ui/`. The roadmap application service is in `app/services/roadmap.py`.

### FalkorDB model

The shared graph contains the seeded course structure and source links. Learner-specific evidence is attached to a `Learner` node. The implemented model includes:

```text
(Course)-[:CONTAINS]->(Topic)
(Topic)-[:PREREQUISITE_OF]->(Topic)
(Resource)-[:TEACHES]->(Topic)
(Assessment)-[:CHECKS]->(Topic)
(Learner)-[:MADE_ATTEMPT]->(Attempt)-[:ABOUT]->(Topic)
(Learner)-[:HAS_KNOWLEDGE]->(LearnerTopic)-[:ABOUT]->(Topic)
(Learner)-[:HAS_SESSION]->(StudySession)-[:FOCUSES_ON]->(Topic)
(Learner)-[:HAS_PLAN]->(StudyPlan)-[:INCLUDES]->(PlanItem)-[:FOCUSES_ON]->(Topic)
(PlanItem)-[:USES]->(Resource)
```

Attempts retain score history. A compact per-learner/per-topic record stores a running average and attempt count. The current recommendation rule uses that average and a fixed 70% mastery cutoff; this is a prototype heuristic, not a validated learning assessment.

### Optional AI through LiteLLM

`app/ai/roadmap_explainer.py` sends a compact set of graph-retrieved candidates to LiteLLM when AI is enabled. Model configuration is in the root `llm_config.json`, with a primary Gemini model and ordered fallbacks. The learner identifier is not included in the AI context. The AI can select and order candidate topic IDs and provide a short summary. The backend validates candidate IDs and prerequisite ordering; invalid output or provider failure falls back to graph ranking.

**Dashboard/API mismatch:** the current dashboard home route calls `repository.plan(...)` directly, so its visible recommendations are graph-ranked and do not use Gemini. The AI-backed path is available through the API roadmap service, especially `POST /api/v1/plan/generate`. The dashboard does not yet display an AI-generated or saved plan.

## 4. What is not implemented yet

- Upload or ingestion of textbooks, PDFs, lecture transcripts, or other learner-provided materials.
- AI extraction of topics, subtopics, prerequisites, references, chapters, or page numbers from source material. Course facts are hand-authored in code.
- A general-purpose or vector-based retrieval pipeline. Current retrieval is over the seeded prerequisite graph and its attached records.
- A user-facing diagnostic quiz or “Grill Me” flow on the dashboard. Diagnostic questions and answer submission exist in the API; the dashboard's quick check is a score the learner enters manually.
- A dashboard flow that calls the AI-backed plan API, shows the returned summary, or reads a persisted generated plan.
- A real calendar/schedule optimizer. The target date is stored; the daily time budget caps suggested topic duration but does not create a day-by-day schedule.
- A calibrated mastery model. Current behavior uses a fixed running-average threshold.
- A complete end-to-end validation of the running UI, API, FalkorDB, and Gemini configuration as one user journey.

Therefore the current application is a **small graph-backed math planner prototype**, not yet the full resource-ingesting, assessment-led GraphRAG product described in the PRD.

## 5. Current local run path

From the repository root:

```sh
docker compose up -d falkordb
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and configure the local environment first. Open `http://localhost:8000/login` for the UI and `http://localhost:8000/docs` for the API reference. In demo mode, the same session cookie can be used to call the API after signing in.

## 6. Relevant code locations

- `app/graph/repository.py` — course seeding, parameterized Cypher, graph reads/writes, deterministic graph plan.
- `app/services/roadmap.py` — graph retrieval, optional AI selection, validation, and fallback behavior.
- `app/ai/roadmap_explainer.py` — LiteLLM request, model fallback, compact prompt context, output parsing/cache.
- `app/api/router.py` — versioned JSON endpoints.
- `app/ui/router.py` — server-rendered routes and form handlers.
- `app/templates/home.html` and `app/templates/login.html` — current browser UI.
- `app/static/style.css` — current visual styling.
- `llm_config.json` — primary and fallback Gemini model IDs and AI request limits.

## 7. Checkpoint conclusion

The strongest working slice for Track 01 is the graph-backed prerequisite lookup and learner-evidence update, with an optional constrained LiteLLM selection exposed through the API. The biggest product gap is connecting that capability to a clear learner flow. The next implementation should make the user-facing diagnostic and AI-backed plan flow visible, while preserving graph-grounded topics, prerequisite order, and source references.
