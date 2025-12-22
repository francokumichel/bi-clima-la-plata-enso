import streamlit as st
from db.connection import DuckDBConnection

@st.cache_data
def enso_dominante_anual():
    con = DuckDBConnection()
    query = """
        SELECT
            anio,
            fase,
            COUNT(*) AS meses
        FROM dw.dim_enso
        GROUP BY anio, fase
        QUALIFY ROW_NUMBER() OVER (
            PARTITION BY anio
            ORDER BY meses DESC
        ) = 1
        ORDER BY anio
    """
    return con.execute(query).df()

@st.cache_data
def extremos_vs_enso_anual(indice, anio_inicio, anio_fin):
    con = DuckDBConnection()
    query = f"""
        WITH enso_anual AS (
            SELECT
                anio,
                fase,
                COUNT(*) AS meses
            FROM dw.dim_enso
            GROUP BY anio, fase
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY anio
                ORDER BY meses DESC
            ) = 1
        )
        SELECT
            f.anio,
            e.fase,
            f.{indice} AS valor
        FROM dw.fact_extremos_anual f
        JOIN enso_anual e USING (anio)
        WHERE f.anio BETWEEN ? AND ?
          AND f.{indice} IS NOT NULL
        ORDER BY f.anio
    """
    return con.execute(query, [anio_inicio, anio_fin]).df()

@st.cache_data
def extremos_vs_enso_estacional(indice, estacion, anio_inicio, anio_fin):

    estaciones_meses = {
        "Verano": (12, 1, 2),
        "Otoño": (3, 4, 5),
        "Invierno": (6, 7, 8),
        "Primavera": (9, 10, 11)
    }

    meses = estaciones_meses[estacion]

    con = DuckDBConnection()
    query = f"""
        WITH enso_estacion AS (
            SELECT
                anio,
                fase,
                COUNT(*) AS meses
            FROM dw.dim_enso
            WHERE mes IN ({",".join(map(str, meses))})
            GROUP BY anio, fase
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY anio
                ORDER BY COUNT(*) DESC
            ) = 1
        )
        SELECT
            f.anio,
            e.fase,
            f.{indice} AS valor
        FROM dw.fact_extremos_estacional f
        JOIN enso_estacion e USING (anio)
        WHERE f.estacion = ?
          AND f.anio BETWEEN ? AND ?
          AND f.{indice} IS NOT NULL
        ORDER BY f.anio
    """

    return con.execute(
        query,
        [estacion, anio_inicio, anio_fin]
    ).df()

@st.cache_data
def scatter_enso_vs_extremo(indice_extremo, indice_enso, anio_inicio, anio_fin):
    con = DuckDBConnection()
    query = f"""
        SELECT
            f.anio,
            AVG(e.{indice_enso}) AS enso_valor,
            f.{indice_extremo} AS extremo_valor,
            MAX(e.fase) AS fase
        FROM dw.fact_extremos_anual f
        JOIN dw.dim_enso e
          ON f.anio = e.anio
        WHERE f.anio BETWEEN ? AND ?
          AND e.{indice_enso} IS NOT NULL
          AND f.{indice_extremo} IS NOT NULL
        GROUP BY f.anio, f.{indice_extremo}
        ORDER BY f.anio
    """
    return con.execute(query, [anio_inicio, anio_fin]).df()

def anomalias_extremos_por_fase_anual(indice, anio_inicio, anio_fin):
    con = DuckDBConnection()
    query = f"""
        WITH enso_anual AS (
            SELECT
                anio,
                fase,
                COUNT(*) AS meses
            FROM dw.dim_enso
            GROUP BY anio, fase
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY anio
                ORDER BY meses DESC
            ) = 1
        ),

        extremos_enso AS (
            SELECT
                f.anio,
                e.fase,
                f.{indice} AS valor
            FROM dw.fact_extremos_anual f
            JOIN enso_anual e USING (anio)
            WHERE f.anio BETWEEN ? AND ?
              AND f.{indice} IS NOT NULL
        ),

        climatologia AS (
            SELECT AVG(valor) AS media_climatologica
            FROM extremos_enso
        )

        SELECT
            fase,
            AVG(valor) - (SELECT media_climatologica FROM climatologia) AS anomalia
        FROM extremos_enso
        GROUP BY fase
        ORDER BY fase
    """

    return con.execute(query, [anio_inicio, anio_fin]).df()
