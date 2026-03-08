from flask import Flask, jsonify, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

METRICS_FILE = "metrics.json"


# Ensure metrics file exists
if not os.path.exists(METRICS_FILE):
    with open(METRICS_FILE, "w") as f:
        json.dump([], f)


@app.route("/")
def home():
    return "Private Cloud Monitoring Backend Running"


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/metrics", methods=["POST"])
def receive_metrics():

    data = request.json

    data["received_at"] = datetime.utcnow().isoformat()

    with open(METRICS_FILE, "r") as f:
        metrics = json.load(f)

    metrics.append(data)

    # keep last 1000 records
    metrics = metrics[-1000:]

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    return jsonify({"status": "ok"}), 200


@app.route("/data")
def get_data():

    with open(METRICS_FILE, "r") as f:
        metrics = json.load(f)

    return jsonify(metrics)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
