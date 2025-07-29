import streamlit as st
import pandas as pd
import numpy as np

def show_self_analysis():
    st.subheader("🧠 Self-Analysis Panel – Demo")
    data = {
        "Module": ["Heatmap", "Prediction", "Telegram", "Watchdog"],
        "Status": ["OK", "OK", "Warning", "OK"],
        "Uptime (%)": [99.8, 99.9, 87.3, 99.5]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.progress(80)
    st.info("Ανάλυση ολοκληρώθηκε – όλα λειτουργούν εντός ορίων.")
