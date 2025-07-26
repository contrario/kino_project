# autogrowth_trigger_scheduler.py
import os
import time
import datetime
from autogrowth_trigger_engine import trigger_autogrowth

MODULE_DIR = "."
CHECK_INTERVAL = 60  # check every 60 sec
TRIGGER_INTERVAL = 600  # force trigger every 10 min
MAX_IDLE_TIME = 3600  # if no new module for 1 hour

def get_last_module_time():
    modules = [f for f in os.listdir(MODULE_DIR) if f.startswith("module_") and f.endswith(".py")]
    if not modules:
        return None
    latest = max(modules, key=lambda f: os.path.getmtime(os.path.join(MODULE_DIR, f)))
    return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(MODULE_DIR, latest)))

def scheduler_loop():
    print("🟢 Autogrowth Trigger Scheduler ξεκίνησε.")
    last_forced = time.time()

    while True:
        now = time.time()
        last_module_time = get_last_module_time()

        # Condition 1: No module for 1 hour
        if last_module_time:
            delta = now - last_module_time.timestamp()
            if delta > MAX_IDLE_TIME:
                print("⚠️ Δεν βρέθηκε νέο module εδώ και 1 ώρα.")
                trigger_autogrowth()
                last_forced = now
        else:
            print("⚠️ Δεν υπάρχει κανένα module. Δημιουργία πρώτου.")
            trigger_autogrowth()
            last_forced = now

        # Condition 2: Force trigger every 10 min
        if now - last_forced >= TRIGGER_INTERVAL:
            print("🔁 10 λεπτά πέρασαν. Εκτελώ trigger.")
            trigger_autogrowth()
            last_forced = now

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    scheduler_loop()
