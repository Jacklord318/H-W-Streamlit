
import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="Red Hidráulica Hazen-Williams", layout="wide")
st.title("Visualización y Cálculo Hidráulico - Hazen-Williams")

archivo = st.file_uploader("📂 Sube el archivo Excel con la red hidráulica", type=["xlsx"])

if archivo:
    df_tramos = pd.read_excel(archivo, sheet_name="tramos")
    st.subheader("📋 Tabla de Tramos")
    st.dataframe(df_tramos)

    st.subheader("🧮 Cálculo de Pérdidas Hazen-Williams")

    def hazen_williams(Q, L, D, C):
        v = 0.849 * (C ** -1.85) * (Q ** 1.85) / (D ** 4.87)
        hf = L * v
        return hf

    df_tramos["hf (m)"] = df_tramos.apply(
        lambda row: hazen_williams(row["Caudal (m3/s)"], row["Longitud (m)"], row["Diámetro (m)"], row["C"]), axis=1
    )
    st.dataframe(df_tramos[["Nodo Inicial", "Nodo Final", "hf (m)"]])

    st.subheader("📈 Visualización de Red (Tipo Grafo)")

    nodos = {}
    for _, row in df_tramos.iterrows():
        nodos[row["Nodo Inicial"]] = Node(id=row["Nodo Inicial"], label=row["Nodo Inicial"])
        nodos[row["Nodo Final"]] = Node(id=row["Nodo Final"], label=row["Nodo Final"])

    edges = []
    for _, row in df_tramos.iterrows():
        edges.append(Edge(
            source=row["Nodo Inicial"],
            target=row["Nodo Final"],
            label=f'{row["Caudal (m3/s)"]} m³/s\n{row["hf (m)"]:.2f} m'
        ))

    config = Config(
        width=900,
        height=600,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=True,
        node={"labelProperty": "label"},
        link={"labelProperty": "label"},
    )

    agraph(list(nodos.values()), edges, config)
