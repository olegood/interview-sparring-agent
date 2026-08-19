"""Shared session state schema for the interview sparring agent."""

import operator
from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, Field


class QAExchange(BaseModel):
    """A single question/answer exchange, including any follow-up."""

    question: str
    answer: str
    follow_up_question: str | None = None
    follow_up_answer: str | None = None
    difficulty: str = "medium"  # "easy" | "medium" | "hard" - kept as str for flexibility


class FeedbackItem(BaseModel):
    """Feedback on a single QAExchange, produced by FeedbackSuperAgent."""

    exchange_index: int  # index into qa_history this feedback refers to
    critique: str
    used_star_method: bool | None = None
    filler_words_flagged: list[str] = Field(default_factory=list)
    # The exact substring(s) from the answer that the critique is grounded in.
    # Sentinel checks these are non-empty and actually appear in the transcript.
    grounding_quotes: list[str] = Field(default_factory=list)


class FeedbackReport(BaseModel):
    """Full feedback pass output, covering the whole session."""

    items: list[FeedbackItem]
    overall_summary: str
    sentinel_approved: bool = False
    sentinel_notes: str | None = None


class SessionState(TypedDict):
    """Top-level LangGraph state for one interview sparring session.

    Nodes return partial updates (a dict with only the keys they change).
    Fields annotated with `operator.add` are appended to across updates
    rather than overwritten - this matters for qa_history, since each
    turn in the interview loop adds one more exchange.
    """

    # --- session config (set once, at session start) ---
    role: str  # e.g. "Backend Engineer"
    level: str  # e.g. "mid-level"
    max_questions: int

    # --- interview loop state ---
    phase: Literal["interviewing", "feedback", "done"]
    current_question: str | None
    current_difficulty: str  # "easy" | "medium" | "hard"
    question_count: int
    qa_history: Annotated[list[QAExchange], operator.add]

    # --- feedback phase state ---
    feedback_report: FeedbackReport | None
