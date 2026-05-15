"""
Counter Service

A simple REST API for managing named counters backed by a Python dictionary.
"""
import logging
from flask import Flask, jsonify, abort

app = Flask(__name__)

COUNTERS = {}


@app.route("/")
def index():
    """Health check endpoint."""
    return jsonify(status="OK", service="Counter Service"), 200


@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Create a new counter with an initial value of 0."""
    if name in COUNTERS:
        return jsonify(error=f"Counter '{name}' already exists"), 409
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), 201


@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """Return the current value of a counter."""
    if name not in COUNTERS:
        abort(404)
    return jsonify({name: COUNTERS[name]}), 200


@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Increment a counter by 1."""
    if name not in COUNTERS:
        abort(404)
    COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), 200


@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """Delete a counter."""
    if name not in COUNTERS:
        abort(404)
    del COUNTERS[name]
    return "", 204


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("SERVICERUNNING")
    app.run(host="0.0.0.0", port=8000)
