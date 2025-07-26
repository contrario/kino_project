import streamlit as st
import os
import json
import importlib.util
from module_12_autogrowth_seed import create_new_module

st.set_page_config(page_title="Harmonic Growth Controller", layout="wide")

st.markdown("## 🎼 Harmonic Engine Controller")
st.write("Διαχείριση της αρμονικής ανάπτυξης του project")

col1, col2 = st.columns([1, 3])

# --- GROWTH LOG ---
with col1:
    st.markdown("### 📘 Growth Log")

    log_path = "logs/harmonic_growth_log.json"
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)
        for entry in reversed(log_data[-10:]):  # Εμφάνιση των 10 τελευταίων
            st.code(f"{entry['timestamp']} → {entry['module']} [Seed: {entry['seed_value']}]")
    else:
        st.warning("Δεν βρέθηκε το αρχείο `harmonic_growth_log.json`")

    if st.button("➕ Δημιουργία Νέου Module"):
        create_new_module()
        st.success("✅ Νέο module δημιουργήθηκε!")
        st.experimental_rerun()  # Επαναφόρτωση της σελίδας για εμφάνιση του νέου αρχείου

# --- MODULES ---
with col2:
    st.markdown("### 📦 Υπάρχοντα Modules")
    modules = sorted([f for f in os.listdir() if f.startswith("module_") and f.endswith(".py")])

    for m in modules:
        st.code(m)

st.markdown("🧠 Συνοπτική επισκόπηση από το Harmonic Autogrowth Engine")
