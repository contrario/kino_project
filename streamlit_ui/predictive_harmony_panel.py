import streamlit as st

st.set_page_config(page_title="Predictive Harmony Panel", layout="wide")

st.title("🎯 Predictive Harmony Panel – KINO System")
st.subheader("Σχεδίασε δελτία ΚΙΝΟ με ευφυΐα και ακρίβεια.")

# Επιλογή αριθμών
num_selection = st.slider("Επίλεξε πλήθος αριθμών:", 5, 10, 7)
selected_numbers = st.multiselect(
    "Επίλεξε τους αριθμούς σου (1-80):", list(range(1, 81)), max_selections=num_selection
)

# Επιλογή συστήματος
system_type = st.selectbox("Επέλεξε σύστημα:", ["Απλό", "Πλήρες", "Μειωμένο", "Τυχαίο"])

# Εισαγωγή αξίας δελτίου
ticket_value = st.number_input("Αξία δελτίου (€):", min_value=0.5, step=0.5, format="%.2f")

# Υπολογισμός πιθανού κέρδους (προσομοιωτικό)
if st.button("💰 Υπολόγισε Κέρδος"):
    possible_win = ticket_value * (num_selection * 1.7)
    st.success(f"Πιθανό Κέρδος: €{possible_win:.2f}")

# Προσομοίωση υποβολής
if st.button("🎟️ Υποβολή Δελτίου"):
    if len(selected_numbers) != num_selection:
        st.warning("Πρέπει να επιλέξεις ακριβώς τον αριθμό αριθμών που ορίζει το slider.")
    else:
        st.success(f"Το δελτίο σου με {num_selection} αριθμούς υποβλήθηκε επιτυχώς!")
