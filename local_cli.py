#!/usr/bin/env python3
"""Direct CLI for offline Veritas using Ollama."""

import argparse
import sys

from veritas.local_client import LocalConfig, LocalModelError
from veritas.local_core import LocalVeritasOrchestrator


def main() -> int:
    parser = argparse.ArgumentParser(description="Veritas Local: private, offline, direct.")
    parser.add_argument("query", nargs="?", help="Question for Veritas")
    parser.add_argument("--model", help="Ollama model, e.g. llama3.1:8b")
    parser.add_argument("--show-all", action="store_true", help="Show every agent output")
    parser.add_argument("--verbose", action="store_true", help="Show pipeline progress")
    args = parser.parse_args()

    query = args.query or input("Ask Veritas Local: ").strip()
    if not query:
        print("Error: query cannot be empty.", file=sys.stderr)
        return 2

    config = LocalConfig.from_env()
    if args.model:
        config.model = args.model

    try:
        result = LocalVeritasOrchestrator(config).run(query, verbose=args.verbose)
    except LocalModelError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.show_all:
        for title, key in (("PLAN", "plan"), ("RESEARCH", "research"),
                           ("VERIFICATION", "verification"), ("SKEPTIC", "critique")):
            print(f"\n--- {title} ---\n{result[key]}")
    print(f"\n--- VERITAS ANSWER ---\n{result['answer']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
