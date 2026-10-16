"""Read-only graph queries over wmd_kg. State (mastered ids) is passed in as parameters."""
from __future__ import annotations

from collections import deque
from typing import Any, Iterable

from app.kg.connection import kg_graph, rows

_OK = "r.status IN ['curated','approved'] AND coalesce(r.scope,'')<>'course'"


def _strength(include_soft: bool) -> str:
    return "" if include_soft else " AND r.strength='recommended'"


_STOP = set("""i me my we want to wants wish would like learn learning study studying understand understanding know
about the a an of in on for and or with how what why can do get be become better master mastering basics basic
introduction intro course topic topics subject need please help into some from""".split())


def _stem(w: str) -> str:
    for suf in ("ations", "ation", "ings", "ing", "ies", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def list_subjects(graph: Any | None = None) -> list[dict]:
    """Every loaded subject with size and data-quality facts (authored vs inferred prerequisites)."""
    import json
    g = graph or kg_graph()
    res = rows(g, "MATCH (c:Course) WHERE c.subject IS NOT NULL "
                  "OPTIONAL MATCH (s:Subtopic {subject:c.subject}) "
                  "RETURN c.subject, c.title, c.prefix, c.structure, count(s) ORDER BY c.title")
    out = []
    for subject, title, prefix, structure, n in res:
        info = json.loads(structure) if structure else {}
        thin = info.get("authored_edges", 0) == 0 or info.get("max_subtopics_per_topic", 0) <= 1
        out.append({"subject": subject, "title": title, "prefix": prefix, "subtopics": n,
                    "topics": info.get("topics", 0), "authored_edges": info.get("authored_edges", 0),
                    "inferred_edges": info.get("inferred_sequence_edges", 0), "thin": thin})
    return out


_prefixes: set[str] | None = None


def id_prefixes(graph: Any | None = None) -> set[str]:
    """Id prefixes of the loaded subjects (e.g. 'math', 'physics'); used to recognise node ids in text."""
    global _prefixes
    if _prefixes is None:
        found = {r[0] for r in rows(graph or kg_graph(), "MATCH (c:Course) WHERE c.prefix IS NOT NULL RETURN c.prefix")}
        if not found:
            return set()
        _prefixes = found
    return _prefixes


def reset_prefixes() -> None:
    global _prefixes
    _prefixes = None


def id_pattern(graph: Any | None = None):
    import re
    pre = sorted(id_prefixes(graph), key=len, reverse=True)
    return re.compile(r"\b(?:%s)-[a-z0-9-]+" % "|".join(re.escape(p) for p in pre)) if pre else None


def _catalog(g: Any, subject: str | None = None) -> list[dict]:
    where = "WHERE s.subject=$subject " if subject else ""
    res = rows(g, f"MATCH (s:Subtopic) {where}OPTIONAL MATCH (t:Topic {{id:s.topic_id}}) "
                  "RETURN s.id, s.title, s.topic_id, t.title, s.estimated_minutes, s.topic_order, s.order",
               {"subject": subject} if subject else None)
    return [{"id": r[0], "title": r[1], "topic_id": r[2], "topic_title": r[3] or "", "minutes": r[4],
             "k": (r[5], r[6])} for r in res]


def find_topics(text: str, limit: int = 8, graph: Any | None = None, subject: str | None = None) -> dict:
    """Typo-tolerant keyword match over subtopic and topic titles.

    Returns {"matches": [...], "topic_match": {...} | None}. A topic_match is set when the goal names a whole
    topic (e.g. 'calculus'), so callers can target all of its subtopics.
    """
    import difflib
    import re

    g = graph or kg_graph()
    cat = _catalog(g, subject)
    vocab: set[str] = set()
    for c in cat:
        vocab.update(_stem(w) for w in re.findall(r"[a-z]+", (c["title"] + " " + c["topic_title"]).lower()) if len(w) > 2)
    terms: list[str] = []
    raw: dict[str, str] = {}
    for w in re.findall(r"[a-z]+", text.lower()):
        if w in _STOP or len(w) < 3:
            continue
        st = _stem(w)
        if st not in vocab:
            close = difflib.get_close_matches(st, vocab, n=1, cutoff=0.78)
            st = close[0] if close else st
        terms.append(st)
        raw[st] = w
    if not terms:
        return {"matches": [], "topic_match": None}

    def toks(s: str) -> set[str]:
        return {_stem(w) for w in re.findall(r"[a-z]+", s.lower())}

    df = {t: sum(1 for c in cat if t in toks(c["title"]) or t in toks(c["topic_title"])) or 1 for t in terms}
    scored = []
    for c in cat:
        sub_hit = sum(1 for t in terms if t in toks(c["title"]))
        # rarer terms weigh more, so 'kkt' beats a generic word like 'conditions'
        words = set(re.findall(r"[a-z]+", (c["title"] + " " + c["topic_title"]).lower()))
        exact = sum(0.5 for t in terms if raw[t] in words)  # same surface form beats a stem-only match
        score = exact + sum((2.0 if t in toks(c["title"]) else 1.0 if t in toks(c["topic_title"]) else 0.0) / df[t] for t in terms)
        if score:
            scored.append({**c, "score": round(score, 3), "sub_hit": sub_hit})
    scored.sort(key=lambda c: (-c["score"], c["k"]))
    matches = [{"id": c["id"], "title": c["title"], "topic_id": c["topic_id"], "minutes": c["minutes"],
                "score": c["score"]} for c in scored[:limit]]
    topic_match = None
    if scored and scored[0]["sub_hit"] == 0:  # matched only through the topic name
        tid = scored[0]["topic_id"]
        members = sorted((c for c in cat if c["topic_id"] == tid), key=lambda c: c["k"])
        topic_match = {"topic_id": tid, "title": members[0]["topic_title"], "subtopic_ids": [c["id"] for c in members]}
    return {"matches": matches, "topic_match": topic_match}


def get_subtopic(sid: str, graph: Any | None = None) -> dict | None:
    out = rows(graph or kg_graph(),
        "MATCH (s:Subtopic {id:$id}) RETURN s.id, s.title, s.topic_id, s.estimated_minutes", {"id": sid})
    if not out:
        return None
    r = out[0]
    return {"id": r[0], "title": r[1], "topic_id": r[2], "minutes": r[3]}


def prerequisite_closure(targets: Iterable[str], mastered: Iterable[str] = (),
                         include_soft: bool = True, graph: Any | None = None) -> list[dict]:
    """Unmastered prerequisites needed for the targets (targets included unless mastered).

    A prerequisite is only needed if the path from it to the target does not pass through a
    mastered subtopic (mastery of an intermediate node cuts the dependency).
    """
    g = graph or kg_graph()
    targets, mastered = list(targets), list(mastered)
    res = rows(g,
        "MATCH (t:Subtopic) WHERE t.id IN $targets "
        "MATCH p=(pre:Subtopic)-[:PREREQUISITE_OF*1..20]->(t) "
        "WHERE NOT pre.id IN $mastered "
        f"AND all(r IN relationships(p) WHERE {_OK}{_strength(include_soft)}) "
        "AND all(n IN nodes(p)[1..size(nodes(p))-1] WHERE NOT n.id IN $mastered) "
        "RETURN DISTINCT pre.id, pre.title, pre.estimated_minutes, pre.topic_order, pre.order",
        {"targets": targets, "mastered": mastered})
    seen = {r[0]: {"id": r[0], "title": r[1], "minutes": r[2], "_k": (r[3], r[4])} for r in res}
    for t in targets:
        if t not in mastered and t not in seen:
            s = get_subtopic(t, g)
            if s:
                seen[t] = {"id": s["id"], "title": s["title"], "minutes": s["minutes"], "_k": (99, 0)}
    return list(seen.values())


def prerequisite_edges(include_soft: bool = True, graph: Any | None = None,
                       subject: str | None = None) -> list[tuple[str, str, str, bool]]:
    sub = " AND a.subject=$subject" if subject else ""
    res = rows(graph or kg_graph(),
        f"MATCH (a:Subtopic)-[r:PREREQUISITE_OF]->(b:Subtopic) WHERE {_OK}{_strength(include_soft)}{sub} "
        "RETURN a.id, b.id, r.strength, r.derived", {"subject": subject} if subject else None)
    return [(r[0], r[1], r[2], bool(r[3])) for r in res]


def order_by_dependency(nodes: list[dict], include_soft: bool = True, graph: Any | None = None) -> list[dict]:
    """Topological order of the closure (Kahn), ties by curriculum order."""
    ids = {n["id"] for n in nodes}
    indeg = {i: 0 for i in ids}
    succ: dict[str, list[str]] = {i: [] for i in ids}
    for a, b, _, _ in prerequisite_edges(include_soft, graph):
        if a in ids and b in ids:
            succ[a].append(b)
            indeg[b] += 1
    by_id = {n["id"]: n for n in nodes}
    ready = sorted([i for i in ids if indeg[i] == 0], key=lambda i: by_id[i].get("_k", (0, 0)))
    out: list[dict] = []
    while ready:
        i = ready.pop(0)
        out.append(by_id[i])
        for j in succ[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                ready.append(j)
        ready.sort(key=lambda k: by_id[k].get("_k", (0, 0)))
    return out


def frontier(mastered: Iterable[str], include_soft: bool = True, graph: Any | None = None,
             subject: str | None = None) -> list[dict]:
    """Unmastered subtopics whose recommended prerequisites are all mastered."""
    res = rows(graph or kg_graph(),
        f"MATCH (s:Subtopic) WHERE NOT s.id IN $mastered{' AND s.subject=$subject' if subject else ''} "
        "OPTIONAL MATCH (p:Subtopic)-[r:PREREQUISITE_OF]->(s) "
        f"WHERE {_OK}{_strength(include_soft)} AND NOT p.id IN $mastered "
        "WITH s, count(p) AS unmet WHERE unmet = 0 "
        "RETURN s.id, s.title, s.estimated_minutes, s.topic_id ORDER BY s.topic_order, s.order",
        {"mastered": list(mastered), "subject": subject})
    return [{"id": r[0], "title": r[1], "minutes": r[2], "topic_id": r[3]} for r in res]


def explain_path(src: str, dst: str, graph: Any | None = None) -> list[str]:
    """Shortest prerequisite chain src -> dst (ids), [] if none. Cypher first, BFS fallback."""
    g = graph or kg_graph()
    try:
        res = rows(g,
            "MATCH (a:Subtopic {id:$a}), (b:Subtopic {id:$b}) "
            "WITH shortestPath((a)-[:PREREQUISITE_OF*]->(b)) AS p "
            "RETURN [n IN nodes(p) | n.id]", {"a": src, "b": dst})
        if res and res[0][0]:
            return list(res[0][0])
        return []
    except Exception:
        adj: dict[str, list[str]] = {}
        for a, b, _, _ in prerequisite_edges(True, g):
            adj.setdefault(a, []).append(b)
        prev: dict[str, str | None] = {src: None}
        dq = deque([src])
        while dq:
            n = dq.popleft()
            if n == dst:
                path = []
                cur: str | None = n
                while cur is not None:
                    path.append(cur)
                    cur = prev[cur]
                return path[::-1]
            for m in adj.get(n, []):
                if m not in prev:
                    prev[m] = n
                    dq.append(m)
        return []


def _betweenness(edges: list[tuple[str, str]]) -> dict[str, float]:
    """Brandes betweenness on a directed, unweighted graph (fallback when the DB algorithm returns nothing)."""
    adj: dict[str, list[str]] = {}
    nodes: set[str] = set()
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        nodes.update((a, b))
    bc = {n: 0.0 for n in nodes}
    for src in nodes:
        stack: list[str] = []
        pred: dict[str, list[str]] = {n: [] for n in nodes}
        sigma = {n: 0 for n in nodes}
        dist = {n: -1 for n in nodes}
        sigma[src], dist[src] = 1, 0
        dq = deque([src])
        while dq:
            v = dq.popleft()
            stack.append(v)
            for w in adj.get(v, []):
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    dq.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = {n: 0.0 for n in nodes}
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != src:
                bc[w] += delta[w]
    return bc


def bottlenecks(node_ids: Iterable[str] | None = None, limit: int = 5, graph: Any | None = None) -> list[dict]:
    """Rank subtopics by betweenness (gatekeepers). Optionally restrict to given ids."""
    g = graph or kg_graph()
    res = rows(g,
        "CALL algo.betweenness({nodeLabels:['Subtopic'], relationshipTypes:['PREREQUISITE_OF']}) "
        "YIELD node, score RETURN node.id, node.title, score ORDER BY score DESC")
    keep = set(node_ids) if node_ids is not None else None
    out = [{"id": r[0], "title": r[1], "score": float(r[2])} for r in res if keep is None or r[0] in keep]
    if keep and not any(o["score"] > 0 for o in out):
        # the DB algorithm can return all zeros on small graphs: compute it directly over the selected subgraph
        titles = {r[0]: r[1] for r in res}
        scores = _betweenness([(a, b) for a, b, _, _ in prerequisite_edges(True, g) if a in keep and b in keep])
        out = [{"id": i, "title": titles.get(i, i), "score": round(v, 3)} for i, v in sorted(scores.items(), key=lambda x: -x[1])]
    return [o for o in out if o["score"] > 0][:limit]


def critical_path(node_ids: list[str], include_soft: bool = True, graph: Any | None = None) -> dict:
    """Longest chain by minutes within the induced subgraph (determines the minimum sequential effort)."""
    g = graph or kg_graph()
    ids = set(node_ids)
    minutes = {r[0]: r[1] for r in rows(g, "MATCH (s:Subtopic) WHERE s.id IN $ids RETURN s.id, s.estimated_minutes",
                                        {"ids": list(ids)})}
    pred: dict[str, list[str]] = {i: [] for i in ids}
    for a, b, _, _ in prerequisite_edges(include_soft, g):
        if a in ids and b in ids:
            pred[b].append(a)
    memo: dict[str, tuple[int, list[str]]] = {}

    def best(n: str) -> tuple[int, list[str]]:
        if n in memo:
            return memo[n]
        cand = max((best(p) for p in pred[n]), key=lambda x: x[0], default=(0, []))
        memo[n] = (cand[0] + int(minutes.get(n, 0)), cand[1] + [n])
        return memo[n]

    if not ids:
        return {"minutes": 0, "path": []}
    total, path = max((best(n) for n in ids), key=lambda x: x[0])
    return {"minutes": total, "path": path}
