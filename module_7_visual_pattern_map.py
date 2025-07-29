import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_visual_map():
    st.subheader("🎨 Visual Pattern Map – Demo")
    x = np.linspace(-2, 2, 400)
    y = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X ** 2 + Y ** 2)
    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, cmap='inferno')
    st.pyplot(fig)
