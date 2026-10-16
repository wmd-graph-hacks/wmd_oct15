from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=300)
    subject: str | None = Field(default=None, max_length=80, description="Subject folder slug, e.g. 'physics'")
    hours_per_week: float = Field(default=5, gt=0, le=60)
    weeks_available: int = Field(default=16, gt=0, le=104)


class TraceStep(BaseModel):
    index: int
    tool: str
    args: dict[str, Any]
    summary: str
    evidence_ids: list[str] = Field(default_factory=list)
    ok: bool = True
    ms: int = 0


class AgentRun(BaseModel):
    id: str
    controller: Literal["playbook", "llm"]
    request: AgentRequest
    steps: list[TraceStep] = Field(default_factory=list)
    explanation: str = ""
    cited_ids: list[str] = Field(default_factory=list)
    proposal_id: str | None = None
    highlight: dict[str, list[str]] = Field(default_factory=dict)
    fallback_reason: str | None = None
    status: Literal["proposed", "failed"] = "proposed"
