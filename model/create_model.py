from db.connection import DuckDBConnection

def create_model(con: DuckDBConnection):
    con.execute("""
        CREATE SCHEMA IF NOT EXISTS dw;

        -- =========================
        -- DIMENSION FECHA
        -- =========================
        CREATE TABLE IF NOT EXISTS dw.dim_fecha (
            fecha_id INTEGER PRIMARY KEY,
            fecha DATE NOT NULL UNIQUE,

            anio INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            dia INTEGER NOT NULL,

            dia_juliano INTEGER NOT NULL,
            trimestre INTEGER NOT NULL,

            estacion_anio VARCHAR NOT NULL  -- DJF, MAM, JJA, SON
        );

        -- =========================
        -- DIMENSION ENSO (mensual)
        -- =========================
        CREATE TABLE IF NOT EXISTS dw.dim_enso (
            enso_id INTEGER PRIMARY KEY,

            anio INTEGER NOT NULL,
            mes INTEGER NOT NULL,

            mei DOUBLE,
            nino12 DOUBLE,
            nino3 DOUBLE,
            nino34 DOUBLE,
            nino4 DOUBLE,
            oni DOUBLE,
            soi DOUBLE,

            fase VARCHAR NOT NULL,        -- Niño, Niña, Neutro
            UNIQUE (anio, mes)
        );

        -- =========================
        -- FACT CLIMA (diario)
        -- =========================
        CREATE TABLE IF NOT EXISTS dw.fact_clima (
            fecha_id INTEGER PRIMARY KEY,

            t_min DOUBLE,
            t_max DOUBLE,
            t_media DOUBLE,
            pp DOUBLE,

            FOREIGN KEY (fecha_id) REFERENCES dw.dim_fecha(fecha_id)
        );

        -- =========================
        -- FACT EXTREMOS ANUAL
        -- =========================
        
        CREATE TABLE IF NOT EXISTS dw.fact_extremos_anual (
            anio INTEGER PRIMARY KEY,
            PRCPTOT DOUBLE,
            SDII DOUBLE,
            CWD INTEGER,
            CDD INTEGER,
            R10mm INTEGER,
            R20mm INTEGER,
            R40mm INTEGER,
            R95pTOT DOUBLE,
            R99pTOT DOUBLE,
            Rx1day DOUBLE,
            Rx5day DOUBLE,
            FD INTEGER,
            SU INTEGER,
            ID INTEGER,
            TR INTEGER,
            TXx DOUBLE,
            TNx DOUBLE,
            TXn DOUBLE,
            TNn DOUBLE,
            TN10p DOUBLE,
            TX10p DOUBLE,
            TN90p DOUBLE,
            TX90p DOUBLE,
            WSDI INTEGER,
            CSDI INTEGER,
            DTR DOUBLE,
            GSL DOUBLE
        );

        CREATE TABLE IF NOT EXISTS dw.fact_extremos_estacional (
            anio INTEGER NOT NULL,
            estacion VARCHAR NOT NULL,
            PRCPTOT DOUBLE,
            SDII DOUBLE,
            CWD INTEGER,
            CDD INTEGER,
            R10mm INTEGER,
            R20mm INTEGER,
            R40mm INTEGER,
            R95pTOT DOUBLE,
            R99pTOT DOUBLE,
            Rx1day DOUBLE,
            Rx5day DOUBLE,
            FD INTEGER,
            SU INTEGER,
            ID INTEGER,
            TR INTEGER,
            TXx DOUBLE,
            TNx DOUBLE,
            TXn DOUBLE,
            TNn DOUBLE,
            TN10p DOUBLE,
            TX10p DOUBLE,
            TN90p DOUBLE,
            TX90p DOUBLE,
            WSDI INTEGER,
            CSDI INTEGER,
            DTR DOUBLE,
            GSL DOUBLE,
            PRIMARY KEY (anio, estacion)
        );
    """)
