# dashboard/graficos.py

import pandas as pd  # Librería para manejar datos en forma de tablas
import altair as alt  # Librería para crear gráficos interactivos
from prophet import Prophet  # Librería para hacer predicciones de series temporales
import datetime  # Para trabajar con fechas

# Importamos funciones que traen datos desde la base de datos
from consultas import ingresos_por_periodo, transacciones_por_periodo, ingresos_transacciones_mensuales

# Lista de nombres de meses en español
SPANISH_MONTHS = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]


def grafico01_comparativo():
    """
    Gráfico de líneas comparativo de Ingresos Mensuales:
    - Línea azul: año anterior
    - Línea naranja: año actual
    """
    hoy = datetime.date.today()  # Obtenemos la fecha actual
    anio = hoy.year  # Año actual
    anio_ant = anio - 1  # Año anterior

    # Definimos las fechas para cada año
    fi_act = f"{anio}-01-01"  # Desde enero del año actual
    ff_act = hoy.strftime("%Y-%m-%d")  # Hasta hoy
    fi_ant = f"{anio_ant}-01-01"  # Desde enero del año anterior
    ff_ant = f"{anio_ant}-{hoy.month:02d}-{hoy.day:02d}"  # Hasta el mismo día del año anterior

    # Consultamos los ingresos por mes
    df_act = ingresos_por_periodo(fi_act, ff_act)
    df_ant = ingresos_por_periodo(fi_ant, ff_ant)

    # Columnas necesarias
    cols = ["mes","mes_dt","mes_num","mes_label","total_mes"]
    for df, year in [(df_act, anio), (df_ant, anio_ant)]:
        if df is None or df.empty:
            df = pd.DataFrame(columns=cols)
        df["año"] = year  # Añadimos columna con el año correspondiente

    # Unimos los datos de ambos años en un solo DataFrame
    df = pd.concat([df_ant, df_act], ignore_index=True)

    # Creamos el gráfico
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("mes_num:O", title="Mes", sort=list(range(1,13)),
                   axis=alt.Axis(labelAngle=-45,
                                 labelExpr="[" + ",".join(f"'{m}'" for m in SPANISH_MONTHS) + "][datum.value-1]")),
            y=alt.Y("total_mes:Q", title="Ingresos ($)"),
            color=alt.Color("año:O", title="Año", scale=alt.Scale(domain=[anio_ant, anio], range=["#1f77b4", "#ff7f0e"])),
            tooltip=[
                alt.Tooltip("año:O", title="Año"),
                alt.Tooltip("mes_num:O", title="Mes", format=""),
                alt.Tooltip("total_mes:Q", title="Total", format=",.0f")
            ]
        )
        .properties(
            width=700,
            height=400,
            title={"text": f"Ingresos Mensuales", "anchor": "middle", "fontSize": 20, "fontWeight": "bold", "dy": -10},
            padding={"left":20,"right":20,"top":30,"bottom":20}
        )
        .configure_title(anchor="middle", fontSize=20, fontWeight="bold", dy=-10)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .interactive()
    )
    return chart


def grafico02_transacciones_combinado():
    """
    Gráfico combinado de barras (año actual) y línea (año anterior)
    para comparar las transacciones mensuales
    """
    hoy = datetime.date.today()
    anio = hoy.year
    anio_ant = anio - 1

    # Fechas de inicio y fin para cada año
    fi_act = f"{anio}-01-01"
    ff_act = hoy.strftime("%Y-%m-%d")
    fi_ant = f"{anio_ant}-01-01"
    ff_ant = f"{anio_ant}-{hoy.month:02d}-{hoy.day:02d}"

    # Obtenemos los datos de transacciones
    df_act = transacciones_por_periodo(fi_act, ff_act)
    df_ant = transacciones_por_periodo(fi_ant, ff_ant)

    # Validamos y agregamos columna "año"
    cols = ["mes","mes_dt","mes_num","mes_label","total_transac"]
    if df_act is None or df_act.empty:
        df_act = pd.DataFrame(columns=cols)
    if df_ant is None or df_ant.empty:
        df_ant = pd.DataFrame(columns=cols)

    df_act["año"] = anio
    df_ant["año"] = anio_ant

    # Aseguramos que los meses estén en orden
    meses_orden = list(range(1,13))
    df_act["mes_num"] = df_act["mes_num"].astype(int)
    df_ant["mes_num"] = df_ant["mes_num"].astype(int)

    # Definimos escala de colores para distinguir los años
    color_scale = alt.Scale(domain=[anio, anio_ant], range=["#1f77b4", "#ff7f0e"])

    # Gráfico de barras para el año actual
    barras = (
        alt.Chart(df_act)
        .mark_bar()
        .encode(
            x=alt.X("mes_num:O", title="Mes", sort=meses_orden,
                   axis=alt.Axis(labelAngle=-45,
                                 labelExpr="[" + ",".join(f"'{m}'" for m in SPANISH_MONTHS) + "][datum.value-1]")),
            y=alt.Y("total_transac:Q", title="Transacciones"),
            color=alt.Color("año:O", title="Año", scale=color_scale),
            tooltip=[
                alt.Tooltip("año:O", title="Año"),
                alt.Tooltip("mes_num:O", title="Mes", format=""),
                alt.Tooltip("total_transac:Q", title="Total")
            ]
        )
    )

    # Gráfico de línea para el año anterior
    linea = (
        alt.Chart(df_ant)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("mes_num:O", sort=meses_orden),
            y="total_transac:Q",
            color=alt.Color("año:O", title="Año", scale=color_scale),
            tooltip=[
                alt.Tooltip("año:O", title="Año"),
                alt.Tooltip("mes_num:O", title="Mes", format=""),
                alt.Tooltip("total_transac:Q", title="Total")
            ]
        )
    )

    # Combinamos ambos gráficos
    chart = (
        (barras + linea)
        .properties(
            width=700,
            height=400,
            title={"text": f"Transacciones Mensuales", "anchor": "middle", "fontSize": 20, "fontWeight": "bold", "dy": -10},
            padding={"left":20,"right":20,"top":30,"bottom":20}
        )
        .configure_title(anchor="middle", fontSize=20, fontWeight="bold", dy=-10)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .interactive()
    )

    return chart


