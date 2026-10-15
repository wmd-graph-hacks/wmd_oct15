# Hackathon project options

*My notes for choosing what we can actually build and demo in two days.*

The hackathon brief is **Graph Hacks: Context for AI Agents** (Oct 15–18, 2026). FalkorDB must be the primary graph database and do meaningful product work. The brief emphasizes connected-data reasoning, memory/coordination, company knowledge, and traceable answers. Track names below follow the event page: [hackathon brief](https://www.wemakedevs.org/hackathons/falkordb).

These are three separate product directions. Each has its own user, graph, build plan, and risks. A two-day version should prove one valuable workflow; it should not pretend to be a production-grade platform.

## 1. Study planner: prerequisite-aware study coach

### User problem and product

Students often have a syllabus, deadlines, and a rough sense of what they do not understand, but no useful way to choose the next topic. Build a planner where a student enters an exam date, topics, available study time, and a few quiz results. It recommends a short, realistic next study session and explains the prerequisite or observed gap behind the recommendation. The user can mark a topic as understood or complete a quick check; the next plan reflects that update.

### How FalkorDB is used, and why it helps

Represent `Topic`, `Course`, `Resource`, `Assessment`, `StudySession`, and `Learner` as nodes. Connect topics with relationships such as `PREREQUISITE_OF`, resources with `TEACHES`, and learners to topics with `STRUGGLES_WITH`, `PRACTICED`, or `MASTERED`. Store assessment evidence and timestamps on learner-topic links or assessment nodes.

The planner traverses prerequisite chains to avoid recommending advanced material before foundational gaps, and finds resources attached to the exact weak topic. The graph is useful because a learner's next step depends on how topics relate, not just a flat checklist or a text search. FalkorDB also makes the explanation inspectable: “Review fractions first; ratios depend on fractions, and your last check showed difficulty there.” Use Cypher for these traversals; use an LLM to turn the retrieved evidence into a readable plan, not to invent mastery facts.

### Hackathon track

**Primary: Track 01 — Agents That Act on Connected Data.** The agent uses prerequisite relationships to decide what to study next and acts by creating/updating the study plan. **Possible secondary: Track 02 — Agent Memory and Coordination**, if learner progress persists across sessions and changes later recommendations. Keep Track 01 as the main story.

### Existing alternatives and how generic this is

Study planning and AI tutoring are already established categories. Khan Academy describes Khanmigo study plans that can be generated and tracked ([Khan Academy](https://blog.khanacademy.org/introducing-study-plans-khanmigo-kl/)); many planner and flashcard products already schedule tasks and practice. A generic “AI makes me a timetable” app is therefore not distinctive.

The sharper angle is **prerequisite-aware planning from a learner's actual evidence**, with a visible path from a quiz miss to a prerequisite topic to a specific resource and next action. In a demo, the recommendation must change when the learner updates a result. I have not established that no existing product does this; the point is to make the graph contribution and the learner benefit concrete, rather than claim novelty for AI study plans generally.

### Pros of choosing it

- Easy to understand and demonstrate to a broad audience; no specialist operational domain is needed.
- A small, carefully authored sample course is enough: perhaps 12–20 linked topics, a handful of resources, and two learner assessment histories. This is manageable seed content, not a large dataset.
- Graph traversal naturally supports “what must I know first?” and makes recommendations explainable.
- Low-risk demo: no external integrations or dangerous actions are required.

### Cons and risks

- Crowded and generic if it only generates schedules, summaries, or quizzes.
- A graph does not establish whether a student truly understands something; quiz evidence and recommendations must be framed honestly.
- Good prerequisite relationships and quality learning resources take human effort to curate, even for a small course.
- Personalization can look fake if the demo history does not visibly affect the plan.

### Two-day completion plan

**Day 1**

1. Pick one narrow subject and one exam goal; define no more than 12–20 topics and their prerequisite edges.
2. Add a small set of resources and quiz questions by hand; record the source or author for each resource.
3. Start FalkorDB and implement seed/reset plus Cypher queries for prerequisite chains, weak topics, and resources for those topics.
4. Build a basic page to enter an exam date, daily time budget, and assessment results.

**Day 2**

1. Implement the recommendation flow: identify a weak topic, traverse its missing prerequisites, choose a resource, and propose a short session.
2. Persist learner state in FalkorDB; let the user complete a check or mark a session done and regenerate the plan.
3. Show the explanation and the exact graph path/evidence used beside the recommendation.
4. Deploy, seed a clean demo learner, rehearse one before/after story, and record a fallback demo video.

**Two-day success test:** after changing one quiz result, the suggested next session changes for a reason visible in the graph.

## 2. Job application tracker: relationship-aware job search companion

### User problem and product

Job seekers lose context across applications: which version of a resume they sent, who they spoke to, what was promised, which skills keep appearing, and when to follow up. Build a private tracker where a user saves a role and its job description, logs application/interview events, tracks contacts and follow-ups, and gets a daily “what should I do next?” queue. A useful differentiator is showing which skills recur across target roles and which real experiences in the user's profile support those skills; do not promise that a graph can guarantee interviews.

### How FalkorDB is used, and why it helps

Represent `Person`, `Company`, `Role`, `Application`, `Contact`, `Skill`, `Experience`, `ResumeVersion`, and `Event` nodes. Connect applications to companies and roles, roles to required skills, a person to evidenced skills/experience, and events to applications and contacts. Keep timestamps and source text or URLs so the user can verify extracted information.

Use graph queries to surface overdue follow-ups, find contacts connected to a target company or team, compare requirements across saved roles, and map a role requirement to the user's supporting experience. FalkorDB is useful for joining these changing relationships and giving the assistant a traceable answer. It is not necessary for a simple Kanban board; if the graph never changes the next action or answer, this idea is just a conventional tracker with a graph-shaped storage layer.

### Hackathon track

**Primary: Track 03 — Company Brain** is the closest fit if the project connects job-search knowledge—companies, teams, contacts, roles, and application history—and answers questions with sources. **Track 01 — Agents That Act on Connected Data** also fits if the agent uses graph reasoning to produce a prioritized follow-up or skills-gap action. Make the submitted track story explicit; this is a personal job-search knowledge graph, not a company's internal brain.

### Existing alternatives and how generic this is

This category is highly served. Teal already offers job tracking, job-description keyword extraction, resume tailoring, and career tools ([Teal](https://www.tealhq.com/how-it-works)). Huntr describes a tracker, contact tracking, metrics, and AI application materials ([Huntr](https://help.huntr.co/en/articles/10477521-what-is-huntr)). A basic application board or AI cover-letter generator is not a compelling alternative to these mature products.

To avoid being generic, focus on a workflow that ordinary trackers do not make central: **“show me the evidence and people that connect me to this role, then tell me the next relationship-building action.”** Demonstrate a saved role linked to relevant experience, repeated skill gaps, a contact, and a dated follow-up. This is a product hypothesis, not a verified claim that competitors lack those features; we should compare actual products before making a market-exclusivity claim.

### Pros of choosing it

- Clear everyday pain point for job seekers; the user can bring their own real data.
- No need to invent a huge corpus. A demo can use one sample profile and 3–5 fictional applications/contacts, clearly labeled as sample data.
- Natural persistence story: every application, conversation, and follow-up adds memory that is useful next session.
- Easy to show a concrete action queue rather than a chatbot that only summarizes.

### Cons and risks

- Very crowded product space; a Kanban tracker plus LLM is not enough differentiation.
- Useful recommendations need accurate job details and user history. Scraping job boards or integrating email/calendar is too much scope for two days.
- Resume, contact, and application data are sensitive. A demo should use synthetic sample data or user-controlled input and avoid exposing it publicly.
- Company Brain is not a perfect track match unless the knowledge graph and source tracing are the core; the story needs careful framing.

### Two-day completion plan

**Day 1**

1. Choose one user persona and one narrow outcome: “never miss a follow-up, and know what evidence fits each role.”
2. Define the node/edge model and seed one demo profile, a few roles, skills, experiences, contacts, and dated application events.
3. Build manual role/application/contact entry; optionally paste a job description and extract skills with user confirmation.
4. Implement FalkorDB queries for upcoming follow-ups, role-to-skill matching, and contact/experience paths.

**Day 2**

1. Build a dashboard with an actionable next-step queue and a role detail view showing matched skills, evidence, and contacts.
2. Add a natural-language query such as “What should I follow up on this week, and why?” backed by graph results and source links.
3. Let one user action (log an interview or follow-up) update persistent graph state and the next recommendation.
4. Deploy with a resettable sample account; rehearse the path from role → evidence/contact → action and record a fallback video.

**Two-day success test:** logging one new event changes the upcoming action list, and the user can inspect why each action is recommended.

## 3. DDoS detection system: graph-assisted traffic investigation

### User problem and product

Small teams often see a traffic spike or a flood of alerts but lack a clear way to understand what is connected: which sources hit which destinations, whether they share a pattern, which service is affected, and what evidence supports the suspected attack. Build a **demo-grade detection and investigation workbench** that ingests labeled network-flow records, flags suspicious time windows using simple measurable signals, and lets an analyst explore the source/destination/service relationships behind an alert.

This is an analyst aid for replaying benchmark traffic, not production DDoS protection. Do not claim that the prototype can defend a live network or automatically block traffic.

### How FalkorDB is used, and why it helps

Represent `SourceIP` (or privacy-preserving source key), `DestinationIP`, `Service/Port`, `Protocol`, `TimeWindow`, `Flow`, and `Alert` as graph entities. Connect flows to source, destination, protocol/service, and time window. Aggregate packet/byte/request counts and labels at time-window or endpoint level rather than storing every packet as a node.

Use Cypher to find sources that converge on one destination/service, destinations hit by a shared source cluster, repeated patterns across adjacent time windows, and neighboring flows related to an alert. A simple threshold or baseline detector can create candidate alerts; FalkorDB then helps the analyst investigate relationships and see the evidence path. The database is useful for multi-hop correlation and explanation, not because a graph database automatically detects attacks. A true learned graph neural network is unnecessary and unrealistic in this two-day MVP.

The official CIC-IDS2017 page provides labeled benign and attack traffic, including DDoS, with flow CSVs and PCAPs; the full capture is large, so use a small relevant CSV subset for the demo and cite the dataset ([Canadian Institute for Cybersecurity: CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)).

### Hackathon track

**Primary: Track 01 — Agents That Act on Connected Data.** The agent investigates a suspicious alert by traversing flow relationships and produces a sourced, explainable finding. Its “action” can be a proposed analyst next step, such as inspect a target service or compare a neighboring time window. Do not imply automated mitigation.

### Existing alternatives and how generic this is

DDoS detection and mitigation are mature product categories. Cloudflare documents automatic DDoS detection and mitigation across network and application layers, using dynamic rules, traffic characteristics, and machine learning ([Cloudflare DDoS Protection](https://developers.cloudflare.com/ddos-protection/)). Research also actively explores graph-based DDoS detection; graph-based detection itself is not a new claim (for example, a recent survey of graph and transformer approaches [2026 survey](https://www.sciencedirect.com/org/science/article/pii/S1546221826004339)).

Our credible hackathon angle is narrower: **an explainable investigation layer over public labeled flow data**, where a reviewer can click from an alert into the connected sources, destination, service, and time evidence. The graph must reveal a relationship that a flat alert table would make harder to inspect. A generic “AI detects DDoS” claim is both crowded and impossible to substantiate in two days.

### Pros of choosing it

- Strong visual and technical fit for graph traversal, connected entities, multi-hop reasoning, and explainability.
- A real public labeled dataset exists, so we do not have to invent the traffic labels or scenario. A small subset is enough for a replayable demo.
- It is easy to show the graph changing the investigation: a cluster of sources converging on a service is more informative than one isolated row.
- Clear distinction between a simple candidate-alert detector and graph-powered investigation keeps the role of FalkorDB honest.

### Cons and risks

- Highest technical and domain risk of the three; traffic formats, flow fields, attack labels, and time aggregation need care.
- Public benchmark traffic is not equivalent to current production traffic. Dataset age, collection setup, class imbalance, and benchmark limitations constrain any accuracy claim.
- Competing with real DDoS protection products is not plausible; production mitigation needs high-throughput telemetry, low latency, operational integration, and low false-positive rates.
- Graph storage alone does not improve classification accuracy. We must evaluate the detector separately and show what graph investigation adds.
- Security framing must stay defensive and offline; no live attack traffic generation or automatic blocking is needed for this product demo.

### Two-day completion plan

**Day 1**

1. Download/use a small labeled CIC-IDS2017 flow CSV subset containing benign and DDoS-labeled rows; document the file, selected fields, labels, and limitations.
2. Limit the schema to source, destination, destination port/service, protocol, coarse time window, and flow counts; avoid packet-level graph expansion.
3. Import the subset into FalkorDB with batching and basic aggregation; keep a reproducible sample file in the project or document how to obtain it.
4. Implement one transparent baseline alert rule (for example, a sudden per-destination flow/packet-rate increase) and retain the dataset label for comparison, not as the live detector input.

**Day 2**

1. Add Cypher investigation queries for top sources, shared sources, destination/service concentration, and neighboring time windows.
2. Build an alert list plus graph/evidence view showing why a window was flagged and the connected entities.
3. Add an agent summary that can only use query results and cites the specific time window, service, and flow evidence; allow the analyst to mark an alert benign/suspicious.
4. Replay a fixed demo scenario, show detector output alongside known labels, state the measured limitations, deploy if feasible, and record a fallback video.

**Two-day success test:** on a replayed labeled window, the app flags a candidate event and lets a reviewer trace the contributing source/destination/service relationships and compare the alert with the known label.

## References and scope notes

- [Hackathon challenge, tracks, FalkorDB requirement, and submission guidance](https://www.wemakedevs.org/hackathons/falkordb)
- [Official CIC-IDS2017 dataset page](https://www.unb.ca/cic/datasets/ids-2017.html)
- [Cloudflare DDoS Protection overview](https://developers.cloudflare.com/ddos-protection/)
- [Khan Academy study-plan overview](https://blog.khanacademy.org/introducing-study-plans-khanmigo-kl/)
- [Teal product overview](https://www.tealhq.com/how-it-works)
- [Huntr product overview](https://help.huntr.co/en/articles/10477521-what-is-huntr)


