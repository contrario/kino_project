import subprocess
import json
from pathlib import Path
import streamlit as st

with st.expander("🧪 Code Quality Evaluator", expanded=False):
    st.markdown("Εκτελεί τον `code_quality_evaluator.py` και εμφανίζει τα αποτελέσματα.")

    if st.button("🔍 Τρέξε Code Quality"):
        with st.spinner("Εκτελείται..."):
            result = subprocess.run(["python", "code_quality_evaluator.py"], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ Ο έλεγχος ολοκληρώθηκε.")
            else:
                st.error(f"❌ Σφάλμα: {result.stderr}")

    report_path = Path("logs/code_quality_report.json")
    if report_path.exists():
        st.subheader("📋 Αναφορά Ποιότητας")
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            st.markdown(f"""
                #### 📁 `{entry['filename']}`
                - 📄 Γραμμές: `{entry['line_count']}`
                - 🔧 Συναρτήσεις: `{entry['function_count']}`
                - 🏷 Κλάσεις: `{entry['class_count']}`
                - 📚 Docstrings: `{"Ναι" if entry['has_docstrings'] else "Όχι"}`
                - 🔡 Τύποι: `{"Ναι" if entry['has_type_annotations'] else "Όχι"}`
                - ✅ Syntax OK: `{"Ναι" if entry['syntax_ok'] else "❌ Όχι"}`
                ---
            """)
    else:
        st.info("🔹 Δεν έχει παραχθεί ακόμα αναφορά. Πάτησε το κουμπί παραπάνω.")
