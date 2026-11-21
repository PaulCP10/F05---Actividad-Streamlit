import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def mostrar(df):
    """Etapa 3 - DESCRIBIR: KPIs y comportamiento por segmento."""

    st.header("3. Estadística descriptiva")
    st.info("KPIs del área y cómo se comporta el incumplimiento por segmento.")

    # --- KPIs principales --------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tickets", len(df))
    c2.metric("% Incumplió SLA", f"{df['incumplio_sla'].mean() * 100:.1f}%")
    c3.metric("% Reabiertos", f"{df['reabierto'].mean() * 100:.1f}%")
    c4.metric("Horas abierto (prom.)", f"{df['horas_abierto'].mean():.1f}")

    # --- Incumplimiento por categoría -------------------------------------
    st.subheader("Incumplimiento de SLA por categoría de compra")
    por_cat = (
        df.groupby("categoria_compra")["incumplio_sla"].mean().sort_values()
    )
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.barh(por_cat.index, por_cat.values * 100, color="#4C78A8")
    ax.set_xlabel("% que incumplió SLA")
    ax.set_title("Incumplimiento por categoría")
    for i, v in enumerate(por_cat.values * 100):
        ax.text(v + 0.5, i, f"{v:.0f}%", va="center", fontsize=9)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # --- Incumplimiento por prioridad -------------------------------------
    st.subheader("Incumplimiento de SLA por prioridad")
    orden = ["Baja", "Media", "Alta", "Crítica"]
    por_pri = df.groupby("prioridad")["incumplio_sla"].mean().reindex(orden)
    fig2, ax2 = plt.subplots(figsize=(7, 3.5))
    ax2.bar(por_pri.index, por_pri.values * 100, color="#F58518")
    ax2.set_ylabel("% que incumplió SLA")
    ax2.set_title("Incumplimiento por prioridad")
    for i, v in enumerate(por_pri.values * 100):
        ax2.text(i, v + 0.5, f"{v:.0f}%", ha="center", fontsize=9)
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=False)
    st.caption(
        "Lectura: las prioridades más altas tienden a incumplir más porque su "
        "SLA es más corto y cualquier demora se nota."
    )

    # --- Tabla de KPIs por categoría --------------------------------------
    st.subheader("KPIs por categoría")
    kpi = df.groupby("categoria_compra").agg(
        tickets=("id_ticket", "count"),
        pct_incumplio=("incumplio_sla", "mean"),
        horas_prom=("horas_abierto", "mean"),
        reasignaciones_prom=("reasignaciones", "mean"),
    ).reset_index()
    kpi["pct_incumplio"] = (kpi["pct_incumplio"] * 100).round(1)
    kpi["horas_prom"] = kpi["horas_prom"].round(1)
    kpi["reasignaciones_prom"] = kpi["reasignaciones_prom"].round(2)
    st.dataframe(kpi, use_container_width=True)
