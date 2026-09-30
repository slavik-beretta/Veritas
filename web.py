#!/usr/bin/env python3
"""Command-line interface for Veritas."""

import sys
import argparse
from veritas.core import VeritasOrchestrator, VeritasConfig, TruthfulnessError


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_agent_output(agent_name: str, output: str):
    """Print output from an agent."""
    print(f"\n[{agent_name.upper()}]")
    print("-" * 70)
    print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Veritas: Direct, honest, and skeptical multi-agent AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "Should I pivot my startup?"
  python cli.py --verbose "What are the risks of AI agents?"
  python cli.py --show-all "How do I scale a team?"
        """,
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Query to ask Veritas",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show agent execution as it happens",
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show output from all agents, not just final answer",
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        help="LLM provider (overrides env var)",
    )
    parser.add_argument(
        "--model",
        help="Model name (overrides env var)",
    )

    args = parser.parse_args()

    # Get query
    if args.query:
        query = args.query
    else:
        print("\nVeritas — Direct. Honest. Skeptical.")
        print("-" * 70)
        try:
            query = input("Ask Veritas: ").strip()
        except KeyboardInterrupt:
            print("\n\nInterrupted.")
            sys.exit(0)

    if not query:
        print("Error: No query provided.")
        sys.exit(1)

    # Setup config
    try:
        config = VeritasConfig.from_env()
        if args.provider:
            config.provider = args.provider
        if args.model:
            config.model = args.model

        print("\nVeritas — Direct. Honest. Skeptical.")
        print("-" * 70)
        if args.verbose:
            print(f"Query: {query}")
            print(f"Provider: {config.provider}")
            print(f"Model: {config.model}")

        orchestrator = VeritasOrchestrator(config)
        result = orchestrator.run(query, verbose=args.verbose)

        if args.show_all:
            print_agent_output("Plan", result["plan"])
            print_agent_output("Research", result["evidence"])
            print_agent_output("Verification", result["verification"])
            print_agent_output("Skeptic", result["critique"])

        print_section("VERITAS ANSWER")
        print(result["answer"])
        print()

    except TruthfulnessError as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Set API keys in .env file (copy .env.example first)")
        print("3. Run: cp .env.example .env")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
