# kino_project/streamlit_ui/predictive_harmony_panel.py

import streamlit as st
import random
import datetime

st.set_page_config(page_title="Predictive Harmony Panel", layout="centered")

st.title("🎯 Predictive Harmony Panel")
st.markdown("Μια προβλεπτική εμπειρία βασισμένη σε συγχρονικότητα, στατιστική και αισθητική αρμονία.")

# Επιλογή ημερομηνίας και ώρας
date = st.date_input("📅 Επιλογή Ημερομηνίας", datetime.date.today())
time = st.time_input("⏰ Επιλογή Ώρας", datetime.datetime.now().time())

# Εισαγωγή custom αριθμών
custom_numbers = st.text_input("🔢 Προαιρετικά: Δώσε αριθμούς (χωρισμένοι με κόμμα)", "")

# Κουμπί πρόβλεψης
if st.button("🔮 Δημιούργησε Προβλέψεις"):
    st.subheader("Προτεινόμενοι Αριθμοί:")

    if custom_numbers.strip():
        base_numbers = [int(x.strip()) for x in custom_numbers.split(",") if x.strip().isdigit()]
    else:
        base_numbers = list(range(1, 81))

    predicted = sorted(random.sample(base_numbers, 12))
    st.success(f"🎲 {predicted}")

    st.bar_chart(predicted)

# Σημείωση
st.markdown("---")
st.caption("🎨 Στυλ: DaVinci + Harmonic Engine | Powered by OntologyCore™ & SynchronicityPulse™")
