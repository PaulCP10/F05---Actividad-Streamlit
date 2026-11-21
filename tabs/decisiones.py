import streamlit as st
import pandas as pd

from tabs.prescriptiva import clasificar_riesgo, ACCIONES


def mostrar(df):
    """Etapa 6 - DECIDIR: selector de segmento con acción, mensaje y justificación."""

    st.header("6. Toma de decisiones")
    st.info("Elige un segmento y obtén la acción, el mensaje y la justificación con datos.")

    df = df.copy()
    df["nivel_riesgo"] = df["prob_incumplir"].apply(clasificar_riesgo)

    # El usuario elige por qué variable segmentar y qué valor mirar.
    dimension = st.selectbox(
        "Segmentar por:",
        ["nivel_riesgo", "categoria_compra", "prioridad", "turno", "region"],
    )
    opciones = sorted(df[dimension].astype(str).unique())
    valor = st.selectbox("Selecciona el segmento:", opciones)

    sub = df[df[dimension].astype(str) == valor]
    if len(sub) == 0:
        st.warning("No hay tickets en este segmento.")
        return

    prob_prom = sub["prob_incumplir"].mean()
    tasa_real = sub["incumplio_sla"].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Tickets", len(sub))
    c2.metric("Prob. promedio de incumplir", f"{prob_prom * 100:.1f}%")
    c3.metric("Incumplimiento real", f"{tasa_real * 100:.1f}%")

    # La acción/mensaje se toman del nivel de riesgo dominante en el segmento.
    tier_dominante = sub["nivel_riesgo"].mode()[0]
    accion, mensaje = ACCIONES[tier_dominante]

    st.subheader("Decisión recomendada")
    st.markdown(f"**Segmento:** `{dimension} = {valor}`  ·  nivel dominante: **{tier_dominante}**")
    st.markdown(f"**Acción:** {accion}")
    st.success(f"**Mensaje para el equipo:** {mensaje}")
    st.caption(
        f"Justificación: en este segmento la probabilidad promedio de incumplir "
        f"el SLA es {prob_prom * 100:.1f}% y el incumplimiento observado es "
        f"{tasa_real * 100:.1f}%."
    )
