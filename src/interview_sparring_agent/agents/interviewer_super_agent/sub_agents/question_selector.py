"""question_selector sub-agent: generates the next interview question."""

from pydantic import BaseModel, Field

from interview_sparring_agent.agents.interviewer_super_agent.prompts import (
    QUESTION_SELECTOR_SYSTEM_PROMPT,
)
from interview_sparring_agent.llm.ollama_client import get_chat_model
from interview_sparring_agent.orchestration.state import SessionState


class GeneratedQuestion(BaseModel):
    """Structured output schema for a freshly generated interview question."""

    question: str = Field(description="The interview question to ask the candidate.")
    topic: str = Field(description="Short label for the skill/topic this question tests.")


def _covered_topics_text(state: SessionState) -> str:
    if not state["qa_history"]:
        return "(none yet)"
    # Using the question text itself as a stand-in for "topic" - simple and
    # good enough for v1. Could be refined to use GeneratedQuestion.topic
    # if we start persisting topic labels per exchange later.
    return "\n".join(f"- {exchange.question}" for exchange in state["qa_history"])


def question_selector_node(state: SessionState) -> dict:
    """LangGraph node: generate the next question and write it into state.

    Returns a partial state update (LangGraph merges this into SessionState).
    """
    model = get_chat_model(temperature=0.8)
    structured_model = model.with_structured_output(GeneratedQuestion)

    prompt = QUESTION_SELECTOR_SYSTEM_PROMPT.format(
        role=state["role"],
        level=state["level"],
        difficulty=state["current_difficulty"],
        covered_topics=_covered_topics_text(state),
    )

    result: GeneratedQuestion = structured_model.invoke(prompt)

    return {
        "current_question": result.question,
    }