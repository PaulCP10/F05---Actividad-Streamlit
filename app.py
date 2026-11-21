import streamlit as st
import pandas as pd

from tabs import (
    entender, limpiar, descriptiva, predictiva, prescriptiva, decisiones, modelo
)

# ---------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Tickets de Compras – SLA",
    page_icon="🎫",
    layout="wide",
)

st.title("🎫 Tickets de Compras: Toma de decisiones")

st.markdown("""
**Pregunta guía:** ¿Qué tickets de compras tienen mayor probabilidad de **incumplir el SLA**,
y qué acción o priorización deberíamos tomar con cada tipo?

**Framework:** Entender → Limpiar → Describir → Predecir → Prescribir → Decidir

*Dataset sintético y anonimizado, generado para esta práctica (no contiene datos reales).*
""")

# ---------------------------------------------------------------------
# CARGA + PREPARACIÓN (una sola vez, se reutiliza en las pestañas)
# ---------------------------------------------------------------------
df_raw = pd.read_csv("data/tickets_compras_sinteticos.csv")   # datos crudos
df_limpio = limpiar.limpiar_datos(df_raw)                     # datos limpios
resultado = modelo.entrenar_modelo(df_limpio)                 # modelo + probabilidades

# ---------------------------------------------------------------------
# PESTAÑAS (una por etapa del framework)
# ---------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Entender",
    "2. Limpiar",
    "3. Descriptiva",
    "4. Predictiva",
    "5. Prescriptiva",
    "6. Decisiones",
])

with tab1:
    entender.mostrar(df_raw)        # mostramos los datos CRUDOS para ver su estado real
with tab2:
    limpiar.mostrar(df_raw)         # diagnóstico y decisiones de limpieza
with tab3:
    descriptiva.mostrar(df_limpio)  # KPIs sobre datos limpios
with tab4:
    predictiva.mostrar(resultado)   # desempeño del modelo y variables clave
with tab5:
    prescriptiva.mostrar(resultado["df_scored"])  # acción por nivel de riesgo
with tab6:
    decisiones.mostrar(resultado["df_scored"])    # selector: acción + mensaje + justificación
