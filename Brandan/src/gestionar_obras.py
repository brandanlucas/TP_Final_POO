import pandas as pd # Permite leer archivos CSV grandes y manipular tablas de datos
import datetime 
import os # Me sirve para ver si un archivo existe o para crear carpetas, cosas del sistema operativo

# ¡Acá importo mis propias cosas! Mis rutas de la configuración,
# y mis clases para la DB (ORM) y para mis objetos en Python (POO).
from src.config import CSV_FILE_PATH, DB_FILE_PATH
from src.modelo_orm import db, MinisterioORM, EmpresaContratistaORM, ObraORM
from src.modelo_poo import Ministerio, EmpresaContratista, Obra, EstadoObra


# Esta función es la que arregla todo (datos vacíos, fechas, etc) y guarde datos prolijos en la DB.
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] A ver, ¡vamos a limpiar y poner orden en estos datos!")

    # 1. ¡Que los nombres de las columnas coincidan!
    # Me aseguro de que el nombre de la columna en el CSV sea igual al nombre de mis atributos en las clases POO/ORM.
    columnas_a_renombrar = {
        'id_obra': 'id_obra_csv',               # Este es el ID original de la obra en el CSV. ¡Mi identificador principal!
        'nombre': 'nombre',
        'etapa': 'etapa',
        'tipo': 'tipo',
        'area_responsable': 'area_responsable',
        'descripcion': 'descripcion',
        'monto_contrato': 'monto',              # El monto lo llamo 'monto' en mi sistema.
        'comuna': 'comuna',
        'barrio': 'barrio',
        'direccion': 'direccion',
        'latitud': 'latitud',
        'longitud': 'longitud',
        'fecha_inicio': 'fecha_inicio',
        'fecha_fin_inicial': 'fecha_fin_inicial',
        'fecha_fin_real': 'fecha_fin_real',
        'porcentaje_avance': 'porcentaje_avance',
        'imagen': 'imagen',
        'licitacion_anio': 'licitacion_anio',
        'contrato_tipo': 'contrato_tipo',
        'nro_contrato': 'nro_contrato',
        'nro_expediente': 'nro_expediente',
        'presupuesto_oficial': 'licitacion_presupuesto', # El presupuesto de la licitación lo llamo así.
        'beneficiarios': 'beneficiarios',
        'observaciones': 'observaciones',
        'estado': 'estado',
        'nombre_ministerio': 'nombre_ministerio', # Necesito el nombre del Ministerio para buscarlo/crearlo después.
        'nombre_contratista': 'nombre_contratista' # Lo mismo para la empresa contratista.
    }
    df = df.rename(columns=columnas_a_renombrar) # ¡Aplicamos los cambios de nombre en mi tabla de Pandas!

    # Acá me aseguro de que si un dato viene vacío (NaN de Pandas), le pongo un valor por defecto
    # Y que cada columna tenga el tipo de dato que quiero (texto, número, etc.) para que la DB no me dé errores

    # Para textos: si están vacíos, los dejo como cadena vacía.
    string_cols = ['etapa', 'tipo', 'area_responsable', 'descripcion', 'barrio', 'direccion',
                    'imagen', 'contrato_tipo', 'nro_contrato', 'nro_expediente',
                    'beneficiarios', 'observaciones', 'estado', 'nombre_ministerio', 'nombre_contratista']
    for col in string_cols:
        if col in df.columns: # Me aseguro de que la columna exista en el CSV.
            df[col] = df[col].fillna('').astype(str) # Relleno NaNs y me aseguro que sean strings.

    # Para números con decimales (flotantes): si están vacíos, los pongo en 0.0.
    numeric_cols = ['monto', 'latitud', 'longitud', 'porcentaje_avance', 'licitacion_presupuesto']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') # Intento convertir a número, si no puede, pone NaN.
            df[col] = df[col].fillna(0.0) # Ahora, los NaNs (sean originales o por error) los pongo en 0.0.

    # Para números enteros (IDs, años, comunas): si están vacíos, los pongo en 0.
    integer_cols = ['id_obra_csv', 'comuna', 'licitacion_anio']
    for col in integer_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int) # Similar a los flotantes, pero a entero.

    # 3. ¡Las fechas! ¡Siempre un desafío!
    # El método 'to_datetime' de Pandas es lo mejor. 'errors='coerce'' es magia:
    # si no es una fecha válida, pone un 'NaT' (Not a Time), y yo después lo convierto a 'None'
    # para que mi objeto POO y la DB entiendan que está vacío.
    date_cols = ['fecha_inicio', 'fecha_fin_inicial', 'fecha_fin_real']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True) # dayfirst=True si el formato es día/mes/año
            df[col] = df[col].apply(lambda x: x.date() if pd.notna(x) else None) # Convierto a objeto date de Python o a None.

    # 4. Normalizar el 'estado' de la obra usando mi Enum (¡Esto es POO puro!)
    # Acá uso mi truquito de EstadoObra.from_string() para que el texto del CSV
    # (ej. "en ejecucion") se transforme en mi objeto Enum (EstadoObra.EN_EJECUCION).
    # ¡Así me aseguro que los estados siempre sean válidos!
    if 'estado' in df.columns:
        df['estado'] = df['estado'].apply(EstadoObra.from_string)

    # 5. ¡Eliminar obras duplicadas!
    # Por si el CSV tiene la misma obra dos veces (mismo id_obra_csv), me quedo solo con una.
    # 'keep='first'' significa que si hay duplicados, me quedo con la primera que aparece.
    if 'id_obra_csv' in df.columns:
        df.drop_duplicates(subset=['id_obra_csv'], keep='first', inplace=True)


    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¡Datos limpios y listos para la batalla!")
    return df

