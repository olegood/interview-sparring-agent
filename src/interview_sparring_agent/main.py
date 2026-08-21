"""CLI entrypoint for the interview sparring agent."""

from interview_sparring_agent.orchestration.router import run_full_session


def _cli_get_answer(payload: dict) -> str:
    question = payload["question"]
    difficulty = payload["difficulty"]
    return input(f"\n[{difficulty}] {question}\n> ")


def main() -> None:
    print("=== Interview Sparring Agent ===\n")
    role = input("Role you're interviewing for (e.g. 'Backend Engineer'): ").strip()
    level = input("Level (e.g. 'junior', 'mid-level', 'senior'): ").strip()
    max_questions_raw = input("Number of questions (default 3): ").strip()
    max_questions = int(max_questions_raw) if max_questions_raw else 3

    result = run_full_session(
        role=role,
        level=level,
        max_questions=max_questions,
        get_answer=_cli_get_answer,
    )

    report = result["feedback_report"]

    print("\n\n=== Session Complete ===")
    print(f"\nOverall summary:\n{report.overall_summary}")

    print(f"\nSentinel approved: {report.sentinel_approved}")
    retry_count = result.get("feedback_retry_count", 0)
    if retry_count:
        print(f"(Feedback was regenerated {retry_count} time(s) after Sentinel rejection)")
    if not report.sentinel_approved:
        print(f"Sentinel notes: {report.sentinel_notes}")
        print("Note: some feedback below may be unreliable - see notes above.")

    for item in report.items:
        exchange = result["qa_history"][item.exchange_index]
        print(f"\n--- Q{item.exchange_index} ({exchange.difficulty}) ---")
        print(f"Q: {exchange.question}")
        print(f"A: {exchange.answer}")
        print(f"Feedback: {item.critique}")
        if item.filler_words_flagged:
            print(f"Filler words: {', '.join(item.filler_words_flagged)}")


if __name__ == "__main__":
    main()