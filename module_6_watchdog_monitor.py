import streamlit as st
import time
import random

def run_watchdog_panel():
    st.subheader("🔍 Watchdog Monitor – Demo")
    fake_logs = [
        "📁 File changed: kino_prediction_engine.py",
        "🧠 Model reloaded successfully",
        "⚠️ Suspicious latency spike detected",
        "✅ Streamlit component synced"
    ]
    if st.button("📡 Προσομοίωση Εποπτείας"):
        with st.spinner("Παρακολούθηση..."):
            time.sleep(1)
            st.code(random.choice(fake_logs), language="text")
