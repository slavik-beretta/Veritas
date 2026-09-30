"""Core Veritas LLM client and orchestrator."""

import os
from typing import Optional
from veritas.config import VeritasConfig

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class TruthfulnessError(Exception):
    """Raised when Veritas cannot guarantee truthfulness."""

    pass


class LLMClient:
    """Unified LLM client for Anthropic and OpenAI."""

    def __init__(self, config: Optional[VeritasConfig] = None):
        if config is None:
            config = VeritasConfig.from_env()

        self.config = config
        self.client = None

        if config.provider == "anthropic":
            if Anthropic is None:
                raise TruthfulnessError("Anthropic SDK not installed. Run: pip install anthropic")
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise TruthfulnessError("ANTHROPIC_API_KEY is missing.")
            self.client = Anthropic(api_key=api_key)

        elif config.provider == "openai":
            if OpenAI is None:
                raise TruthfulnessError("OpenAI SDK not installed. Run: pip install openai")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise TruthfulnessError("OPENAI_API_KEY is missing.")
            self.client = OpenAI(api_key=api_key)

        else:
            raise TruthfulnessError(f"Unsupported provider: {config.provider}")

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Get LLM completion."""
        if self.config.provider == "anthropic":
            resp = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return resp.content[0].text

        if self.config.provider == "openai":
            resp = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return resp.choices[0].message.content

        raise TruthfulnessError("No supported provider available")


class VeritasOrchestrator:
    """Orchestrates all Veritas agents."""

    def __init__(self, config: Optional[VeritasConfig] = None, llm: Optional[LLMClient] = None):
        if llm is None:
            if config is None:
                config = VeritasConfig.from_env()
            llm = LLMClient(config)

        self.llm = llm
        self.config = config or VeritasConfig.from_env()

        # Import agents here to avoid circular import
        from veritas.agents import (
            PlannerAgent,
            ResearchAgent,
            VerifierAgent,
            SkepticAgent,
            WriterAgent,
        )

        self.planner = PlannerAgent(llm)
        self.research = ResearchAgent(llm)
        self.verifier = VerifierAgent(llm)
        self.skeptic = SkepticAgent(llm)
        self.writer = WriterAgent(llm)

    def run(self, user_query: str, verbose: bool = False) -> dict:
        """Run Veritas on a user query.

        Returns:
            Dict with keys: query, plan, evidence, verification, critique, answer, steps
        """
        if verbose:
            print("[Planner] Breaking down the query...")
        plan = self.planner.run(user_query)

        if verbose:
            print("[Researcher] Gathering evidence...")
        evidence = self.research.run(
            f"""
User query:
{user_query}

Plan:
{plan}
"""
        )

        if verbose:
            print("[Verifier] Checking consistency...")
        verification = self.verifier.run(
            f"""
User query:
{user_query}

Evidence:
{evidence}
"""
        )

        if verbose:
            print("[Skeptic] Finding weak points...")
        critique = self.skeptic.run(
            f"""
User query:
{user_query}

Evidence:
{evidence}

Verification:
{verification}
"""
        )

        if verbose:
            print("[Writer] Synthesizing final answer...")
        final = self.writer.run(
            f"""
User query:
{user_query}

Plan:
{plan}

Evidence:
{evidence}

Verification:
{verification}

Critique:
{critique}
"""
        )

        return {
            "query": user_query,
            "plan": plan,
            "evidence": evidence,
            "verification": verification,
            "critique": critique,
            "answer": final,
            "steps": ["Plan", "Research", "Verify", "Critique", "Synthesize"],
        }
