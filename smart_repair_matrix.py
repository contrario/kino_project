# smart_repair_matrix.py

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

LOGS_DIR = Path("kino_project/logs")
STREAM_LOG = LOGS_DIR / "module_stream.log"
MATRIX_OUTPUT = LOGS_DIR / "smart_repair_matrix.json"


def load_stream_logs():
    if not STREAM_LOG.exists():
        return []
    with open(STREAM_LOG, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) if line.strip().startswith("{") else {"raw": line.strip()} for line in f.readlines()]


def analyze_failure_patterns(logs):
    module_errors = defaultdict(list)
    now = datetime.utcnow()

    for log in logs:
        if isinstance(log, dict) and log.get("status") in ["error", "failed"]:
            timestamp = log.get("timestamp")
            module = log.get("module")
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except:
                continue
            if module and (now - dt).total_seconds() < 86400:  # τελευταίο 24ωρο
                module_errors[module].append(timestamp)

    pattern_matrix = {}
    for module, times in module_errors.items():
        count = len(times)
        freq = Counter(times)
        pattern_matrix[module] = {
            "count": count,
            "timestamps": times,
            "recent_fail_rate": round(count / 24, 2),
            "recovery_action": "auto_restart" if count < 5 else "deep_diagnosis"
        }

    return pattern_matrix


def save_matrix(matrix):
    with open(MATRIX_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=4, ensure_ascii=False)


def generate_smart_repair_matrix():
    logs = load_stream_logs()
    matrix = analyze_failure_patterns(logs)
    save_matrix(matrix)
    return matrix


if __name__ == "__main__":
    matrix = generate_smart_repair_matrix()
    print("✅ Smart Repair Matrix Generated with", len(matrix), "entries.")
