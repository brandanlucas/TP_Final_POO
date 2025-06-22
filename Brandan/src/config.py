# src/config.py
import os

# --- Rutas de Archivos ---
# Obtener el directorio base del proyecto.
# os.path.abspath(__file__) da la ruta completa de este archivo (config.py).
# os.path.dirname(...) dos veces para subir dos niveles y llegar a la carpeta raíz del proyecto.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta al archivo CSV de obras
CSV_FILE_NAME = "observatorio-de-obras-urbanas.csv"
# Une la ruta base con la carpeta 'data' y el nombre del archivo CSV
CSV_FILE_PATH = os.path.join(BASE_DIR, 'data', CSV_FILE_NAME)

# Ruta al archivo de la base de datos SQLite
DB_FILE_NAME = "obras_urbanas.db"
# El TP indica "ubicada en la misma carpeta solución del proyecto",
# así que la ponemos directamente en BASE_DIR.
DB_FILE_PATH = os.path.join(BASE_DIR, DB_FILE_NAME)

# --- Configuraciones del CSV ---
# Es CRÍTICO que la codificación y el delimitador coincidan con tu archivo CSV real.
# 'latin-1' es común para archivos generados en Windows o con caracteres especiales en español.
# Si tus caracteres aparecen raros (ej. Ã±, Ã¡), prueba con 'utf-8' o 'iso-8859-1'.
CSV_ENCODING = 'latin-1' # ¡Verifica esto con tu CSV!
CSV_DELIMITER = ';'      # ¡Verifica esto con tu CSV! Si es de Excel puede ser ';'

# --- Mensajes de la Aplicación (Opcional, pero recomendado para centralizar textos) ---
MSG_BIENVENIDA = "--- Sistema de Gestión de Obras Urbanas del GCBA ---"
MSG_MENU_PRINCIPAL = """
Seleccione una opción:
1. Cargar datos del archivo CSV en la Base de Datos
2. Crear nueva Obra
3. Buscar Obra por Nombre
4. Buscar Obra por ID
5. Listar Cantidad de Obras por Barrio
6. Modificar Estado de una Obra
7. Borrar una Obra
8. Listar todas las Obras
9. Listar Obras por Rango de Costos
10. Listar Obras por Porcentaje de Aumento
11. Listar Obras por Fechas
12. Descargar listado de Obras como CSV
0. Salir
"""
MSG_OPCION_INVALIDA = "Opción no válida. Por favor, intente de nuevo."
MSG_PRESIONE_ENTER = "\nPresione Enter para continuar..."

# --- Otras configuraciones (si fueran necesarias en el futuro) ---
# Por ejemplo, valores por defecto, formatos de fecha, etc.
DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'] # Formatos de fecha esperados en el CSV