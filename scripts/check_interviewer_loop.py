"""Manual check: run a full interactive interview loop via the terminal.

Run with: uv run python scripts/check_interviewer_loop.py
"""

from langgraph.types import Command

from interview_sparring_agent.agents.interviewer_super_agent.graph import (
    build_interviewer_graph,
)
from interview_sparring_agent.orchestration.state import SessionState


def main() -> None:
    graph = build_interviewer_graph()

    initial_state: SessionState = {
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

    config = {"configurable": {"thread_id": "check-session-1"}}

    result = graph.invoke(initial_state, config=config)

    while "__interrupt__" in result:
        payload = result["__interrupt__"][0].value
        answer = input(f"\n[{payload['difficulty']}] {payload['question']}\n> ")
        result = graph.invoke(Command(resume=answer), config=config)

    print("\n--- Interview complete ---")
    for i, exchange in enumerate(result["qa_history"], start=1):
        print(f"\nQ{i} ({exchange.difficulty}): {exchange.question}")
        print(f"A{i}: {exchange.answer}")


if __name__ == "__main__":
    main()