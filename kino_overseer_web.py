import streamlit as st
import requests

# === Telegram Settings ===
TELEGRAM_BOT_TOKEN = "8393168645:AAG-acWe2Kdw_JXYPQ3ZvNYaBrb64lgivPA"
TELEGRAM_CHAT_ID = "6046304883"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print("Telegram error:", response.text)
    except Exception as e:
        print("Telegram exception:", str(e))

# === Streamlit App ===
st.set_page_config(page_title="KINO Project Overseer", layout="wide", page_icon="🎬")

st.markdown("<h1 style='color:white;'>🎬 KINO Overseer Interface</h1>", unsafe_allow_html=True)
st.write("Welcome to the **Genesis Activation Panel** of the KINO Project.")

with st.expander("🧠 Activate Genesis Modules"):
    st.subheader("🧬 Genesis Control Layer")

    if st.button("💡 Dimensional Harmonics Engine"):
        from genesis_modules.dimensional_harmonics_engine import run as run_dhe
        run_dhe()
        st.success("✅ Dimensional Harmonics Engine synchronized.")
        send_telegram_message("💡 *Dimensional Harmonics Engine* has been activated by Hlias.")

    if st.button("🧬 Genetic Pattern Modulator"):
        from genesis_modules.genetic_pattern_modulator import run as run_gpm
        run_gpm()
        st.success("✅ Genetic Pattern Modulator synchronized.")
        send_telegram_message("🧬 *Genetic Pattern Modulator* has been activated by Hlias.")

    if st.button("🔵 Psychodynamic Filter"):
        from genesis_modules.liberated_psychodynamic_filter import run as run_psycho
        run_psycho()
        st.success("✅ Psychodynamic Filter synchronized.")
        send_telegram_message("🔵 *Psychodynamic Filter* has been activated by Hlias.")

st.markdown("---")
st.markdown("<small>🌱 Genesis Pulse v1.0 – Powered by ARVIA SYSTEMS</small>", unsafe_allow_html=True)
