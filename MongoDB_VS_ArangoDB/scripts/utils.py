import json
import psutil
from datetime import datetime

def monitor_resources():
    process = psutil.Process()
    cpu = process.cpu_percent(interval=1)
    mem = process.memory_info().rss / 1024 / 1024
    return cpu, mem

def save_stats_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
