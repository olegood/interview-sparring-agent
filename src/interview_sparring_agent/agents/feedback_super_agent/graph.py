"""FeedbackSuperAgent graph: single-pass critique over a completed transcript."""

from langgraph.graph import END, START, StateGraph

from interview_sparring_agent.agents.feedback_super_agent.sub_agents.answer_critiquer import (
    answer_critiquer_node,
)
from interview_sparring_agent.orchestration.state import SessionState


def build_feedback_graph():
    """Compile and return the FeedbackSuperAgent graph.

    v1 is a single node - Sentinel review will be added as a second node
    in Stage 7, once the groundedness check exists.
    """
    builder = StateGraph(SessionState)
    builder.add_node("answer_critiquer", answer_critiquer_node)
    builder.add_edge(START, "answer_critiquer")
    builder.add_edge("answer_critiquer", END)
    return builder.compile()