def grafico_forecasting(fecha_inicio_base: str, fecha_fin_base: str,
                        fecha_inicio_act:  str, fecha_fin_act:   str,
                        meses_proyeccion:    int = 12) -> alt.Chart:
    """
    Gráfico de líneas con:
    - Serie histórica año base (por ejemplo, 2024)
    - Serie histórica año actual (por ejemplo, 2025)
    - Proyección futura con Prophet
    """
    # Cargamos los datos históricos desde la base
    df_base = ingresos_transacciones_mensuales(fecha_inicio_base, fecha_fin_base)
    df_act  = ingresos_transacciones_mensuales(fecha_inicio_act, fecha_fin_act)
    df_base["año"] = fecha_inicio_base[:4]
    df_act["año"]  = fecha_inicio_act[:4]

    # Preparamos los datos para Prophet
    df_prophet = df_act.copy()
    df_prophet["ds"] = pd.to_datetime(df_prophet["mes"] + "-01")  # fecha
    df_prophet["y"]  = df_prophet["ingresos"]  # variable objetivo
    modelo = Prophet(yearly_seasonality=True)
    modelo.fit(df_prophet[["ds", "y"]])

    # Creamos las fechas futuras y predecimos
    futuro     = modelo.make_future_dataframe(periods=meses_proyeccion, freq="MS")
    pronostico = modelo.predict(futuro)
    df_pred = pronostico[pronostico["ds"] > df_prophet["ds"].max()].copy()
    df_pred["mes"]      = df_pred["ds"].dt.strftime("%Y-%m")
    df_pred["ingresos"] = df_pred["yhat"]
    df_pred["año"]      = "Proyección"

    # Unimos base + actual + proyección
    df_final = pd.concat([
        df_base[["mes","ingresos","año"]],
        df_act[["mes","ingresos","año"]],
        df_pred[["mes","ingresos","año"]]
    ], ignore_index=True)
    df_final["ingresos"] = df_final["ingresos"].astype(float)

    # Formateamos fechas para mostrar mes/año abreviado
    df_final["mes_dt"]    = pd.to_datetime(df_final["mes"] + "-01")
    df_final["mes_label"] = (
        df_final["mes_dt"].dt.month.apply(lambda m: SPANISH_MONTHS[m-1]) + " " + df_final["mes_dt"].dt.year.astype(str)
    )
    orden = df_final.sort_values("mes_dt")["mes_label"].unique().tolist()

    # Creamos el gráfico final
    chart = (
        alt.Chart(df_final)
        .mark_line(point=True)
        .encode(
            x=alt.X("mes_label:O", title="Mes", sort=orden, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("ingresos:Q", title="Ingresos ($)"),
            color=alt.Color("año:N", title="Serie"),
            tooltip=[
                alt.Tooltip("año:N", title="Serie"),
                alt.Tooltip("mes_label:O", title="Mes"),
                alt.Tooltip("ingresos:Q", title="Ingresos", format=",.0f")
            ]
        )
        .properties(
            width=800,
            height=400,
            title="Ingresos Mensuales (Base vs Actual) + Forecast"
        )
        .interactive()
    )
    return chart
