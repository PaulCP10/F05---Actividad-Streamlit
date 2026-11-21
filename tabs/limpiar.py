import streamlit as st
import pandas as pd


def limpiar_datos(df):
    """Devuelve una copia limpia del dataset.

    Reglas de limpieza (se aplican una vez y se reutilizan en todas las etapas):
    - Duplicados: se eliminan.
    - Faltantes numéricos: se imputan con la MEDIANA (robusta a valores extremos).
    - Faltantes categóricos: se marcan como "Desconocido" (no inventamos una
      categoría real).
    """
    df = df.drop_duplicates().copy()
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("Desconocido")
    return df


def mostrar(df):
    """Etapa 2 - LIMPIAR: ¿qué tan confiables son los datos?"""

    st.header("2. Limpiar los datos")
    st.info("Revisamos nulos y duplicados, y decidimos qué hacer con cada uno.")

    # --- Faltantes (antes) -------------------------------------------------
    st.subheader("Valores faltantes (antes)")
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    if len(nulos) == 0:
        st.success("No hay valores faltantes.")
    else:
        st.dataframe(
            pd.DataFrame({"Variable": nulos.index, "Faltantes": nulos.values}),
            use_container_width=True,
        )

    # --- Duplicados --------------------------------------------------------
    st.subheader("Duplicados")
    st.metric("Registros duplicados", int(df.duplicated().sum()))

    # --- Decisiones y antes/después ---------------------------------------
    df_limpio = limpiar_datos(df)

    st.subheader("Antes y después de limpiar")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filas antes", len(df))
    c2.metric("Filas después", len(df_limpio))
    c3.metric("Faltantes restantes", int(df_limpio.isnull().sum().sum()))

    st.markdown("""
**Decisiones tomadas y por qué**
- **Duplicados → se eliminan.** Un mismo ticket contado dos veces inflaría cualquier
  conteo o tasa y sesgaría el modelo.
- **Faltantes numéricos → mediana.** La mediana no se deja arrastrar por valores
  extremos (p. ej. un ticket con 400 horas abiertas).
- **Faltantes categóricos → "Desconocido".** Preferimos reconocer que no sabemos el
  dato antes que asignarle a la fuerza una categoría real.
""")
