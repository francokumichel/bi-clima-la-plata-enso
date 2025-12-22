def load_dim_fecha(con):
    con.execute("""
        INSERT INTO dw.dim_fecha
        SELECT
            ROW_NUMBER() OVER (ORDER BY fecha) AS fecha_id,
            fecha,

            EXTRACT(YEAR FROM fecha) AS anio,
            EXTRACT(MONTH FROM fecha) AS mes,
            EXTRACT(DAY FROM fecha) AS dia,

            EXTRACT(DOY FROM fecha) AS dia_juliano,
            EXTRACT(QUARTER FROM fecha) AS trimestre,

            CASE
                WHEN EXTRACT(MONTH FROM fecha) IN (12,1,2) THEN 'DJF'
                WHEN EXTRACT(MONTH FROM fecha) IN (3,4,5) THEN 'MAM'
                WHEN EXTRACT(MONTH FROM fecha) IN (6,7,8) THEN 'JJA'
                ELSE 'SON'
            END AS estacion_anio
        FROM generate_series(
            DATE '1961-01-01',
            DATE '2024-12-31',
            INTERVAL 1 DAY
        ) AS t(fecha);
    """)

def load_dim_enso(con):
    con.execute("""
        INSERT INTO dw.dim_enso
        SELECT
            ROW_NUMBER() OVER (ORDER BY fecha) AS enso_id,

            EXTRACT(YEAR FROM fecha) AS anio,
            EXTRACT(MONTH FROM fecha) AS mes,

            mei,
            nino12,
            nino3,
            nino34,
            nino4,
            oni,
            soi,
            fase,

        FROM read_csv_auto('data/curated/enso.csv');
    """)
