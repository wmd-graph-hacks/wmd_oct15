"""Personalized, cited answers grounded in retrieved lesson passages and the learner's mastery state."""
from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any, Awaitable, Callable

from pydantic import BaseModel, Field

from app.config import settings
from app.kg import queries as kg
from app.learn import bank, state
from app.learn.profile import Profile, get_profile
from app.rag import retrieve as rt

logger = logging.getLogger(__name__)
Completion = Callable[..., Awaitable[Any]]
_CITE = re.compile(r"\[(\d+)\]")


class Citation(BaseModel):
    n: int
    subtopic_id: str
    subtopic_title: str
    section: str
    excerpt: str


class PrereqNote(BaseModel):
    subtopic_id: str
    title: str
    status: str  # mastered | learning | gap | unseen
    quiz_url: str | None = None


class Answer(BaseModel):
    question: str
    answer: str
    covered: bool
    mode: str  # llm | extractive | not_covered
    level_used: str
    level_reason: str
    focus_subtopic_id: str | None = None
    focus_title: str | None = None
    focus_status: str | None = None
    focus_has_quiz: bool = False
    prereq_basis: str = "authored"
    citations: list[Citation] = Field(default_factory=list)
    weak_prerequisites: list[PrereqNote] = Field(default_factory=list)
    related: list[dict] = Field(default_factory=list)
    retrieval: str = "bm25"
    fallback_reason: str | None = None


def _level(profile: Profile, belief: dict | None) -> tuple[str, str]:
    if belief and belief["evidence"] >= 1.0:
        m = belief["mean"]
        lvl = "beginner" if m < 0.45 else "intermediate" if m < 0.7 else "advanced"
        return lvl, f"from your quiz history on this topic ({round(m * 100)}% estimated mastery)"
    return profile.level, "from your onboarding level (no quiz evidence on this topic yet)"


def _sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text.replace("**", ""))
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(])", flat) if len(s.strip()) > 25]


def _extractive(question: str, passages: list[rt.Passage], level: str, vocab: set[str]) -> str:
    terms = set(rt.correct_terms(question, vocab))
    parts: list[str] = []
    for p in passages[:3]:
        sents = _sentences(p.text)
        ranked = sorted(sents, key=lambda s: -len(terms & set(rt.tokenize(s))))
        take = ranked[:1] if level == "advanced" else ranked[:2]
        take = [s for s in sents if s in take]  # keep original order
        if take:
            parts.append(" ".join(take) + f" [{p.n}]")
    return "\n\n".join(parts)


def _system(level: str) -> str:
    style = {"beginner": "Use plain language, define terms, go step by step, and use one concrete example from the passages.",
             "intermediate": "Be precise but explain the key idea and when it applies.",
             "advanced": "Be concise and rigorous; state assumptions and edge cases."}[level]
    return ("You are a tutor for the selected subject. Answer ONLY from the numbered passages. Cite sources as [n] after each claim. "
            "If the passages do not contain the answer, say so. Never invent theorems, formulas, numbers or sources. "
            f"{style} Maximum 170 words. If prerequisite gaps are listed, end with one short sentence suggesting them.")


async def _llm(completion: Completion | None, question: str, passages: list[rt.Passage], level: str,
               weak: list[PrereqNote]) -> str:
    if completion is None:
        from litellm import acompletion
        completion = acompletion
    ctx = "\n\n".join(f"[{p.n}] ({p.subtopic_title} / {p.section})\n{p.text}" for p in passages)
    gaps = ", ".join(w.title for w in weak) or "none"
    msgs = [{"role": "system", "content": _system(level)},
            {"role": "user", "content": f"Passages:\n{ctx}\n\nPrerequisite gaps: {gaps}\n\nQuestion: {question}"}]
    last: Exception | None = None
    for model in dict.fromkeys((settings.ai_model, *settings.ai_fallback_models)):
        try:
            r = await completion(model=model, messages=msgs, max_tokens=settings.tutor_max_tokens,
                                 timeout=settings.agent_timeout_seconds, num_retries=0)
            text = (r.choices[0].message.content or "").strip()
            nums = {int(n) for n in _CITE.findall(text)}
            if text and nums and nums <= {p.n for p in passages}:
                return text
            last = RuntimeError("answer was not grounded in the passages")
        except Exception as exc:  # provider error: try the next model
            last = exc
    raise RuntimeError(str(last))


async def ask(uid: str, question: str, *, subtopic_id: str | None = None, subject: str | None = None, completion: Completion | None = None,
              embed: Callable[[list[str]], Awaitable[list[list[float]]]] | None = None) -> Answer:
    qvec = None
    if embed is not None:
        try:
            qvec = (await embed([question]))[0]
        except Exception:
            qvec = None
    ret = await asyncio.to_thread(rt.retrieve, question, subtopic_id=subtopic_id, subject=subject, query_embedding=qvec)
    profile = await asyncio.to_thread(get_profile, uid)
    scope = subject or "selected"
    if not ret.covered:
        return Answer(question=question, answer=f"I could not find this in the {scope} curriculum, so I will not guess. "
                      "Try naming the topic or a term from its lesson.", covered=False,
                      mode="not_covered", level_used=profile.level, level_reason="from your onboarding level",
                      retrieval=ret.method)
    beliefs = await asyncio.to_thread(state.get_beliefs, uid)
    focus = ret.focus or {}
    level, reason = _level(profile, beliefs.get(focus.get("id", "")))
    mastered = {s for s, v in beliefs.items() if v["status"] == "mastered"}
    weak = []
    for p in ret.prerequisites:
        st = beliefs.get(p["id"], {}).get("status", "unseen")
        if p["id"] not in mastered:
            weak.append(PrereqNote(subtopic_id=p["id"], title=p["title"], status=st,
                                   quiz_url=f"/quiz/{p['id']}" if bank.questions_for(p["id"]) else None))
    weak = weak[:4]
    mode, fb, text = "llm", None, ""
    if settings.ai_enabled:
        try:
            text = await _llm(completion, question, ret.passages, level, weak)
        except Exception as exc:
            fb = f"{type(exc).__name__}: {exc}"[:140]
            logger.warning("tutor LLM failed (%s); using extractive answer", type(exc).__name__)
    if not text:
        mode = "extractive"
        text = _extractive(question, ret.passages, level, (await asyncio.to_thread(rt.get_index)).vocab)
        if weak:
            text += "\n\nBefore this, you may want to firm up: " + ", ".join(w.title for w in weak) + "."
    cites = [Citation(n=p.n, subtopic_id=p.subtopic_id, subtopic_title=p.subtopic_title, section=p.section,
                      excerpt=re.sub(r"\s+", " ", p.text)[:280]) for p in ret.passages]
    return Answer(question=question, answer=text, covered=True, mode=mode, level_used=level, level_reason=reason,
                  focus_subtopic_id=focus.get("id"), focus_title=focus.get("title"),
                  focus_status=beliefs.get(focus.get("id", ""), {}).get("status", "unseen"),
                  focus_has_quiz=bool(bank.questions_for(focus.get("id", ""))), prereq_basis=ret.prereq_basis, citations=cites,
                  weak_prerequisites=weak, related=ret.related, retrieval=ret.method, fallback_reason=fb)
