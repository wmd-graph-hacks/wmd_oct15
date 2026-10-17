from datetime import date

from pydantic import BaseModel, Field


class PlanPreferences(BaseModel):
    exam_date: date
    minutes_per_day: int = Field(ge=10, le=480)
    exam_topic: str


class AttemptInput(BaseModel):
    topic_id: str = Field(min_length=1, max_length=80)
    score: int = Field(ge=0)
    max_score: int = Field(default=5, ge=1, le=100)


class SessionInput(BaseModel):
    topic_id: str = Field(min_length=1, max_length=80)


class AssessmentAnswer(BaseModel):
    assessment_id: str = Field(min_length=1, max_length=100)
    answer: str = Field(min_length=1, max_length=40)
