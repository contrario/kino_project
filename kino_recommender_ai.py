# kino_recommender_ai.py
import os
from datetime import datetime
import streamlit as st
from watchdog_logger import log_recommendation

MODULES = {
    "watchdog_core": "Παρακολούθηση",
    "heatmap_generator": "Οπτικοποίηση",
    "pattern_analyzer": "Ανάλυση Patterns",
    "kino_overseer_web": "Κεντρικό Dashboard",
    "auto_fixer": "Αυτόματες Επιδιορθώσεις",
    "memory_profiler": "Έλεγχος RAM/CPU",
}

def suggest_modules():
    now = datetime.now().strftime('%H:%M:%S')
    st.subheader("🤖 Προτάσεις Εκτέλεσης Modules")

    for module, desc in MODULES.items():
        if "watchdog" in module or "overseer" in module:
            st.success(f"[{now}] ⚙️ Προτείνεται επανεκτέλεση: **{module}** ({desc})")
            log_recommendation(f"[{now}] Suggest to rerun: {module}")
        else:
            st.info(f"[{now}] 🧠 Χρήσιμη ανάλυση: **{module}** ({desc})")

def suggest_visualizations():
    st.subheader("📊 Προτάσεις Οπτικοποιήσεων")
    visuals = ["heatmap", "timeline plot", "fractal structure", "draw frequency"]

    for visual in visuals:
        st.write(f"🟢 Να ενεργοποιηθεί: **{visual}**")
        log_recommendation(f"Suggest visualization: {visual}")

def suggest_fixes():
    st.subheader("🛠️ Πιθανές Επιδιορθώσεις")
    fixes = ["Missing matplotlib", "Circular imports", "No logs found", "Unoptimized memory"]

    for fix in fixes:
        st.warning(f"⚠️ AI υποψιάζεται: **{fix}**")
        log_recommendation(f"Fix suggested: {fix}")
