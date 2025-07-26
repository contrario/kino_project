# auto_fix_engine.py

import json
import os
import time
from datetime import datetime
from pathlib import Path
from watchdog_logger import log_autofix

# === Paths ===
LOGS_DIR = Path("kino_project/logs")
STREAM_LOG = LOGS_DIR / "module_stream.log"
AUTO_FIX_LOG = LOGS_DIR / "ai_autofix.log"

# === Core AutoFix Engine ===
def load_stream_logs():
    if not STREAM_LOG.exists():
        return []
    with open(STREAM_LOG, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) if line.strip().startswith("{") else {"raw": line.strip()} for line in f.readlines()]

def generate_autofix_action(module_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fix_command = f"# AutoFix Recovery Plan for {module_name}\ntry:\n    import {module_name}\n    {module_name}.recover()\nexcept Exception as e:\n    print(\"[AutoFix] Recovery failed:", e)"
    log_autofix(f"[{timestamp}] 🔧 AutoFix for {module_name}\n{fix_command}")
    return fix_command

def auto_fix_recent_errors():
    logs = load_stream_logs()
    error_modules = []
    for entry in reversed(logs):
        if entry.get("status") in ["error", "failed"]:
            mod = entry.get("module")
            if mod not in error_modules:
                error_modules.append(mod)
    
    for mod in error_modules:
        fix_code = generate_autofix_action(mod)
        print(fix_code)
        time.sleep(1)

def run():
    print("🔁 Running Auto-Fix Engine...")
    auto_fix_recent_errors()
    print("✅ Auto-Fix Complete")

if __name__ == "__main__":
    run()
