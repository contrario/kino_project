import os
import sys
import ast
import json
import time
import logging
import requests
import streamlit as st
from datetime import datetime
from github import Github
from typing import List

# === ΡΥΘΜΙΣΕΙΣ (συμπλήρωσε τα δικά σου) ===
GITHUB_TOKEN = "your_github_token_here"
REPO_NAME = "contrario/kino_project_ai"
TELEGRAM_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "6046304883"

# === ΑΡΧΙΚΟΠΟΙΗΣΗ ===
logging.basicConfig(level=logging.INFO)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# === 🔍 AST SCANNER για deprecated ή προβληματικά στοιχεία ===
class CodeInspector(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "watchdog":
                self.issues.append(("Deprecated import: watchdog", node.lineno))
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.attr == "_scriptrunner":
            self.issues.append(("Deprecated attribute: _scriptrunner", node.lineno))
        self.generic_visit(node)

# === 🔧 ΕΦΑΡΜΟΓΗ FIXES ===
def apply_fixes_to_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    inspector = CodeInspector()
    inspector.visit(tree)

    if not inspector.issues:
        return False, []

    new_lines = source.splitlines()
    for issue, lineno in inspector.issues:
        if "watchdog" in issue:
            new_lines[lineno - 1] = "# FIXED: Replaced watchdog import\nimport watchdog.events as events"
        if "_scriptrunner" in issue:
            for i, line in enumerate(new_lines):
                if "_scriptrunner" in line:
                    new_lines[i] = line.replace("session._scriptrunner is not None", "hasattr(session, '_scriptrunner')")

    fixed_code = "\n".join(new_lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    return True, inspector.issues

# === 🔍 ΕΝΤΟΠΙΣΜΟΣ ΑΡΧΕΙΩΝ ===
def get_python_files(root_path="."):
    py_files = []
    for root, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

# === 📤 ΤΗΛΕΓΡΑΦΙΚΗ ΕΙΔΟΠΟΙΗΣΗ ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Telegram error: {e}")

# === 🧠 STREAMLIT INTERFACE ===
def launch_ui():
    st.title("🧬 Genesis Forge AI")
    st.markdown("### Αυτόματη Επιδιόρθωση Python Κώδικα για το KINO Project")
    if st.button("🔍 Σάρωση και Επιδιόρθωση Τώρα"):
        st.info("Εκτελείται σάρωση...")

        files = get_python_files(".")
        fixed = 0
        for file in files:
            result, issues = apply_fixes_to_file(file)
            if result:
                st.success(f"✔️ {file} - Διορθώθηκε!")
                send_telegram_message(f"[Genesis AI] Διορθώθηκε το: {file}")
                fixed += 1

        if fixed == 0:
            st.warning("🔎 Δεν εντοπίστηκαν προβλήματα.")
        else:
            st.balloons()
            st.success(f"✅ Ολοκληρώθηκε. Διορθώθηκαν {fixed} αρχεία.")

# === MAIN ===
if __name__ == "__main__":
    if "streamlit" in sys.argv[0]:
        launch_ui()
    else:
        print("💡 Για εκκίνηση UI: streamlit run genesis_forge_ai.py")
