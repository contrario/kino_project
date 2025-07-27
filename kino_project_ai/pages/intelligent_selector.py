import streamlit as st
import datetime
import random

st.set_page_config(page_title="Intelligent Number Selector", layout="centered")

st.title("🎯 Intelligent Number Selector")

col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("📅 Επιλέξτε Ημερομηνία", datetime.date.today())
with col2:
    selected_time = st.time_input("⏰ Επιλέξτε Ώρα", datetime.datetime.now().time())

month_name = selected_date.strftime("%B")

st.subheader("🔢 Επιλογές Παιχνιδιού")
num_count = st.slider("Πόσους αριθμούς θέλετε;", 5, 10, 7)
draw_count = st.slider("Σε πόσες συνεχόμενες κληρώσεις;", 3, 10, 5)

st.markdown("---")
st.write(f"📌 Επιλέχθηκαν οι παρακάτω παράμετροι:")
st.info(f"""
- 📅 Ημερομηνία: **{selected_date.strftime('%d/%m/%Y')}**
- 🕓 Ώρα: **{selected_time.strftime('%H:%M')}**
- 📆 Μήνας: **{month_name}**
- 🔢 Πλήθος αριθμών: **{num_count}**
- 🔁 Συνεχόμενες κληρώσεις: **{draw_count}**
""")

numbers = sorted(random.sample(range(1, 81), num_count))
st.success(f"🎰 Προτεινόμενοι αριθμοί: {numbers}")

st.markdown("---")
st.caption("🚀 Τα δεδομένα θα συνδυαστούν με το υπόλοιπο AI σύστημα για πιο ακριβείς προτάσεις.")
