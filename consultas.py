# dashboard/consultas.py

# Importamos datetime para trabajar con fechas
import datetime

# Importamos pandas para manipular datos en DataFrames
import pandas as pd

# Importamos la función ejecutar_query desde conexion.py, que se encarga de ejecutar sentencias SQL
from conexion import ejecutar_query

# -------------------------- FUNCION 1 --------------------------
def ingresos_totales(fecha_inicio: str, fecha_fin: str) -> float:
    """
    Calcula la suma total de ingresos (monto_total) en el rango de fechas dado.
    Devuelve 0.0 si no hay datos.
    """
    # Consulta SQL que suma los montos de la tabla ventas entre dos fechas
    sql = f"""
    SELECT 
        CAST(COALESCE(SUM(monto_total), 0) AS DECIMAL(18,2)) AS total
    FROM ventas
    WHERE fecha_venta BETWEEN '{fecha_inicio}' AND '{fecha_fin}';
    """
    # Ejecutamos la consulta y guardamos el resultado en un DataFrame
    df = ejecutar_query(sql)

    # Si el resultado está vacío, devolvemos 0.0
    if df is None or df.empty:
        return 0.0

    try:
        # Convertimos el primer valor de la columna "total" a float y lo devolvemos
        return float(df.iloc[0]["total"])
    except Exception:
        # Si hay error, devolvemos 0.0
        return 0.0

# -------------------------- FUNCION 2 --------------------------
def total_transacciones(fecha_inicio: str, fecha_fin: str) -> int:
    """
    Cuenta cuántas transacciones se hicieron en el rango de fechas dado.
    """
    # Consulta SQL que cuenta las filas en la tabla ventas entre dos fechas
    sql = f"""
    SELECT 
        COUNT(*) AS total_transacciones
    FROM ventas
    WHERE fecha_venta BETWEEN '{fecha_inicio}' AND '{fecha_fin}';
    """
    # Ejecutamos la consulta
    df = ejecutar_query(sql)

    # Si no hay resultados, devolvemos 0
    if df is None or df.empty:
        return 0

    try:
        # Devolvemos el número total de transacciones como entero
        return int(df.iloc[0]["total_transacciones"])
    except Exception:
        return 0

# -------------------------- FUNCION 3 --------------------------
def categoria_top(fecha_inicio: str, fecha_fin: str):
    """
    Busca la categoria con mayor ingreso entre dos fechas.
    Devuelve id, nombre y monto total de esa categoria.
    """
    # Consulta SQL que agrupa las ventas por categoría y obtiene la que más vendió
    sql = f"""
    SELECT
        c.id AS categoria_id,
        c.nombre AS categoria_top,
        CAST(COALESCE(SUM(v.monto_total), 0) AS DECIMAL(18,2)) AS total_ingresos
    FROM ventas v
    JOIN productos pr ON v.producto_id = pr.id
    JOIN categorias c ON pr.categoria_id = c.id
    WHERE v.fecha_venta BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    GROUP BY c.id, c.nombre
    ORDER BY total_ingresos DESC
    LIMIT 1;
    """
    # Ejecutamos la consulta
    df = ejecutar_query(sql)

    # Si no hay resultados, devolvemos valores vacíos
    if df is None or df.empty:
        return None, None, 0.0

    try:
        # Extraemos el id, nombre y monto de la categoría con más ventas
        categoria_id = int(df.iloc[0]["categoria_id"])
        nombre_cat   = df.iloc[0]["categoria_top"]
        monto_top    = float(df.iloc[0]["total_ingresos"])
        return categoria_id, nombre_cat, monto_top
    except Exception:
        return None, None, 0.0

# -------------------------- FUNCION 4 --------------------------
def monto_categoria_anterior(categoria_id: int, fecha_inicio_ant: str, fecha_fin_ant: str) -> float:
    """
    Dado un ID de categoria y un rango de fechas, devuelve el total vendido en ese periodo.
    """
    # Consulta SQL para obtener el total de ventas de una categoría específica en un periodo
    sql = f"""
    SELECT
        CAST(COALESCE(SUM(v.monto_total), 0) AS DECIMAL(18,2)) AS total_ingresos
    FROM ventas v
    JOIN productos pr ON v.producto_id = pr.id
    WHERE pr.categoria_id = {categoria_id}
      AND v.fecha_venta BETWEEN '{fecha_inicio_ant}' AND '{fecha_fin_ant}';
    """
    # Ejecutamos la consulta
    df = ejecutar_query(sql)

    # Si no hay resultados, devolvemos 0.0
    if df is None or df.empty:
        return 0.0

    try:
        # Devolvemos el total convertido a float
        return float(df.iloc[0]["total_ingresos"])
    except Exception:
        return 0.0

# -------------------------- FUNCION 5 --------------------------
def producto_top(fecha_inicio: str, fecha_fin: str):
    """
    Devuelve el producto con mayor ingreso (nombre, id, monto total).
    """
    # Consulta SQL que agrupa ventas por producto y devuelve el de mayor ingreso
    sql = f"""
    SELECT
        pr.id AS producto_id,
        pr.nombre AS producto_top,
        CAST(COALESCE(SUM(v.monto_total), 0) AS DECIMAL(18,2)) AS monto_total
    FROM ventas v
    JOIN productos pr ON v.producto_id = pr.id
    WHERE v.fecha_venta BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    GROUP BY pr.id, pr.nombre
    ORDER BY monto_total DESC
    LIMIT 1;
    """
    # Ejecutamos la consulta
    df = ejecutar_query(sql)

    # Si no hay datos, devolvemos valores vacíos
    if df is None or df.empty:
        return None, None, 0.0

    try:
        # Obtenemos id, nombre y monto del producto con más ingresos
        producto_id  = int(df.iloc[0]["producto_id"])
        nombre_prod  = df.iloc[0]["producto_top"]
        monto_top    = float(df.iloc[0]["monto_total"])
        return producto_id, nombre_prod, monto_top
    except Exception:
        return None, None, 0.0
