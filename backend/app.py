from flask import Flask, request, jsonify, render_template_string
import json
import os
import datetime

app = Flask(__name__)

DATA_FILE = "metrics.json"


# ---------------------------------------
# Receive Metrics
# ---------------------------------------
@app.route("/metrics", methods=["POST"])
def receive_metrics():
    data = request.json

    if not data:
        return jsonify({"error": "No data received"}), 400

    data["received_at"] = datetime.datetime.now(datetime.UTC).isoformat()

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    with open(DATA_FILE, "r+") as f:
        existing = json.load(f)
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=4)

    return jsonify({"status": "success"}), 200


# ---------------------------------------
# Serve Data to Dashboard
# ---------------------------------------
@app.route("/data", methods=["GET"])
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return jsonify(data[-30:])  # last 30 records


# ---------------------------------------
# Dashboard UI
# ---------------------------------------
@app.route("/dashboard")
def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Private Cloud Monitoring Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 40px;
            }
            h1 {
                text-align: center;
            }
            .chart-container {
                width: 80%;
                margin: 30px auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>

        <h1>Private Cloud Monitoring Dashboard</h1>

        <div class="chart-container">
            <canvas id="cpuChart"></canvas>
        </div>

        <div class="chart-container">
            <canvas id="memoryChart"></canvas>
        </div>

        <div class="chart-container">
            <canvas id="diskChart"></canvas>
        </div>

        <div class="chart-container">
            <canvas id="networkChart"></canvas>
        </div>

        <script>
            let cpuChart, memoryChart, diskChart, networkChart;

            async function fetchData() {
                const response = await fetch('/data');
                const data = await response.json();

                if (data.length === 0) return;

                const timestamps = data.map(d => {
                    const date = new Date(d.timestamp);
                    return date.toLocaleTimeString();
                });

                const cpuData = data.map(d => d.cpu_percent);
                const memoryData = data.map(d => d.memory_percent);
                const diskData = data.map(d => d.disk_percent);
                const networkData = data.map(d => d.network_bytes_recv);

                updateChart(cpuChart, timestamps, cpuData);
                updateChart(memoryChart, timestamps, memoryData);
                updateChart(diskChart, timestamps, diskData);
                updateChart(networkChart, timestamps, networkData);
            }

            function createChart(ctx, label) {
                return new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [{
                            label: label,
                            data: [],
                            borderWidth: 2,
                            tension: 0.3,
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        animation: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }

            function updateChart(chart, labels, data) {
                chart.data.labels = labels;
                chart.data.datasets[0].data = data;
                chart.update();
            }

            window.onload = function() {
                cpuChart = createChart(
                    document.getElementById('cpuChart').getContext('2d'),
                    'CPU Usage (%)'
                );

                memoryChart = createChart(
                    document.getElementById('memoryChart').getContext('2d'),
                    'Memory Usage (%)'
                );

                diskChart = createChart(
                    document.getElementById('diskChart').getContext('2d'),
                    'Disk Usage (%)'
                );

                networkChart = createChart(
                    document.getElementById('networkChart').getContext('2d'),
                    'Network Bytes Received'
                );

                fetchData();
                setInterval(fetchData, 5000);
            };
        </script>

    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
