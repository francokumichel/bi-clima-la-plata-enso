import pandas as pd

def filtrar_periodo(df, ini=1961, fin=2024):
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df[(df["fecha"].dt.year >= ini) & (df["fecha"].dt.year <= fin)]

def daily_from_hourly(df):
    df_mean = (
        df.groupby("fecha", as_index=False)
        .mean()
        .rename(columns={"temp": "t_media"})
        .drop(columns=["hora"])
    )

    df_max = (
        df.groupby("fecha", as_index=False)
        .max()
        .rename(columns={"temp": "t_max"})
        .drop(columns=["pp", "hora"])
    )

    df_min = (
        df.groupby("fecha", as_index=False)
        .min()
        .rename(columns={"temp": "t_min"})
        .drop(columns=["pp", "hora"])
    )

    return df_mean.merge(df_min, on="fecha").merge(df_max, on="fecha")
