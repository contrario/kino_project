import streamlit as st
import subprocess
import json
from pathlib import Path

st.set_page_config(page_title="Code Quality Evaluator", layout="centered")

st.title("🧪 Code Quality Evaluator")

if st.button("🔍 Τρέξε αξιολόγηση ποιότητας κώδικα"):
    try:
        result = subprocess.run(["python", "code_quality_evaluator.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ Ο έλεγχος ολοκληρώθηκε!")
        else:
            st.error(f"⚠️ Σφάλμα: {result.stderr}")
    except Exception as e:
        st.error(f"🚨 Σφάλμα εκτέλεσης: {e}")

report_path = Path("logs/code_quality_report.json")
if report_path.exists():
    st.subheader("📋 Αποτελέσματα Αναφοράς")
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        st.markdown(f"""
        **🗂 Αρχείο**: `{entry['filename']}`  
        📄 Γραμμές: {entry['line_count']}  
        🔧 Συναρτήσεις: {entry['function_count']}  
        🏷 Κλάσεις: {entry['class_count']}  
        📚 Docstrings: {'Ναι' if entry['has_docstrings'] else 'Όχι'}  
        🔡 Τύποι: {'Ναι' if entry['has_type_annotations'] else 'Όχι'}  
        ✅ Syntax OK: {'Ναι' if entry['syntax_ok'] else 'Όχι'}
        ---
        """)
else:
    st.info("ℹ️ Δεν έχει δημιουργηθεί ακόμη αναφορά.")
