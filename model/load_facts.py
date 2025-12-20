from db.connection import DuckDBConnection

def load_fact_clima(con: DuckDBConnection):
    con.execute("""
        INSERT INTO dw.fact_clima (
            fecha_id,
            t_min,
            t_max,
            t_media,
            pp
        )
        SELECT
            f.fecha_id,

            lp.t_min,
            lp.t_max,
            lp.t_media,
            lp.pp
        FROM read_csv_auto('data/curated/lp_imputada.csv') lp
        JOIN dw.dim_fecha f
          ON CAST(lp.fecha AS DATE) = f.fecha;
    """)

def load_fact_extremos_anual(con: DuckDBConnection):
    con.execute("""
        INSERT INTO dw.fact_extremos_anual
        SELECT
            anio,
            PRCPTOT, SDII, CWD, CDD,
            R10mm, R20mm, R40mm,
            R95pTOT, R99pTOT,
            Rx1day, Rx5day,
            FD, SU, ID, TR,
            TXx, TNx, TXn, TNn,
            TN10p, TX10p, TN90p, TX90p,
            WSDI, CSDI, DTR, GSL
        FROM read_csv_auto('data/curated/extremos_anuales.csv');
    """)


def load_fact_extremos_estacional(con: DuckDBConnection):
    con.execute("""
        INSERT INTO dw.fact_extremos_estacional
        SELECT
            anio,
            estacion,
            PRCPTOT, SDII, CWD, CDD,
            R10mm, R20mm, R40mm,
            R95pTOT, R99pTOT,
            Rx1day, Rx5day,
            FD, SU, ID, TR,
            TXx, TNx, TXn, TNn,
            TN10p, TX10p, TN90p, TX90p,
            WSDI, CSDI, DTR, GSL
        FROM read_csv_auto('data/curated/extremos_estacionales.csv');
    """)
