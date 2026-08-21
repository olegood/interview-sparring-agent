"""Manual check: run FeedbackSuperAgent over a hand-built transcript.

Run with: uv run python scripts/check_feedback_agent.py
"""

from interview_sparring_agent.agents.feedback_super_agent.graph import (
    build_feedback_graph,
)
from interview_sparring_agent.orchestration.state import QAExchange, SessionState


def main() -> None:
    state: SessionState = {
        "role": "Backend Engineer",
        "level": "mid-level",
        "max_questions": 2,
        "phase": "interviewing",
        "current_question": None,
        "current_difficulty": "medium",
        "question_count": 2,
        "qa_history": [
            QAExchange(
                question="Tell me about a time you debugged a hard production issue.",
                answer="idk, I guess I just looked at the logs and kind of found it eventually.",
                difficulty="medium",
            ),
            QAExchange(
                question="How would you design a rate limiter for an API?",
                answer=(
                    "I'd use a token bucket algorithm stored in Redis, with each "
                    "client getting a bucket that refills at a fixed rate. This "
                    "handles bursts well while enforcing an average rate limit."
                ),
                difficulty="medium",
            ),
        ],
        "feedback_report": None,
    }

    graph = build_feedback_graph()
    result = graph.invoke(state)

    report = result["feedback_report"]
    print("=== Overall summary ===")
    print(report.overall_summary)

    print("\n=== Sentinel review ===")
    print("Approved:", report.sentinel_approved)
    print("Notes:", report.sentinel_notes)

    for item in report.items:
        print(f"\n--- Feedback for Q{item.exchange_index} ---")
        print("Critique:", item.critique)
        print("STAR used:", item.used_star_method)
        print("Filler words:", item.filler_words_flagged)
        print("Grounding quotes:", item.grounding_quotes)


if __name__ == "__main__":
    main()