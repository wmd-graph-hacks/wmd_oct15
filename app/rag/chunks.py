"""Split subtopic lesson markdown into retrievable chunks."""
from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel

_FM = re.compile(r"\A---\n.*?\n---\n", re.S)
MAX_CHARS = 900


class Chunk(BaseModel):
    id: str
    subtopic_id: str
    idx: int
    section: str
    text: str


def _paragraphs(body: str) -> list[tuple[str, str]]:
    """(section heading, paragraph) pairs; H1 is treated as the opening section."""
    section, out = "Overview", []
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block:
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", block)
        if m and "\n" not in block:
            section = m.group(2).strip()
            continue
        out.append((section, block))
    return out


def split_subtopic(subtopic_id: str, markdown: str) -> list[Chunk]:
    body = _FM.sub("", markdown, count=1)
    chunks: list[Chunk] = []
    cur_section, cur = "", ""

    def flush() -> None:
        nonlocal cur
        if cur.strip():
            chunks.append(Chunk(id=f"{subtopic_id}#{len(chunks)}", subtopic_id=subtopic_id, idx=len(chunks),
                                section=cur_section, text=cur.strip()))
        cur = ""

    for section, para in _paragraphs(body):
        if section != cur_section or (cur and len(cur) + len(para) > MAX_CHARS):
            flush()
            cur_section = section
        cur = f"{cur}\n\n{para}" if cur else para
    flush()
    return chunks


def _norm(text: str, title: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace(title.lower(), "§")).strip()


def load_all_chunks(root: Path, subtopic_ids: set[str], min_repeats: int = 3) -> tuple[list[Chunk], int]:
    """Chunks of every subtopic lesson under a subject folder, minus template boilerplate.

    A chunk whose text (with the topic name masked) occurs in `min_repeats`+ lessons is boilerplate from a
    shared lesson template; it carries no subject knowledge and would only add noise to retrieval.
    Returns (chunks, dropped_count).
    """
    from app.kg.parse import _frontmatter  # reuse the frontmatter parser

    per: list[tuple[str, str, list[Chunk]]] = []
    for readme in sorted(root.glob("*/*/README.md")):
        fm, _ = _frontmatter(readme)
        if fm.get("type") == "subtopic" and fm["id"] in subtopic_ids:
            title = str(fm.get("title", "")).split(" — ")[0]
            per.append((fm["id"], title, split_subtopic(fm["id"], readme.read_text(encoding="utf-8"))))
    freq: dict[str, int] = {}
    for _, title, chunks in per:
        for key in {_norm(c.text, title) for c in chunks}:
            freq[key] = freq.get(key, 0) + 1
    out: list[Chunk] = []
    dropped = 0
    for sid, title, chunks in per:
        kept = [c for c in chunks if freq[_norm(c.text, title)] < min_repeats]
        dropped += len(chunks) - len(kept)
        out.extend(c.model_copy(update={"id": f"{sid}#{i}", "idx": i}) for i, c in enumerate(kept))
    return out, dropped
