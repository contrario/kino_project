import os
import json
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS_FOLDER = os.path.join(PROJECT_ROOT, "logs")
OUTPUT_FILE = os.path.join(LOGS_FOLDER, "code_quality_report.json")

def ensure_logs_folder():
    os.makedirs(LOGS_FOLDER, exist_ok=True)

def run_linting(path):
    """Εκτελεί linting στον φάκελο και επιστρέφει τα αποτελέσματα."""
    try:
        result = subprocess.run(
            ["flake8", path, "--format=json"],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout.strip()
        return json.loads(output) if output else {}
    except Exception as e:
        return {"error": str(e)}

def run_black_check(path):
    """Ελέγχει format με black --check"""
    try:
        result = subprocess.run(
            ["black", "--check", "--diff", path],
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "passed": result.returncode == 0,
            "output": result.stdout.strip() + result.stderr.strip()
        }
    except Exception as e:
        return {"error": str(e)}

def evaluate_code_quality():
    ensure_logs_folder()
    code_path = PROJECT_ROOT
    flake8_results = run_linting(code_path)
    black_results = run_black_check(code_path)

    report = {
        "timestamp": datetime.now().isoformat(),
        "flake8": flake8_results,
        "black": black_results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"[✅] Code quality report saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    evaluate_code_quality()
