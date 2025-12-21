import streamlit as st
from db.connection import DuckDBConnection

@st.cache_data
def get_fases_por_anio():
    con = DuckDBConnection()
    query = """
        SELECT
            anio,
            fase,
            COUNT(*) AS meses
        FROM dw.dim_enso
        GROUP BY anio, fase
        ORDER BY anio
    """
    return con.execute(query).df()


@st.cache_data
def get_distribucion_fases():
    con = DuckDBConnection()
    query = """
        SELECT
            fase,
            COUNT(*) AS meses,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
        FROM dw.dim_enso
        GROUP BY fase
    """
    return con.execute(query).df()


@st.cache_data
def get_distribucion_fases_by_lapse(start, end):
    con = DuckDBConnection()
    query = f"""
        SELECT
            fase,
            COUNT(*) AS meses,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
                2
            ) AS porcentaje
        FROM dw.dim_enso
        WHERE anio BETWEEN {start} AND {end}
        GROUP BY fase
        ORDER BY fase
    """
    return con.execute(query).df()


@st.cache_data
def get_oni_temporal(anio_inicio, anio_fin):
    con = DuckDBConnection()
    query = f"""
        SELECT
            anio,
            mes,
            oni,
            fase
        FROM dw.dim_enso
        WHERE anio BETWEEN {anio_inicio} AND {anio_fin}
        ORDER BY anio, mes
    """
    return con.execute(query).df()


@st.cache_data
def get_enso_por_anio_fase_intensidad(intensidad):
    con = DuckDBConnection()
    query = """
        SELECT
            anio,
            fase,
            COUNT(*) AS meses
        FROM dw.dim_enso
        WHERE intensidad = ?
        GROUP BY anio, fase
        ORDER BY anio
    """
    return con.execute(query, [intensidad]).df()


@st.cache_data
def get_intensidad_ultimos_20_anios():
    con = DuckDBConnection()
    query = """
        SELECT
            intensidad,
            COUNT(*) AS meses,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
                2
            ) AS porcentaje
        FROM dw.dim_enso
        WHERE anio >= (SELECT MAX(anio) - 19 FROM dw.dim_enso)
        GROUP BY intensidad
    """
    return con.execute(query).df()


@st.cache_data
def get_enso_por_estacion_20_anios(estacion):
    con = DuckDBConnection()

    estaciones = {
        "DJF": (12, 1, 2),
        "MAM": (3, 4, 5),
        "JJA": (6, 7, 8),
        "SON": (9, 10, 11)
    }

    meses = estaciones[estacion]

    query = f"""
        SELECT
            fase,
            COUNT(*) AS meses,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
                2
            ) AS porcentaje
        FROM dw.dim_enso
        WHERE
            anio >= (SELECT MAX(anio) - 19 FROM dw.dim_enso)
            AND mes IN {meses}
        GROUP BY fase
    """
    return con.execute(query).df()

@st.cache_data
def get_indice_por_fase_y_periodo(indice_sql, fase, anio_inicio, anio_fin):
    con = DuckDBConnection()

    query = f"""
        SELECT
            anio,
            mes,
            {indice_sql} AS valor
        FROM dw.dim_enso
        WHERE
            fase = ?
            AND anio BETWEEN ? AND ?
        ORDER BY anio, mes
    """
    return con.execute(query, [fase, anio_inicio, anio_fin]).df()
