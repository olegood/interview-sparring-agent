"""FeedbackSuperAgent graph: critique + Sentinel review, with retry on rejection."""

from langgraph.graph import END, START, StateGraph

from interview_sparring_agent.agents.feedback_super_agent.sub_agents.answer_critiquer import (
    answer_critiquer_node,
)
from interview_sparring_agent.agents.sentinel.graph import (
    sentinel_review_node,
    should_retry_feedback,
)
from interview_sparring_agent.orchestration.state import SessionState


def build_feedback_graph():
    """Compile and return the FeedbackSuperAgent graph.

    If Sentinel rejects the feedback report (ungrounded quotes or
    index-coverage issues), the graph loops back to answer_critiquer for a
    fresh attempt - up to MAX_FEEDBACK_RETRIES times - before giving up.
    """
    builder = StateGraph(SessionState)
    builder.add_node("answer_critiquer", answer_critiquer_node)
    builder.add_node("sentinel_review", sentinel_review_node)

    builder.add_edge(START, "answer_critiquer")
    builder.add_edge("answer_critiquer", "sentinel_review")
    builder.add_conditional_edges(
        "sentinel_review",
        should_retry_feedback,
        {"retry": "answer_critiquer", "done": END},
    )

    return builder.compile()