"""Idempotent loader: curriculum markdown -> wmd_kg."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from app.kg.connection import kg_graph, rows
from app.kg.parse import Curriculum, discover_subjects, load_curriculum

ARTIFACTS_ROOT = Path(__file__).resolve().parents[2] / "artifacts"


def _source_hash(root: Path) -> str:
    """Fingerprint curriculum markdown so app startup refreshes changed graph data."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.md")):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_graph(cur: Curriculum, graph: Any | None = None) -> dict[str, int]:
    """Idempotently (re)load one subject; other subjects in the graph are untouched."""
    g = graph or kg_graph()
    for q in (
        "CREATE INDEX FOR (n:Subtopic) ON (n.id)",
        "CREATE INDEX FOR (n:Topic) ON (n.id)",
        "CREATE INDEX FOR (n:Course) ON (n.id)",
        "CREATE INDEX FOR (n:Subtopic) ON (n.subject)",
    ):
        try:
            g.query(q)
        except Exception:  # index already exists
            pass
    sub = cur.subject
    source_hash = _source_hash(cur.root or ARTIFACTS_ROOT / sub)
    g.query(
        "MERGE (c:Course {id:$id}) SET c.title=$title, c.subject=$subject, c.prefix=$prefix, c.structure=$structure",
        {"id": cur.course_id, "title": cur.course_title, "subject": sub, "prefix": cur.prefix,
         "structure": json.dumps(cur.structure)},
    )
    g.query(
        "UNWIND $rows AS t MERGE (n:Topic {id:t.id}) "
        "SET n.title=t.title, n.phase=t.phase, n.order=t.order, n.estimated_hours=t.hours, n.subject=$subject "
        "WITH n MATCH (c:Course {id:$cid}) MERGE (c)-[:CONTAINS]->(n)",
        {"cid": cur.course_id, "subject": sub, "rows": [
            {"id": t.id, "title": t.title, "phase": t.phase, "order": t.order, "hours": t.estimated_hours}
            for t in cur.topics]},
    )
    g.query(
        "UNWIND $rows AS s MERGE (n:Subtopic {id:s.id}) "
        "SET n.title=s.title, n.topic_id=s.topic_id, n.phase=s.phase, n.order=s.order, n.subject=$subject, "
        "n.topic_order=s.topic_order, n.estimated_minutes=s.minutes "
        "WITH n, s MATCH (t:Topic {id:s.topic_id}) MERGE (t)-[:CONTAINS]->(n)",
        {"subject": sub, "rows": [
            {"id": s.id, "title": s.title, "topic_id": s.topic_id, "phase": s.phase,
             "order": s.order, "topic_order": s.topic_order, "minutes": s.estimated_minutes}
            for s in cur.subtopics]},
    )
    dropped = _load_chunks(g, cur)
    g.query("MATCH (a:Subtopic {subject:$s})-[r:PREREQUISITE_OF]->() DELETE r", {"s": sub})
    g.query(
        "UNWIND $rows AS e MATCH (a:Subtopic {id:e.src}), (b:Subtopic {id:e.dst}) "
        "CREATE (a)-[:PREREQUISITE_OF {strength:e.strength, status:'curated', scope:e.scope, derived:e.derived}]->(b)",
        {"rows": cur.edges},
    )
    from app.kg import queries
    queries.reset_prefixes()
    out = verify(g, cur)
    # Mark the source current only after nodes, edges, chunks, and counts verify.
    g.query("MATCH (c:Course {id:$id}) SET c.source_hash=$source_hash",
            {"id": cur.course_id, "source_hash": source_hash})
    out["boilerplate_chunks_dropped"] = dropped
    return out


