from pyhomogeneity import pettitt_test, snht_test, buishand_u_test
import pandas as pd

def aplicar_tests(series):
    res = {}

    for test, fn in {
        "pettitt": pettitt_test,
        "snht": snht_test,
        "buishand": buishand_u_test
    }.items():
        r = fn(series)
        res[test] = {
            "h": r.h,
            "cp": r.cp if pd.notna(r.cp) else None,
            "p": r.p
        }

    return res

def construir_periodos(df_quiebres, fecha_ini, fecha_fin):
    fechas = (
        [fecha_ini]
        + sorted(df_quiebres["fecha_quiebre"].tolist())
        + [fecha_fin]
    )

    return [
        (fechas[i], fechas[i + 1])
        for i in range(len(fechas) - 1)
    ]
