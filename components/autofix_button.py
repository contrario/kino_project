
import streamlit as st
import subprocess

def display_autofix_button():
    st.markdown("---")
    st.header("🛠️ AutoFix Engine")

    if st.button("⚙️ Εκτέλεσε AutoFix Overlord"):
        with st.spinner("🔄 Επιδιόρθωση σε εξέλιξη..."):
            try:
                result = subprocess.run(
                    ["python", "kino_project/src/kino_autofix_overlord.py"],
                    capture_output=True, text=True
                )
                st.success("✅ AutoFix ολοκληρώθηκε!")
                st.code(result.stdout)
            except Exception as e:
                st.error(f"❌ Σφάλμα κατά την εκτέλεση: {e}")
