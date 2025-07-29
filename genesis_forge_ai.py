# genesis_forge_ai.py

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Genesis Forge AI", layout="centered")

st.title("🧬 Genesis Forge AI")
st.subheader("⚙️ Δημιουργία & Ενεργοποίηση Νοημοσύνης")

# Intro
st.markdown("---")
st.markdown("Αυτό το πάνελ ενεργοποιεί τη **γενεσιουργό διεπαφή** για modules και νοημοσύνη του KINO Project.")

# Text Input
agent_name = st.text_input("🔹 Όνομα νέου AI Agent", placeholder="π.χ. Harmonia")

# Select purpose
purpose = st.selectbox("🎯 Σκοπός του Agent", [
    "Οπτικοποίηση", "Ανάλυση Δεδομένων", "Αλληλεπίδραση με χρήστη",
    "Διαχείριση Modules", "Στρατηγική / Υποστήριξη Απόφασης", "Άλλο"
])

# Button
if st.button("🚀 Δημιουργία Agent"):
    st.success(f"✅ Ο Agent **{agent_name}** δημιουργήθηκε με σκοπό: *{purpose}*.")
    st.balloons()
    with open("logs/genesis_agents_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Δημιουργήθηκε ο Agent: {agent_name} με σκοπό: {purpose}\n")

# Divider
st.markdown("---")
st.markdown("📁 Αρχείο καταγραφής: `logs/genesis_agents_log.txt`")
