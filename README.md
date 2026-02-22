
# Private Cloud Monitoring System  
Custom CloudWatch-Like Telemetry Agent for Private Cloud Environments

---

## Overview

This project implements a custom CloudWatch-like monitoring system designed for private cloud environments where managed monitoring services (such as AWS CloudWatch) are unavailable.

The system includes:

- A lightweight telemetry agent running as a background Linux service
- A centralized monitoring backend (REST API)
- Persistent structured metric storage
- A live web dashboard with real-time visualization
- Production-style daemonization using systemd

This forms the Telemetry and Visualization Layer of a predictive FinOps architecture.
<img width="1240" height="626" alt="network-bytes" src="https://github.com/user-attachments/assets/a2f6254e-ec96-489e-88d3-794a6f9dc052" />
<img width="861" height="438" alt="memory-used" src="https://github.com/user-attachments/assets/8f640f58-8b75-47f9-a9d4-f8d560f0b146" />
<img width="499" height="222" alt="linux-service" src="https://github.com/user-attachments/assets/84f0c9cd-d1fa-49e5-9bea-e598052725a3" />
<img width="395" height="477" alt="json" src="https://github.com/user-attachments/assets/8df5677a-a593-4ba3-b4ad-06529834d1b3" />
<img width="503" height="261" alt="dashboard-overview png" src="https://github.com/user-attachments/assets/e0b7ad0d-5f19-4627-910a-bed2b0951571" />


---

## Problem Statement

Public cloud providers offer managed monitoring tools such as AWS CloudWatch. However, private cloud environments lack:

- Managed telemetry collection  
- Centralized metric aggregation  
- Automated resource insight pipelines  
- FinOps-aligned cost intelligence hooks  

This project recreates core monitoring capabilities in a cloud-agnostic, provider-independent manner, providing raw telemetry natively without relying on external vendor lock-in.

---

## System Architecture

```

+-------------------------+
|     Private Compute     |

| Instance                    |
| --------------------------- |
| Telemetry Agent             |
| (systemd service)           |
| +-----------+-------------+ |

```
        |
        | HTTP POST (JSON)
        v
```

+-------------------------+

| Monitoring Backend          |
| --------------------------- |
| Flask REST API              |
| /metrics endpoint           |
| Persistent Storage          |
| +-----------+-------------+ |

```
        |
        | HTTP GET (JSON)
        v
```

+-------------------------+
|     Web Dashboard       |
|   (Chart.js + Flask)    |
+-------------------------+

```

---

## Components

### 1. Telemetry Agent

The agent performs:

- CPU utilization collection (%)
- Memory utilization collection (%)
- Disk utilization collection (%)
- Network bytes sent/received
- Secure instance identification via IMDSv2
- UTC timezone-aware timestamp generation
- JSON payload transmission every 5 seconds
- Background execution as a systemd service
- Automatic restart on failure

---

### 2. Monitoring Backend

The backend:

- Is built using Flask
- Exposes REST endpoint `/metrics`
- Accepts structured JSON telemetry
- Appends records to persistent storage (`metrics.json`)
- Adds server-side `received_at` timestamp
- Exposes `/data` endpoint for dashboard consumption
- Runs as a systemd daemon

---

### 3. Dashboard Layer

The dashboard:

- Is built with Chart.js
- Auto-refreshes every 5 seconds
- Displays:
  - CPU Usage
  - Memory Usage
  - Disk Usage
  - Network Activity
- Provides a clean and responsive UI

Accessible via:

```

http://<public-ip>:5000/dashboard

````

---

## Deployment Instructions

### Prerequisites

- Ubuntu Server 22.04+
- Python 3.x
- Git
- Open firewall ports:
  - 22 (SSH)
  - 5000 (Dashboard / API)

---

## Clone Repository

```bash
git clone https://github.com/pranyth/private-cloud-monitoring.git
cd private-cloud-monitoring
````

---

## Install Dependencies

### Agent Setup

```bash
cd agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Backend Setup

```bash
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Run in Development Mode

### Run Backend

```bash
cd backend
python app.py
```

### Run Agent

```bash
cd agent
python agent.py
```

---

## Production Deployment (systemd)

To ensure the services run autonomously, survive reboots, and restart on failure, deploy them using systemd.

---

### Agent Service

Create:

`/etc/systemd/system/private-cw-agent.service`

```
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
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable private-cw-agent
sudo systemctl start private-cw-agent
```

---

### Backend Service

Create:

`/etc/systemd/system/monitoring-backend.service`

```
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
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable monitoring-backend
sudo systemctl start monitoring-backend
```

---

## Dashboard Preview

Add screenshots in the `docs/` folder and reference them like:

```markdown
![Dashboard Overview](docs/dashboard-overview.png)
```

---

## Secure Instance Identification (IMDSv2)

The agent securely retrieves instance identity using AWS IMDSv2 token-based metadata access.

This ensures:

* Accurate instance tagging
* Multi-node monitoring readiness
* Compatibility with predictive capacity models

---

## FinOps Alignment

This monitoring system forms the foundational telemetry layer required for:

* Capacity forecasting
* Resource utilization analysis
* Idle resource detection
* Predictive scaling workflows
* Cost governance integration

By replacing reactive monitoring with structured time-series telemetry, this project enables proactive FinOps-driven decision systems.

---

## Current Capabilities

* Custom CloudWatch-like telemetry agent
* Secure IMDSv2 identity tagging
* Multi-metric monitoring
* Centralized REST aggregation
* Persistent storage
* Live dashboard visualization
* systemd daemonized deployment
* Auto-start on reboot
* Crash recovery

---

## Future Enhancements

* Replace JSON storage with SQLite or time-series databases
* Multi-instance aggregation
* Predictive capacity modeling (ARIMA / LSTM)
* Threshold-based alerting
* Cost estimation layer
* Kubernetes node monitoring support
* Grafana integration

---

## Repository Structure

```
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
│   └── (screenshots)
│
├── README.md
└── .gitignore
```

---

## License

This project is intended for academic and research purposes.

````

