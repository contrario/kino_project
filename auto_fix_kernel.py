# auto_fix_kernel.py

import os
import datetime

def fix_logger_future_import():
    try:
        venv_path = os.path.join(os.getcwd(), ".venv", "Lib", "site-packages", "streamlit")
        logger_path = os.path.join(venv_path, "logger.py")

        if not os.path.exists(logger_path):
            return False, f"File not found: {logger_path}"

        with open(logger_path, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()

        future_imports = [line for line in lines if line.strip().startswith("from __future__")]
        other_lines = [line for line in lines if not line.strip().startswith("from __future__")]
        fixed_code = "".join(future_imports + other_lines)

        with open(logger_path, "w", encoding="utf-8") as file:
            file.write(fixed_code)

        return True, f"✅ Fixed {logger_path}"

    except Exception as e:
        return False, str(e)

def log_result(success, message):
    log_path = os.path.join(os.getcwd(), "kernel_log.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as log_file:
        status = "✔" if success else "❌"
        log_file.write(f"[{timestamp}] {status} {message}\n")

if __name__ == "__main__":
    result, msg = fix_logger_future_import()
    log_result(result, msg)
    print(msg)


