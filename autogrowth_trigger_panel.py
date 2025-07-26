# autogrowth_trigger_panel.py
import streamlit as st
import subprocess
import os
from datetime import datetime

st.set_page_config(page_title="Autogrowth Trigger Panel", layout="centered")

st.title("🌱 Autogrowth Trigger Panel")

# Εμφάνιση τελευταίου trigger
log_file = "autogrowth_last_trigger.log"
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        last_trigger = f.read().strip()
        st.success(f"Τελευταία ενεργοποίηση: {last_trigger}")
else:
    st.warning("Δεν έχει ενεργοποιηθεί ακόμη.")

# Trigger κουμπί
if st.button("🚀 Εκτέλεσε Trigger Τώρα"):
    result = subprocess.run(["python", "autogrowth_trigger_engine.py"], capture_output=True, text=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(now)
    st.info("✅ Autogrowth Triggered χειροκίνητα.")
    st.code(result.stdout)

st.markdown("---")
st.caption("Made with ❤️ για τον Hlias από το Autopoietic System.")
