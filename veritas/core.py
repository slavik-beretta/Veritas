"""Configuration for Veritas."""

import os
from dataclasses import dataclass


@dataclass
class VeritasConfig:
    """Configuration for Veritas system."""

    model: str = "claude-3-5-sonnet-20241022"
    provider: str = "anthropic"  # "anthropic" or "openai"
    max_tokens: int = 1500
    temperature: float = 0.2

    @staticmethod
    def from_env() -> "VeritasConfig":
        """Load configuration from environment variables."""
        provider = os.getenv("VERITAS_PROVIDER", "anthropic").lower()
        model = os.getenv(
            "VERITAS_MODEL",
            "claude-3-5-sonnet-20241022" if provider == "anthropic" else "gpt-4o-mini",
        )
        max_tokens = int(os.getenv("VERITAS_MAX_TOKENS", "1500"))
        temperature = float(os.getenv("VERITAS_TEMPERATURE", "0.2"))
        return VeritasConfig(
            model=model, provider=provider, max_tokens=max_tokens, temperature=temperature
        )
