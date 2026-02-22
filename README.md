# Private Cloud Monitoring System

## Overview
A custom CloudWatch-like monitoring system built for private cloud environments.

## Architecture
Instance → Agent → HTTP → Backend → Storage → Dashboard

## Components
- Telemetry Agent (systemd service)
- Monitoring Backend (Flask REST API)
- Live Dashboard (Chart.js)

## Setup

### Agent
cd agent
pip install -r requirements.txt
python agent.py

### Backend
cd backend
pip install -r requirements.txt
python app.py

Dashboard:
http://<public-ip>:5000/dashboard
