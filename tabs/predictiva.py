import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def mostrar(resultado):
    """Etapa 4 - PREDECIR: mostramos el desempeño del modelo y qué pesa más.

    Recibe el diccionario que devuelve modelo.entrenar_modelo(...).
    """

    st.header("4. Estadística predictiva")
    st.info(
        "Regresión logística que estima la probabilidad de que un ticket "
        "incumpla el SLA, a partir de sus características."
    )

    m = resultado["metricas"]

    # --- Desempeño del modelo ---------------------------------------------
    c1, c2, c3 = st.columns(3)
    c1.metric("Exactitud (accuracy)", f"{m['accuracy'] * 100:.1f}%")
    c2.metric("ROC-AUC", f"{m['roc_auc']:.2f}")
    c3.metric("Tickets de prueba", m["n_test"])
    st.caption("ROC-AUC: 1.0 = separa perfecto, 0.5 = azar. Mide qué tan bien "
               "ordena a los tickets por riesgo.")

    # --- Matriz de confusión ----------------------------------------------
    st.subheader("Matriz de confusión (datos de prueba)")
    cm = m["confusion"]
    cm_df = pd.DataFrame(
        cm,
        index=["Real: cumplió", "Real: incumplió"],
        columns=["Predijo: cumplió", "Predijo: incumplió"],
    )
    st.dataframe(cm_df, use_container_width=True)

    # --- Variables que más pesan ------------------------------------------
    st.subheader("Variables que más influyen en el riesgo")
    top = resultado["coeficientes"].head(10).iloc[::-1]
    colores = ["#E45756" if c > 0 else "#54A24B" for c in top["coeficiente"]]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(top["variable"], top["coeficiente"], color=colores)
    ax.axvline(0, color="#888", linewidth=0.8)
    ax.set_xlabel("Peso (coeficiente estandarizado)")
    ax.set_title("Top 10 variables")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)
    st.caption(
        "Rojo (coeficiente positivo) = sube la probabilidad de incumplir; "
        "verde (negativo) = la baja."
    )
