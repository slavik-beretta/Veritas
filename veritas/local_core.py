"""Local-only Veritas orchestrator using Ollama."""

from typing import Optional

from veritas.agents import (
    PlannerAgent,
    ResearchAgent,
    VerifierAgent,
    SkepticAgent,
    WriterAgent,
)
from veritas.local_client import LocalConfig, LocalLLMClient


class LocalVeritasOrchestrator:
    """Run the complete Veritas pipeline without a cloud API."""

    def __init__(self, config: Optional[LocalConfig] = None):
        self.config = config or LocalConfig.from_env()
        self.llm = LocalLLMClient(self.config)
        self.planner = PlannerAgent(self.llm)
        self.research = ResearchAgent(self.llm)
        self.verifier = VerifierAgent(self.llm)
        self.skeptic = SkepticAgent(self.llm)
        self.writer = WriterAgent(self.llm)

    def run(self, query: str, verbose: bool = False) -> dict:
        def step(label: str):
            if verbose:
                print(f"[{label}]")

        step("Planner")
        plan = self.planner.run(query)
        step("Researcher")
        research = self.research.run(f"User query:\n{query}\n\nPlan:\n{plan}")
        step("Verifier")
        verification = self.verifier.run(f"User query:\n{query}\n\nResearch:\n{research}")
        step("Skeptic")
        critique = self.skeptic.run(
            f"User query:\n{query}\n\nResearch:\n{research}\n\nVerification:\n{verification}"
        )
        step("Writer")
        answer = self.writer.run(
            f"User query:\n{query}\n\nPlan:\n{plan}\n\nResearch:\n{research}"
            f"\n\nVerification:\n{verification}\n\nSkeptic critique:\n{critique}"
        )
        return {
            "query": query,
            "plan": plan,
            "research": research,
            "verification": verification,
            "critique": critique,
            "answer": answer,
        }
