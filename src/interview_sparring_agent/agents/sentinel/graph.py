"""Sentinel node: reviews FeedbackSuperAgent output for groundedness."""

from interview_sparring_agent.agents.sentinel.policies import (
    check_feedback_groundedness,
)
from interview_sparring_agent.orchestration.state import SessionState


def sentinel_review_node(state: SessionState) -> dict:
    report = state["feedback_report"]
    if report is None:
        return {}

    approved, notes = check_feedback_groundedness(report, state)

    report.sentinel_approved = approved
    report.sentinel_notes = notes

    return {"feedback_report": report, "phase": "done"}