def _load_chunks(g: Any, cur: Curriculum) -> int:
    from app.rag import retrieve
    from app.rag.chunks import load_all_chunks

    chunks, dropped = load_all_chunks(cur.root or ARTIFACTS_ROOT / cur.subject, {s.id for s in cur.subtopics})
    try:
        g.query("CREATE INDEX FOR (n:Chunk) ON (n.id)")
    except Exception:
        pass
    g.query("MATCH (:Subtopic {subject:$s})-[:HAS_CHUNK]->(c:Chunk) DETACH DELETE c", {"s": cur.subject})
    for i in range(0, len(chunks), 100):
        g.query(
            "UNWIND $rows AS c MATCH (s:Subtopic {id:c.sid}) "
            "CREATE (s)-[:HAS_CHUNK]->(:Chunk {id:c.id, subject:$subject, subtopic_id:c.sid, idx:c.idx, "
            "section:c.section, text:c.text})",
            {"subject": cur.subject, "rows": [
                {"id": c.id, "sid": c.subtopic_id, "idx": c.idx, "section": c.section, "text": c.text}
                for c in chunks[i:i + 100]]})
    retrieve.reset_index()
    return dropped


def verify(g: Any, cur: Curriculum) -> dict[str, int]:
    p = {"s": cur.subject}
    counts = {
        "topics": rows(g, "MATCH (n:Topic {subject:$s}) RETURN count(n)", p)[0][0],
        "subtopics": rows(g, "MATCH (n:Subtopic {subject:$s}) RETURN count(n)", p)[0][0],
        "edges": rows(g, "MATCH (:Subtopic {subject:$s})-[r:PREREQUISITE_OF]->() RETURN count(r)", p)[0][0],
        "orphans": rows(g, "MATCH (n:Subtopic {subject:$s}) WHERE NOT ()-[:CONTAINS]->(n) RETURN count(n)", p)[0][0],
        "chunks": rows(g, "MATCH (c:Chunk {subject:$s}) RETURN count(c)", p)[0][0],
    }
    if counts["chunks"] < len(cur.subtopics):
        raise RuntimeError(f"graph verification failed for {cur.subject}: only {counts['chunks']} chunks")
    expected = {"topics": len(cur.topics), "subtopics": len(cur.subtopics),
                "edges": len(cur.edges), "orphans": 0}
    if {k: counts[k] for k in expected} != expected:
        raise RuntimeError(f"graph verification failed for {cur.subject}: {counts} != {expected}")
    return counts


def load_all(root: Path = ARTIFACTS_ROOT, graph: Any | None = None) -> dict[str, dict]:
    """Load every subject folder under `root`. A broken subject is reported, not fatal to the others."""
    report: dict[str, dict] = {}
    for d in discover_subjects(root):
        try:
            report[d.name] = load_graph(load_curriculum(d), graph)
        except Exception as exc:
            report[d.name] = {"error": f"{type(exc).__name__}: {exc}"[:300]}
    return report


_loaded = False


def ensure_loaded() -> None:
    """Load any subject missing from wmd_kg. Cheap after the first success; retried while the DB is down."""
    global _loaded
    if _loaded:
        return
    g = kg_graph()
    have = {r[0]: r[1] for r in rows(g, "MATCH (c:Course) WHERE c.subject IS NOT NULL RETURN c.subject, c.source_hash")}
    for d in discover_subjects(ARTIFACTS_ROOT):
        cur = load_curriculum(d)
        # Older graph entries have no fingerprint and are refreshed once.
        if have.get(d.name) != _source_hash(d):
            load_graph(cur, g)
    _loaded = True


def main() -> None:
    ap = argparse.ArgumentParser(description="Load curriculum subjects into wmd_kg")
    ap.add_argument("--root", type=Path, default=ARTIFACTS_ROOT, help="artifacts folder (all subjects) or one subject folder")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dirs = discover_subjects(args.root) or [args.root]
    for d in dirs:
        cur = load_curriculum(d)
        print(f"{cur.subject}: {len(cur.topics)} topics, {len(cur.subtopics)} subtopics, {len(cur.edges)} edges {cur.structure}")
        if not args.dry_run:
            print("  loaded:", load_graph(cur))


if __name__ == "__main__":
    main()
