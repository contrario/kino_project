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

# === Root Cause Estimator ===
st.markdown("### 🧠 Root Cause Estimator (Prototype)")
if stream_logs:
    df = pd.DataFrame(stream_logs)
    issues = df[df['status'].isin(['error', 'failed'])]
    if not issues.empty:
        cause_summary = issues['module'].value_counts().head(5)
        st.write("🔎 Top πιθανά modules αιτίας αποτυχίας:")
        st.bar_chart(cause_summary)
    else:
        st.success("Δεν υπάρχουν κρίσιμες αποτυχίες.")

# === Dependency Graph ===
st.markdown("### 🔗 Γράφημα Εξάρτησης Modules")
if stream_logs:
    G = nx.DiGraph()
    df = pd.DataFrame(stream_logs)
    module_list = df['module'].unique()
    for i in range(len(module_list) - 1):
        G.add_edge(module_list[i], module_list[i + 1])
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), hoverinfo='none', mode='lines')
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=list(G.nodes()),
        marker=dict(size=10, color='skyblue'), textposition='top center')
    fig_dep = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='🧬 Module Dependency Graph',
                            showlegend=False, hovermode='closest'))
    st.plotly_chart(fig_dep, use_container_width=True)

# === Smart AI Recommendation Panel ===
st.markdown("### 🧠 Smart AI Recommender Panel")
# === Dynamic Pipeline DAG Map ===
st.markdown("### 🔀 Dynamic Pipeline DAG Map")

def build_dynamic_dag(df):
    G_dag = nx.DiGraph()
    for i in range(len(df) - 1):
        src = df.iloc[i]['module']
        dst = df.iloc[i + 1]['module']
        if src != dst:
            G_dag.add_edge(src, dst)

    pos = nx.spring_layout(G_dag, seed=42)
    edge_trace = go.Scatter(x=[], y=[], line=dict(width=1, color='#888'), mode='lines')
    for edge in G_dag.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.x += [x0, x1, None]
        edge_trace.y += [y0, y1, None]

    node_x, node_y, node_color, node_text = [], [], [], []
    for node in G_dag.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        status = df[df['module'] == node]['status'].iloc[-1]
        if status in ['created', 'modified']:
            color = '#00CC96'
        elif status in ['error', 'failed']:
            color = '#EF553B'
        else:
            color = '#636EFA'

        node_color.append(color)
        node_text.append(f"{node}: {status}")

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=node_text,
        marker=dict(size=14, color=node_color), textposition='top center'
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='🔁 DAG Pipeline Map',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                    ))
    return fig

if stream_logs:
    df = pd.DataFrame(stream_logs)
    if 'module' in df.columns and 'status' in df.columns:
        dag_fig = build_dynamic_dag(df)
        st.plotly_chart(dag_fig, use_container_width=True)
    else:
        st.warning("⚠️ Το log δεν περιέχει module/status.")
else:
    st.info("🕐 Δεν υπάρχουν δεδομένα για pipeline DAG.")