import streamlit as st
import pandas as pd

# Umbrales de política (ajustables según la capacidad del equipo).
UMBRAL_ALTO = 0.60
UMBRAL_MEDIO = 0.30

# Acción y mensaje recomendados por nivel de riesgo.
ACCIONES = {
    "Alto riesgo": (
        "Escalar de inmediato a un agente senior y marcar como seguimiento prioritario.",
        "Este ticket está en riesgo de incumplir el SLA; atiéndelo hoy.",
    ),
    "Riesgo medio": (
        "Revisar antes de cerrar el turno y reasignar si lleva más de 8 h sin avance "
        "(aquí se concentra la mayoría de los incumplimientos reales).",
        "No lo dejes en espera: dale seguimiento activo este mismo turno.",
    ),
    "Bajo riesgo": (
        "Flujo estándar, sin acción especial.",
        "Ticket bajo control; sigue el proceso normal.",
    ),
}


def clasificar_riesgo(prob):
    if prob >= UMBRAL_ALTO:
        return "Alto riesgo"
    if prob >= UMBRAL_MEDIO:
        return "Riesgo medio"
    return "Bajo riesgo"


def mostrar(df):
    """Etapa 5 - PRESCRIBIR: de la probabilidad a una acción por segmento."""

    st.header("5. Estadística prescriptiva")
    st.info("Traducimos la probabilidad del modelo en una acción concreta por nivel de riesgo.")

    df = df.copy()
    df["nivel_riesgo"] = df["prob_incumplir"].apply(clasificar_riesgo)

    resumen = df.groupby("nivel_riesgo").agg(
        tickets=("id_ticket", "count"),
        prob_promedio=("prob_incumplir", "mean"),
        incumplimiento_real=("incumplio_sla", "mean"),
    ).reindex(["Alto riesgo", "Riesgo medio", "Bajo riesgo"]).reset_index()

    resumen["prob_promedio"] = (resumen["prob_promedio"] * 100).round(1)
    resumen["incumplimiento_real"] = (resumen["incumplimiento_real"] * 100).round(1)
    resumen["acción recomendada"] = resumen["nivel_riesgo"].map(lambda t: ACCIONES[t][0])

    st.subheader("Acción recomendada por nivel de riesgo")
    st.dataframe(resumen, use_container_width=True)
    st.caption(
        f"Umbrales usados: ≥ {int(UMBRAL_ALTO*100)}% = alto, "
        f"≥ {int(UMBRAL_MEDIO*100)}% = medio. Son una política ajustable: si el "
        "equipo tiene poca capacidad, se suben para enfocar solo lo más crítico."
    )