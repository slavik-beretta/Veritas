# Veritas Local (no API required)

This branch runs Veritas against a model on your own computer through [Ollama](https://ollama.com/). Your prompts and responses are sent to the local Ollama server, not to Anthropic or OpenAI. Internet is only needed once to install Ollama and download a model.

## Setup

Install Ollama, then download a model:

```bash
ollama serve
ollama pull llama3.1:8b
```

`qwen2.5:7b` is another reasonable option for machines with less memory. Set a different model with `VERITAS_LOCAL_MODEL` or `--model`.

Create an environment and install only local dependencies:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements-local.txt
```

## Local CLI

```bash
python local_cli.py "Is this business idea worth pursuing?"
python local_cli.py --show-all "What are the risks of my plan?"
python local_cli.py --model qwen2.5:7b "Be direct about this decision."
```

## Local web UI

```bash
python local_web.py
```

Open `http://127.0.0.1:5001`. The existing `templates/index.html` is reused, so the UI stays consistent with the cloud version.

## Configuration

Optional environment variables:

```bash
export VERITAS_LOCAL_MODEL=llama3.1:8b
export OLLAMA_HOST=http://127.0.0.1:11434
export VERITAS_TEMPERATURE=0.2
export VERITAS_MAX_TOKENS=1200
export VERITAS_LOCAL_TIMEOUT=180
```

## Limitations

This is private and local, but it is not automatically as capable as a hosted frontier model. Five sequential agent calls are also slower and consume more local compute than one call. The local researcher has no web access; it can only use its model's training knowledge and the information in the prompt. It should therefore say when something is unknown rather than pretending to have current evidence.
