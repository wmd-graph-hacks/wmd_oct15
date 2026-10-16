---
id: backend-engineering-course
type: course
title: Backend Engineering
level: foundation-to-advanced
language: en
status: authored-learning-map
---

# Backend Engineering: course map

This catalog turns the supplied subject outline into a staged learning pathway. Topic pages state scope and outcomes; linked lesson pages provide instructional notes and retrieval practice. The pathway ranges from introductory to advanced study. Use the syllabus to choose a suitable stage and follow prerequisite links.

For a staged sequence, pacing, lesson cycle, and assessment guidance, see the [syllabus](./syllabus.md).

## Topic index

- [Databases](./databases/README.md) — Relational: Entity-relationship modeling, normalization (1NF through BCNF), SQL (joins, subqueries, window functions, CTEs), indexes (B-tree, hash, composite, c…
- [Distributed Systems](./distributed-systems/README.md) — CAP and PACELC theorems, consistency models (strong, eventual, causal, linearizability), consensus algorithms (Paxos, Raft), leader election, distributed transa…
- [API Design](./api-design/README.md) — REST principles and resource modeling, HTTP methods and status codes, GraphQL schemas and resolvers, gRPC and Protocol Buffers, pagination (offset, cursor), ver…
- [Authentication and Authorization](./authentication-and-authorization/README.md) — Sessions and cookies, password hashing (bcrypt, Argon2), JWT, OAuth 2.0 flows, OpenID Connect, role-based and attribute-based access control, API keys, secrets …
- [Messaging and Asynchronous Processing](./messaging-and-asynchronous-processing/README.md) — Message queues (RabbitMQ, SQS), publish-subscribe, event streaming (Kafka), delivery semantics (at-most-once, at-least-once, exactly-once), dead-letter queues, …
- [Caching](./caching/README.md) — Cache-aside, write-through, write-back, eviction policies (LRU, LFU), cache invalidation, Redis and Memcached, CDN caching, cache stampede prevention
- [Software Architecture](./software-architecture/README.md) — Monolith vs. microservices, modular monoliths, domain-driven design (bounded contexts, aggregates), hexagonal and clean architecture, service boundaries, API ga…
- [Reliability and Observability](./reliability-and-observability/README.md) — Structured logging, metrics (counters, gauges, histograms), distributed tracing (OpenTelemetry), SLIs, SLOs, and error budgets, health checks, graceful shutdown…
- [Testing](./testing/README.md) — Unit testing, integration testing, end-to-end testing, contract testing (Pact), property-based testing, test doubles (mocks, stubs, fakes), test-driven developm…
- [Software Engineering Practice](./software-engineering-practice/README.md) — Git workflows, code review, design documents and RFCs, CI basics, refactoring, clean code, technical debt management, documentation, on-call practices, secure c…

## Resource graph

The subject root is a `course`; each folder below is a `topic`; each topic's linked lesson pages are graph-linked `subtopic` teaching resources. Use `CONTAINS` from course to topic and topic to subtopic. The lesson metadata records prerequisite IDs. Keep learner assessment evidence separate from curriculum facts.
