"""Factory for constructing ChatOllama model instances."""

from langchain_ollama import ChatOllama

from interview_sparring_agent.config import get_settings


class OllamaConnectionError(RuntimeError):
    """Raised when the local Ollama server can't be reached."""


def get_chat_model(model: str | None = None, temperature: float = 0.7) -> ChatOllama:
    """Return a ChatOllama instance.

    Args:
        model: Ollama model name/tag to use. Defaults to settings.ollama_model.
        temperature: Sampling temperature.

    Raises:
        OllamaConnectionError: if the model can't be reached at invoke time
            (the error is only detected on first call, since ChatOllama
            doesn't eagerly connect on construction).
    """
    settings = get_settings()
    resolved_model = model or settings.ollama_model

    return ChatOllama(
        model=resolved_model,
        base_url=settings.ollama_host,
        temperature=temperature,
    )


def check_connection() -> None:
    """Raise OllamaConnectionError with a clear message if Ollama is unreachable."""
    settings = get_settings()
    try:
        model = get_chat_model()
        model.invoke("ping")
    except Exception as exc:  # noqa: BLE001 - we want to wrap any connection failure
        raise OllamaConnectionError(
            f"Could not reach Ollama at {settings.ollama_host}. "
            f"Is it running? Try `ollama serve` and confirm OLLAMA_HOST is correct."
        ) from exc
