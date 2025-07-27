
import time
import streamlit as st

def run_watchdog_monitor():
    with st.spinner("Εκτελείται παρακολούθηση..."):
        for i in range(5):
            st.write(f"📡 Watchdog ενεργός... Βήμα {i+1}")
            time.sleep(1)
        st.success("✅ Παρακολούθηση ολοκληρώθηκε.")
