import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from dashboard.data.enso_queries import (
    get_enso_por_estacion_20_anios,
    get_indice_por_fase_y_periodo,
    get_fases_por_anio,
    get_distribucion_fases_by_lapse,
    get_oni_temporal
)

INDICES_ENSO = {
    "ONI": '"oni"',
    "Niño 1+2": '"nino12"',
    "Niño 3": '"nino3"',
    "Niño 3.4": '"nino34"',
    "Niño 4": '"nino4"',
    "MEI": '"mei"',
    "SOI": '"soi"',
}

st.set_page_config(
    page_title="ENSO – Análisis y clasificación",
    layout="wide"
)

st.title("🌊 Clasificación ENSO")

# ─────────────────────────────
# SLIDER DE PERÍODO (ARRIBA)
# ─────────────────────────────
st.markdown("### 📅 Período de análisis")

anio_inicio, anio_fin = st.slider(
    "Seleccionar rango temporal",
    min_value=1961,
    max_value=2024,
    value=(1980, 2020)
)

# ─────────────────────────────
# PRIMER BLOQUE DE GRÁFICOS
# ─────────────────────────────
c1, c2 = st.columns([2, 1])

df_oni = get_oni_temporal(anio_inicio, anio_fin)
df_fases = get_fases_por_anio()
df_dist = get_distribucion_fases_by_lapse(anio_inicio, anio_fin)

df_fases_filtrado = df_fases[
    (df_fases["anio"] >= anio_inicio) &
    (df_fases["anio"] <= anio_fin)
]

with c1:
    st.subheader("📊 Niño vs Niña vs Neutro (anual)")

    pivot = (
        df_fases_filtrado
        .pivot(index="anio", columns="fase", values="meses")
        .fillna(0)
        .sort_index()
    )

    st.bar_chart(pivot)

with c2:
    st.subheader("Distribución")

    st.bar_chart(
        df_dist.set_index("fase")["meses"]
    )


st.markdown("---")
st.markdown("### 📈 Evolución temporal comparativa de índices ENSO")

c_sel1, c_sel2 = st.columns(2)

with c_sel1:
    fase_seleccionada = st.selectbox(
        "Fase ENSO",
        ["Niño", "Niña", "Neutro"]
    )

with c_sel2:
    indice_label = st.selectbox(
        "Índice climático",
        list(INDICES_ENSO.keys())
    )

indice_sql = INDICES_ENSO[indice_label]

# Índice principal
df_indice = get_indice_por_fase_y_periodo(
    indice_sql=indice_sql,
    fase=fase_seleccionada,
    anio_inicio=anio_inicio,
    anio_fin=anio_fin
)

if df_indice.empty:
    st.warning("No hay datos para la combinación seleccionada.")
else:
    df_indice["fecha"] = (
        df_indice["anio"].astype(str)
        + "-"
        + df_indice["mes"].astype(str).str.zfill(2)
    )

    fig = go.Figure()

    # ─────────────────────────────
    # Índice seleccionado (principal)
    # ─────────────────────────────
    fig.add_trace(go.Scatter(
        x=df_indice["fecha"],
        y=df_indice["valor"],
        mode="lines",
        name=indice_label,
        line=dict(width=3)
    ))

    # ─────────────────────────────
    # Otros índices ENSO (comparativos)
    # ─────────────────────────────
    for idx_label, idx_sql in INDICES_ENSO.items():
        if idx_label == indice_label:
            continue

        df_aux = get_indice_por_fase_y_periodo(
            indice_sql=idx_sql,
            fase=fase_seleccionada,
            anio_inicio=anio_inicio,
            anio_fin=anio_fin
        )

        if df_aux.empty:
            continue

        df_aux["fecha"] = (
            df_aux["anio"].astype(str)
            + "-"
            + df_aux["mes"].astype(str).str.zfill(2)
        )

        fig.add_trace(go.Scatter(
            x=df_aux["fecha"],
            y=df_aux["valor"],
            mode="lines",
            name=idx_label,
            line=dict(width=1.2, dash="dot"),
            opacity=0.7
        ))

    # Línea base
    fig.add_hline(y=0, line_dash="dash", opacity=0.4)

    fig.update_layout(
        title=f"Índices ENSO durante fase {fase_seleccionada}",
        xaxis_title="Tiempo",
        yaxis_title="Valor del índice",
        hovermode="x unified",
        legend_title_text="Índices ENSO"
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.markdown("### 📦 Distribución y valores atípicos de índices ENSO")

# Selectores
c_b1, c_b2 = st.columns(2)

with c_b1:
    fase_box = st.selectbox(
        "Fase ENSO (boxplot)",
        ["Niño", "Niña", "Neutro"]
    )

with c_b2:
    indices_box = st.multiselect(
        "Índices a comparar",
        list(INDICES_ENSO.keys()),
        default=["ONI", "Niño 3.4", "MEI"]
    )

if not indices_box:
    st.warning("Seleccioná al menos un índice.")
    st.stop()

fig_box = go.Figure()

for idx_label in indices_box:
    df_box = get_indice_por_fase_y_periodo(
        indice_sql=INDICES_ENSO[idx_label],
        fase=fase_box,
        anio_inicio=anio_inicio,
        anio_fin=anio_fin
    )

    if df_box.empty:
        continue

    fig_box.add_trace(go.Box(
        y=df_box["valor"],
        name=idx_label,
        boxmean="sd",       # media + desviación estándar
        jitter=0.3,
        pointpos=-1.8,
        marker=dict(size=5),
        line=dict(width=1.5)
    ))

fig_box.update_layout(
    title=f"Distribución de índices ENSO durante fase {fase_box}",
    yaxis_title="Valor del índice",
    xaxis_title="Índice ENSO",
    showlegend=False,
    height=450
)

st.plotly_chart(fig_box, use_container_width=True)



# SELECTOR COMÚN
estacion = st.selectbox(
    "Seleccionar estación climatológica",
    ["DJF", "MAM", "JJA", "SON"],
    key="estacion_pie"
)

c3 = st.columns(1)
col = c3[0]   # ← extraes la columna

with col:
    st.subheader("📉 Distribución ENSO últimos 20 años")
    df_estacion = get_enso_por_estacion_20_anios(estacion)
    fig_estacion = px.pie(
        df_estacion,
        names="fase",
        values="porcentaje",
        title=f"Distribución ENSO – {estacion}",
        hole=0.45
    )

    fig_estacion.update_layout(
        legend_title_text="Fase ENSO",
        margin=dict(t=40, b=20)
    )

    st.plotly_chart(fig_estacion, use_container_width=True)
