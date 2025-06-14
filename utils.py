
# --------------------------------------------
# utils.py - Funciones de utilidad para dashboard
# --------------------------------------------

# Importamos la librería pandas para manipular datos
import pandas as pd

# ----------------------------------------------------
# FUNCION: formatear_moneda_chile
# ----------------------------------------------------
# Esta función transforma un número float a un formato de moneda chilena
def formatear_moneda_chile(valor_float):
    """
    Recibe un número decimal, por ejemplo: 140937.85
    Y lo transforma a formato chileno: "140.937,85"
    """
    # Paso 1: Formateamos el número con coma como miles y punto decimal → "140,937.85"
    s = f"{valor_float:,.2f}"

    # Paso 2: Intercambiamos las comas y puntos para usar el formato chileno
    # - Primero cambiamos comas por una letra temporal "X"
    # - Luego cambiamos el punto por coma
    # - Finalmente cambiamos la letra "X" por punto
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


# ----------------------------------------------------
# FUNCION: calcular_variacion_porcentual
# ----------------------------------------------------
# Esta función calcula cuánto creció o bajó un valor en porcentaje
def calcular_variacion_porcentual(actual: float, anterior: float) -> float:
    """
    Fórmula: ((actual - anterior) / anterior) * 100
    Si el valor anterior es 0, se evita dividir y se retorna 0.0
    """

    # Si anterior es 0 o None, devolvemos 0.0 para evitar error
    if anterior is None or anterior == 0:
        return 0.0

    try:
        # Calculamos el cambio porcentual
        variacion = ((actual - anterior) / anterior) * 100

        # Redondeamos a 2 decimales y lo devolvemos
        return round(variacion, 2)
    except Exception:
        # Si algo sale mal, devolvemos 0.0 como fallback
        return 0.0


# ----------------------------------------------------
# FUNCION: calcular_ticket_promedio
# ----------------------------------------------------
# Esta función calcula el ticket promedio, o sea:
# ¿Cuánto se vendió en promedio por cada transacción?
def calcular_ticket_promedio(ingresos_totales: float, total_transacciones: int) -> float:
    """
    Si hubo ventas y transacciones, se divide:
        ingresos_totales / total_transacciones

    Si no hubo ninguna transacción, devuelve 0.0 para evitar error.
    """
    try:
        # Si no hay transacciones, no se puede dividir → devuelve 0.0
        if total_transacciones == 0:
            return 0.0

        # Se divide y redondea a 2 decimales
        return round(ingresos_totales / total_transacciones, 2)
    except Exception:
        # Si ocurre un error (por ejemplo tipo de datos), devolvemos 0.0
        return 0.0
