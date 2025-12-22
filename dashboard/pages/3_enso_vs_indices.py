import streamlit as st
import plotly.express as px
from data.indices_vs_enso_queries import (
    extremos_vs_enso_anual,
    extremos_vs_enso_estacional,
    scatter_enso_vs_extremo,
    anomalias_extremos_por_fase_anual
)

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="ENSO y Extremos Climáticos",
    layout="wide"
)

st.title("🌊 ENSO y su impacto en los extremos climáticos")

# =========================
# METADATOS
# =========================

INDICES_EXTREMOS = {
    "PRCPTOT": "Precipitación total",
    "Rx1day": "Máx. precipitación 1 día",
    "Rx5day": "Máx. precipitación 5 días",
    "CDD": "Días secos consecutivos",
    "TXx": "Temperatura máxima extrema",
    "TNn": "Temperatura mínima extrema",
    "TX90p": "Días cálidos extremos",
    "TN10p": "Noches frías extremas",
}

INDICES_ENSO = {
    "oni": "ONI",
    "mei": "MEI",
    "nino34": "Niño 3.4"
}

# =========================
# FILTROS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    escala = st.selectbox("Escala", ["Anual", "Estacional"])

with col2:
    indice_extremo = st.selectbox(
        "Índice extremo",
        options=list(INDICES_EXTREMOS.keys()),
        format_func=lambda x: f"{x} – {INDICES_EXTREMOS[x]}"
    )

with col3:
    if escala == "Estacional":
        estacion = st.selectbox("Estación", ["Verano", "Otoño", "Invierno", "Primavera"])
    else:
        estacion = None

with col4:
    indice_enso = st.selectbox(
        "Índice ENSO",
        options=list(INDICES_ENSO.keys()),
        format_func=lambda x: INDICES_ENSO[x]
    )

anio_inicio, anio_fin = st.slider(
    "Período",
    1950, 2025, (1980, 2020)
)

# =========================
# CONSULTAS
# =========================

if escala == "Anual":
    df_box = extremos_vs_enso_anual(
        indice_extremo, anio_inicio, anio_fin
    )
else:
    df_box = extremos_vs_enso_estacional(
        indice_extremo, estacion, anio_inicio, anio_fin
    )

df_scatter = scatter_enso_vs_extremo(
    indice_extremo, indice_enso, anio_inicio, anio_fin
)

# =========================
# BOXPLOT
# =========================

st.subheader("📦 Distribución del índice por fase ENSO")

fig_box = px.box(
    df_box,
    x="fase",
    y="valor",
    color="fase",
    category_orders={"fase": ["Niño", "Neutral", "Niña"]},
    title=f"{indice_extremo} según fase ENSO"
)

st.plotly_chart(fig_box, use_container_width=True)

# =========================
# SCATTER
# =========================

st.subheader("🔎 Relación índice ENSO vs extremo")

fig_scatter = px.scatter(
    df_scatter,
    x="enso_valor",
    y="extremo_valor",
    color="fase",
    trendline="ols",
    labels={
        "enso_valor": INDICES_ENSO[indice_enso],
        "extremo_valor": indice_extremo
    }
)

st.plotly_chart(fig_scatter, use_container_width=True)


st.subheader("📊 Anomalías del índice por fase ENSO")

df_anom = anomalias_extremos_por_fase_anual(
    indice_extremo,
    anio_inicio,
    anio_fin
)

if df_anom.empty:
    st.warning("No hay datos suficientes para calcular anomalías.")
else:
    fig_anom = px.bar(
        df_anom,
        x="fase",
        y="anomalia",
        color="fase",
        title=f"Anomalía de {indice_extremo} según fase ENSO",
        labels={
            "fase": "Fase ENSO",
            "anomalia": "Anomalía respecto a la climatología"
        }
    )

    # Línea horizontal en 0
    fig_anom.add_hline(
        y=0,
        line_dash="dash",
        line_color="black"
    )

    fig_anom.update_layout(
        template="simple_white",
        showlegend=False
    )

    st.plotly_chart(fig_anom, use_container_width=True)


# =========================
# DATOS
# =========================

with st.expander("📄 Ver datos"):
    st.dataframe(df_box)