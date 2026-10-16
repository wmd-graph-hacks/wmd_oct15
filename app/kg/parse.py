"""Parse and validate curriculum markdown (any subject folder) into typed records."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, ValidationError

_FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_SUBTOPIC_LINE = re.compile(r"^- \[.*?\]\(.*?\) \(`([^`]+)`\)", re.M)


class CurriculumError(ValueError):
    pass


class PrereqRef(BaseModel):
    id: str
    target_type: Literal["topic", "subtopic", "course"] = "subtopic"
    strength: Literal["recommended", "soft", "sequence"] = "recommended"


class SubtopicRec(BaseModel):
    id: str
    title: str
    topic_id: str
    phase: str = ""
    estimated_minutes: int = 45
    order: int = 0
    topic_order: int = 0
    outcomes: list[str] = Field(default_factory=list)
    prerequisites: list[PrereqRef] = Field(default_factory=list)


class TopicRec(BaseModel):
    id: str
    title: str
    phase: str = ""
    order: int = 0
    estimated_hours: float = 0
    subtopic_ids: list[str] = Field(default_factory=list)


class Curriculum(BaseModel):
    subject: str = ""  # folder slug, e.g. "physics"
    prefix: str = ""  # id prefix shared by every node of the subject
    course_id: str
    course_title: str
    structure: dict = Field(default_factory=dict)  # data-quality facts, see _structure()
    topics: list[TopicRec]
    subtopics: list[SubtopicRec]
    edges: list[dict]  # {src, dst, strength, scope, derived}
    root: Path | None = None


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = _FM.match(text)
    if not m:
        raise CurriculumError(f"{path}: missing frontmatter")
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        raise CurriculumError(f"{path}: bad YAML: {exc}") from exc
    return data, text[m.end():]


def _prereqs(raw: object, path: Path) -> list[PrereqRef]:
    out: list[PrereqRef] = []
    for item in raw or []:
        if isinstance(item, str):
            if item.strip().lower() in {"none", ""}:
                continue
            raise CurriculumError(f"{path}: bare string prerequisite {item!r}")
        try:
            out.append(PrereqRef(**item))
        except ValidationError as exc:
            raise CurriculumError(f"{path}: bad prerequisite {item!r}: {exc}") from exc
    return out


def load_curriculum(root: Path) -> Curriculum:
    course_fm, _ = _frontmatter(root / "README.md")
    topics: list[TopicRec] = []
    subtopics: list[SubtopicRec] = []
    for topic_readme in sorted(root.glob("*/README.md")):
        fm, body = _frontmatter(topic_readme)
        if fm.get("type") != "topic":
            continue
        listed = _listed_subtopics(body)
        topic = TopicRec(
            id=fm["id"], title=fm["title"], phase=str(fm.get("phase", "")),
            order=int(fm.get("order", 0)), estimated_hours=float(fm.get("estimated_hours", 0)),
            subtopic_ids=listed,
        )
        topics.append(topic)
        by_id: dict[str, SubtopicRec] = {}
        for sub_readme in sorted(topic_readme.parent.glob("*/README.md")):
            sfm, _ = _frontmatter(sub_readme)
            if sfm.get("type") != "subtopic":
                continue
            rec = SubtopicRec(
                id=sfm["id"], title=str(sfm["title"]).replace(" — study lesson", ""), topic_id=sfm["parent_topic"],
                phase=str(sfm.get("phase", "")), estimated_minutes=int(sfm.get("estimated_minutes", 45)),
                topic_order=topic.order, outcomes=list(sfm.get("learning_outcomes") or []),
                prerequisites=_prereqs(sfm.get("prerequisites"), sub_readme),
            )
            by_id[rec.id] = rec
        for pos, sid in enumerate(listed):
            if sid in by_id:
                by_id[sid].order = pos
        unlisted = sorted(set(by_id) - set(listed))
        if unlisted and listed:
            raise CurriculumError(f"{topic.id}: subtopics not listed in README: {unlisted}")
        if not listed:  # flat topics: fall back to folder order
            for pos, sid in enumerate(sorted(by_id)):
                by_id[sid].order = pos
        topic.subtopic_ids = [s for s in (listed or sorted(by_id)) if s in by_id]
        subtopics.extend(sorted(by_id.values(), key=lambda s: s.order))
    topics.sort(key=lambda t: t.order)
    cid = course_fm["id"]
    cur = Curriculum(
        subject=root.name, prefix=cid[:-len("-course")] if cid.endswith("-course") else cid,
        course_id=cid, course_title=course_fm["title"],
        topics=topics, subtopics=subtopics, edges=[], root=root,
    )
    cur.edges = _build_edges(cur)
    cur.structure = _structure(cur)
    if not any(e["strength"] != "sequence" for e in cur.edges):
        cur.edges.extend(_sequence_edges(cur))  # no authored prerequisites: use the syllabus stage order
        cur.structure = _structure(cur)
    validate(cur)
    return cur


def _listed_subtopics(body: str) -> list[str]:
    """Subtopic ids in README order: from `## Subtopics`, else the `## Study lesson` list (flat subjects)."""
    for head in ("## Subtopics", "## Study lesson"):
        if head in body:
            return _SUBTOPIC_LINE.findall(body.split(head, 1)[1].split("\n## ", 1)[0])
    return []


_STAGE = re.compile(r"^## Stage:.*$", re.M)
_TOPIC_LINK = re.compile(r"\]\(\./([^/)]+)/README\.md\)")


def _stages(cur: Curriculum) -> list[list[str]]:
    """Topic ids per syllabus stage, in stage order ([] when the subject has no staged syllabus)."""
    path = (cur.root or Path()) / "syllabus.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    by_dir = {r.parent.name: _frontmatter(r)[0].get("id") for r in cur.root.glob("*/README.md")}
    parts = _STAGE.split(text)[1:]
    stages = []
    for part in parts:
        part = part.split("\n## ", 1)[0]
        ids = [by_dir[d] for d in _TOPIC_LINK.findall(part) if by_dir.get(d)]
        if ids:
            stages.append(ids)
    return stages


def _sequence_edges(cur: Curriculum) -> list[dict]:
    """Inferred ordering: last subtopic of every topic in stage k -> first subtopic of every topic in stage k+1.

    These are NOT authored prerequisites. They are labelled strength='sequence' so the UI and agent can say so.
    """
    topic_by_id = {t.id: t for t in cur.topics}
    stages = _stages(cur)
    out = []
    for a, b in zip(stages, stages[1:]):
        for ta in a:
            for tb in b:
                src, dst = topic_by_id[ta].subtopic_ids, topic_by_id[tb].subtopic_ids
                if src and dst:
                    out.append({"src": src[-1], "dst": dst[0], "strength": "sequence", "scope": "", "derived": True})
    return out


def _structure(cur: Curriculum) -> dict:
    """Facts about how much real structure the source data carries (used to flag thin subjects)."""
    kinds = {"recommended": 0, "soft": 0, "sequence": 0}
    for e in cur.edges:
        kinds[e["strength"]] = kinds.get(e["strength"], 0) + 1
    per_topic = [len(t.subtopic_ids) for t in cur.topics]
    return {"topics": len(cur.topics), "subtopics": len(cur.subtopics), "authored_edges": kinds["recommended"] + kinds["soft"],
            "inferred_sequence_edges": kinds["sequence"], "max_subtopics_per_topic": max(per_topic, default=0),
            "stages": len(_stages(cur)) if cur.root else 0}


def discover_subjects(artifacts_root: Path) -> list[Path]:
    """Subject folders: direct children whose README.md has `type: course`."""
    out = []
    for d in sorted(p for p in artifacts_root.iterdir() if p.is_dir() and (p / "README.md").exists()):
        try:
            fm, _ = _frontmatter(d / "README.md")
        except CurriculumError:
            continue
        if fm.get("type") == "course":
            out.append(d)
    return out


def _build_edges(cur: Curriculum) -> list[dict]:
    sub_ids = {s.id for s in cur.subtopics}
    topic_by_id = {t.id: t for t in cur.topics}
    edges: dict[tuple[str, str], dict] = {}

    def add(src: str, dst: str, strength: str, derived: bool) -> None:
        key = (src, dst)
        if key in edges:
            # keep the stronger relationship
            if strength == "recommended":
                edges[key]["strength"] = "recommended"
            return
        edges[key] = {"src": src, "dst": dst, "strength": strength, "scope": "", "derived": derived}

    # direct subtopic edges first so terminal-subtopic computation can use them
    for s in cur.subtopics:
        for p in s.prerequisites:
            if p.target_type == "subtopic":
                if p.id not in sub_ids:
                    raise CurriculumError(f"{s.id}: unknown prerequisite {p.id}")
                add(p.id, s.id, p.strength, False)

    def terminals(topic: TopicRec) -> list[str]:
        ids = set(topic.subtopic_ids)
        has_succ = {a for (a, b) in edges if a in ids and b in ids}
        found = [i for i in topic.subtopic_ids if i not in has_succ]
        return found or topic.subtopic_ids[-1:]

    for s in cur.subtopics:
        for p in s.prerequisites:
            if p.target_type == "topic":
                if p.id not in topic_by_id:
                    raise CurriculumError(f"{s.id}: unknown topic prerequisite {p.id}")
                for t in terminals(topic_by_id[p.id]):
                    add(t, s.id, p.strength, True)
    return list(edges.values())


def validate(cur: Curriculum) -> None:
    ids = [s.id for s in cur.subtopics]
    if len(ids) != len(set(ids)):
        raise CurriculumError("duplicate subtopic ids")
    adj: dict[str, list[str]] = {i: [] for i in ids}
    for e in cur.edges:
        if e["src"] == e["dst"]:
            raise CurriculumError(f"self loop on {e['src']}")
        adj[e["src"]].append(e["dst"])
    state: dict[str, int] = {}

    def dfs(n: str, stack: list[str]) -> None:
        state[n] = 1
        for m in adj[n]:
            if state.get(m) == 1:
                raise CurriculumError(f"cycle: {' -> '.join(stack + [n, m])}")
            if m not in state:
                dfs(m, stack + [n])
        state[n] = 2

    for n in ids:
        if n not in state:
            dfs(n, [])
