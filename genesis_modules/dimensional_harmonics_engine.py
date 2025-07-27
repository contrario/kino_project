import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def generate_harmonic_field(size=100, frequency=5, phase_shift=0.0):
    x = np.linspace(0, 2 * np.pi, size)
    y = np.linspace(0, 2 * np.pi, size)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(frequency * X + phase_shift) + np.cos(frequency * Y + phase_shift)
    return X, Y, Z


def plot_harmonic_field(X, Y, Z, title="Dimensional Harmonics Visualization"):
    fig, ax = plt.subplots(figsize=(6, 6))
    contour = ax.contourf(X, Y, Z, cmap="viridis")
    ax.set_title(title)
    ax.set_xlabel("X-axis (Harmonics)")
    ax.set_ylabel("Y-axis (Harmonics)")
    plt.colorbar(contour, ax=ax, label="Amplitude")
    return fig


def run():
    st.subheader("🌀 Dimensional Harmonics Engine")

    st.markdown("This module visualizes synthetic dimensional harmonic fields based on adjustable parameters.")

    with st.sidebar.expander("⚙️ Harmonic Settings", expanded=True):
        size = st.slider("Resolution", 50, 500, 200, step=10)
        frequency = st.slider("Frequency", 1, 20, 5)
        phase_shift = st.slider("Phase Shift", 0.0, 2 * np.pi, 0.0, step=0.1)

    X, Y, Z = generate_harmonic_field(size=size, frequency=frequency, phase_shift=phase_shift)
    fig = plot_harmonic_field(X, Y, Z)

    st.pyplot(fig)
