import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json




# ================================
# Título centrado
# ================================
st.markdown(
    "<h1 style='text-align: center;'>📊 Attendance Dashboard</h1>",
    unsafe_allow_html=True
)

DATA = [
    {
        "ID": 1,
        "Date": "2026-03-01",
        "Start": "08:00",
        "End": "17:00",
        "Status_x": "Present",
        "Pipkins ID": "PK1001",
        "Name": "Juan Pérez",
        "Status_y": "Active",
        "Role": "Agent",
        "LOB": "Sales",
        "Supervisor": "María López",
        "Phone Number": "555-1234",
        "Address": "Av. Central 123",
        "Longitud": -99.1332,
        "Latitud": 19.4326
    },
    {
        "ID": 2,
        "Date": "2026-03-01",
        "Start": "09:00",
        "End": "18:00",
        "Status_x": "Absent",
        "Pipkins ID": "PK1002",
        "Name": "Ana Gómez",
        "Status_y": "Active",
        "Role": "Agent",
        "LOB": "Support",
        "Supervisor": "Carlos Ruiz",
        "Phone Number": "555-5678",
        "Address": "Calle Norte 456",
        "Longitud": -99.1400,
        "Latitud": 19.4300
    },
    {
        "ID": 3,
        "Date": "2026-03-01",
        "Start": "10:00",
        "End": "16:00",
        "Status_x": "Present",
        "Pipkins ID": "PK1003",
        "Name": "Luis Martínez",
        "Status_y": "Inactive",
        "Role": "Supervisor",
        "LOB": "Sales",
        "Supervisor": "N/A",
        "Phone Number": "555-8765",
        "Address": "Av. Sur 789",
        "Longitud": -99.1200,
        "Latitud": 19.4400
    },
    {
        "ID": 4,
        "Date": "2026-03-01",
        "Start": "10:00",
        "End": "19:00",
        "Status_x": "Late",
        "Pipkins ID": "PK1004",
        "Name": "Sofía Ramírez",
        "Status_y": "Active",
        "Role": "Agent",
        "LOB": "Retention",
        "Supervisor": "María López",
        "Phone Number": "555-3456",
        "Address": "Calle Este 321",
        "Longitud": -99.1500,
        "Latitud": 19.4200
    },
    {
        "ID": 5,
        "Date": "2026-03-01",
        "Start": "08:30",
        "End": "10:00",
        "Status_x": "Present",
        "Pipkins ID": "PK1005",
        "Name": "Pedro Sánchez",
        "Status_y": "Active",
        "Role": "Agent",
        "LOB": "Support",
        "Supervisor": "Carlos Ruiz",
        "Phone Number": "555-6543",
        "Address": "Av. Oeste 654",
        "Longitud": -99.1100,
        "Latitud": 19.4500
    }
]

df = pd.DataFrame(DATA)

# ================================
# Configuración de la página
# ================================
st.set_page_config(layout="wide")

# ================================
# Inicializar STATUS en session_state
# ================================
if "df_editado" not in st.session_state:
    df["STATUS"] = ""
    st.session_state.df_editado = df.copy()

# ================================
# Contenedores para KPIs y tabla
# ================================
kpi_container = st.container()

# ================================
# FILTROS
# ================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    supervisores = ["All"] + st.session_state.df_editado["Supervisor"].unique().tolist()
    supervisor = st.selectbox("Supervisor", supervisores)

with col2:
    fechas = ["All"] + st.session_state.df_editado["Date"].unique().tolist()
    Selected_date = st.selectbox("Date", fechas)

with col3:
    lobs = ["All"] + st.session_state.df_editado["LOB"].unique().tolist()
    Selected_lob = st.selectbox("LOB", lobs)

with col4:
    statuses = ["All","Showed Up","NCNS","Medical Leave","Resignation","Day Off","Abandonment"]
    Selected_sch = st.selectbox("Status", statuses)

# ================================
# FILTRADO
# ================================
df_filtrado = st.session_state.df_editado.copy()

if supervisor != "All":
    df_filtrado = df_filtrado[df_filtrado["Supervisor"] == supervisor]

if Selected_date != "All":
    df_filtrado = df_filtrado[df_filtrado["Date"] == Selected_date]

if Selected_lob != "All":
    df_filtrado = df_filtrado[df_filtrado["LOB"] == Selected_lob]

if Selected_sch != "All":
    df_filtrado = df_filtrado[df_filtrado["STATUS"] == Selected_sch]

# Reordenar columnas
column_order = ["ID","Name", "Supervisor", "Date", "Start", "End","STATUS"]
df_filtrado = df_filtrado[column_order]

# ================================
# KPIs
# ================================
with kpi_container:
    col1, col2, col3 = st.columns(3)
    col1.metric("Showed Up", (df_filtrado["STATUS"] == "Showed Up").sum())
    col2.metric("NCNS", (df_filtrado["STATUS"] == "NCNS").sum())
    col3.metric("Medical Leave", (df_filtrado["STATUS"] == "Medical Leave").sum())

# ================================
# Gráfico de horas
# ================================

df_filtrado["Start"] = pd.to_datetime(df_filtrado["Start"], format="%H:%M")
df_filtrado["End"] = pd.to_datetime(df_filtrado["End"], format="%H:%M")

# Crear rango de horas del día
horas = pd.date_range("00:00", "23:00", freq="H")

conteo_activos = []

for hora in horas:
    activos = df_filtrado[
        (df_filtrado["Start"] <= hora) &
        (df_filtrado["End"] > hora)
    ].shape[0]
    
    conteo_activos.append(activos)

# Crear serie final
conteo_horas = pd.Series(conteo_activos, index=horas)

# Graficar
st.line_chart(conteo_horas)

# ================================
# Tabla editable
# ================================
opciones_status = ["Showed Up","NCNS","Medical Leave","Resignation","Day Off","Abandonment"]
table_container = st.container()

with table_container:
    st.session_state.df_editado.loc[df_filtrado.index] = st.data_editor(
        df_filtrado,
        column_config={
            "STATUS": st.column_config.SelectboxColumn(
                "STATUS",
                options=opciones_status
            )
        },
        use_container_width=True
    )
