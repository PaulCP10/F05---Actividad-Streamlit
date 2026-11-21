import streamlit as st
import pandas as pd


def mostrar(df):
    """Etapa 1 - ENTENDER: inspeccionamos los datos SIN modificarlos todavía."""

    st.header("1. Entender los datos")

    st.markdown("""
### Pregunta

**¿Qué tickets tenemos y qué información conocemos de cada uno?**
""")

    # --- Dimensiones -------------------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Número de tickets", len(df))
    with col2:
        st.metric("Número de variables", len(df.columns))

    # --- Vista previa ------------------------------------------------------
    st.subheader("Vista previa del dataset")
    st.dataframe(df.head(10), use_container_width=True)

    # --- Diagnóstico -------------------------------------------------------
    st.subheader("Diagnóstico del dataset")
    diagnostico = pd.DataFrame({
        "Variable": df.columns,
        "Tipo": df.dtypes.astype(str).values,
        "Valores únicos": df.nunique().values,
        "Valores faltantes": df.isnull().sum().values,
    })
    st.dataframe(diagnostico, use_container_width=True)
    st.caption(
        "Aquí distinguimos variables numéricas de categóricas y detectamos "
        "dónde hay huecos. Todavía NO corregimos nada: eso es la etapa 2."
    )

    # --- Problemas potenciales --------------------------------------------
    st.subheader("Problemas potenciales")
    duplicados = df.duplicated().sum()
    st.metric("Registros duplicados", int(duplicados))

    # --- Explorador de variables ------------------------------------------
    st.subheader("Explorar una variable")
    variable = st.selectbox(
        "Selecciona una variable:",
        df.columns,
        key="variable_entender",
    )

    if pd.api.types.is_numeric_dtype(df[variable]):
        st.write("**Tipo:** Variable numérica")
        st.dataframe(df[variable].describe(), use_container_width=True)
    else:
        st.write("**Tipo:** Variable categórica")
        frecuencias = (
            df[variable]
            .value_counts(dropna=False)
            .reset_index()
        )
        frecuencias.columns = ["Valor", "Frecuencia"]
        st.dataframe(frecuencias, use_container_width=True)
