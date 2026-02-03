import streamlit as st
from db.connection import DuckDBConnection

@st.cache_data
def get_registros_por_anio():
    
    con = DuckDBConnection()
    query = """
        SELECT
            d.anio,
            COUNT(*) AS registros
        FROM dw.fact_clima f
        JOIN dw.dim_fecha d ON f.fecha_id = d.fecha_id
        GROUP BY d.anio
        ORDER BY d.anio
    """
    return con.execute(query).df()
