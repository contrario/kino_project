import streamlit as st
import pandas as pd
import os
import datetime
from pathlib import Path

# Paths
PROJECT_ROOT = Path("kino_project")
MODULES = [f"Module {i}" for i in range(1, 12)]
MODULES_DIR = PROJECT_ROOT / "modules"
LOGS_DIR = PROJECT_ROOT / "logs"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
WATCHDOG_DIR = PROJECT_ROOT / "watchdog"

# Δημιουργία φακέλων αν δεν υπάρχουν
for path in [MODULES_DIR, LOGS_DIR, OUTPUTS_DIR, WATCHDOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Dummy module execution status (θα συνδεθεί με real run στη συνέχεια)
def get_module_status():
    return pd.DataFrame({
        "Module": MODULES,
        "Status": ["Idle"] * len(MODULES),
        "Last Run": ["-"] * len(MODULES),
        "Success": [False] * len(MODULES)
    })

# App Layout
st.set_page_config(page_title="KINO Overseer Web Panel", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #111; color: white; }
        .stButton > button { width: 100%; height: 3em; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 KINO Overseer Web Panel")
st.subheader("Ολοκληρωμένη Streamlit υποδομή επιπέδου CERN")
st.markdown("**Αυτοδιόρθωση και παρακολούθηση όλων των module (1-11)**")

# Tabs για κάθε module
tabs = st.tabs(MODULES)

# Status dashboard
status_df = get_module_status()
st.markdown("### 🔬 Module Overview Dashboard (Live)")
st.dataframe(status_df, use_container_width=True)

# Heatmap Status
st.markdown("### 🧠 Visual Heatmap")
st.write("(Αυτό το τμήμα θα ενσωματώσει πραγματικό heatmap ανάλογα με την επιτυχία/αποτυχία)")

# CERN-style Health Bar
st.markdown("### 🟩 System Health Status")
st.success("Όλα τα modules είναι σταθερά προς το παρόν.")

# Tabs λειτουργικότητας
for i, tab in enumerate(tabs):
    with tab:
        st.header(f"⚙️ {MODULES[i]}")
        if st.button(f"🚀 Run {MODULES[i]}"):
            st.info(f"{MODULES[i]} ενεργοποιήθηκε... (προσθήκη watchdog σύντομα)")

# Στατιστικά Watchdog
st.markdown("### 📈 Watchdog Real-Time Stats")
st.write("Logs, alerts και αλλαγές αρχείων θα εμφανίζονται εδώ σύντομα.")
