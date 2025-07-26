try:
    import webbrowser
    webbrowser.open(url)
except Exception as e:
    print(f"Could not open browser: {e}")

import streamlit as st
import os
import json
from datetime import datetime

# Path to log and system info files
LOG_FILE = "logs/auto_repair.log"
MODULES_DIR = "modules"
PLACEHOLDER_NOTE = "__PLACEHOLDER__"

def read_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    return ["\u26a0\ufe0f Δεν εντοπίστηκε αρχείο log."]

def scan_modules():
    modules_info = []
    if not os.path.exists(MODULES_DIR):
        return [("[Μη διαθέσιμο φάκελος modules]", False)]
    for filename in sorted(os.listdir(MODULES_DIR)):
        if filename.endswith(".py"):
            full_path = os.path.join(MODULES_DIR, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if PLACEHOLDER_NOTE in content:
                        modules_info.append((filename, False))
                    else:
                        modules_info.append((filename, True))
            except Exception as e:
                modules_info.append((filename, f"Error: {str(e)}"))
    return modules_info

def show_diagnostics():
    st.title("\ud83e\uddea AI Self-Diagnostic Panel")
    st.markdown("""
        Αυτό το πάνελ δείχνει την κατάσταση των modules, τα logs από το Watchdog, 
        και προτάσεις για αναβάθμιση του οικοσυστήματος.
    """)

    with st.expander("\ud83d\udd0d Έλεγχος Modules"):
        modules = scan_modules()
        for module, status in modules:
            if status is True:
                st.success(f"{module} \u2714\ufe0f")
            elif status is False:
                st.warning(f"{module} (placeholder)")
            else:
                st.error(f"{module} \u274c {status}")

    with st.expander("\ud83d\udd24 Auto-Healing Log"):
        logs = read_log()
        for line in logs[-50:]:
            st.text(line)

    with st.expander("\ud83d\udcc8 Προτάσεις Βελτίωσης"):
        st.markdown("""
        - \u2728 Αντικατάσταση όλων των placeholder με λειτουργικό κώδικα.
        - \u2699\ufe0f Ενσωμάτωση inline unit testing ανά module.
        - \ud83d\udd04 Προσθήκη real-time status alerts σε sidebar.
        - \ud83d\udd27 Επέκταση του Watchdog σε επίπεδο API/Network.
        """)

if __name__ == "__main__":
    show_diagnostics()
