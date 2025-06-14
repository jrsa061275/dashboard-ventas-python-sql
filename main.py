import sys
import os

# ────────────────────────────────────────────────────────────────────────────────
# 1) Añadimos la carpeta actual (dashboard/) al PYTHONPATH
#    para que Python encuentre los módulos locales antes de importarlos
# ────────────────────────────────────────────────────────────────────────────────
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from prophet import Prophet
import datetime
from consultas import (
    ingresos_totales,
    total_transacciones,
    categoria_top,
    monto_categoria_anterior,
    producto_top,
    monto_producto_anterior,
    unidades_vendidas,
    nuevos_clientes,
    promedio_items_por_transaccion,
    top_vendedores,
    top_productos,
    ingresos_transacciones_mensuales
)
from utils import formatear_moneda_chile, calcular_variacion_porcentual, calcular_ticket_promedio
from graficos import grafico01_comparativo, grafico02_transacciones_combinado,grafico_forecasting
from datetime import date





def main():
    # ────────────────────────────────────────────────────────────────────────────────
    # 1) Obtienes el año actual (o el año que tú quieras)
    # ────────────────────────────────────────────────────────────────────────────────
    hoy = datetime.date.today()
    anio = hoy.year

    # 2) Fechas de inicio y fin para el año actual
    primer_dia = datetime.date(anio, 1, 1)
    fecha_inicio = primer_dia.strftime("%Y-%m-%d")
    fecha_fin    = hoy.strftime("%Y-%m-%d")

    # 3) Fechas de inicio y fin para el año anterior
    anio_anterior = anio - 1
    primer_dia_anterior = datetime.date(anio_anterior, 1, 1)
    # Para comparar hasta la misma fecha del año anterior (mismo día/mes)
    fecha_inicio_anterior = primer_dia_anterior.strftime("%Y-%m-%d")
    fecha_fin_anterior    = date(anio_anterior, hoy.month, hoy.day).strftime("%Y-%m-%d")

    # ────────────────────────────────────────────────────────────────────────────────
    # CONFIGURACIÓN DE LA PÁGINA EN “MODO ANCHO”
    # ────────────────────────────────────────────────────────────────────────────────
    st.set_page_config(
        page_title=f"Panel de Ventas Empresa {anio}",
        layout="wide"
    )

    # ────────────────────────────────────────────────────────────────────────────────
    # INYECTAR CSS PARA FONDO GRIS Y ESTILO DE TARJETAS KPI
    # ────────────────────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <style>
          /* 1.1) Aseguramos que cada “card” use el 100% del ancho de su columna */
          .stColumn > div {
              width: 100%;
              margin-bottom: 1rem;    /* Espacio debajo de cada tarjeta */
          }

          /* 1.2) Estilos generales para tarjetas KPI y para tarjetas de gráficos */
          .card {
              background: #ffffff;
              border-radius: 10px;
              padding: 16px;
              margin: 8px 0;                /* Márgenes verticales entre tarjetas */
              box-shadow: 0 2px 4px rgba(0,0,0,0.1);
              text-align: center;
              font-family: Arial, sans-serif;
              width: 100%;
          }
          .card-title {
              font-size: 16px;
              color: #1F3B73;
              margin-bottom: 6px;
              font-weight: bold;
          }
          /* Para mostrar un contenido interno (gráfico) con un pequeño espaciado */
          .card-content {
              padding-top: 8px;
          }

          /* 1.3) Reglas específicas para las tarjetas KPI existentes */
          .card-value {
              font-size: 24px;
              font-weight: bold;
              color: #1F3B73;
              margin: 4px 0;
          }
          .card-delta {
              font-size: 14px;
              color: #008f39;   /* positivo en azul */
              margin: 2px 0;
          }
          .card-delta.negative {
              color: #FF0000;   /* negativo en rojo */
          }
          .card-subtext {
              font-size: 12px;
              color: #666666;
              margin-top: 4px;
          }

          .card .card-title {
            text-align: center;
            font-size: 1.25rem;
            margin-bottom: 12px;
          }
          /* Tabla centrada dentro del card */
            .card .table {
                margin: 0 auto;
                border-collapse: collapse;
                width: auto;
            }
             /* Encabezados y celdas centrados */
                .card .table th,
                .card .table td {
                    text-align: center;
                    padding: 8px;
                    border: 1px solid #ddd;
                }

          /* 1.4) Fondo general de la página en gris muy claro */
          html, body, [class*="css"], .stApp {
              background-color: #eef2f6 !important;
          }

          /* 1.5) Forzar ancho máximo de 1920px y centrar horizontalmente */
          .stApp {
              max-width: 1920px !important;
              margin-left: auto !important;
              margin-right: auto !important;
          }

          /* 1.6) Responsivo: para pantallas < 768px, apilamos columnas */
          @media (max-width: 768px) {
            .stColumns {
                flex-wrap: wrap !important;
            }
            .stColumn {
                width: 100% !important;
                flex: 100% !important;
            }
          }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ────────────────────────────────────────────────────────────────────────────────
    # TÍTULO PRINCIPAL Y RANGO FIJO PARA TODO EL AÑO
    # ────────────────────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <h1 style="text-align:center; margin:2rem 0 1rem 0;">
            Panel de Ventas Empresa {anio}
        </h1>
        <br>
        """,
        unsafe_allow_html=True
    )

    # ────────────────────────────────────────────────────────────────────────────────
    # LLAMADA A LA BASE DE DATOS: OBTENEMOS TODOS LOS KPI
    # ────────────────────────────────────────────────────────────────────────────────

    # 1) Ingresos Totales año actual y año anterior
    ingresos_anio_actual = 0.0
    try:
        resultado = ingresos_totales(fecha_inicio, fecha_fin)
        ingresos_anio_actual = resultado if resultado is not None else 0.0
    except Exception as e:
        st.error(f"Error al obtener ingresos actuales: {e}")

    ingresos_anio_anterior = 0.0
    try:
        resultado = ingresos_totales(fecha_inicio_anterior, fecha_fin_anterior)
        ingresos_anio_anterior = resultado if resultado is not None else 0.0
    except Exception as e:
        st.error(f"Error al obtener ingresos año anterior: {e}")

    try:
        variacion_ingreso_porcentual = calcular_variacion_porcentual(
            ingresos_anio_actual, ingresos_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación de ingresos: {e}")
        variacion_ingreso_porcentual = 0.0

    # 2) Total de Transacciones año actual y año anterior
    transacciones_anio_actual = 0
    try:
        resultado = total_transacciones(fecha_inicio, fecha_fin)
        transacciones_anio_actual = resultado if resultado is not None else 0
    except Exception as e:
        st.error(f"Error al obtener transacciones actuales: {e}")

    transacciones_anio_anterior = 0
    try:
        resultado = total_transacciones(fecha_inicio_anterior, fecha_fin_anterior)
        transacciones_anio_anterior = resultado if resultado is not None else 0
    except Exception as e:
        st.error(f"Error al obtener transacciones año anterior: {e}")

    try:
        variacion_transaccion_porcentual = calcular_variacion_porcentual(
            transacciones_anio_actual, transacciones_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación de transacciones: {e}")
        variacion_transaccion_porcentual = 0.0

    # 3) Categoría Top año actual y año anterior
    cat_id_anio_actual = None
    cat_nombre_anio_actual = ""
    cat_monto_anio_actual = 0.0
    try:
        tupla_actual = categoria_top(fecha_inicio, fecha_fin)
        if tupla_actual is not None and len(tupla_actual) == 3:
            cat_id_anio_actual, cat_nombre_anio_actual, cat_monto_anio_actual = tupla_actual
        else:
            # Si devuelve None o no tiene 3 elementos, dejamos valores por defecto
            cat_id_anio_actual, cat_nombre_anio_actual, cat_monto_anio_actual = (None, "", 0.0)
    except Exception as e:
        st.error(f"Error al obtener categoría top año actual: {e}")

    cat_monto_anio_anterior = 0.0
    try:
        if cat_id_anio_actual is not None:
            resultado = monto_categoria_anterior(
                cat_id_anio_actual, fecha_inicio_anterior, fecha_fin_anterior
            )
            cat_monto_anio_anterior = resultado if resultado is not None else 0.0
        else:
            cat_monto_anio_anterior = 0.0
    except Exception as e:
        st.error(f"Error al obtener monto categoría año anterior: {e}")

    try:
        variacion_transaccion_porcentual_cat = calcular_variacion_porcentual(
            cat_monto_anio_actual, cat_monto_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación categoría: {e}")
        variacion_transaccion_porcentual_cat = 0.0

    # 4) Producto Top año actual y año anterior
    prod_id_top_actual = None
    prod_nombre_top_actual = ""
    prod_monto_top_actual = 0.0
    try:
        tupla_prod = producto_top(fecha_inicio, fecha_fin)
        if tupla_prod is not None and len(tupla_prod) == 3:
            prod_id_top_actual, prod_nombre_top_actual, prod_monto_top_actual = tupla_prod
        else:
            prod_id_top_actual, prod_nombre_top_actual, prod_monto_top_actual = (None, "", 0.0)
    except Exception as e:
        st.error(f"Error al obtener producto top año actual: {e}")

    prod_monto_top_anterior = 0.0
    try:
        if prod_id_top_actual is not None:
            resultado = monto_producto_anterior(
                prod_id_top_actual, fecha_inicio_anterior, fecha_fin_anterior
            )
            prod_monto_top_anterior = resultado if resultado is not None else 0.0
        else:
            prod_monto_top_anterior = 0.0
    except Exception as e:
        st.error(f"Error al obtener monto producto top año anterior: {e}")

    try:
        variacion_transaccion_porcentual_prod = calcular_variacion_porcentual(
            prod_monto_top_actual, prod_monto_top_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación producto top: {e}")
        variacion_transaccion_porcentual_prod = 0.0

    # 5) Ticket Promedio año actual y año anterior
    try:
        ticket_promedio_anio_actual = calcular_ticket_promedio(
            ingresos_anio_actual, transacciones_anio_actual
        )
    except Exception as e:
        st.error(f"Error al calcular ticket promedio actual: {e}")
        ticket_promedio_anio_actual = 0.0

    try:
        ticket_promedio_anio_anterior = calcular_ticket_promedio(
            ingresos_anio_anterior, transacciones_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular ticket promedio año anterior: {e}")
        ticket_promedio_anio_anterior = 0.0

    try:
        variacion_transaccion_porcentual_ticke = calcular_variacion_porcentual(
            ticket_promedio_anio_actual, ticket_promedio_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación ticket promedio: {e}")
        variacion_transaccion_porcentual_ticke = 0.0

    # 6) Unidades Vendidas Totales año actual y año anterior
    unidades_vendidas_anio_actual = 0
    try:
        resultado = unidades_vendidas(fecha_inicio, fecha_fin)
        unidades_vendidas_anio_actual = resultado if resultado is not None else 0
    except Exception as e:
        st.error(f"Error al obtener unidades vendidas actuales: {e}")

    unidades_vendidas_anio_anterior = 0
    try:
        resultado = unidades_vendidas(fecha_inicio_anterior, fecha_fin_anterior)
        unidades_vendidas_anio_anterior = resultado if resultado is not None else 0
    except Exception as e:
        st.error(f"Error al obtener unidades vendidas año anterior: {e}")

    try:
        variacion_transaccion_porcentual_unidades = calcular_variacion_porcentual(
            unidades_vendidas_anio_actual, unidades_vendidas_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación unidades vendidas: {e}")
        variacion_transaccion_porcentual_unidades = 0.0

    # 7) Nuevos Clientes año actual y año anterior
    nuevos_clientes_anio_actual = 0
    try:
        resultado = nuevos_clientes(fecha_inicio, fecha_fin)
        nuevos_clientes_anio_actual = resultado if resultado is not None else 0
    except Exception as e:
        st.error(f"Error al obtener nuevos clientes actuales: {e}")

    nuevos_clientes_anio_anterior = 0
    try:
        resultado = nuevos_clientes(fecha_inicio_anterior, fecha_fin_anterior)
        nuevos_clientes_anio_anterior = resultado if resultado is not None else 0
    except Exception as e:
        st.error(f"Error al obtener nuevos clientes año anterior: {e}")

    try:
        variacion_transaccion_porcentual_clientes = calcular_variacion_porcentual(
            nuevos_clientes_anio_actual, nuevos_clientes_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación nuevos clientes: {e}")
        variacion_transaccion_porcentual_clientes = 0.0

    # 8) Promedio Items por Transacción año actual y año anterior
    try:
        promedio_item_por_transaccion_anio_actual = promedio_items_por_transaccion(
            fecha_inicio, fecha_fin
        ) or 0.0
    except Exception as e:
        st.error(f"Error al obtener promedio ítems actual: {e}")
        promedio_item_por_transaccion_anio_actual = 0.0

    try:
        promedio_item_por_transaccion_anio_anterior = promedio_items_por_transaccion(
            fecha_inicio_anterior, fecha_fin_anterior
        ) or 0.0
    except Exception as e:
        st.error(f"Error al obtener promedio ítems año anterior: {e}")
        promedio_item_por_transaccion_anio_anterior = 0.0

    try:
        variacion_transaccion_porcentual_promedio_iten_transaccion = calcular_variacion_porcentual(
            promedio_item_por_transaccion_anio_actual,
            promedio_item_por_transaccion_anio_anterior
        )
    except Exception as e:
        st.error(f"Error al calcular variación promedio ítems: {e}")
        variacion_transaccion_porcentual_promedio_iten_transaccion = 0.0

    # ────────────────────────────────────────────────────────────────────────────────
    # MOSTRAR LOS 8 PRIMEROS CUADROS (KPI)
    # ────────────────────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1], gap="large")

    with c1:
        signo_ing = "▲" if variacion_ingreso_porcentual >= 0 else "▼"
        clase_ing = "card-delta" if variacion_ingreso_porcentual >= 0 else "card-delta negative"
        valor_ing = f"{abs(variacion_ingreso_porcentual):.1f} %"
        monto_ing = formatear_moneda_chile(ingresos_anio_actual)
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Ingresos Totales</div>
                <div class="card-value">$ {monto_ing}</div>
                <div class="{clase_ing}">{signo_ing} {valor_ing}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        signo_tx = "▲" if variacion_transaccion_porcentual >= 0 else "▼"
        clase_tx = "card-delta" if variacion_transaccion_porcentual >= 0 else "card-delta negative"
        valor_tx = f"{abs(variacion_transaccion_porcentual):.1f} %"
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Total Transacciones</div>
                <div class="card-value">{transacciones_anio_actual}</div>
                <div class="{clase_tx}">{signo_tx} {valor_tx}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        signo_cat = "▲" if variacion_transaccion_porcentual_cat >= 0 else "▼"
        clase_cat = "card-delta" if variacion_transaccion_porcentual_cat >= 0 else "card-delta negative"
        valor_cat = f"{abs(variacion_transaccion_porcentual_cat):.1f} %"
        monto_cat = formatear_moneda_chile(cat_monto_anio_actual)
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Top Cat.  <strong>({cat_nombre_anio_actual})</strong></div>
                <div class="card-value">$ {monto_cat}</div>
                <div class="{clase_cat}">{signo_cat} {valor_cat}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        signo_prod = "▲" if variacion_transaccion_porcentual_prod >= 0 else "▼"
        clase_prod = "card-delta" if variacion_transaccion_porcentual_prod >= 0 else "card-delta negative"
        valor_prod = f"{abs(variacion_transaccion_porcentual_prod):.1f} %"
        monto_prod = formatear_moneda_chile(prod_monto_top_actual)
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Top Prod.  <strong>({prod_nombre_top_actual})</strong></div>
                <div class="card-value">$ {monto_prod}</div>
                <div class="{clase_prod}">{signo_prod} {valor_prod}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ────────────────────────────────────────────────────────────────────────────────
    # SIGUIENTES 4 CUADROS (KPI)
    # ────────────────────────────────────────────────────────────────────────────────
    c5, c6, c7, c8 = st.columns(4, gap="large")

    with c5:
        signo_tix = "▲" if variacion_transaccion_porcentual_ticke >= 0 else "▼"
        clase_tix = "card-delta" if variacion_transaccion_porcentual_ticke >= 0 else "card-delta negative"
        valor_tix = f"{abs(variacion_transaccion_porcentual_ticke):.1f} %"
        monto_tix = formatear_moneda_chile(ticket_promedio_anio_actual)
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">VPT</div>
                <div class="card-value">$ {monto_tix}</div>
                <div class="{clase_tix}">{signo_tix} {valor_tix}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c6:
        signo_uni = "▲" if variacion_transaccion_porcentual_unidades >= 0 else "▼"
        clase_uni = "card-delta" if variacion_transaccion_porcentual_unidades >= 0 else "card-delta negative"
        valor_uni = f"{abs(variacion_transaccion_porcentual_unidades):.1f} %"
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">UVT</div>
                <div class="card-value">{unidades_vendidas_anio_actual}</div>
                <div class="{clase_uni}">{signo_uni} {valor_uni}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c7:
        signo_cli = "▲" if variacion_transaccion_porcentual_clientes >= 0 else "▼"
        clase_cli = "card-delta" if variacion_transaccion_porcentual_clientes >= 0 else "card-delta negative"
        valor_cli = f"{abs(variacion_transaccion_porcentual_clientes):.1f} %"
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Nuevos Clientes</div>
                <div class="card-value">{nuevos_clientes_anio_actual}</div>
                <div class="{clase_cli}">{signo_cli} {valor_cli}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c8:
        signo_itn = "▲" if variacion_transaccion_porcentual_promedio_iten_transaccion >= 0 else "▼"
        clase_itn = "card-delta" if variacion_transaccion_porcentual_promedio_iten_transaccion >= 0 else "card-delta negative"
        valor_itn = f"{abs(variacion_transaccion_porcentual_promedio_iten_transaccion):.1f} %"
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">PIT</div>
                <div class="card-value">{promedio_item_por_transaccion_anio_actual:.2f}</div>
                <div class="{clase_itn}">{signo_itn} {valor_itn}</div>
                <div class="card-subtext">vs año anterior</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ────────────────────────────────────────────────────────────────────────────────
    # NUEVA FILA: DOS COLUMNAS PARA LOS DOS GRÁFICOS
    # ────────────────────────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    g1, g2 = st.columns(2, gap="large")

    with g1:
        st.altair_chart(
            grafico01_comparativo(),
            use_container_width=True
        )

    with g2:
        st.altair_chart(
            grafico02_transacciones_combinado(),
            use_container_width=True
        )


    # … tu código existente de KPI, filtros y gráficos …

    # ────────────────────────────────────────────────────────────────────────────────
    # TABLAS TOP 10 COMPARATIVAS
    # ────────────────────────────────────────────────────────────────────────────────
   
    # Creamos tres columnas con gap “large” entre ellas
    col_vendedores, col_productos = st.columns(2, gap="large")

        # ────────────────────────────────────────────────────────────────────────────
    # TABLA TOP 5 VENDEDORES + OTROS COMPARATIVOS
    # ────────────────────────────────────────────────────────────────────────────
    # Llamada al helper
    df_top_v = top_vendedores(fecha_inicio, fecha_fin, limit=5)

    # 2) Columnas semánticas
    col_vendedores, col_productos = st.columns([1, 1], gap="large")

    with col_vendedores:
        # Renombrar columnas
        df_v = df_top_v.rename(columns={
            "vendedor": "Vendedor",
            "monto_actual": "Monto Actual",
            "monto_anterior": "Monto Anterior"
        }).copy()

        # Insertar “No.”
        df_v.insert(0, "No.", range(1, len(df_v) + 1))

        # Calcular variación porcentual numérica
        df_v["Variación_raw"] = (
            (df_v["Monto Actual"] - df_v["Monto Anterior"])
            / df_v["Monto Anterior"]
            * 100
        )

        # Mapear a HTML con símbolo y clase
        def format_delta(x):
            sign = "▲" if x >= 0 else "▼"
            cls = "" if x >= 0 else " negative"
            return f'<span class="card-delta{cls}">{sign}{abs(x):.2f}%</span>'

        df_v["Variación %"] = df_v["Variación_raw"].map(format_delta)

        # Formatear montos
        df_v["Monto Actual"]   = df_v["Monto Actual"].map(lambda x: f"$ {x:,.0f}")
        df_v["Monto Anterior"] = df_v["Monto Anterior"].map(lambda x: f"$ {x:,.0f}")

        # Preparamos HTML (permitiendo HTML en celdas)
        tabla_v = df_v.drop(columns="Variación_raw")\
                     .to_html(index=False, classes="table", border=0, escape=False)

        # Renderizamos la card
        st.markdown(f"""
        <div class="card">
          <div class="card-title">Top 5 Vendedores {anio} y {anio_anterior}</div>
          <div style="display:flex; justify-content:center; padding:0 16px 16px;">
            {tabla_v}
          </div>
        </div>
        """, unsafe_allow_html=True)




    # —————— Columna 2: Top Productos (ejemplo) ——————
    with col_productos:
        # 1) Traer los datos de Top 5 Productos
        df_p = top_productos(fecha_inicio, fecha_fin, limit=5)

        # 2) Renombrar columnas para mostrarlas “bonitas”
        df_p = df_p.rename(columns={
            "categoria": "Categoría",
            "producto": "Producto",
            "monto_actual": "Monto Actual",
            "cantidad_actual": "Cantidad"
        }).copy()

        # 3) Insertar la columna “No.” con numeración 1…5
        df_p.insert(0, "No.", range(1, len(df_p) + 1))

        # 4) Formatear el monto como moneda
        df_p["Monto Actual"] = df_p["Monto Actual"].map(lambda x: f"$ {x:,.0f}")

        # 5) Convertir a HTML usando la clase “table” (sin escape para permitir HTML)
        tabla_p = df_p.to_html(index=False, classes="table", border=0)

        # 6) Renderizar dentro del mismo estilo de card, centrado y sin scroll
        st.markdown(f"""
        <div class="card">
        <div class="card-title">Top 5 Productos {anio}</div>
        <div style="display:flex; justify-content:center; padding:0 16px 16px;">
            {tabla_p}
        </div>
        </div>
        """, unsafe_allow_html=True)


    ################ INTELIGENCIA ARTIFICIA PRONOSTICOS#########################
    st.title("Dashboard de Ventas + Forecast")

    hoy = datetime.date.today()
    anio_act = hoy.year
    anio_base = anio_act - 1

    # 1) Calcular el último día del mes completo anterior
    primer_dia_mes = hoy.replace(day=1)              # ej. 2025-06-01
    ultimo_mes_completo = primer_dia_mes - timedelta(days=1)  
    # -> ej. 2025-05-31

    # 2) Rango año base (2024-01-01 → 2024-05-31)
    fecha_inicio_base = f"{anio_base}-01-01"
    fecha_fin_base    = f"{anio_base}-{ultimo_mes_completo.month:02d}-{ultimo_mes_completo.day:02d}"

    # 3) Rango año actual (2025-01-01 → 2025-05-31)
    fecha_inicio_act  = f"{anio_act}-01-01"
    fecha_fin_act     = f"{anio_act}-{ultimo_mes_completo.month:02d}-{ultimo_mes_completo.day:02d}"

    # 4) DEBUG: ver tabla histórica sin junio parcial
    df_debug = ingresos_transacciones_mensuales(fecha_inicio_base, fecha_fin_base)
    st.markdown("### Datos históricos año base (hasta mayo)")
    st.dataframe(df_debug)

    df_debug2 = ingresos_transacciones_mensuales(fecha_inicio_act, fecha_fin_act)
    st.markdown("### Datos históricos año actual (hasta mayo)")
    st.dataframe(df_debug2)

    # 5) Generar gráfico (forecast comenzará en junio-2025)
    chart = grafico_forecasting(
        fecha_inicio_base, fecha_fin_base,
        fecha_inicio_act,   fecha_fin_act,
        meses_proyeccion=12
    )

    st.markdown("### 📈 Forecast de Ingresos Mensuales (sin junio parcial)")
    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
