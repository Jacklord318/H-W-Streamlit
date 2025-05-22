import streamlit as st
import pandas as pd

def calcular_perdida_hazen_williams(Q, L, D, C):
    v = 0.849 * (C ** -1.85) * (Q ** 1.85) / (D ** 4.87)
    hf = L * v
    return hf

st.set_page_config(layout="wide")
st.title("Red Hidráulica Cerrada - Cálculo con Hazen-Williams")

uploaded_file = st.file_uploader("Carga el archivo Excel con los tramos", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="tramos")
    st.write("Datos de entrada:", df)

    resultados = []
    for i, row in df.iterrows():
        hf = calcular_perdida_hazen_williams(row["Caudal (m3/s)"], row["Longitud (m)"], row["Diámetro (m)"], row["C"])
        resultados.append(hf)

    df["hf (m)"] = resultados
    st.write("Resultados con pérdidas por fricción:", df)

    st.line_chart(df.set_index("Nodo Final")[["hf (m)"]])