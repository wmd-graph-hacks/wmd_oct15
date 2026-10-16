"""Pure mastery model: decayed Beta posterior per (learner, subtopic)."""
from __future__ import annotations

import math
from dataclasses import dataclass

TAU_DAYS = 90.0
TAU_MS = TAU_DAYS * 86_400_000
LEVEL_WEIGHT = {1: 0.6, 2: 1.0, 3: 1.4}
MASTERED_MEAN = 0.7
GAP_MEAN = 0.4
MIN_EVIDENCE = 2.0
HINT_PENALTY = 0.25
MIN_CORRECT_CREDIT = 0.25


def credit(correct: bool, hints_used: int, llm_graded: bool = False) -> float:
    if not correct:
        return 0.0
    c = max(MIN_CORRECT_CREDIT, 1.0 - HINT_PENALTY * hints_used)
    return c * 0.5 if llm_graded else c


def decay(value: float, elapsed_ms: float) -> float:
    """Decay a pseudo-count toward the prior (1.0)."""
    return 1.0 + (value - 1.0) * math.exp(-max(elapsed_ms, 0.0) / TAU_MS)


@dataclass(frozen=True)
class Belief:
    alpha: float = 1.0
    beta: float = 1.0

    @property
    def mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    @property
    def evidence(self) -> float:
        return self.alpha + self.beta - 2.0

    @property
    def status(self) -> str:
        if self.evidence >= MIN_EVIDENCE and self.mean >= MASTERED_MEAN:
            return "mastered"
        if self.evidence >= MIN_EVIDENCE and self.mean < GAP_MEAN:
            return "gap"
        if self.evidence > 0:
            return "learning"
        return "unseen"

    def decayed(self, elapsed_ms: float) -> "Belief":
        return Belief(decay(self.alpha, elapsed_ms), decay(self.beta, elapsed_ms))

    def updated(self, level: int, cr: float, elapsed_ms: float = 0.0) -> "Belief":
        b = self.decayed(elapsed_ms)
        w = LEVEL_WEIGHT[level]
        return Belief(b.alpha + w * cr, b.beta + w * (1.0 - cr))
