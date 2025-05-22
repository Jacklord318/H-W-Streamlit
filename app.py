
import streamlit as st
import math
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

def calculate_diameter(Q_m3s, target_velocity=1):
    return math.sqrt((4 * Q_m3s) / (math.pi * target_velocity))

def calculate_velocity(Q_m3s, D):
    return (4 * Q_m3s) / (math.pi * D**2)

def calculate_head_loss(Q_m3s, D, C, L=1000):
    Q_lps = Q_m3s * 1000
    D_mm = D * 1000
    hf_per_km = (10.67 * Q_lps**1.852) / (C**1.852 * D_mm**4.87)
    return hf_per_km * (L / 1000)

st.title("Cálculo con Hazen-Williams")

flow = st.number_input("Caudal", min_value=0.0, value=10.0)
unit = st.selectbox("Unidad", options=["lps", "m3s"])
material = st.selectbox("Material de la tubería", options=list(materials.keys()))
length = st.number_input("Longitud del tramo (m)", min_value=0, value=1000)

C = materials[material]
Q_m3s = flow / 1000 if unit == "lps" else flow
D = calculate_diameter(Q_m3s)
velocity = calculate_velocity(Q_m3s, D)
head_loss = calculate_head_loss(Q_m3s, D, C, length)

st.write(f"**Coeficiente C:** {C}")
st.write(f"**Diámetro recomendado:** {D:.3f} m")
st.write(f"**Velocidad:** {velocity:.2f} m/s")
st.write(f"**Pérdida de carga:** {head_loss:.2f} m")

# Gráfica
diameters = [0.02 + i * 0.005 for i in range(50)]
velocities = [calculate_velocity(Q_m3s, d) for d in diameters]

df = pd.DataFrame({
    "Diámetro (m)": diameters,
    "Velocidad (m/s)": velocities
})

st.line_chart(df.set_index("Diámetro (m)"))
