from __future__ import annotations

import streamlit as st
import os
import subprocess
from datetime import datetime

# ==== Βασικές Ρυθμίσεις ====
st.set_page_config(page_title="KINO OS Kernel Integrator", layout="wide")

# ==== Header ====
st.markdown("## 🧠 **KINO OS Kernel Integrator**")
st.markdown("### Ολοκληρωμένος Πυρήνας του Prediction System")
st.markdown("Αυτό το dashboard λειτουργεί ως **κεντρικός ενοποιητής** όλων των υποσυστημάτων του KINO Prediction System. Παρακάτω εμφανίζεται λίστα με όλα τα ενεργά modules:")

# ==== Εντοπισμός ενεργών modules ====
modules_dir = "modules"
found_modules = []

if os.path.exists(modules_dir):
    for item in os.listdir(modules_dir):
        item_path = os.path.join(modules_dir, item)
        if item.endswith(".py") or os.path.isdir(item_path):
            found_modules.append(item)

if found_modules:
    st.success(f"✅ Εντοπίστηκαν {len(found_modules)} ενεργά modules:")
    for mod in found_modules:
        st.markdown(f"- {mod}")
else:
    st.error("⚠️ Δεν εντοπίστηκαν ενεργά modules στον φάκελο `modules/`.")

# ==== Κουμπί Εκκίνησης Περιβάλλοντος ====
st.markdown("---")
st.subheader("⚙️ Περιβάλλον Συστήματος")

if st.button("🚀 Εκκίνηση Περιβάλλοντος"):
    try:
        result = subprocess.run(["python", "initialize_kernel_env.py"], capture_output=True, text=True)

        output = (result.stdout or '') + "\n" + (result.stderr or '')
        st.text_area("📤 Αποτέλεσμα εκτέλεσης:", output, height=200)

        # Καταγραφή στο kernel_log.txt
        with open("kernel_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n{output}\n{'='*40}\n")

    except Exception as e:
        st.error(f"Σφάλμα κατά την εκκίνηση περιβάλλοντος: {e}")
        with open("kernel_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\nERROR: {str(e)}\n{'='*40}\n")

# ==== Προβολή kernel_log.txt ====
st.markdown("---")
st.subheader("📊 Κεντρικός Έλεγχος & Κατάσταση")

log_path = "kernel_log.txt"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        log_content = f.read()
    st.text_area("📄 Kernel Log", log_content, height=250)
else:
    st.warning("❌ Δεν βρέθηκε αρχείο kernel_log.txt")

# ==== Footer ====
st.sidebar.markdown("📅 **Συστήματος**")
st.sidebar.markdown(f"Ημερομηνία: {datetime.today().strftime('%d/%m/%Y')}")
