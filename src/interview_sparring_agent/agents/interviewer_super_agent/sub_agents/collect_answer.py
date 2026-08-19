"""collect_answer sub-agent: pauses the graph and waits for the candidate's
typed answer via LangGraph's interrupt() human-in-the-loop mechanism.
"""

from langgraph.types import interrupt

from interview_sparring_agent.orchestration.state import QAExchange, SessionState


def collect_answer_node(state: SessionState) -> dict:
    """LangGraph node: ask the current question and pause for a human answer.

    interrupt() suspends graph execution here. The caller (CLI driver) must
    resume with Command(resume=<answer string>). The value passed to resume
    becomes this function's return value from interrupt().
    """
    answer: str = interrupt(
        {
            "question": state["current_question"],
            "difficulty": state["current_difficulty"],
        }
    )

    exchange = QAExchange(
        question=state["current_question"],
        answer=answer,
        difficulty=state["current_difficulty"],
    )

    return {
        "qa_history": [exchange],  # merged via the operator.add reducer
        "question_count": state["question_count"] + 1,
    }
