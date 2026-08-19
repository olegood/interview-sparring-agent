"""InterviewerSuperAgent graph: runs the adaptive interview loop."""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from interview_sparring_agent.agents.interviewer_super_agent.sub_agents.collect_answer import (
    collect_answer_node,
)
from interview_sparring_agent.agents.interviewer_super_agent.sub_agents.difficulty_adapter import (
    difficulty_adapter_node,
)
from interview_sparring_agent.agents.interviewer_super_agent.sub_agents.question_selector import (
    question_selector_node,
)
from interview_sparring_agent.orchestration.state import SessionState


def _should_continue(state: SessionState) -> str:
    if state["question_count"] >= state["max_questions"]:
        return "done"
    return "continue"


def build_interviewer_graph():
    """Compile and return the InterviewerSuperAgent graph.

    Uses an in-memory checkpointer - required for interrupt()/resume to
    work, even though we don't persist sessions across process restarts.
    """
    builder = StateGraph(SessionState)

    builder.add_node("question_selector", question_selector_node)
    builder.add_node("collect_answer", collect_answer_node)
    builder.add_node("difficulty_adapter", difficulty_adapter_node)

    builder.add_edge(START, "question_selector")
    builder.add_edge("question_selector", "collect_answer")
    builder.add_edge("collect_answer", "difficulty_adapter")
    builder.add_conditional_edges(
        "difficulty_adapter",
        _should_continue,
        {"continue": "question_selector", "done": END},
    )

    return builder.compile(checkpointer=MemorySaver())