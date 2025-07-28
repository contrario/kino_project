
# kino_autofix_overlord.py

import os
import subprocess
import ast
import requests
import shutil
import time
from datetime import datetime
from pathlib import Path

# GitHub Repo Details (edit as needed)
GITHUB_REPO = "contrario/kino_project_ai"
LOCAL_REPO_PATH = "./kino_project_ai"
GITHUB_TOKEN = "your_github_token_here"  # Replace securely
TELEGRAM_TOKEN = "8393168645:AAG-acWe2Kdw_JXYPQ3ZvNYaBrb64lgivPA"
TELEGRAM_CHAT_ID = "6046304883"

# Utility Functions
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram error:", e)

def clone_repo():
    if not Path(LOCAL_REPO_PATH).exists():
        subprocess.run(["git", "clone", f"https://github.com/{GITHUB_REPO}.git"])

def find_and_fix_watchdog_conflict():
    rename_log = []
    for root, _, files in os.walk(LOCAL_REPO_PATH):
        for file in files:
            if file == "watchdog.py":
                old_path = Path(root) / file
                new_path = Path(root) / "watchdog_local.py"
                shutil.move(old_path, new_path)
                rename_log.append((str(old_path), str(new_path)))
    return rename_log

def fix_import_conflicts():
    fix_log = []
    for root, _, files in os.walk(LOCAL_REPO_PATH):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                content = path.read_text()
                if "from watchdog import events" in content:
                    new_content = content.replace(
                        "from watchdog import events",
                        "from watchdog.events import FileSystemEventHandler"
                    )
                    path.write_text(new_content)
                    fix_log.append(str(path))
    return fix_log

def fix_streamlit_session_check():
    fix_log = []
    for root, _, files in os.walk(LOCAL_REPO_PATH):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                content = path.read_text()
                if "session._scriptrunner" in content:
                    new_content = content.replace(
                        "if session._scriptrunner is not None:",
                        "if hasattr(session, '_scriptrunner'):"
                    )
                    path.write_text(new_content)
                    fix_log.append(str(path))
    return fix_log

def git_commit_push():
    subprocess.run(["git", "-C", LOCAL_REPO_PATH, "add", "."])
    subprocess.run(["git", "-C", LOCAL_REPO_PATH, "commit", "-m", "AutoFix: Watchdog conflict and Streamlit compatibility"])
    subprocess.run(["git", "-C", LOCAL_REPO_PATH, "push"])

def run_autofix():
    clone_repo()
    logs = []
    logs += find_and_fix_watchdog_conflict()
    logs += fix_import_conflicts()
    logs += fix_streamlit_session_check()
    git_commit_push()
    send_telegram_message("✅ Kino Autofix ολοκληρώθηκε με επιτυχία.\n\nΑρχεία:\n" + "\n".join(logs))

if __name__ == "__main__":
    run_autofix()
