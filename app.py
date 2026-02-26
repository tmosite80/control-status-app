import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Attendance Dashboard")

# Simulación backend
df = pd.DataFrame({
    "ID": [101,102,103,104,105],
    "DATE": ["2026-02-25"]*5,
    "HOUR": ["13:00","14:00","15:00","16:00","15:00"],
    "STATUS": ["","Showed Up","",""],
    "NAME": ["Juan","Ana","Luis","Maria","Nicolas"],
    "SUPERVISOR": ["Daniela","Daniela","Maria","Maria","millitos"]
})

# ================================
# FILTROS
# ================================
col1, col2 = st.columns(2)

with col1:
    supervisores = list(df["SUPERVISOR"].unique())
    supervisores.insert(0, "Todos")
    supervisor = st.selectbox("Supervisor", supervisores)

with col2:
    fecha = st.selectbox("Fecha", df["DATE"].unique())

# ================================
# FILTRADO
# ================================
if supervisor == "Todos":
    df_filtrado = df[df["DATE"] == fecha]
else:
    df_filtrado = df[
        (df["SUPERVISOR"] == supervisor) & 
        (df["DATE"] == fecha)
    ]

# Reordenar columnas
column_order = ["NAME", "ID", "SUPERVISOR", "DATE", "HOUR", "STATUS"]
df_filtrado = df_filtrado[column_order]

# ================================
# KPIs ARRIBA
# ================================
st.subheader("Resumen")
col1, col2, col3 = st.columns(3)
col1.metric("Showed Up", (df_filtrado["STATUS"] == "Showed Up").sum())
col2.metric("NCNS", (df_filtrado["STATUS"] == "NCNS").sum())
col3.metric("Medical Leave", (df_filtrado["STATUS"] == "Medical Leave").sum())

# ================================
# GRÁFICO DE BARRAS POR HORA
# ================================
st.subheader("Conteo por Hora")
conteo_horas = df_filtrado.groupby("HOUR").size()
st.line_chart(conteo_horas)

# ================================
# TABLA EDITABLE
# ================================
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
