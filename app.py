import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Attendance Dashboard")

# Simulación backend
df = pd.DataFrame({
    "ID": [101,102,103,104,105],
    "Date": ["2026-02-25","02/16/2026","02/16/2026","2026-02-26","2026-02-25"],
    "Start": ["13:00","14:00","15:00","16:00","15:00"],
    "End": ["18:00","19:00","20:00","00:00","03:00"],
    "Status_x": ["Scheduled","Scheduled","Scheduled","Day Off","Day Off"],
    "Name": ["Juan","Ana","Luis","Maria","Nicolas"],
    "Status_y": ["Active"]*5,
    "Role": ["Agent","Agent","Agent","Agent","Supervisor"],
    "LOB": ["TMO Telesales Spanish","TMO Chats English","TMO Chats Spanish","TMO Chats Spanish","tmo"],
    "Supervisor": ["Paulina Esther Zalabata Pantoja","Yulieth Alejandra Mur Barrios","Yulieth Alejandra Mur Barrios","Stefanny Ramirez Ramirez","Nicolas"],
    "Phone Number": ["3124016489","3134230509","3012006087","3213752540","3112649520"],
    "Address": ["Calle 4 #36-70","Carrera 157 # 132 - 41","Calle 6 sur #16A134 sur","Carrera 111A #152C - 15","carrera 57 b 75 c 09"],
    "Longitud": ["4.68235","4.67179","4.75562","4.58491","4.59735"],
    "Latitud": ["-74.13265","-74.12842","-74.14382","-74.17222","-74.07612"]
})

# ================================
# FILTROS
# ================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    supervisores = list(df["Supervisor"].unique())
    supervisores.insert(0, "Todos")
    supervisor = st.selectbox("Supervisor", supervisores)

with col2:
    Selected_date = st.selectbox("Fecha", df["Date"].unique())
    Selected_date.insert(0, "Todos")
    Selected_date = st.selectbox("Date", supervisores)

    
with col3:
    Selected_lob = st.selectbox("LOB", df["LOB"].unique())

with col4:
    Selected_sch = st.selectbox("Sch", df["Status_x"].unique())

# ================================
# FILTRADO
# ================================

df["STATUS"] = ""
if supervisor == "Todos":
    df_filtrado = df[df["Date"] == Selected_date]
else:
    df_filtrado = df[
        (df["Supervisor"] == supervisor) &
        (df["Date"] == Selected_date)
    ]

# Reordenar columnas

column_order = ["ID","Name","ID", "Supervisor", "Date", "Start", "End","STATUS"]
df_filtrado = df_filtrado[column_order]

# ================================
# KPIs ARRIBA
# ================================
#st.subheader("Resumen")
col1, col2, col3 = st.columns(3)
col1.metric("Showed Up", (df_filtrado["STATUS"] == "Showed Up").sum())
col2.metric("NCNS", (df_filtrado["STATUS"] == "NCNS").sum())
col3.metric("Medical Leave", (df_filtrado["STATUS"] == "Medical Leave").sum())

# ================================
# GRÁFICO DE BARRAS POR HORA
# ================================
#st.subheader("")
conteo_horas = df_filtrado.groupby("Start").size()
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
