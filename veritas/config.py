"""Veritas: Truth-first multi-agent AI system."""

from veritas.core import VeritasConfig, LLMClient, VeritasOrchestrator
from veritas.agents import PlannerAgent, ResearchAgent, VerifierAgent, SkepticAgent, WriterAgent

__version__ = "0.1.0"
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
