"""answer_critiquer sub-agent: produces grounded, per-answer feedback plus
an overall session summary, in a single LLM call over the full transcript.
"""

from pydantic import BaseModel, Field

from interview_sparring_agent.agents.feedback_super_agent.prompts import (
    ANSWER_CRITIQUER_SYSTEM_PROMPT,
    RETRY_CONTEXT_TEMPLATE
)
from interview_sparring_agent.agents.feedback_super_agent.sub_agents.filler_word_detector import (
    detect_filler_words,
)
from interview_sparring_agent.llm.ollama_client import get_chat_model
from interview_sparring_agent.orchestration.state import (
    FeedbackItem,
    FeedbackReport,
    SessionState,
)


class _CritiqueItem(BaseModel):
    exchange_index: int
    critique: str
    used_star_method: bool | None = None
    grounding_quotes: list[str] = Field(default_factory=list)


class _CritiqueResult(BaseModel):
    items: list[_CritiqueItem]
    overall_summary: str


def _format_transcript(state: SessionState) -> str:
    lines = []
    for i, exchange in enumerate(state["qa_history"]):
        lines.append(f"Q{i} ({exchange.difficulty}): {exchange.question}")
        lines.append(f"A{i}: {exchange.answer}")
        lines.append("")
    return "\n".join(lines)


def answer_critiquer_node(state: SessionState) -> dict:
    model = get_chat_model(temperature=0.4)
    structured_model = model.with_structured_output(_CritiqueResult)

    prompt = ANSWER_CRITIQUER_SYSTEM_PROMPT.format(
        role=state["role"],
        level=state["level"],
        transcript=_format_transcript(state),
    )

    prior_report = state.get("feedback_report")
    if prior_report is not None and not prior_report.sentinel_approved and prior_report.sentinel_notes:
        prompt += RETRY_CONTEXT_TEMPLATE.format(notes=prior_report.sentinel_notes)

    result: _CritiqueResult = structured_model.invoke(prompt)

    items: list[FeedbackItem] = []
    for critique_item in result.items:
        exchange = state["qa_history"][critique_item.exchange_index]
        items.append(
            FeedbackItem(
                exchange_index=critique_item.exchange_index,
                critique=critique_item.critique,
                used_star_method=critique_item.used_star_method,
                filler_words_flagged=detect_filler_words(exchange.answer),
                grounding_quotes=critique_item.grounding_quotes,
            )
        )

    report = FeedbackReport(
        items=items,
        overall_summary=result.overall_summary,
    )

    return {"feedback_report": report, "phase": "feedback"}
