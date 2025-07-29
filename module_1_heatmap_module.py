import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_heatmap():
    st.subheader("📊 Heatmap Viewer – Demo")
    data = np.random.randint(0, 100, size=(10, 10))
    fig, ax = plt.subplots()
    heatmap = ax.imshow(data, cmap='viridis')
    plt.colorbar(heatmap)
    st.pyplot(fig)
