#!/usr/bin/env python3
"""Local Veritas web UI. Uses Ollama; no cloud API is required."""

from flask import Flask, jsonify, render_template, request

from veritas.local_client import LocalConfig, LocalModelError
from veritas.local_core import LocalVeritasOrchestrator

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/query")
def query():
    body = request.get_json(silent=True) or {}
    text = str(body.get("query", "")).strip()
    if not text:
        return jsonify(error="Query cannot be empty."), 400

    try:
        result = LocalVeritasOrchestrator(LocalConfig.from_env()).run(text)
    except LocalModelError as exc:
        return jsonify(error=str(exc)), 503
    return jsonify(query=text, answer=result["answer"], details={
        "plan": result["plan"],
        "research": result["research"],
        "verification": result["verification"],
        "skeptic": result["critique"],
    })


if __name__ == "__main__":
    print("Veritas Local: http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
