# Veritas

Veritas is a multi-agent AI system built around a simple principle: tell the truth, or say you do not know.

It is intentionally direct, skeptical, and unflattering when necessary. It is not a sycophant. It does not invent certainty. It calls out weak assumptions, missing evidence, and bad decisions.

This repo contains a working starter implementation with:
- a direct command-line interface (CLI)
- a minimal web UI
- multi-agent orchestration
- support for cloud LLMs and an offline local-only mode

## What Veritas does

Veritas runs a pipeline of specialized agents:

1. Planner
   - breaks the problem into tasks
   - identifies risks and missing facts
2. Researcher
   - gathers relevant evidence
   - distinguishes facts from guesses
3. Verifier
   - checks claims for consistency and logic
4. Skeptic
   - attacks the plan from the weak side
   - exposes blind spots
5. Writer
   - synthesizes the final answer into a clear, actionable response

The result is a blunt but useful answer: direct, honest, not overconfident.

## Why the name Veritas

Veritas means truth in Latin. That is the spirit of the project:
- no fake praise
- no false certainty
- no shallow reassurance
- no pretending to know what is not known

## Repository structure

- `veritas/` — agent system and core logic
- `cli.py` — terminal interface
- `web.py` — Flask web app for cloud-based usage
- `requirements.txt` — Python dependencies for cloud mode
- `.env.example` — environment variables
- `README.md` — project documentation
- `local_cli.py` and `local_web.py` — offline local-model version available on the `local-llm` branch

## Quick start: cloud version

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

4. Copy the example env file and add your keys

```bash
cp .env.example .env
```

Then set one of these in your shell or `.env`:

```bash
export VERITAS_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_key_here
```

or

```bash
export VERITAS_PROVIDER=openai
export OPENAI_API_KEY=your_key_here
```

5. Run the CLI

```bash
python cli.py "Should I pivot my startup into AI?"
```

6. Run the web UI

```bash
python web.py
```

Then open:

```text
http://localhost:5000
```

## Quick start: local/offline version

The offline model version lives on the `local-llm` branch.

You need Ollama installed locally.

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

6. Run the local web UI

```bash
python local_web.py
```

Then open:

```text
http://127.0.0.1:5001
```

## Example usage

### CLI

```bash
python cli.py "How should I evaluate this startup idea?"
```

### Web UI

Open the app and type a question like:
- Is this product idea real?
- Should I hire before I validate?
- What are the biggest risks in this plan?
- Is this strategy likely to work?

## Environment variables

### Cloud version

```bash
VERITAS_PROVIDER=anthropic
VERITAS_MODEL=claude-3-5-sonnet-20241022
VERITAS_TEMPERATURE=0.2
VERITAS_MAX_TOKENS=1500
ANTHROPIC_API_KEY=...
```

or

```bash
VERITAS_PROVIDER=openai
VERITAS_MODEL=gpt-4o-mini
VERITAS_TEMPERATURE=0.2
VERITAS_MAX_TOKENS=1500
OPENAI_API_KEY=...
```

### Local version

```bash
VERITAS_LOCAL_MODEL=llama3.1:8b
OLLAMA_HOST=http://127.0.0.1:11434
VERITAS_TEMPERATURE=0.2
VERITAS_MAX_TOKENS=1200
```

## How to use it well

Ask direct questions. Veritas works best when you want a real answer, not a comforting one.

Good prompts:
- Should I launch this product now?
- What is the biggest risk in this plan?
- Is this business model credible?
- What would make this fail?
- What are the assumptions I am relying on?

Bad prompts:
- Tell me I am doing great
- Give me a motivational answer
- Be vague and positive

Veritas is designed for honesty. If evidence is weak, it says so. If the answer is uncertain, it says so.

## Philosophy

Veritas is not trying to impress you.
It is trying to help you make better decisions.

If the idea is weak, it will say the idea is weak.
If the facts are missing, it will say the facts are missing.
If the path is uncertain, it will say the path is uncertain.

That is the point.

## License

MIT

## Author

slavik-beretta
