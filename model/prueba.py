from db.connection import DuckDBConnection

con = DuckDBConnection()

def test_database(con):
    '''
    Consultas básicas a la base de datos para probar que funciona.
    '''
    try:
        print(con.execute('''
            SELECT
                (SELECT COUNT(*) FROM dw.dim_fecha)          AS dias,
                (SELECT COUNT(*) FROM dw.dim_enso)           AS meses_enso,
                (SELECT COUNT(*) FROM dw.fact_clima)         AS registros_clima,
                (SELECT COUNT(*) FROM dw.fact_extremos_anual)     AS extremos_anual,
                (SELECT COUNT(*) FROM dw.fact_extremos_estacional) AS extremos_estacional;
        ''').fetchone())

        print(con.execute('''
            SELECT COUNT(*) AS sin_enso
            FROM dw.fact_clima fc
            JOIN dw.dim_fecha f ON fc.fecha_id = f.fecha_id
            LEFT JOIN dw.dim_enso e ON f.anio = e.anio
                                    AND f.mes  = e.mes
            WHERE e.enso_id IS NULL;
        ''').fetchall())
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        raise    
    
test_database(con)