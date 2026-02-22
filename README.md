Private Cloud Monitoring System

Custom CloudWatch-Like Telemetry Agent for Private Cloud Environments

 Overview

This project implements a custom CloudWatch-like monitoring system designed for private cloud environments where managed monitoring services (such as AWS CloudWatch) are unavailable.

The system includes:

A lightweight telemetry agent running as a background Linux service

A centralized monitoring backend (REST API)

Persistent structured metric storage

A live web dashboard with real-time visualization

Production-style daemonization using systemd

This forms the Telemetry and Visualization Layer of a predictive FinOps architecture.

<img width="503" height="261" alt="dashboard-overview png" src="https://github.com/user-attachments/assets/b6df1f41-1b74-4c69-b67b-7cdc27502b29" />
<img width="1240" height="626" alt="network-bytes" src="https://github.com/user-attachments/assets/ec3fee13-5679-4fa1-ad45-dc1497ecbb92" />
<img width="861" height="438" alt="memory-used" src="https://github.com/user-attachments/assets/3b2f2c35-2851-46ad-acd4-efeb307ffd01" />
<img width="499" height="222" alt="linux-service" src="https://github.com/user-attachments/assets/363fb4d7-3ca3-4916-ac0c-53f67d6a554e" />
<img width="395" height="477" alt="json" src="https://github.com/user-attachments/assets/47a095a5-d53a-49cf-a270-8eb429860b02" />


 Problem Statement

Public cloud providers offer managed monitoring tools such as AWS CloudWatch. However, private cloud environments lack:

Managed telemetry collection

Centralized metric aggregation

Automated resource insight pipelines

FinOps-aligned cost intelligence hooks

This project recreates core monitoring capabilities in a cloud-agnostic, provider-independent manner, providing raw telemetry natively without relying on external vendor lock-in.

 System Architecture

+-------------------------+
|     Private Compute     |
|        Instance         |
|                         |
|     Telemetry Agent     |
|    (systemd service)    |
+----------+--------------+
           |
           | HTTP POST (JSON)
           v
+-------------------------+
|   Monitoring Backend    |
|                         |
|     Flask REST API      |
|    /metrics endpoint    |
|   Persistent Storage    |
+----------+--------------+
           |
           | HTTP GET (JSON)
           v
+-------------------------+
|      Web Dashboard      |
|   (Chart.js + Flask)    |
+-------------------------+


⚙️ Components

1. Telemetry Agent

Collects:

CPU utilization (%)

Memory utilization (%)

Disk utilization (%)

Network bytes sent/received

Retrieves instance identity via IMDSv2.

Generates UTC timezone-aware timestamps.

Sends JSON payload every 5 seconds.

Runs as a systemd background service.

Automatically restarts on failure.

2️. Monitoring Backend

Built using Flask.

Exposes REST endpoint: /metrics.

Accepts structured JSON telemetry.

Appends records to persistent storage (metrics.json).

Adds server-side received_at timestamp.

Exposes /data endpoint for dashboard.

Runs as a systemd daemon.

3️. Dashboard Layer

Built with Chart.js.

Auto-refresh every 5 seconds.

Displays: CPU Usage, Memory Usage, Disk Usage, Network Activity.

Clean and responsive UI.

Accessible via: http://<public-ip>:5000/dashboard

-> Deployment Instructions

Prerequisites

Ubuntu Server 22.04+

Python 3.x

Git

Open firewall ports:

22 (SSH)

5000 (Dashboard / API)

1. Clone Repository

git clone [https://github.com/](https://github.com/)pranyth/private-cloud-monitoring.git
cd private-cloud-monitoring


2. Install Dependencies

Agent Setup:

cd agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Backend Setup:

cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


3. Run in Development Mode

Run Backend:

# In the backend directory
python app.py


Run Agent:

# In the agent directory
python agent.py


🛠 Production Deployment (systemd)

To ensure the services run autonomously, survive reboots, and restart on failure, deploy them using systemd.

Agent Service

Create the service file: /etc/systemd/system/private-cw-agent.service

[Unit]
Description=Private CloudWatch Agent
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/private-cloud-monitoring/agent
ExecStart=/home/ubuntu/private-cloud-monitoring/agent/venv/bin/python agent.py
Restart=always

[Install]
WantedBy=multi-user.target


Enable and start the agent:

sudo systemctl daemon-reload
sudo systemctl enable private-cw-agent
sudo systemctl start private-cw-agent


Backend Service

Create the service file: /etc/systemd/system/monitoring-backend.service

[Unit]
Description=Private Cloud Monitoring Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/private-cloud-monitoring/backend
ExecStart=/home/ubuntu/private-cloud-monitoring/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target


Enable and start the backend:

sudo systemctl daemon-reload
sudo systemctl enable monitoring-backend
sudo systemctl start monitoring-backend


 Dashboard Preview

(Add screenshots here after capturing from your browser)

🔐 Secure Instance Identification (IMDSv2)

The agent securely retrieves instance identity using AWS IMDSv2 token-based metadata access. This ensures:

Accurate instance tagging

Multi-node monitoring readiness

Compatibility with predictive capacity models

 FinOps Alignment

This monitoring system forms the foundational telemetry layer required for:

Capacity forecasting

Resource utilization analysis

Idle resource detection

Predictive scaling workflows

Cost governance integration

By replacing reactive monitoring with structured time-series telemetry, this project enables proactive FinOps-driven decision systems.

 Current Capabilities

[x] Custom CloudWatch-like telemetry agent

[x] Secure IMDSv2 identity tagging

[x] Multi-metric monitoring

[x] Centralized REST aggregation

[x] Persistent storage

[x] Live dashboard visualization

[x] systemd daemonized deployment

[x] Auto-start on reboot & crash recovery

 Future Enhancements

Replace JSON storage with SQLite / Time-Series DB (e.g., Prometheus/InfluxDB)

Multi-instance aggregation

Predictive capacity modeling (ARIMA / LSTM)

Threshold-based alerting

Cost estimation layer

Kubernetes node monitoring support

Grafana integration

 Repository Structure

private-cloud-monitoring/
│
├── agent/
│   ├── agent.py
│   └── requirements.txt
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── docs/
│   └── (images go here)
│
├── README.md
└── .gitignore


 License

This project is intended for academic and research purposes.
