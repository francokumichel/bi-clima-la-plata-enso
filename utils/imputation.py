from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import pandas as pd

def ajustar_modelo_periodo(y, X, min_n=365):
    df = pd.concat([y, X], axis=1).dropna()

    if len(df) < min_n:
        return None

    model = LinearRegression()
    model.fit(df.iloc[:, 1:], df.iloc[:, 0])

    return {
        "modelo": model,
        "coef": model.coef_,
        "intercepto": model.intercept_,
        "r2": r2_score(df.iloc[:, 0], model.predict(df.iloc[:, 1:])),
        "n": len(df)
    }

def imputar_serie(serie, modelos, X):
    out = serie.copy()

    for bloque in modelos:
        ini, fin = bloque["periodo"]
        model = bloque["modelo"]
        cols = bloque["pred_cols"]

        for fecha in out.loc[ini:fin].index:
            if pd.notna(out.loc[fecha]):
                continue

            vals = X.loc[fecha, cols]
            if vals.isna().any():
                continue

            out.loc[fecha] = model.predict([vals.values])[0]

    return out
