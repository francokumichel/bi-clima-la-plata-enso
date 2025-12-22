import streamlit as st
from data.panorama_queries import (
    extremos_anual,
    extremos_estacional,
    distribucion_indice
)
from components.charts import line_chart, boxplot_indice, histogram_indice

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Índices Climáticos",
    layout="wide"
)

st.title("📊 Índices Climáticos Extremos (ETCCDI)")

# =========================
# METADATOS DE ÍNDICES
# =========================

INDICES = {
    "PRCPTOT": {"label": "Precipitación total", "unidad": "mm"},
    "SDII": {"label": "Intensidad media diaria", "unidad": "mm/día"},
    "Rx1day": {"label": "Máx. precipitación 1 día", "unidad": "mm"},
    "Rx5day": {"label": "Máx. precipitación 5 días", "unidad": "mm"},
    "CDD": {"label": "Días secos consecutivos", "unidad": "días"},
    "CWD": {"label": "Días húmedos consecutivos", "unidad": "días"},
    "TXx": {"label": "Máx. temperatura máxima", "unidad": "°C"},
    "TNn": {"label": "Mín. temperatura mínima", "unidad": "°C"},
    "FD": {"label": "Días de helada", "unidad": "días"},
    "SU": {"label": "Días cálidos", "unidad": "días"},
    "TX90p": {"label": "Días cálidos extremos", "unidad": "%"},
    "TN10p": {"label": "Noches frías extremas", "unidad": "%"},
    "DTR": {"label": "Rango térmico diario", "unidad": "°C"},
}

# =========================
# FILTROS
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    tipo = st.selectbox(
        "Tipo de índice",
        ["Anual", "Estacional"]
    )

with col2:
    indice = st.selectbox(
        "Índice",
        options=list(INDICES.keys()),
        format_func=lambda x: f"{x} – {INDICES[x]['label']}"
    )

with col3:
    if tipo == "Estacional":
        estacion = st.selectbox(
            "Estación",
            ["Verano", "Otoño", "Invierno", "Primavera"]
        )
    else:
        estacion = None

anio_inicio, anio_fin = st.slider(
    "Período de análisis",
    min_value=1961,
    max_value=2024,
    value=(1961, 2024),
    step=1
)

# =========================
# CONSULTA
# =========================

if tipo == "Anual":
    df = extremos_anual(indice, anio_inicio, anio_fin)
else:
    df = extremos_estacional(indice, estacion, anio_inicio, anio_fin)

# =========================
# VALIDACIÓN
# =========================

if df.empty:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
    st.stop()

# =========================
# GRÁFICO PRINCIPAL
# =========================

st.subheader("📈 Evolución temporal")

fig = line_chart(
    df=df,
    x="anio",
    y="valor",
    title=f"{indice} – {INDICES[indice]['label']}",
    y_label=INDICES[indice]["unidad"]
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📦 Distribución del índice")

df_dist = distribucion_indice(
    indice=indice,
    anio_inicio=anio_inicio,
    anio_fin=anio_fin,
    estacion=estacion
)

if df_dist.empty:
    st.warning("No hay datos para construir la distribución.")
else:
    col1, col2 = st.columns(2)

    with col1:
        fig_box = boxplot_indice(
            df=df_dist,
            indice=indice,
            unidad=INDICES[indice]["unidad"],
            estacion=estacion
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        bins = st.slider(
            "Número de bins",
            min_value=5,
            max_value=50,
            value=20,
            step=1
        )

        fig_hist = histogram_indice(
            df=df_dist,
            indice=indice,
            unidad=INDICES[indice]["unidad"],
            estacion=estacion,
            bins=bins
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
# =========================
# TABLA (OPCIONAL)
# =========================

with st.expander("📄 Ver datos"):
    st.dataframe(df)
