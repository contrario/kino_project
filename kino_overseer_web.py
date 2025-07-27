
import streamlit as st
from watchdog import run_watchdog_monitor

st.set_page_config(page_title="KINO Overseer Web", layout="wide")

st.title("🎛️ KINO Project Control Panel")

if st.button("Run Watchdog Monitor"):
    st.success("Watchdog Monitor ενεργοποιήθηκε.")
    run_watchdog_monitor()
