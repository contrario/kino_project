# watchdog_logger.py

import os
import datetime

STREAM_LOG_PATH = "logs/stream_log.txt"
AUTOFIX_LOG_PATH = "logs/autofix_log.txt"
ANOMALY_LOG_PATH = "logs/anomaly_log.txt"

os.makedirs("logs", exist_ok=True)

def log_message(message: str, log_type: str = "stream"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}\n"

    if log_type == "stream":
        log_path = STREAM_LOG_PATH
    elif log_type == "autofix":
        log_path = AUTOFIX_LOG_PATH
    elif log_type == "anomaly":
        log_path = ANOMALY_LOG_PATH
    else:
        raise ValueError("Invalid log_type. Choose from 'stream', 'autofix', or 'anomaly'.")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(formatted_message)

def clear_logs():
    for path in [STREAM_LOG_PATH, AUTOFIX_LOG_PATH, ANOMALY_LOG_PATH]:
        if os.path.exists(path):
            open(path, "w", encoding="utf-8").close()

def read_log(log_type: str = "stream"):
    if log_type == "stream":
        log_path = STREAM_LOG_PATH
    elif log_type == "autofix":
        log_path = AUTOFIX_LOG_PATH
    elif log_type == "anomaly":
        log_path = ANOMALY_LOG_PATH
    else:
        raise ValueError("Invalid log_type. Choose from 'stream', 'autofix', or 'anomaly'.")

    if not os.path.exists(log_path):
        return []

    with open(log_path, "r", encoding="utf-8") as f:
        return f.readlines()

if __name__ == "__main__":
    clear_logs()
    log_message("Ξεκίνησε η παρακολούθηση του συστήματος.", log_type="stream")
    log_message("Εντοπίστηκε και επιδιορθώθηκε ανωμαλία στο module_7.", log_type="autofix")
    log_message("Αναγνωρίστηκε ασυνήθιστη συμπεριφορά στο module_5.", log_type="anomaly")

    print("✅ Οι δοκιμαστικές εγγραφές καταχωρήθηκαν επιτυχώς στα logs.")

