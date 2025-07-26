# multi_fixer_web.py – Streamlit-based Advanced Maintenance Tool

import os
import streamlit as st
import subprocess
import shutil
import time
from pathlib import Path

# --- SETTINGS ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = PROJECT_ROOT / "logs/multi_fixer.log"
REQUIRED_FOLDERS = ["outputs", "dashboards", "modules", "data", "logs"]
REQUIRED_FILES = ["initialize_kernel_env.py", "auto_fix_kernel.py"]

# --- HELPERS ---
def log(msg, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(DEFAULT_LOG, "a") as f:
        f.write(f"[{timestamp}] {level}: {msg}\n")


def fix_missing_folders():
    created = []
    for folder in REQUIRED_FOLDERS:
        path = PROJECT_ROOT / folder
        if not path.exists():
            path.mkdir(parents=True)
            created.append(folder)
            log(f"Created missing folder: {folder}")
    return created


def fix_missing_files():
    repaired = []
    templates_dir = PROJECT_ROOT / "templates"
    for file in REQUIRED_FILES:
        target_path = PROJECT_ROOT / file
        if not target_path.exists():
            template_path = templates_dir / file
            if template_path.exists():
                shutil.copy(template_path, target_path)
                repaired.append(file)
                log(f"Restored missing file: {file}")
    return repaired


def run_env_initialization():
    try:
        result = subprocess.run(["python", str(PROJECT_ROOT / "initialize_kernel_env.py")], capture_output=True, text=True)
        log("Ran initialize_kernel_env.py")
        return result.stdout + result.stderr
    except Exception as e:
        log(f"Initialization failed: {str(e)}", level="ERROR")
        return str(e)


def run_auto_fix_kernel():
    try:
        result = subprocess.run(["python", str(PROJECT_ROOT / "auto_fix_kernel.py")], capture_output=True, text=True)
        log("Ran auto_fix_kernel.py")
        return result.stdout + result.stderr
    except Exception as e:
        log(f"Auto fix kernel failed: {str(e)}", level="ERROR")
        return str(e)


# --- UI ---
st.set_page_config(page_title="Multi Fixer Tool", layout="wide")
st.title("🛠️ Multi Fixer Tool for KINO Prediction System")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Έλεγχος & Δημιουργία Φακέλων"):
        created = fix_missing_folders()
        if created:
            st.success(f"Δημιουργήθηκαν: {', '.join(created)}")
        else:
            st.info("Όλοι οι φάκελοι υπάρχουν ήδη.")

    if st.button("🧩 Έλεγχος & Αποκατάσταση Αρχείων"):
        repaired = fix_missing_files()
        if repaired:
            st.success(f"Αρχεία επαναφέρθηκαν: {', '.join(repaired)}")
        else:
            st.info("Όλα τα απαιτούμενα αρχεία είναι παρόντα.")

with col2:
    if st.button("🚀 Εκκίνηση Περιβάλλοντος"):
        output = run_env_initialization()
        st.text_area("Αποτελέσματα:", output, height=250)

    if st.button("🔧 Auto Kernel Fix"):
        output = run_auto_fix_kernel()
        st.text_area("Αποτελέσματα:", output, height=250)

st.markdown("---")

if st.checkbox("📜 Προβολή Log Αρχείου"):
    if DEFAULT_LOG.exists():
        with open(DEFAULT_LOG, "r") as f:
            st.code(f.read(), language="text")
    else:
        st.warning("Δεν βρέθηκε το αρχείο log.")
