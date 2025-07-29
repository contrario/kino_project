import streamlit as st

def show_modules_status():
    st.subheader("📦 Modules Overview – Demo")
    modules = {
        "Heatmap Viewer": "✅",
        "Prediction Engine": "✅",
        "Telegram Alerts": "⚠️",
        "Watchdog Monitor": "✅"
    }
    for name, status in modules.items():
        st.write(f"{status} {name}")
