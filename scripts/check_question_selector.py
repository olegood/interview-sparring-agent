"""Manual check: generate a single interview question.

Run with: uv run python scripts/check_question_selector.py
"""

from interview_sparring_agent.agents.interviewer_super_agent.sub_agents.question_selector import (
    question_selector_node,
)
from interview_sparring_agent.orchestration.state import SessionState


def main() -> None:
    state: SessionState = {
        "role": "Backend Engineer",
        "level": "mid-level",
        "max_questions": 3,
        "phase": "interviewing",
        "current_question": None,
        "current_difficulty": "medium",
        "question_count": 0,
        "qa_history": [],
        "feedback_report": None,
    }

    update = question_selector_node(state)
    print("Generated question:", update["current_question"])


if __name__ == "__main__":
    main()