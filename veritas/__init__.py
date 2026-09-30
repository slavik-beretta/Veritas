"""Veritas: Truth-first multi-agent AI system."""

from veritas.config import VeritasConfig
from veritas.core import LLMClient, VeritasOrchestrator
from veritas.agents import PlannerAgent, ResearchAgent, VerifierAgent, SkepticAgent, WriterAgent

__version__ = "0.2.0"
__all__ = [
    "VeritasConfig",
    "LLMClient",
    "VeritasOrchestrator",
    "PlannerAgent",
    "ResearchAgent",
    "VerifierAgent",
    "SkepticAgent",
    "WriterAgent",
]
