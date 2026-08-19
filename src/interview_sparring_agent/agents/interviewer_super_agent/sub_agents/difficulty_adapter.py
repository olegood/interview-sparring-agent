"""difficulty_adapter sub-agent: adjusts difficulty for the next question
based on the quality of the most recent answer.
"""

from typing import Literal

from pydantic import BaseModel, Field

from interview_sparring_agent.agents.interviewer_super_agent.prompts import (
    DIFFICULTY_ADAPTER_SYSTEM_PROMPT,
)
from interview_sparring_agent.llm.ollama_client import get_chat_model
from interview_sparring_agent.orchestration.state import SessionState


class DifficultyAdjustment(BaseModel):
    next_difficulty: Literal["easy", "medium", "hard"] = Field(
        description="Difficulty level for the next question."
    )
    reasoning: str = Field(description="Brief reasoning for this adjustment.")


def difficulty_adapter_node(state: SessionState) -> dict:
    last_exchange = state["qa_history"][-1]

    model = get_chat_model(temperature=0.3)
    structured_model = model.with_structured_output(DifficultyAdjustment)

    prompt = DIFFICULTY_ADAPTER_SYSTEM_PROMPT.format(
        current_difficulty=state["current_difficulty"],
        question=last_exchange.question,
        answer=last_exchange.answer,
    )

    result: DifficultyAdjustment = structured_model.invoke(prompt)

    return {"current_difficulty": result.next_difficulty}