Dashboard de Ventas con Python, MySQL y Streamlit

Este repositorio contiene un dashboard interactivo para el análisis de ventas empresariales, desarrollado con Python, Streamlit, Altair, MySQL y Prophet.

Incluye la estructura completa de base de datos, consultas analíticas, gráficos comparativos e informes automáticos.

📂 Estructura del Proyecto
├── crear_base_datos.sql           # Script para crear tablas en MySQL
├── base_datos_insertar_datos.sql # Datos de ejemplo para poblar la base
├── conexion_mysql.py             # Configuración de conexión a la base de datos
├── consultas.py                  # Funciones de consulta y KPIs
├── utils.py                      # Funciones auxiliares: formateo, cálculo de variaciones, etc.
├── graficos.py                   # Generación de gráficos con Altair y Prophet
├── main.py                       # Archivo principal que ejecuta el dashboard en Streamlit
├── img01.png                     # KPIs visuales
├── img02.png                     # Gráficos comparativos
├── img03.png                     # Top Vendedores y Productos
├── informe                       # Análisis detallados en formato markdown

⚙️ Tecnologías Utilizadas

Python 3.10+

MySQL (motor de base de datos)

Streamlit (framework para dashboards)

Pandas / Altair / Prophet (análisis y visualización de datos)

# 1. Clona el repositorio
https://github.com/jrsa061275/dashboard-ventas-python-sql.git

# 2. Instala las dependencias necesarias
pip install streamlit pandas altair mysql-connector-python prophet

# 3. Ejecuta el dashboard
streamlit run main.py

📊 Funcionalidades

Comparación de KPIs: ingresos, transacciones, clientes y productos.

Gráficos comparativos entre año actual y anterior.

Predicción de ingresos futuros con inteligencia artificial (Prophet).

Tablas Top 5 de vendedores y productos.

Panel responsivo, con estilo visual limpio y profesional.

📚 Informes

Los informes se encuentran en el archivo informe, incluyendo:

Explicación de KPIs.

Análisis mensual.

Evaluación de variaciones.

Recomendaciones por vendedor y producto.


📝 Autor

Juan Ricardo Sánchez ÁlvarezDesarrollador y analista de datos LinkedIn | GitHub

✨ Capturas del Dashboard

KPIs Visuales
Comparativo Mensual
Top 5 Vendedores y Productos
