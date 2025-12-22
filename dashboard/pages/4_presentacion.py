import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Presentación TABI – TP Final",
    layout="wide"
)

# =========================
# TÍTULO
# =========================
st.title("🌍 Análisis Climático y ENSO")
st.markdown(
    """
    **Objetivo de la presentación:**  
    Exponer el proceso completo de obtención, tratamiento, modelado y análisis
    de datos climáticos, con foco en el fenómeno **ENSO** y su relación con el
    panorama climático regional.
    """
)

st.markdown("---")

# =========================
# INTRODUCCIÓN Y TECNOLOGÍAS
# =========================
st.markdown("## ✍ Introducción y tecnologías utilizadas")

st.markdown(
    """
    **Presentación del proyecto**
    - Análisis de datos climáticos reales
    - Enfoque exploratorio y comparativo
    - Integración de índices ENSO y variables meteorológicas

    **Tecnologías empleadas**
    - Python  
    - Pandas (análisis y transformación)
    - Google Colab (procesamiento inicial)
    - DuckDB (motor analítico, eficiente para grandes volúmenes de datos)
    - Streamlit (visualización y exposición)
    """
)

st.markdown("---")

# =========================
# CLASIFICACIÓN ENSO
# =========================
st.markdown("""## ¿Qué es el ENSO?
##### 🧭 Fenómeno de escala global que actúa cómo un patrón climático natural "anómalo" del océano Pacífico tropical.
###### ➬ Desempeña un papel fundamental en la variabilidad interanual del clima sudamericano.
###### ➬ Sus fases varían alternandose, cambiando su intensidad .
""")


st.markdown("## 🌊 Clasificación ENSO")
st.markdown(
    """
    #### ✔ _El Niño_: Fase cálida. Generalmente trae más lluvias (Reg. pampeana y el centro-oeste).
    #### ✔ _La Niña_: Fase fría. Disminución de precipitaciones y aumento de sequías en varias regiones.
    #### ✔ _Condición Neutra_: Ausencia de anomalías significativas en la temperatura superficial del mar.

    ###### **Criterios de clasificación**
    ###### - Temperatura superficial del mar
    ###### - Índices oceánicos y atmosféricos

    ###### **Importancia**
    ###### - Impacto directo en temperatura y precipitaciones
    ###### - Influencia en eventos climáticos extremos
    """
)

st.markdown("---")

# =========================
# SOLICITUD Y OBTENCIÓN DE DATOS
# =========================
st.markdown("## 📂 Solicitud y obtención de datos")

st.markdown(
    """
    #### **Origen de los datos:** Solicitud inicial al MSN de variables (Estación AERO La Plata)
    ##### - Estaciones adicionales:
    ######    - Ezeiza
    ######    - CABA (Observatorio)
    ######    - AeroParque CABA
    ######    - Punta Indio

    #### **Variables solicitadas**
    #####  - Temperatura máxima, media y mínima
    #####  - Precipitaciones diarias

    #### **Formato original**
    ##### - Archivos .txt
    ##### - Presencia de datos faltantes

    """
)

st.markdown("---")

# =========================
# TRATAMIENTO Y PROCESAMIENTO
# =========================
st.markdown("## 🧤 Tratamiento y procesamiento de datos")

st.markdown(
    """
    #### **Procesamiento inicial**
    ##### - Análisis exploratorio con Pandas
    ##### - Trabajo en Google Colab (notebooks)
    ##### - Identificación de faltantes e inconsistencias

    #### **Precipitaciones**
    ##### - Series incompletas
    ##### - Descarte de datos originales
    ##### - Uso de dataset del ensayo:*“Variación de índices extremos y precipitaciones”*

    ##### Cómo resultado se obtuvieron datasets limpios y completos para el análisis posterior en formato .csv

    """
)

st.markdown("---")

# =========================
# DATA QUALITY
# =========================
st.markdown("## 📐 Proceso de Data Quality")

st.markdown(
    """
    ##### **Relleno de datos**
    ###### - Regresión Lineal Múltiple (RLM)
    ###### - Uso de valores cercanos en el tiempo

    #### **Control de calidad**
    ###### - Tests de homogeneidad
    ###### - Detección de rupturas temporales

    #### **Objetivo**
    ###### - Asegurar consistencia estadística
    ###### - Garantizar confiabilidad del análisis

    #### **Resultado**
    ###### - Series homogéneas
    ###### - Datos validados
    ###### - Re-conversión final a .csv
    ###### - Obtención de índices para poder explotar en el análisis

    *(Mención de rolling window)*
    """
)
st.markdown("---")

# =========================
# MODELADO DIMENSIONAL
# =========================
st.markdown("## 🌐 Modelado y estructura elegida")

# Crear columnas: izquierda (texto) | derecha (imagen)
col_texto, col_img = st.columns([2, 1])  # ajustá proporción si querés

with col_texto:
    st.markdown(
        """
        #### **Tablas de hechos**
        ##### - Clima diario (temperatura y precipitación – granularidad diaria)
        ##### - Valores extremos **ANUALES** (conjunto de parámetros, granularidad anual)
        ##### - Valores extremos **ESTACIONALES** (conjunto de parámetros, granularidad anual por estación)

        #### **Dimensiones**
        ##### - Fecha (Día, Mes, Año, Trimestre, Estación, Día Juliano)
        ##### - ENSO (MEI, ONI, Niño 3.4, Fase ENSO, etc.)

        #### *Beneficios*
        ##### - Claridad semántica (procesos de negocio reales y distintos)
        ##### - Granularidad adecuada
        ##### - Facilidad de mantenimiento

        **Motor analítico**
        - DuckDB  
        - Consultas SQL embebidas en Python
        """
    )
with col_img:
    with st.expander("Ver esquema dimensional"):
        st.image(
            "dashboard/modelo_dimensional.png",
            use_container_width=True
        )

st.markdown("---")

# =========================
# DASHBOARD
# =========================
st.markdown("## 📊 Dashboard y análisis visual")

st.markdown(
    """
    **Características principales**
    - Visualización interactiva
    - Filtros temporales y por fase ENSO
    - Comparación de índices climáticos

    **Ejemplos a mostrar**
    - Evolución temporal de índices ENSO
    - Boxplots para detección de valores extremos
    - Análisis estacional y de intensidad

    *(Navegar el dashboard mientras se explica)*
    """
)

st.markdown("---")

# =========================
# CIERRE
# =========================
st.markdown("## ❓ Cierre y preguntas")

st.markdown(
    """
    **Conclusión**
    - Integración de datos reales
    - Proceso completo de análisis
    - Herramienta flexible para exploración climática

    **Espacio para preguntas**
    """
)
