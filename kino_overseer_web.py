# kino_overseer_web.py

import streamlit as st

# Εισαγωγές modules
from genesis_modules.dimensional_harmonics_engine import run as run_dhe
from genesis_modules.genetic_pattern_modulator import run as run_gpm
from genesis_modules.liberated_psychodynamic_filter import run as run_psycho

# Τίτλος και Στυλ
st.set_page_config(page_title="KINO Overseer", layout="wide")

st.markdown("""
    <style>
        .main {background-color: #111;}
        .stButton>button {
            background-color: #880e4f;
            color: white;
            border-radius: 12px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #c51162;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Genesis Control Layer")

# Επιλογή Εργαλείου
selected_tool = st.sidebar.radio("🔮 Select a Module:", [
    "🌌 Dimensional Harmonics Engine",
    "🧬 Genetic Pattern Modulator",
    "🧿 Psychodynamic Filter"
])

# Εκτέλεση του επιλεγμένου module
if selected_tool == "🌌 Dimensional Harmonics Engine":
    run_dhe()
elif selected_tool == "🧬 Genetic Pattern Modulator":
    run_gpm()
elif selected_tool == "🧿 Psychodynamic Filter":
    run_psycho()
