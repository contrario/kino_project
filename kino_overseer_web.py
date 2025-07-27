
import streamlit as st
from modules import watchdog_panel

# Title & Styling
st.set_page_config(page_title="KINO Overseer Web", layout="wide")
st.title("🎛️ KINO Overseer Web Control Panel")

# Sidebar Navigation
st.sidebar.title("📂 Modules")
selected_module = st.sidebar.radio("Επιλέξτε λειτουργία:", ["🔍 Watchdog Panel", "📊 Coming Soon"])

# Dynamic Content
if selected_module == "🔍 Watchdog Panel":
    watchdog_panel.render()

elif selected_module == "📊 Coming Soon":
    st.info("Περισσότερα modules θα προστεθούν σύντομα.")

# Footer
st.markdown("---")
st.markdown("🎯 **ARVIA SYSTEMS — Unified AI Ecosystem** | Powered by Da Vinci Protocol 🚀")
