from __future__ import annotations
# system_repair.py
import os
import re
import time
from datetime import datetime

LOG_FILE = "kernel_log.txt"
PROJECT_DIR = os.getcwd()
TARGET_EXTENSIONS = ['.py']

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        logf.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def fix_future_import(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    has_future = any(FUTURE_IMPORT in line for line in lines)
    if not has_future:
        return False  # Δεν χρειάζεται διόρθωση

    # Διαγραφή γραμμής future import και επανατοποθέτηση στην αρχή
    new_lines = [line for line in lines if FUTURE_IMPORT not in line]
    new_lines.insert(0, FUTURE_IMPORT + "\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    log(f"[FIXED] Corrected future import position in {file_path}")
    return True

def scan_and_fix_files():
    log("🔍 Scanning project files for future import issues...")
    fixes = 0
    for root, _, files in os.walk(PROJECT_DIR):
        for fname in files:
            if fname.endswith(tuple(TARGET_EXTENSIONS)):
                fpath = os.path.join(root, fname)
                if fix_future_import(fpath):
                    fixes += 1
    log(f"✅ Completed scan. Files fixed: {fixes}")

def check_streamlit_health():
    log("⚙️ Running streamlit health check...")
    try:
        import streamlit
        log(f"✅ Streamlit version {streamlit.__version__} is correctly installed.")
    except Exception as e:
        log(f"[ERROR] Streamlit issue: {str(e)}")
        log("⛏️ Suggest: pip uninstall streamlit && pip install streamlit")

def check_pip_integrity():
    log("⚙️ Checking pip integrity...")
    try:
        import pip
        log(f"✅ Pip version {pip.__version__} loaded successfully.")
    except Exception as e:
        log(f"[ERROR] Pip broken: {str(e)}")
        log("💡 Suggest: python -m ensurepip --upgrade")

def final_summary():
    log("🔁 Final check complete. Ready to rerun your Streamlit app safely.")
    log("✅ RECOMMENDED: Run: `streamlit run kernel_dashboard.py`")

if __name__ == "__main__":
    log("===== SYSTEM REPAIR STARTED =====")
    scan_and_fix_files()
    check_pip_integrity()
    check_streamlit_health()
    final_summary()
    log("===== SYSTEM REPAIR COMPLETE =====\n")
