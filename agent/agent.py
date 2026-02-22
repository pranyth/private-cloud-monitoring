import psutil
import requests
import time
import datetime
import json


# ----------------------------------------
# Get Instance ID using IMDSv2
# ----------------------------------------
def get_instance_id():
    try:
        token_response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )

        token = token_response.text

        instance_id_response = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )

        return instance_id_response.text

    except Exception as e:
        print("Error fetching instance ID:", e)
        return "unknown-instance"


# ----------------------------------------
# Collect System Metrics
# ----------------------------------------
def collect_metrics():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv

        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "disk_percent": disk_percent,
            "network_bytes_sent": bytes_sent,
            "network_bytes_recv": bytes_recv
        }

    except Exception as e:
        print("Error collecting metrics:", e)
        return None


# ----------------------------------------
# Main Agent Loop
# ----------------------------------------
def main():
    instance_id = get_instance_id()
    print(f"\nStarting Private CloudWatch Agent for {instance_id}\n")

    backend_url = "http://127.0.0.1:5000/metrics"

    while True:
        try:
            timestamp = datetime.datetime.now(datetime.UTC).isoformat()
            metrics = collect_metrics()

            if metrics is None:
                continue

            payload = {
                "instance_id": instance_id,
                "timestamp": timestamp,
                **metrics
            }

            try:
                response = requests.post(backend_url, json=payload, timeout=2)
                print(f"Sent metrics - Status: {response.status_code}")
            except Exception as e:
                print("Failed to send metrics:", e)

            time.sleep(5)

        except KeyboardInterrupt:
            print("\nAgent stopped manually.")
            break

        except Exception as e:
            print("Unexpected error in main loop:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
