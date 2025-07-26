# harmonic_autogrowth_panel.py

import streamlit as st
import subprocess
import os
import time

st.set_page_config(page_title="Harmonic Scheduler", layout="centered")

st.title("📅 Harmonic Autogrowth Panel")
st.markdown("Διαχείριση του Harmonic Scheduler για αυτόματη ανάπτυξη modules.")

SCHEDULER_LOCK_FILE = "kino_project/.scheduler_lock"

def is_scheduler_running():
    return os.path.exists(SCHEDULER_LOCK_FILE)

def start_scheduler():
    subprocess.Popen(["python", os.path.join(os.getcwd(), "harmonic_autogrowth_scheduler.py")])
    time.sleep(1)

def stop_scheduler():
    if os.path.exists(SCHEDULER_LOCK_FILE):
        os.remove(SCHEDULER_LOCK_FILE)

# --- UI
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("▶️ Start Scheduler"):
        start_scheduler()

    if st.button("⏹ Stop Scheduler"):
        stop_scheduler()

with col2:
    st.markdown("### Κατάσταση:")
    if is_scheduler_running():
        st.success("✅ Ο Scheduler ΤΡΕΧΕΙ αυτή τη στιγμή.")
    else:
        st.error("⛔ Ο Scheduler ΔΕΝ τρέχει.")

st.markdown("---")
auto_refresh = st.checkbox("🔁 Αυτόματη Ανανέωση", value=False)
if auto_refresh:
    time.sleep(3)
    st.experimental_rerun()
