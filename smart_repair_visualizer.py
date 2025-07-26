# kino_hypervisor_hub.py

import os
import json
import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np
import networkx as nx
from pathlib import Path
from sklearn.ensemble import IsolationForest
from collections import Counter
import requests

# === Paths ===
LOGS_DIR = Path("kino_project/logs")
STATUS_LOG = LOGS_DIR / "module_status.json"
STREAM_LOG = LOGS_DIR / "module_stream.log"
AUTO_FIX_LOG = LOGS_DIR / "ai_autofix.log"
REPAIR_MATRIX_JSON = LOGS_DIR / "smart_repair_matrix.json"

# === Telegram Bot Credentials ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                st.warning("❗ Αποτυχία αποστολής μηνύματος Telegram")
        except Exception as e:
            st.warning(f"Telegram error: {e}")

# === Streamlit Setup ===
st.set_page_config(page_title="🧠 KINO Hypervisor Hub", layout="wide")
st.title("🧠 Hypervisor Intelligence Hub")
st.subheader("CERN/NASA Diagnostic Layer for Smart Self-Repair & Visualization")

# === Load Logs ===
def load_logs(log_path):
    if not log_path.exists():
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) if line.strip().startswith("{") else {"raw": line.strip()} for line in f.readlines()]

def load_status_log():
    if STATUS_LOG.exists():
        with open(STATUS_LOG, "r") as f:
            return json.load(f)
    return {"module": "-", "timestamp": "-", "status": "-"}

def load_repair_matrix():
    if REPAIR_MATRIX_JSON.exists():
        return pd.read_json(REPAIR_MATRIX_JSON)
    return pd.DataFrame()

status_entry = load_status_log()
stream_logs = load_logs(STREAM_LOG)
autofix_logs = load_logs(AUTO_FIX_LOG)

# === Timeline Diagnostic ===
st.markdown("### 📍 Timeline Ανάλυση Logs")
if stream_logs:
    df = pd.DataFrame(stream_logs)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = px.scatter(df, x="timestamp", y="module", color="status",
                         title="📈 Watchdog Events Over Time",
                         height=400)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Δεν υπάρχουν δεδομένα stream log.")

# === Anomaly Detection ===
st.markdown("### ⚠️ Εντοπισμός Ανωμαλιών")
if stream_logs:
    df = pd.DataFrame(stream_logs)
    df['status_num'] = df['status'].map({'created': 1, 'modified': 2, 'deleted': -1, 'error': -2, 'failed': -3}).fillna(0)
    df['module_code'] = df['module'].astype('category').cat.codes
    if len(df) > 5:
        clf = IsolationForest(contamination=0.2)
        X = df[['status_num', 'module_code']].values
        preds = clf.fit_predict(X)
        df['anomaly'] = preds

        anomaly_df = df[df['anomaly'] == -1]
        if not anomaly_df.empty:
            st.error("Εντοπίστηκαν ανωμαλίες:")
            st.dataframe(anomaly_df[['timestamp', 'module', 'status']])
        else:
            st.success("Δεν εντοπίστηκαν ανωμαλίες.")
    else:
        st.info("Ανεπαρκή δεδομένα για ανάλυση.")

# === AutoFix Tracking ===
st.markdown("### 🤖 Ανάλυση AI AutoFix Επεμβάσεων")
if autofix_logs:
    fix_texts = [entry.get("raw", str(entry)) for entry in autofix_logs[-10:]]
    for txt in fix_texts:
        st.code(txt)
else:
    st.warning("Δεν υπάρχουν δεδομένα autofix log.")

# === Diagnostic Summary ===
st.markdown("### 🧠 Γενική Επισκόπηση Hypervisor")
col1, col2, col3 = st.columns(3)
col1.metric("📦 Τελευταίο Module", status_entry.get("module", "-"))
col2.metric("🕐 Χρόνος", status_entry.get("timestamp", "-"))
col3.metric("📊 Κατάσταση", status_entry.get("status", "-"))

# === Heatmap History ===
st.markdown("### 🌡️ Ιστορική Θερμική Χαρτογράφηση Module Καταστάσεων")
if stream_logs:
    df = pd.DataFrame(stream_logs)
    if 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        pivot_df = df.pivot_table(index='module', columns='date', values='status', aggfunc='count', fill_value=0)
        fig_heat = px.imshow(pivot_df, text_auto=True, color_continuous_scale='Viridis',
                             title='📊 Κατανομή Καταστάσεων Module Ανά Ημερομηνία')
        st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.warning("Δεν υπάρχουν δεδομένα για heatmap.")

# === Smart Repair Visualizer ===
st.markdown("### 🔧 Smart Repair Visualizer")
repair_df = load_repair_matrix()
if not repair_df.empty:
    st.dataframe(repair_df)
    fig1 = px.bar(repair_df, x="module", y="frequency", title="🔁 Συχνότητα Αναγκών Επισκευής")
    fig2 = px.bar(repair_df, x="module", y="failure_rate", title="⚠️ Failure Rate per Module")
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Δεν υπάρχουν δεδομένα για smart repair matrix.")