# --- Función para leer el CSV (¡El punto de partida!) ---
# Esta es simple: solo lee el archivo que le digo y lo mete en una tabla de Pandas.
def cargar_csv(ruta_csv: str) -> pd.DataFrame:
    # Primero, me aseguro de que el archivo exista para no chocar.
    if not os.path.exists(ruta_csv):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ERROR: ¡No encuentro el archivo CSV en '{ruta_csv}'! ¿Lo pusiste bien en la carpeta 'data'?")
        return pd.DataFrame() # Si no lo encuentro, devuelvo una tabla vacía.

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¡Leyendo los datos del CSV desde '{ruta_csv}'!")
    try:
        # Intento leerlo. El 'sep=';'' es importante si el CSV usa punto y coma como separador.
        # Y 'encoding='utf-8'' es lo más común, si da error, probá con 'latin1' o 'ISO-8859-1'.
        df = pd.read_csv(ruta_csv, sep=';', encoding='utf-8')
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] CSV cargado. ¡Tenemos {len(df)} filas iniciales!")
        return df
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ERROR al cargar el CSV: ¡Algo salió mal! {e}")
        return pd.DataFrame() # Si hay error al leer, devuelvo tabla vacía.

# --- Mi Función Principal para Cargar la Base de Datos (¡El gran paso!) ---
# Esta función es la que va a coordinar todo. Por ahora, solo lee y limpia,
# pero en el siguiente paso, ¡acá es donde vamos a meter los datos en la DB!
def inicializar_base_de_datos_con_datos_csv():
    print(f"\n--- ¡Arrancando el proceso de meter los datos del CSV a mi base de datos! ---")

    # Paso 1: Primero, vamos a leer el CSV.
    df_obras = cargar_csv(CSV_FILE_PATH)
    if df_obras.empty:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¡Ups! No hay datos en el CSV o no se pudo cargar. No hay nada que procesar.")
        return # Si la tabla está vacía, no sigo.

    # Paso 2: Ahora, vamos a limpiar esa data para que esté perfecta.
    df_obras_limpio = limpiar_datos(df_obras)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¡Datos limpios! Nos quedaron {len(df_obras_limpio)} filas después de toda la limpieza.")

    # Por ahora, solo te muestro cómo quedaron los datos.
    print("\n--- Mirá las primeras 5 filas de tu tabla de datos LIMPIA: ---")
    print(df_obras_limpio.head()) # 'head()' te muestra las primeras filas.
    print("\n--- Y acá están los tipos de datos de cada columna (¡importante que sean los correctos!): ---")
    print(df_obras_limpio.info()) # 'info()' te da un resumen con los tipos de datos y cuántos valores no nulos hay.
    print("--- Proceso de inicialización (solo lectura y limpieza por ahora) ¡FINALIZADO por este paso! ---")


# Si abro la terminal y pongo 'python src/gestionar_obras.py', este bloque se ejecuta.
if __name__ == "__main__":
    # Una pequeña verificación: me aseguro que la carpeta 'data' exista. Si no, la creo.
    if not os.path.exists('data'):
        os.makedirs('data')
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Creada carpeta 'data'. ¡Ahí va el CSV!")

    inicializar_base_de_datos_con_datos_csv()