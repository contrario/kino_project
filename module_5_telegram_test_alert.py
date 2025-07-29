import streamlit as st
import requests

def send_test_alert():
    st.subheader("📡 Telegram Alerts – Demo")

    chat_id = "6046304883"  # Από τον Hlia
    token = "8393168645:AAG-acWe2Kdw_JXYPQ3ZvNYaBrb64lgivPA"

    if st.button("📤 Στείλε Test Alert"):
        msg = "📢 Αυτό είναι test μήνυμα από το KINO Project AI."
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, data={"chat_id": chat_id, "text": msg})
        if r.status_code == 200:
            st.success("Μήνυμα εστάλη!")
        else:
            st.error("Σφάλμα αποστολής.")
