# Study Planner

An explainable study planner built with FastAPI and FalkorDB for **Track 01: Agents That Act on Connected Data**. The first course is a small Foundational Mathematics syllabus. Graph traversal finds the learner's prerequisite gaps and linked resources; optional AI selects and orders only among those retrieved candidates, then the backend validates its selection before saving the plan.

## Run locally

Requirements: Python 3.11+ and Docker Compose.

```sh
cp .env.example .env
docker compose up -d falkordb
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000). Local mode uses a clearly labeled demo learner. Check `http://localhost:8000/health` to see whether FalkorDB is reachable. Course seeding runs idempotently when the planner opens.

## API

The JSON API is versioned under `/api/v1` and uses the same signed-in learner as the web UI. In demo mode, sign in at `/login` first; the `study_session` cookie is used for API requests too. Open `/docs` for the interactive OpenAPI reference. Run the backend tests with `python -m unittest discover -s tests -v`.

```sh
curl http://localhost:8000/api/v1/health
curl -c cookies.txt -X POST http://localhost:8000/auth/demo
curl -b cookies.txt http://localhost:8000/api/v1/courses/foundational_math
curl -b cookies.txt http://localhost:8000/api/v1/plan
curl -b cookies.txt -X POST http://localhost:8000/api/v1/plan/generate
curl -b cookies.txt http://localhost:8000/api/v1/topics/limits/assessment
curl -b cookies.txt -H 'Content-Type: application/json' \
  -d '{"assessment_id":"quick_check_limits","answer":"B"}' \
  -X POST http://localhost:8000/api/v1/assessments/submit
curl -b cookies.txt -H 'Content-Type: application/json' \
  -d '{"exam_date":"2099-12-01","minutes_per_day":45,"exam_topic":"derivatives"}' \
  -X PUT http://localhost:8000/api/v1/plan/preferences
curl -b cookies.txt -H 'Content-Type: application/json' \
  -d '{"topic_id":"limits","score":3,"max_score":5}' \
  -X POST http://localhost:8000/api/v1/attempts
curl -b cookies.txt -H 'Content-Type: application/json' \
  -d '{"topic_id":"limits"}' \
  -X POST http://localhost:8000/api/v1/sessions/complete
```

Routes return JSON errors (`401` when signed out, `404` for unknown courses/topics, `422` for invalid input, and `503` when FalkorDB cannot be reached). API code is in `app/api/`, server-rendered routes are in `app/ui/`, and `app/ai/` contains the optional LiteLLM integration. When enabled, AI may select and order retrieved candidate topics; the backend validates every proposal against graph candidates and prerequisite order.

## Google Gemini through LiteLLM

The roadmap endpoint makes a real LiteLLM chat-completion request when AI is enabled. LiteLLM routes Gemini API calls with the `gemini/` model prefix and reads `GEMINI_API_KEY`. Model selection and fallbacks are in the root `llm_config.json`: primary `gemini-3.8-flash`, then `gemini-3.6-flash`, then `gemini-3.5-flash-lite`. Check Google's current model availability for your account before changing model IDs. An `AI_MODEL` value in `.env` overrides the configured primary; `AI_FALLBACK_MODELS` can override the fallback list as a comma-separated list.

1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Install the optional LiteLLM dependency: `pip install -e '.[llm]'`.
3. Put the key in your local `.env` as `GEMINI_API_KEY=...`. Do not commit or paste the key into source code.
4. Set `AI_ENABLED=true` in `.env`, leave `AI_MODEL` blank to use `llm_config.json`, then restart `uvicorn`.
5. Sign in and request a plan. This call invokes Gemini when the cache has no matching graph context:

```sh
curl -b cookies.txt -X POST http://localhost:8000/api/v1/plan/generate
```

Inspect `plan_selection` in the JSON response. `graph_context_ai` means the model proposal passed backend validation; `graph_ranked_fallback` means the graph-ranked plan was used (AI disabled, provider error, invalid model output, or a proposal that failed validation). `ai_summary` is the model's short explanation when accepted. The LLM receives only graph-retrieved candidate facts and cannot invent topics, dependencies, mastery, or references. Plan generation persists the accepted plan in FalkorDB.

