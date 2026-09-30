"""Offline Ollama client for Veritas.

Requires Ollama running locally. No cloud API key is used.
"""

from dataclasses import dataclass
from typing import Optional

import requests


class LocalModelError(RuntimeError):
    """Raised when the local model cannot be reached or returns an invalid response."""


@dataclass
class LocalConfig:
    model: str = "llama3.1:8b"
    base_url: str = "http://127.0.0.1:11434"
    temperature: float = 0.2
    max_tokens: int = 1200
    timeout: int = 180

    @classmethod
    def from_env(cls) -> "LocalConfig":
        import os

        return cls(
            model=os.getenv("VERITAS_LOCAL_MODEL", "llama3.1:8b"),
            base_url=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/"),
            temperature=float(os.getenv("VERITAS_TEMPERATURE", "0.2")),
            max_tokens=int(os.getenv("VERITAS_MAX_TOKENS", "1200")),
            timeout=int(os.getenv("VERITAS_LOCAL_TIMEOUT", "180")),
        )


class LocalLLMClient:
    """LLM client compatible with Veritas agents, backed by Ollama."""

    def __init__(self, config: Optional[LocalConfig] = None):
        self.config = config or LocalConfig.from_env()

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        prompt = f"""System instructions:
{system_prompt}

User/task:
{user_prompt}

Answer according to the system instructions. Do not invent facts."""
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        }
        try:
            response = requests.post(
                f"{self.config.base_url}/api/generate",
                json=payload,
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise LocalModelError(
                "Could not reach Ollama. Start it with `ollama serve`, then pull a model "
                f"with `ollama pull {self.config.model}`. Details: {exc}"
            ) from exc

        answer = data.get("response")
        if not isinstance(answer, str) or not answer.strip():
            raise LocalModelError("Ollama returned no usable response.")
        return answer.strip()

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.config.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = [m.get("name") for m in response.json().get("models", [])]
            return self.config.model in models or self.config.model.split(":")[0] in models
        except requests.RequestException:
            return False
