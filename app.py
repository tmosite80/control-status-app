import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ================================
# Configuración de la página
# ================================
st.set_page_config(layout="wide")

# ================================
# Título centrado
# ================================
st.markdown(
    "<h1 style='text-align: center;'>📊 Attendance DashboardSSS</h1>",
    unsafe_allow_html=True
)

# ================================
# Data
# ================================
ATTENDANCE_SHEET_ID = "1qABgFnVHSI-yYBvy6Ppbm_DMWBnlhnov9q0QV3pdpFY"
CREDENTIALS_FILE = "/content/control-status-app/credentials.json"

# --------------------------------------------------
# CONEXIÓN A GOOGLE
# --------------------------------------------------

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=scope
)

client = gspread.authorize(creds)

# --------------------------------------------------
# ABRIR SHEET
# --------------------------------------------------

spreadsheet = client.open_by_key(ATTENDANCE_SHEET_ID)
worksheet = spreadsheet.worksheet("python")

# --------------------------------------------------
# CARGAR DATA
# --------------------------------------------------

data = worksheet.get_all_records()
df = pd.DataFrame(data)


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
conteo_horas = df_filtrado.groupby("Start").size()
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
