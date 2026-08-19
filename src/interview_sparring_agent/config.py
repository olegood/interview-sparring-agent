"""Application configuration loaded from environment variables / .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Flat application settings.

    All values can be overridden via environment variables or a `.env` file
    in the project root. See `.env.example` for the full list.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Ollama / local LLM ---
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    # --- LangSmith / LangChain tracing ---
    langchain_api_key: str | None = None
    langchain_tracing_v2: bool = False
    langchain_project: str = "interview-sparring-agent"


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton Settings instance."""
    return Settings()
