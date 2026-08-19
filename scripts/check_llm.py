"""Quick manual check that config + Ollama connection work end to end.

Run with: uv run python scripts/check_llm.py
"""

from interview_sparring_agent.llm.ollama_client import get_chat_model


def main() -> None:
    model = get_chat_model()
    response = model.invoke("Say hello in one sentence.")
    print(response.content)


if __name__ == "__main__":
    main()