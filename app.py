import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Configuración inicial ---
st.title("💧 Control de Consumo de Agua")

# Cargar o crear datos
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Fecha", "Actividad", "Litros"])

# --- Formulario ---
st.header("Registrar Consumo")
with st.form("form_consumo"):
    fecha = st.date_input("Fecha", datetime.today())
    actividad = st.selectbox("Actividad", ["Ducha", "Cocinar", "Lavar ropa", "Otro"])
    litros = st.number_input("Litros usados", min_value=1)
    enviar = st.form_submit_button("Guardar")

if enviar:
    nuevo = pd.DataFrame([[fecha, actividad, litros]], columns=["Fecha", "Actividad", "Litros"])
    st.session_state["data"] = pd.concat([st.session_state["data"], nuevo], ignore_index=True)
    st.success("✅ Registro guardado")

# --- Mostrar datos ---
st.header("Histórico de Consumo")
df = st.session_state["data"]
st.dataframe(df)

if not df.empty:
    # Agrupar por fecha
    consumo_diario = df.groupby("Fecha")["Litros"].sum()

    # Gráfica diaria
    st.subheader("Consumo diario")
    fig, ax = plt.subplots()
    consumo_diario.plot(ax=ax, marker="o")
    ax.set_ylabel("Litros")
    st.pyplot(fig)

    # Gráfico semanal
    df["Semana"] = pd.to_datetime(df["Fecha"]).dt.to_period("W")
    consumo_semanal = df.groupby("Semana")["Litros"].sum()

    st.subheader("Consumo semanal")
    fig, ax = plt.subplots()
    consumo_semanal.plot(kind="bar", ax=ax)
    ax.set_ylabel("Litros")
    st.pyplot(fig)

    # --- Alertas y recomendaciones ---
    st.header("🔔 Recomendaciones")
    if consumo_diario.iloc[-1] > 50:
        st.warning("🚨 Has consumido más de 50 litros hoy. Intenta reducir duchas largas.")
    else:
        st.info("🌱 Buen trabajo, tu consumo diario está dentro de lo recomendado.")
