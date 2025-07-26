# oracle_dashboard.py

import streamlit as st
import os

st.set_page_config(page_title="KINO Oracle Dashboard", layout="wide")

st.title("🔮 KINO Oracle Dashboard")
st.markdown("Καλωσήρθες στο κεντρικό πάνελ προβλέψεων του συστήματος.")

menu = st.sidebar.selectbox("Ενότητες", [
    "📊 Αρχική",
    "🔎 Ανάλυση Αριθμών",
    "🔥 Θερμικοί Χάρτες",
    "🧠 AI Προβλέψεις",
    "📈 Απόδοση Στρατηγικών",
    "🛠️ Ρυθμίσεις & Παρακολούθηση"
])

if menu == "📊 Αρχική":
    st.subheader("Επισκόπηση του Συστήματος")
    st.info("Εδώ θα εμφανίζεται γενική πρόβλεψη, χρόνοι, KPIs κλπ.")

elif menu == "🔎 Ανάλυση Αριθμών":
    st.subheader("Ανάλυση ΚΙΝΟ Αριθμών")
    st.success("Θα ενσωματωθεί το module: `number_analysis.py`")

elif menu == "🔥 Θερμικοί Χάρτες":
    st.subheader("Οπτικοποίηση συχνοτήτων")
    st.warning("Θα προστεθεί `heatmap_visualizer.py`")

elif menu == "🧠 AI Προβλέψεις":
    st.subheader("Αυτόματες Προβλέψεις AI")
    st.error("Module `ai_predictor.py` σε εκκρεμότητα")

elif menu == "📈 Απόδοση Στρατηγικών":
    st.subheader("Backtesting & KPIs")
    st.info("Module `strategy_performance.py` θα προστεθεί")

elif menu == "🛠️ Ρυθμίσεις & Παρακολούθηση":
    st.subheader("Σύστημα Watchdog & Ρυθμίσεις")
    st.success("Ενεργοποιείται `watchdog_logger.py` κ.ά.")
