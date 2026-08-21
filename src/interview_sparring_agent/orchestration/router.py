"""Top-level session orchestration: chains InterviewerSuperAgent and
FeedbackSuperAgent into one continuous session.

Kept transport-agnostic - callers supply an `AnswerProvider` callback to
collect answers, so this module doesn't care whether answers come from a
CLI, a web form, or a test harness.
"""

from typing import Callable

from langgraph.types import Command

from interview_sparring_agent.agents.feedback_super_agent.graph import (
    build_feedback_graph,
)
from interview_sparring_agent.agents.interviewer_super_agent.graph import (
    build_interviewer_graph,
)
from interview_sparring_agent.orchestration.state import SessionState

# Called with the interrupt payload ({"question": ..., "difficulty": ...})
# and must return the candidate's answer as a string.
AnswerProvider = Callable[[dict], str]


def run_interview_phase(
        role: str,
        level: str,
        max_questions: int,
        get_answer: AnswerProvider,
        thread_id: str = "session-1",
) -> SessionState:
    """Run the interviewer loop to completion.

    Repeatedly invokes the graph and, whenever it pauses via interrupt(),
    calls get_answer() to collect the candidate's response and resumes.
    """
    graph = build_interviewer_graph()

    initial_state: SessionState = {
        "role": role,
        "level": level,
        "max_questions": max_questions,
        "phase": "interviewing",
        "current_question": None,
        "current_difficulty": "medium",
        "question_count": 0,
        "qa_history": [],
        "feedback_report": None,
        "feedback_retry_count": 0,
    }

    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(initial_state, config=config)

    while "__interrupt__" in result:
        payload = result["__interrupt__"][0].value
        answer = get_answer(payload)
        result = graph.invoke(Command(resume=answer), config=config)

    return result


def run_feedback_phase(interview_result: SessionState) -> SessionState:
    """Run FeedbackSuperAgent (including Sentinel review) over a completed
    interview transcript.
    """
    graph = build_feedback_graph()
    return graph.invoke(interview_result)


def run_full_session(
        role: str,
        level: str,
        max_questions: int,
        get_answer: AnswerProvider,
        thread_id: str = "session-1",
) -> SessionState:
    """Run a complete session end to end: interview loop, then feedback pass."""
    interview_result = run_interview_phase(
        role, level, max_questions, get_answer, thread_id
    )
    return run_feedback_phase(interview_result)
