"""Состояние интервью хранится в коде, а не только в контексте LLM (п. 4.1.1 г ТЗ)."""

from enum import StrEnum

from pydantic import BaseModel, Field


class Topic(BaseModel):
    """Тема плана интервью."""

    id: str
    core_question: str
    goal: str
    max_probes: int = Field(default=2, ge=0, le=5)
    required: bool = True


class InterviewPlan(BaseModel):
    """План интервью в формате JSON (п. 4.1.2 ТЗ)."""

    version: int = 1
    topics: list[Topic]
    max_turns: int = 30


class SessionStatus(StrEnum):
    CONSENT = "consent"
    IN_PROGRESS = "in_progress"
    SUMMARY = "summary"
    FINISHED = "finished"
    STOPPED_SAFETY = "stopped_safety"


class InterviewState(BaseModel):
    current_topic_index: int = 0
    probes_used: int = 0
    turn_count: int = 0
    covered: dict[str, str] = Field(default_factory=dict)
    status: SessionStatus = SessionStatus.CONSENT

    def can_probe(self, plan: InterviewPlan) -> bool:
        if self.current_topic_index >= len(plan.topics):
            return False
        topic = plan.topics[self.current_topic_index]
        return self.probes_used < topic.max_probes

    def should_finish(self, plan: InterviewPlan) -> bool:
        required = {t.id for t in plan.topics if t.required}
        return required <= self.covered.keys() or self.turn_count >= plan.max_turns