Gemini 3 models have model-specific sampling behavior; this integration leaves `temperature` unset rather than forcing a low value. Each model request is capped at 200 output tokens, times out after `AI_TIMEOUT_SECONDS`, and makes no internal retries; if a request fails or returns unusable JSON, the next model in the configured list is called. Accepted proposals are cached in-process by graph context. See [LiteLLM's Gemini provider guide](https://docs.litellm.ai/docs/providers/gemini) and [Google's Gemini model list](https://ai.google.dev/gemini-api/docs/models) for current model IDs and provider behavior.

## Graph model and recommendation behavior

The course graph stores shared curriculum facts; each learner's evidence is attached to that learner:

```text
(Course)-[:CONTAINS]->(Topic)-[:PREREQUISITE_OF]->(Topic)
(Resource)-[:TEACHES]->(Topic)       (Assessment)-[:CHECKS]->(Topic)
(Learner)-[:MADE_ATTEMPT]->(Attempt)-[:ABOUT]->(Topic)
(Learner)-[:HAS_SESSION]->(StudySession)-[:FOCUSES_ON]->(Topic)
(Learner)-[:HAS_KNOWLEDGE]->(LearnerTopic)-[:ABOUT]->(Topic)
(Learner)-[:HAS_PLAN]->(StudyPlan)-[:INCLUDES]->(PlanItem)-[:FOCUSES_ON]->(Topic)
(PlanItem)-[:USES]->(Resource)
```

`app/graph/repository.py` owns Cypher and converts driver rows into application data. Query inputs such as course IDs, learner UIDs, topic IDs, scores, and status values are bound as Cypher parameters; only fixed labels, relationship types, and query structure remain in the query text. The API and UI call repository methods instead of running Cypher themselves.

Assessment submission records an `Attempt` and updates compact per-learner/per-topic `LearnerTopic` evidence (running average, count, timestamp). The assessment answer key stays server-side. FalkorDB traverses prerequisite paths to the selected exam topic and removes topics whose recorded average is at least 70%. With AI enabled, LiteLLM selects and orders up to three topics from the remaining graph-retrieved candidates. The backend rejects unknown topic IDs or ordering that violates an unresolved prerequisite and falls back to graph order. It then persists a `StudyPlan` and `PlanItem` graph, superseding the prior active plan. AI receives only the compact candidate set and can write a short summary; it cannot change scores or resource citations. This is a hackathon prototype: the 70% threshold is not a validated mastery model, and exam-date scheduling and general-purpose optimization remain future work.

The first page lets you choose an exam goal (quadratics, limits, or derivatives), save an exam date and daily study time, review graph-backed recommendations, mark a study session complete, and record checks for recommended topics. API clients can fetch a targeted, seeded diagnostic question and submit its answer; the resulting evidence changes later recommendations. The goal selects which prerequisite paths FalkorDB traverses. The demo learner data is stored in FalkorDB and remains until you reset it in the app or remove the volume with `docker compose down -v`.

## Google sign-in setup

The default `AUTH_MODE=demo` is only for local development. To use Google sign-in, create a Firebase project, enable Google as a sign-in provider, add the app's local/deployed domain to authorized domains, and set `AUTH_MODE=firebase` plus the Firebase web configuration values in `.env`. Set `FIREBASE_SERVICE_ACCOUNT` to the path of a service-account JSON file available to the server, or configure Application Default Credentials. Never commit credentials. For deployment, set `APP_ENV=production`, a strong `SESSION_SECRET`, and `SESSION_COOKIE_SECURE=true`.

## Current scope

- One hand-authored, 12-topic course and a short list of source-linked resources.
- FalkorDB stores course topics, prerequisite relationships, resources, targeted checks, learner evidence, and persisted plans.
- Graph retrieval and knowledge updates are deterministic; optional LiteLLM may select and order graph candidates. Configure Gemini as described above. The graph-validated fallback remains available if the provider is unavailable.
- Local demo authentication is not suitable for a public deployment. Firebase session verification is enabled when `AUTH_MODE=firebase`.
