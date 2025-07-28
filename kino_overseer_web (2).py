
import streamlit as st
from components.autofix_button import render_autofix_button

def main():
    st.set_page_config(page_title="KINO Overseer", layout="wide")
    st.title("🎯 KINO Project – Overseer Panel")
    st.markdown("---")

    # Κουμπί αυτοδιόρθωσης (mobile-friendly)
    render_autofix_button()

    # Placeholder για μελλοντικά modules (tabs, charts, κλπ.)
    st.info("Περισσότερες λειτουργίες έρχονται σύντομα...")

if __name__ == "__main__":
    main()
