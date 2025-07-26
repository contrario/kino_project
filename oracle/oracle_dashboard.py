# kino_project/oracle/oracle_dashboard.py

import streamlit as st
from oracle_core_engine import OracleCoreEngine

st.set_page_config(page_title="KINO ORACLE", layout="centered")

engine = OracleCoreEngine()

st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🔮 KINO ORACLE</h1>", unsafe_allow_html=True)
st.markdown("### 🎲 Προτάσεις Αριθμών")
st.info("Η έξυπνη μηχανή πρόβλεψης αριθμών είναι διαθέσιμη. Πίεσε το κουμπί για προβλέψεις!")

if st.button("🔁 Δημιουργία Νέων Προτάσεων"):
    numbers = engine.generate_numbers()
    st.success("🎯 Προτεινόμενοι Αριθμοί:")
    st.markdown(f"### {numbers}")

st.markdown("---")
st.markdown("### 🧠 Ανάλυση Ψυχολογικών & Fractal Μοτίβων")
if st.button("📊 Εκτέλεσε Ανάλυση"):
    result = engine.analyze_patterns()
    st.markdown(f"**Αποτελέσματα:** {result}")

st.markdown("<br><hr><p style='text-align:center;'>Τελευταία ανανέωση: 2025-07-26 | Powered by KINO ORACLE ENGINE</p>", unsafe_allow_html=True)
