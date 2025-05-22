
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

materials = {
    "Acero sin costura": 120,
    "Acero soldado en espiral": 100,
    "Cobre sin costura": 150,
    "Concreto": 110,
    "Fibra de vidrio": 150,
    "Hierro fundido": 100,
    "Hierro dúctil con revestimiento": 140,
    "Hierro galvanizado": 100,
    "Polietileno": 140,
    "PVC": 150,
}

def calculate_diameter(Q_m3s, target_velocity=1.0):
    return np.sqrt((4 * Q_m3s) / (np.pi * target_velocity))

def calculate_velocity(Q_m3s, D):
    return (4 * Q_m3s) / (np.pi * D**2)

def calculate_head_loss(Q_m3s, D, C, L=1000):
    Q_lps = Q_m3s * 1000
    D_mm = D * 1000
    hf_per_km = (10.67 * Q_lps**1.852) / (C**1.852 * D_mm**4.87)
    return hf_per_km * (L / 1000)

st.set_page_config(page_title="Diseño Hidráulico - Hazen-Williams", layout="wide")
st.title("Diseño Hidráulico usando la fórmula de Hazen-Williams")

col1, col2 = st.columns(2)

with col1:
    flow = st.number_input("Caudal", value=10.0, min_value=0.1)
    unit = st.selectbox("Unidad", options=["lps", "m3s"])
    Q_m3s = flow / 1000 if unit == "lps" else flow

with col2:
    material = st.selectbox("Material de la tubería", options=list(materials.keys()))
    default_C = materials[material]
    custom_C = st.number_input("Coeficiente de rugosidad C", value=default_C, min_value=1)
    length = st.number_input("Longitud del tramo (m)", value=1000)

D = calculate_diameter(Q_m3s)
v = calculate_velocity(Q_m3s, D)
hf = calculate_head_loss(Q_m3s, D, custom_C, length)

st.markdown("### Resultados")
st.write(f"- Diámetro recomendado: **{D:.3f} m**")
st.write(f"- Velocidad: **{v:.2f} m/s**")
st.write(f"- Pérdida de carga: **{hf:.2f} m**")

diams = np.arange(0.02, 0.27, 0.005)
velocities = [calculate_velocity(Q_m3s, d) for d in diams]
head_losses = [calculate_head_loss(Q_m3s, d, custom_C, length) for d in diams]

fig, ax1 = plt.subplots(figsize=(10, 5))

color1 = "tab:blue"
ax1.set_xlabel("Diámetro (m)")
ax1.set_ylabel("Velocidad (m/s)", color=color1)
ax1.plot(diams, velocities, label="Velocidad", color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = "tab:red"
ax2.set_ylabel("Pérdida de carga (m)", color=color2)
ax2.plot(diams, head_losses, label="Pérdida de carga", color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

fig.tight_layout()
st.pyplot(fig)
