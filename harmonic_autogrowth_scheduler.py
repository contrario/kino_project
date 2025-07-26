print("🚀 Scheduler ξεκίνησε επιτυχώς.")
import os
import json
import time
from datetime import datetime, timedelta
import subprocess
import sys

# Αυτόματες ρυθμίσεις
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_DIR, "harmonic_growth_log.json")
SEED_SCRIPT = os.path.join(PROJECT_DIR, "module_12_autogrowth_seed.py")
CHECK_INTERVAL = 600   # 10 λεπτά
MAX_IDLE_TIME = 3600   # 1 ώρα

def load_growth_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_last_module_timestamp():
    log = load_growth_log()
    if not log:
        return None
    last_entry = log[-1]
    return datetime.fromisoformat(last_entry["timestamp"])

def trigger_autogrowth():
    print(f"[{datetime.now().isoformat()}] 🔄 Autogrowth Triggered")
    try:
        subprocess.run([sys.executable, SEED_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Σφάλμα κατά την εκτέλεση του seed: {e}")

def scheduler_loop():
    print("🔁 Harmonic Autogrowth Scheduler ξεκίνησε...\n")
    while True:
        now = datetime.now()
        last_time = get_last_module_timestamp()

        if last_time is None:
            print("⚠️ Δεν βρέθηκε προηγούμενο module. Δημιουργία τώρα...")
            trigger_autogrowth()
        elif (now - last_time).total_seconds() > MAX_IDLE_TIME:
            print("⏰ Πέρασε 1 ώρα χωρίς νέο module.")
            trigger_autogrowth()
        else:
            print(f"[{now.strftime('%H:%M:%S')}] ✅ Τελευταίο module: {last_time.strftime('%H:%M:%S')} — αναμονή...")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    scheduler_loop()
