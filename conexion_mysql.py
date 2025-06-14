# dashboard/conexion.py

import pymysql
import pandas as pd

# ————————————————
# REEMPLAZA AQUÍ CON TUS CREDENCIALES REALES
# ————————————————
DB_HOST     = "localhost"
DB_USER     = "root"      # ej. "root" o tu usuario real
DB_PASSWORD = ""   # ej. "mi_clave"
DB_NAME     = "ventas_empresa" # ej. "ventas_empresa"
# ————————————————

def obtener_conexion():
    """
    Abre y devuelve una conexión a MySQL usando pymysql.
    """
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def ejecutar_query(sql):
    """
    Ejecuta la consulta SQL usando cursor.execute() y devuelve un DataFrame de pandas.
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            filas = cursor.fetchall()  # Devuelve lista de diccionarios [{ 'total': 12345.00 }, ...]
            # Creamos un DataFrame a partir de esa lista
            df = pd.DataFrame(filas)
        return df
    finally:
        conn.close()
