import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ENSO_COLORS = {
    "Niño": "rgba(255, 0, 0, 0.15)",
    "Niña": "rgba(0, 0, 255, 0.15)",
    "Neutro": "rgba(160, 160, 160, 0.15)"
}

def timeseries_con_sombreado_enso(df, indice, unidad):
    fig = go.Figure()

    # Línea del índice extremo
    fig.add_trace(
        go.Scatter(
            x=df["anio"],
            y=df["valor"],
            mode="lines+markers",
            name=indice,
            line=dict(color="black")
        )
    )

    # Sombreado ENSO
    for _, row in df.iterrows():
        fig.add_vrect(
            x0=row["anio"] - 0.5,
            x1=row["anio"] + 0.5,
            fillcolor=ENSO_COLORS.get(row["fase"], "rgba(200,200,200,0.1)"),
            opacity=0.5,
            layer="below",
            line_width=0
        )

    fig.update_layout(
        title=f"Serie temporal de {indice} con fases ENSO",
        xaxis_title="Año",
        yaxis_title=unidad,
        template="simple_white",
        showlegend=False
    )

    return fig

def line_chart(df, x, y, title, y_label):
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        labels={
            x: "Año",
            y: y_label
        },
        title=title
    )
    fig.update_layout(template="simple_white")
    return fig

def boxplot_indice(df, indice, unidad, estacion=None):
    titulo = f"Distribución de {indice}"
    if estacion:
        titulo += f" – {estacion}"

    fig = px.box(
        df,
        y="valor",
        points="outliers",
        title=titulo,
        labels={"valor": unidad}
    )

    fig.update_layout(
        yaxis_title=unidad,
        showlegend=False
    )

    return fig

def histogram_indice(
    df,
    indice,
    unidad,
    estacion=None,
    bins=20
):
    titulo = f"Distribución de {indice}"
    if estacion:
        titulo += f" – {estacion}"

    fig = px.histogram(
        df,
        x="valor",
        nbins=bins,
        marginal="rug",  # muestra densidad en el eje
        title=titulo,
        labels={
            "valor": f"{indice} ({unidad})",
            "count": "Frecuencia"
        },
        opacity=0.75
    )

    fig.update_layout(
        bargap=0.05,
        template="plotly_white"
    )

    return fig
