"""Flask web interface for Veritas."""

import os
import json
from flask import Flask, render_template, request, jsonify
from veritas.core import VeritasOrchestrator, VeritasConfig, TruthfulnessError

app = Flask(__name__, template_folder="templates", static_folder="templates")


@app.route("/", methods=["GET"])
def index():
    """Serve the web UI."""
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def query():
    """Process a query through Veritas."""
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "No query provided"}), 400

        user_query = data["query"].strip()
        show_all = data.get("show_all", False)

        if not user_query:
            return jsonify({"error": "Query cannot be empty"}), 400

        # Load config and run Veritas
        config = VeritasConfig.from_env()
        orchestrator = VeritasOrchestrator(config)
        result = orchestrator.run(user_query, verbose=False)

        response = {
            "query": user_query,
            "answer": result["answer"],
        }

        if show_all:
            response["details"] = {
                "plan": result["plan"],
                "research": result["evidence"],
                "verification": result["verification"],
                "skeptic": result["critique"],
            }

        return jsonify(response), 200

    except TruthfulnessError as e:
        return jsonify({"error": f"Configuration error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
