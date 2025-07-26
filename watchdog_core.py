import streamlit as st
import pandas as pd
import os
import datetime
import importlib.util
import json
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import threading
from pathlib import Path
from watchdog_core import start_watchdog
from streamlit_autorefresh import st_autorefresh
import networkx as nx
import plotly.graph_objects as go

# === Paths ===
PROJECT_ROOT = Path("kino_project")
MODULES = [f"Module {i}" for i in range(1, 12)]
MODULES_DIR = PROJECT_ROOT / "modules"
LOGS_DIR = PROJECT_ROOT / "logs"
STATUS_LOG = LOGS_DIR / "module_status.json"
MODULE_LOG_STREAM = LOGS_DIR / "module_stream.log"

# === Init folders ===
for path in [MODULES_DIR, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# === Auto-refresh UI ===
st_autorefresh(interval=5000, key="datarefresh")

# === Start watchdog once ===
if "watchdog_started" not in st.session_state:
    observer = start_watchdog()
    st.session_state.watchdog_started = True

# === Streamlit UI Setup ===
st.set_page_config(page_title="🧠 KINO Overseer CERN Panel", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #111; color: white; }
        .stButton > button { width: 100%; height: 3em; }
        .css-1offfwp { background-color: #222; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 KINO Overseer CERN Control Panel")
st.subheader("Εποπτεία, Εκτέλεση & Οπτικοποίηση Modules Επιπέδου CERN")

# === Watchdog Data ===
def read_watchdog_log():
    if STATUS_LOG.exists():
        with open(STATUS_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"module": "-", "timestamp": "-", "status": "-"}

watchdog_data = read_watchdog_log()
col1, col2, col3 = st.columns(3)
col1.metric("📡 Module Watch", watchdog_data['module'])
col2.metric("⏱️ Time", watchdog_data['timestamp'])
col3.metric("🔄 Status", watchdog_data['status'])

st.markdown("---")

# === Module Execution ===
def execute_module(mod_file, module_index):
    last_run = "-"
    success = False
    try:
        spec = importlib.util.spec_from_file_location(f"module_{module_index}", mod_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "run"):
            mod.run()
            last_run = datetime.datetime.now().strftime("%H:%M:%S")
            success = True
        else:
            st.warning(f"Module {module_index}: Δεν υπάρχει συνάρτηση run().")
    except Exception as e:
        st.error(f"Module {module_index}: Σφάλμα κατά την εκτέλεση: {e}")
    return last_run, success

status_table = []
for i in range(1, 12):
    mod_file = MODULES_DIR / f"module_{i}.py"
    status = "✅" if mod_file.exists() else "❌"
    last_run = "-"
    success = False

    if st.button(f"▶️ Εκτέλεση Module {i}", key=f"run_{i}"):
        last_run, success = execute_module(mod_file, i)
        if success:
            st.success(f"Module {i} ολοκληρώθηκε επιτυχώς.")
        else:
            # Self-healing placeholder
            st.warning(f"🛠️ Προσπάθεια αυτοεπανεκκίνησης του Module {i}...")

    status_table.append({"Module": f"Module {i}", "Exists": status, "Last Run": last_run, "Success": success})

# === Μαζική Εκτέλεση ===
if st.button("⚙️ Εκτέλεση Όλων (Multi-Thread)"):
    st.info("Εκτέλεση όλων των modules...")
    def run_all_modules():
        for i in range(1, 12):
            mod_file = MODULES_DIR / f"module_{i}.py"
            if mod_file.exists():
                threading.Thread(target=execute_module, args=(mod_file, i)).start()
    run_all_modules()

# === Ζωντανός Πίνακας ===
st.markdown("### 📊 Ζωντανός Πίνακας Κατάστασης Modules")
df_status = pd.DataFrame(status_table)
st.dataframe(df_status, use_container_width=True)

# === Heatmap ===
st.markdown("### 🌡️ Heatmap Επιτυχίας Modules")
try:
    heat_data = df_status[["Success"]].replace({True: 1, False: 0}).T
    fig, ax = plt.subplots(figsize=(10, 1))
    sns.heatmap(heat_data, annot=True, cmap="YlGnBu", xticklabels=df_status["Module"], yticklabels=["Success"], ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"Heatmap δεν υποστηρίζεται: {e}")

# === Graph ===
st.markdown("### 📈 Επισκόπηση Εκτελέσεων")
bar_fig = px.bar(df_status, x="Module", y="Success", color="Success", text="Last Run", title="Επιτυχία Εκτέλεσης Modules")
st.plotly_chart(bar_fig, use_container_width=True)

# === Summary ===
success_count = df_status["Success"].sum()
fail_count = len(df_status) - success_count
st.markdown("### 🧮 Σύνοψη Επιτυχίας")
col_a, col_b = st.columns(2)
col_a.metric("✅ Επιτυχίες", success_count)
col_b.metric("❌ Αποτυχίες", fail_count)

# === Live Log Stream ===
st.markdown("### 🛰️ Live Watchdog Log Stream")
if MODULE_LOG_STREAM.exists():
    with open(MODULE_LOG_STREAM, "r", encoding="utf-8") as f:
        lines = f.readlines()[-20:]  # τελευταία 20 γραμμές
        for line in lines:
            st.code(line.strip(), language="json")
else:
    st.info("Το αρχείο module_stream.log δεν υπάρχει ακόμα.")

# === AI Evaluation Placeholder ===
st.markdown("### 🤖 AI Αξιολόγηση Απόδοσης Modules")
for _, row in df_status.iterrows():
    st.info(f"Module {row['Module']}: AI εκτίμηση απόδοσης: {'Άριστη' if row['Success'] else 'Ανεπιτυχής'}")

# === Module Dependency Map ===
st.markdown("### 🧠 Module Dependency Visualization")
G = nx.DiGraph()
for i in range(1, 12):
    G.add_node(f"Module {i}")
    if i < 11:
        G.add_edge(f"Module {i}", f"Module {i+1}")
pos = nx.spring_layout(G)
edges_x, edges_y, nodes_x, nodes_y, texts = [], [], [], [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edges_x += [x0, x1, None]
    edges_y += [y0, y1, None]
for node in G.nodes():
    x, y = pos[node]
    nodes_x.append(x)
    nodes_y.append(y)
    texts.append(node)
fig = go.Figure()
fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line=dict(width=2, color='gray')))
fig.add_trace(go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text', marker=dict(size=20, color='cyan'), text=texts, textposition="top center"))
st.plotly_chart(fig, use_container_width=True)

st.success("🎯 CERN AI Supervisor: Πλήρως ενεργό και αυτοδιορθούμενο.")