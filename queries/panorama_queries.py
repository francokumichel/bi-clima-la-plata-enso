import streamlit as st
from db.connection import DuckDBConnection

@st.cache_data
def extremos_anual(indice, anio_inicio, anio_fin):
    con = DuckDBConnection()
    query = f"""
        SELECT
            anio,
            {indice} AS valor
        FROM dw.fact_extremos_anual
        WHERE anio BETWEEN ? AND ?
        ORDER BY anio
    """
    return con.execute(query, [anio_inicio, anio_fin]).df()

@st.cache_data
def extremos_estacional(indice, estacion, anio_inicio, anio_fin):
    con = DuckDBConnection()
    query = f"""
        SELECT
            anio,
            {indice} AS valor
        FROM dw.fact_extremos_estacional
        WHERE estacion = ?
          AND anio BETWEEN ? AND ?
        ORDER BY anio
    """
    return con.execute(query, [estacion, anio_inicio, anio_fin]).df()

def distribucion_indice(indice, anio_inicio, anio_fin, estacion=None):
    con = DuckDBConnection()

    if estacion is None:
        query = f"""
        SELECT
            anio,
            {indice} AS valor
        FROM dw.fact_extremos_anual
        WHERE anio BETWEEN ? AND ?
          AND {indice} IS NOT NULL
        ORDER BY anio
        """
        params = [anio_inicio, anio_fin]

    else:
        query = f"""
        SELECT
            anio,
            estacion,
            {indice} AS valor
        FROM dw.fact_extremos_estacional
        WHERE estacion = ?
          AND anio BETWEEN ? AND ?
          AND {indice} IS NOT NULL
        ORDER BY anio
        """
        params = [estacion, anio_inicio, anio_fin]

    return con.execute(query, params).df()

