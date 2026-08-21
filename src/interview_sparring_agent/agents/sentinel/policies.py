"""Deterministic policy checks used by the Sentinel agent.

These are intentionally plain Python (no LLM calls) - Sentinel's job is to
be a reliable, boring guardrail, not another model that can also hallucinate.
"""

import re

from interview_sparring_agent.orchestration.state import FeedbackReport, SessionState


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, and collapse whitespace for fuzzy matching."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # strip punctuation
    text = re.sub(r"\s+", " ", text).strip()  # collapse whitespace
    return text


def is_quote_grounded(quote: str, answer: str) -> bool:
    """Check whether `quote` genuinely appears in `answer`, ignoring minor
    punctuation/whitespace/case differences.
    """
    if not quote.strip():
        return False
    return _normalize(quote) in _normalize(answer)


def check_feedback_groundedness(report: FeedbackReport, state: SessionState) -> tuple[bool, str | None]:
    """Verify every FeedbackItem has at least one grounding quote that
    actually appears in its corresponding answer.

    Returns (approved, notes). notes is None when approved is True.
    """
    problems: list[str] = []

    for item in report.items:
        if item.exchange_index >= len(state["qa_history"]):
            problems.append(
                f"Item {item.exchange_index}: exchange_index out of range."
            )
            continue

        answer = state["qa_history"][item.exchange_index].answer

        if not item.grounding_quotes:
            problems.append(
                f"Item {item.exchange_index}: no grounding quotes provided."
            )
            continue

        ungrounded = [
            q for q in item.grounding_quotes if not is_quote_grounded(q, answer)
        ]
        if ungrounded:
            problems.append(
                f"Item {item.exchange_index}: quote(s) not found in answer: {ungrounded}"
            )

    if problems:
        return False, "; ".join(problems)
    return True, None
