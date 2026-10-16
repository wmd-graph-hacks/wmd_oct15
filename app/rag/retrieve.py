"""GraphRAG retrieval: BM25 (+ optional embeddings) over Chunk nodes, then expansion over the prerequisite graph."""
from __future__ import annotations

import difflib
import math
import re
import threading
from dataclasses import dataclass, field
from typing import Any, Callable

from app.kg import queries as kg
from app.kg.connection import kg_graph, rows

_STOP = set("""a an the of in on for and or with to is are was were be been it its this that these those what why how
when where which who whom do does did can could should would explain tell me about please give define meaning mean
i we you my your our not no as at by from into than then there their they them""".split())
K1, B = 1.4, 0.75
MIN_SCORE = 1.2  # below this the corpus almost certainly does not cover the question


def _stem(w: str) -> str:
    for suf in ("ations", "ation", "ings", "ing", "ies", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def tokenize(text: str) -> list[str]:
    return [_stem(w) for w in re.findall(r"[a-z][a-z0-9]+", text.lower()) if w not in _STOP and len(w) > 1]


@dataclass
class IndexedChunk:
    id: str
    subtopic_id: str
    subtopic_title: str
    topic_title: str
    section: str
    text: str
    tokens: list[str]
    subject: str = ""
    embedding: list[float] | None = None


@dataclass
class Index:
    chunks: list[IndexedChunk]
    df: dict[str, int] = field(default_factory=dict)
    avg_len: float = 1.0
    vocab: set[str] = field(default_factory=set)
    n_docs: int = 0  # corpus size the df statistics were computed over (may exceed len(chunks) when filtered)


_index: Index | None = None
_lock = threading.Lock()


def reset_index() -> None:
    global _index
    with _lock:
        _index = None


def _stats(chunks: list[IndexedChunk]) -> Index:
    idx = Index(chunks)
    for c in chunks:
        for t in set(c.tokens):
            idx.df[t] = idx.df.get(t, 0) + 1
    idx.avg_len = (sum(len(c.tokens) for c in chunks) / len(chunks)) if chunks else 1.0
    idx.vocab = set(idx.df)
    idx.n_docs = len(chunks)
    return idx


def get_index(graph: Any | None = None) -> Index:
    global _index
    with _lock:
        if _index is not None and graph is None:
            return _index
        g = graph or kg_graph()
        res = rows(g,
            "MATCH (s:Subtopic)-[:HAS_CHUNK]->(c:Chunk) OPTIONAL MATCH (t:Topic {id:s.topic_id}) "
            "RETURN c.id, s.id, s.title, t.title, c.section, c.text, c.embedding, s.subject ORDER BY s.topic_order, s.order, c.idx")
        chunks = [IndexedChunk(r[0], r[1], r[2], r[3] or "", r[4] or "", r[5],
                               tokenize(f"{r[2]} {r[2]} {r[3] or ''} {r[4] or ''} {r[5]}"), r[7] or "", r[6] or None) for r in res]
        idx = _stats(chunks)
        if graph is None:
            _index = idx
        return idx


def correct_terms(query: str, vocab: set[str]) -> list[str]:
    out = []
    for t in tokenize(query):
        if t not in vocab and len(t) >= 6:
            close = difflib.get_close_matches(t, vocab, n=1, cutoff=0.84)
            t = close[0] if close else t
        out.append(t)
    return out


def bm25(idx: Index, terms: list[str]) -> list[tuple[float, IndexedChunk]]:
    n = idx.n_docs or len(idx.chunks)
    scored = []
    for c in idx.chunks:
        tf: dict[str, int] = {}
        for t in c.tokens:
            tf[t] = tf.get(t, 0) + 1
        s = 0.0
        for t in set(terms):
            f = tf.get(t, 0)
            if not f:
                continue
            idf = math.log(1 + (n - idx.df.get(t, 0) + 0.5) / (idx.df.get(t, 0) + 0.5))
            s += idf * f * (K1 + 1) / (f + K1 * (1 - B + B * len(c.tokens) / idx.avg_len))
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return scored


def _cos(a: list[float], b: list[float]) -> float:
    da = math.sqrt(sum(x * x for x in a)) or 1.0
    db = math.sqrt(sum(x * x for x in b)) or 1.0
    return sum(x * y for x, y in zip(a, b)) / (da * db)


@dataclass
class Passage:
    n: int
    chunk_id: str
    subtopic_id: str
    subtopic_title: str
    section: str
    text: str
    score: float


@dataclass
class Retrieval:
    passages: list[Passage]
    focus: dict | None  # best subtopic
    related: list[dict]  # other subtopics the passages came from
    prerequisites: list[dict]  # direct prerequisites of the focus subtopic (all, with ids/titles)
    covered: bool
    method: str
    prereq_basis: str = "authored"  # 'inferred' when the links only come from syllabus stage order


def retrieve(question: str, *, k: int = 5, subtopic_id: str | None = None, subject: str | None = None,
             query_embedding: list[float] | None = None, graph: Any | None = None) -> Retrieval:
    full = get_index(graph)
    # statistics (idf, vocabulary) come from the selected subject so rankings are not skewed by other subjects
    idx = _stats([c for c in full.chunks if c.subject == subject]) if subject else full
    terms = correct_terms(question, idx.vocab)
    pool = idx.chunks if not subtopic_id else [c for c in idx.chunks if c.subtopic_id == subtopic_id]
    sub = Index(pool, idx.df, idx.avg_len, idx.vocab, idx.n_docs)
    lex = bm25(sub, terms)
    method = "bm25"
    ranks: dict[str, float] = {}
    for r, (s, c) in enumerate(lex[:30]):
        ranks[c.id] = ranks.get(c.id, 0) + 1 / (60 + r)
    if query_embedding and any(c.embedding for c in pool):
        sem = sorted(((_cos(query_embedding, c.embedding), c) for c in pool if c.embedding), key=lambda x: -x[0])
        for r, (s, c) in enumerate(sem[:30]):
            ranks[c.id] = ranks.get(c.id, 0) + 1 / (60 + r)
        method = "bm25+embeddings"
    by_id = {c.id: c for c in pool}
    lex_score = {c.id: s for s, c in lex}
    top = sorted(ranks, key=lambda i: -ranks[i])[:k]
    uniq = set(terms)
    n_chunks = idx.n_docs or 1
    max_idf = math.log(1 + n_chunks + 0.5)

    def idf(t: str) -> float:  # words the corpus has never seen count as maximally informative but unmatched
        d = idx.df.get(t)
        return max_idf if d is None else math.log(1 + (n_chunks - d + 0.5) / (d + 0.5))
    total = sum(idf(t) for t in uniq)
    hit = sum(idf(t) for t in uniq & set(lex[0][1].tokens)) if lex else 0.0
    coverage = hit / total if total else 0.0
    # the informative words of the question must (mostly) appear together in the best passage
    covered = bool(lex) and lex[0][0] >= MIN_SCORE and (len(uniq) < 2 or coverage >= 0.6)
    passages = [Passage(n + 1, i, by_id[i].subtopic_id, by_id[i].subtopic_title, by_id[i].section, by_id[i].text,
                        round(lex_score.get(i, 0.0), 3)) for n, i in enumerate(top)]
    if not passages or not covered:
        return Retrieval([], None, [], [], False, method)
    agg: dict[str, float] = {}
    for p in passages:
        agg[p.subtopic_id] = agg.get(p.subtopic_id, 0) + ranks[p.chunk_id]
    order = sorted(agg, key=lambda s: -agg[s])
    focus_id = subtopic_id or order[0]
    focus = kg.get_subtopic(focus_id, graph)
    related = [kg.get_subtopic(s, graph) for s in order if s != focus_id][:3]
    incoming = [(a, st) for a, b, st, _ in kg.prerequisite_edges(True, graph) if b == focus_id]
    prereq_ids = [a for a, _ in incoming]
    basis = "inferred" if incoming and all(st == "sequence" for _, st in incoming) else "authored"
    prereqs = [p for p in (kg.get_subtopic(i, graph) for i in prereq_ids) if p]
    return Retrieval(passages, focus, [r for r in related if r], prereqs, True, method, basis)
