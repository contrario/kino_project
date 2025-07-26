
import streamlit as st
import time

# Global status dict for modules
status = {i: "Idle" for i in range(1, 12)}
last_run = {i: "-" for i in range(1, 12)}
success = {i: False for i in range(1, 12)}

st.set_page_config(page_title="KINO Overseer Web Panel", layout="wide")

# === Sidebar με κουμπί Force Sync ===
with st.sidebar:
    st.header("🔧 Διαχείριση")
    if st.button("🔁 Force Sync All Modules"):
        st.session_state["sync_trigger"] = True

# === Τίτλος ===
st.markdown("# 🎯 KINO Overseer Web Panel")
st.markdown("Ολοκληρωμένη Streamlit υποδομή επιπέδου CERN")
st.markdown("**Αυτοδιόρθωση και παρακολούθηση όλων των module (1-11)**")

# === Tab Selection ===
tabs = st.tabs(["Module " + str(i) for i in range(1, 12)])

# === Συνάρτηση εκτέλεσης module ===
def run_module(module_id):
    with tabs[module_id - 1]:
        st.subheader(f"⚙️ Module {module_id}")
        st.code(f"🚀 Running Module {module_id}...", language="markdown")
        status[module_id] = "Running"
        time.sleep(1.5)  # simulate processing
        status[module_id] = "Idle"
        last_run[module_id] = time.strftime("%Y-%m-%d %H:%M:%S")
        success[module_id] = True
        st.success(f"Module {module_id} ολοκληρώθηκε.")

# === Δημιουργία κουμπιών ===
for i in range(1, 12):
    with tabs[i - 1]:
        if st.button(f"🚀 Run Module {i}", key=f"btn_{i}"):
            run_module(i)

# === Force Sync Trigger ===
if st.session_state.get("sync_trigger", False):
    for i in range(1, 12):
        run_module(i)
    st.sidebar.success("✅ Όλα τα Modules εκτελέστηκαν")
    st.session_state["sync_trigger"] = False

# === Πίνακας επισκόπησης ===
st.markdown("---")
st.markdown("## 📊 Module Overview Dashboard (Live)")
st.dataframe({
    "Module": [f"Module {i}" for i in range(1, 12)],
    "Status": [status[i] for i in range(1, 12)],
    "Last Run": [last_run[i] for i in range(1, 12)],
    "Success": [success[i] for i in range(1, 12)],
})
