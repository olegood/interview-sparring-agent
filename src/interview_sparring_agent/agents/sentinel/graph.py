"""Sentinel node: reviews FeedbackSuperAgent output for groundedness and coverage."""

from interview_sparring_agent.agents.sentinel.policies import review_feedback_report
from interview_sparring_agent.orchestration.state import SessionState

MAX_FEEDBACK_RETRIES = 2


def sentinel_review_node(state: SessionState) -> dict:
    report = state["feedback_report"]
    if report is None:
        return {}

    approved, notes = review_feedback_report(report, state)
    report.sentinel_approved = approved
    report.sentinel_notes = notes

    updates: dict = {"feedback_report": report}

    if approved:
        updates["phase"] = "done"
        return updates

    retry_count = state.get("feedback_retry_count", 0) + 1
    updates["feedback_retry_count"] = retry_count

    if retry_count > MAX_FEEDBACK_RETRIES:
        # Give up - exit with the rejected report intact so the caller can
        # still show which items are untrusted, rather than looping forever.
        updates["phase"] = "done"

    return updates


def should_retry_feedback(state: SessionState) -> str:
    """Conditional edge: route back to answer_critiquer for a retry, or exit."""
    report = state["feedback_report"]
    if report.sentinel_approved:
        return "done"
    if state.get("feedback_retry_count", 0) > MAX_FEEDBACK_RETRIES:
        return "done"
    return "retry"
