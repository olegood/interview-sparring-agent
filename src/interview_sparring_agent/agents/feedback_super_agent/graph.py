"""FeedbackSuperAgent graph: single-pass critique + Sentinel groundedness review."""

from langgraph.graph import END, START, StateGraph

from interview_sparring_agent.agents.feedback_super_agent.sub_agents.answer_critiquer import (
    answer_critiquer_node,
)
from interview_sparring_agent.agents.sentinel.graph import sentinel_review_node
from interview_sparring_agent.orchestration.state import SessionState


def build_feedback_graph():
    """Compile and return the FeedbackSuperAgent graph, with Sentinel review
    as the final step before the report is considered complete.
    """
    builder = StateGraph(SessionState)
    builder.add_node("answer_critiquer", answer_critiquer_node)
    builder.add_node("sentinel_review", sentinel_review_node)

    builder.add_edge(START, "answer_critiquer")
    builder.add_edge("answer_critiquer", "sentinel_review")
    builder.add_edge("sentinel_review", END)

    return builder.compile()