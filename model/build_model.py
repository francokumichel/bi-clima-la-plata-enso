from db.connection import DuckDBConnection
from model.create_model import create_model
from model.load_dims import load_dim_fecha, load_dim_enso
from model.load_facts import (
    load_fact_clima,
    load_fact_extremos_anual,
    load_fact_extremos_estacional
)

def build_model():
    con = DuckDBConnection()
    try:
        create_model(con)

        load_dim_fecha(con)
        load_dim_enso(con)

        load_fact_clima(con)
        load_fact_extremos_anual(con)
        load_fact_extremos_estacional(con)

    except Exception as e:
        print(f"Error al construir el modelo: {e}")
        raise

build_model()
