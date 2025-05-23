
import streamlit as st
import pandas as pd
import math

def calcular_velocidad(Q, D):
    area = math.pi * (D/2)**2
    return Q / area

def calcular_perdida_hf(Q, L, D, C):
    return 10.67 * L * (Q**1.85) / ((C**1.85) * (D**4.87))

def sugerir_diametro(Q, v_objetivo=1.0):
    area = Q / v_objetivo
    D = (4 * area / math.pi) ** 0.5
    return D

st.title("📊 Cálculo de Pérdidas por Hazen-Williams")

uploaded_file = st.file_uploader("Carga un archivo Excel con los datos de la red", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📄 Datos de Entrada")
    st.dataframe(df)

    resultados = []

    for index, row in df.iterrows():
        Q = row["Caudal (m3/s)"]
        L = row["Longitud (m)"]
        D = row["Diametro (m)"]
        C = row["C"]
        tramo = row["Tramo"]

        hf = calcular_perdida_hf(Q, L, D, C)
        v = calcular_velocidad(Q, D)
        D_sugerido = sugerir_diametro(Q)

        resultados.append({
            "Tramo": tramo,
            "Pérdida (m)": hf,
            "Velocidad (m/s)": v,
            "Diámetro sugerido (m)": D_sugerido
        })

    resultado_df = pd.DataFrame(resultados)

    def resaltar_velocidad(val):
        if val < 0.9 or val > 1.1:
            return 'color: red'
        return ''

    st.subheader("📈 Resultados por Tramo")
    st.dataframe(resultado_df.style.applymap(resaltar_velocidad, subset=["Velocidad (m/s)"]))

