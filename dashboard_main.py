# dashboard_main.py

import streamlit as st

st.set_page_config(
    page_title="KINO Project AI - Dashboard",
    layout="wide",
    page_icon="🎯"
)

# ================================
# 🔹 HEADER
# ================================
st.markdown("## ✅ KINO Project AI – Modular Dashboard")
st.markdown("Ενεργοποίησε δυναμικά οποιοδήποτε module του project από την πλαϊνή μπάρα ➡️")

# ================================
# 🔸 SIDEBAR
# ================================
st.sidebar.title("🎯 Επιλογή Modules")
selected_module = st.sidebar.radio(
    "Διάλεξε λειτουργία:",
    [
        "📊 Heatmap Viewer",
        "📈 Prediction Engine",
        "🧠 Self-Analysis Panel",
        "📦 Modules Overview",
        "📡 Telegram Alerts",
        "🔍 Watchdog Monitor",
        "🎨 Visual Pattern Maps",
        "💡 Harmonic AI Button"
    ]
)

# ================================
# 🔹 MODULE LOADER
# ================================
try:
    if selected_module == "📊 Heatmap Viewer":
        from module_1_heatmap_module import show_heatmap
        show_heatmap()

    elif selected_module == "📈 Prediction Engine":
        from module_2_prediction_engine import run_prediction
        run_prediction()

    elif selected_module == "🧠 Self-Analysis Panel":
        from module_3_self_analysis_panel import show_self_analysis
        show_self_analysis()

    elif selected_module == "📦 Modules Overview":
        from module_4_modules_overview import show_modules_status
        show_modules_status()

    elif selected_module == "📡 Telegram Alerts":
        from module_5_telegram_test_alert import send_test_alert
        send_test_alert()

    elif selected_module == "🔍 Watchdog Monitor":
        from module_6_watchdog_monitor import run_watchdog_panel
        run_watchdog_panel()

    elif selected_module == "🎨 Visual Pattern Maps":
        from module_7_visual_pattern_map import show_visual_map
        show_visual_map()

    elif selected_module == "💡 Harmonic AI Button":
        from super_harmonic_engine import activate_harmonic_ai
        activate_harmonic_ai()

except Exception as e:
    st.error(f"⚠️ Σφάλμα κατά την εκτέλεση του module: {e}")
