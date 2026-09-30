# Veritas

Veritas is a multi-agent AI system designed around one rule: tell the truth, or say you do not know.

It is direct. It is skeptical. It does not flatter. It does not fake certainty. If the idea is weak, it says so. If the evidence is thin, it says so. If the answer is uncertain, it says so.

This repository contains a working multi-agent system with:
- a command-line interface
- a minimal web UI
- cloud LLM support
- a local/offline mode

## The idea

Veritas runs a set of specialized agents in sequence:

1. Planner
   - breaks the problem into tasks
   - identifies missing facts and obvious risks
2. Researcher
   - gathers useful evidence
   - separates facts from guesses
3. Verifier
   - checks consistency and logic
4. Skeptic
   - attacks the idea and exposes weak assumptions
5. Writer
   - produces the final answer in a direct, useful format

The result is a blunt but useful answer. Not fluff. Not fake confidence. Just the truth.

## Why "Veritas"

Veritas means truth in Latin. The project is intentionally honest:
- no fake praise
- no fake certainty
- no comforting nonsense
- no pretending to know things you do not know

## Cloud version: how to run

1. Clone the repo

```bash
git clone https://github.com/slavik-beretta/Veritas.git
cd Veritas
```

2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Copy the example environment file

```bash
cp .env.example .env
```

5. Add your API key

For Anthropic:

```bash
export VERITAS_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_key_here
```

For OpenAI:

```bash
export VERITAS_PROVIDER=openai
export OPENAI_API_KEY=your_key_here
```

6. Run the CLI

```bash
python cli.py "Should I pivot my startup into AI?"
```

7. Or run the web app

```bash
python web.py
```

Then open:

```text
http://localhost:5000
```

## Local/offline version: how to run

This version is on the `local-llm` branch.

1. Install Ollama
   - https://ollama.com/

2. Pull a model

```bash
ollama serve
ollama pull llama3.1:8b
```

3. Switch to the local branch

```bash
git checkout local-llm
```

4. Install local dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-local.txt
```

5. Run the local CLI

```bash
python local_cli.py "Is this idea worth pursuing?"
```

6. Or run the local web app

```bash
python local_web.py
```

Then open:

```text
http://127.0.0.1:5001
```

## Good questions to ask Veritas

Use direct questions. This system works best when you want a real answer.

Examples:
- Should I launch this product now?
- What is the biggest risk in this plan?
- Is this business model credible?
- What assumptions am I relying on?
- What would make this fail?
- Is this team structure realistic?

## What not to ask

Avoid vague or emotional prompts like:
- Tell me I am doing great
- Be encouraging
- Make this sound good

Veritas is not here to flatter you. It is here to help you think better.

## Repo layout

- `veritas/` — core logic and agent classes
- `cli.py` — cloud CLI
- `web.py` — cloud web UI
- `local_cli.py` — local/offline CLI
- `local_web.py` — local/offline web UI
- `requirements.txt` — cloud dependencies
- `requirements-local.txt` — local/offline dependencies
- `README.md` — main setup guide
- `LOCAL.md` — local-only quick guide
- `.env.example` — environment template

## Philosophy

Veritas is built on a single idea:

Truth is more useful than comfort.

If the answer is uncertain, it says so.
If the evidence is weak, it says so.
If the plan is bad, it says so.
If the idea is good, it explains why.

That is the point.

## License

MIT
