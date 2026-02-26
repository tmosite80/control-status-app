import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Control de Status Hora a Hora")

# Simulación backend
df = pd.DataFrame({
    "ID": [101,102,103,104],
    "DATE": ["2026-02-25"]*4,
    "HOUR": ["13:00","14:00","15:00","16:00"],
    "STATUS": ["","Showed Up","",""],
    "NAME": ["Juan","Ana","Luis","Maria"],
    "SUPERVISOR": ["Daniela","Daniela","Maria","Maria"]
})

# Filtros
col1, col2 = st.columns(2)

with col1:
    supervisor = st.selectbox("Supervisor", df["SUPERVISOR"].unique())

with col2:
    fecha = st.selectbox("Fecha", df["DATE"].unique())

df_filtrado = df[
    (df["SUPERVISOR"] == supervisor) &
    (df["DATE"] == fecha)
]

st.subheader("Editar STATUS")

opciones_status = [
    "Showed Up",
    "NCNS",
    "Medical Leave",
    "Resignation",
    "Day Off",
    "Abandonment"
]

df_editado = st.data_editor(
    df_filtrado,
    column_config={
        "STATUS": st.column_config.SelectboxColumn(
            "STATUS",
            options=opciones_status
        )
    },
    use_container_width=True
)

st.dataframe(df_editado)
