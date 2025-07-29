import streamlit as st
import random

def run_prediction():
    st.subheader("📈 Prediction Engine – Demo")
    seed = st.slider("Seed (για αναπαραγωγή):", 0, 1000, 42)
    random.seed(seed)
    numbers = random.sample(range(1, 81), 20)
    st.write("🎯 Προτεινόμενοι αριθμοί:")
    st.success(sorted(numbers))
