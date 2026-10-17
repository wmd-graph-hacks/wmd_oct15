"""Question bank loader (YAML in git). Answer keys never leave the server before submission."""
from __future__ import annotations

import random
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

BANK_DIR = Path(__file__).resolve().parents[2] / "question_bank"  # <subject>/<file>.yaml


class Question(BaseModel):
    id: str
    level: int = Field(ge=1, le=3)
    stem: str
    options: list[str] = Field(min_length=2, max_length=6)
    answer: int
    hints: list[str] = Field(default_factory=list)
    explanation: str = ""
    subtopic_id: str = ""

    @model_validator(mode="after")
    def _check(self) -> "Question":
        if not 0 <= self.answer < len(self.options):
            raise ValueError(f"{self.id}: answer index out of range")
        if len(set(self.options)) != len(self.options):
            raise ValueError(f"{self.id}: duplicate options")
        return self


@lru_cache(maxsize=1)
def load_bank(directory: Path = BANK_DIR) -> dict[str, list[Question]]:
    bank: dict[str, list[Question]] = {}
    for f in sorted(directory.glob("*/*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        sid = data["subtopic_id"]
        qs = [Question(**q, subtopic_id=sid) for q in data["questions"]]
        if len({q.id for q in qs}) != len(qs):
            raise ValueError(f"{f.name}: duplicate question ids")
        bank[sid] = qs
    return bank


def questions_for(subtopic_id: str) -> list[Question]:
    return load_bank().get(subtopic_id, [])


def find_question(subtopic_id: str, qid: str) -> Question | None:
    return next((q for q in questions_for(subtopic_id) if q.id == qid), None)


def shuffled_order(seed: str, n: int) -> list[int]:
    """Deterministic option permutation: displayed position -> original option index."""
    order = list(range(n))
    random.Random(seed).shuffle(order)
    return order
