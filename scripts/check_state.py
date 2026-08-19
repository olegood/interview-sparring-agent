from interview_sparring_agent.orchestration.state import SessionState, QAExchange

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

exchange = QAExchange(question="Tell me about a time you debugged a hard issue.", answer="...")
print(exchange.model_dump())
print(state["phase"])