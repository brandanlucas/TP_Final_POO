# test_inicial.py
import os # Necesitamos esto para manejar archivos y rutas, como borrar la DB de prueba.
from src.config import DB_FILE_PATH # Importo la ruta de la DB desde mi archivo de configuración. ¡Así no la tengo hardcodeada!
from src.modelo_orm import db, ALL_MODELS # Importo la conexión a la DB y la lista de todos mis modelos ORM.
from src.modelo_poo import Ministerio, EmpresaContratista, Obra, EstadoObra # Importo mis clases POO y el Enum.
import datetime # Para poder crear fechas en mis objetos Obra.

print("--- Iniciando prueba inicial del proyecto ---")

# --- Paso 1: Limpiar base de datos anterior si existe ---
# Esto es para asegurarnos de que siempre empezamos con una base de datos limpia en cada prueba.
# Si el archivo de la DB ya existe, lo borro.
if os.path.exists(DB_FILE_PATH):
    os.remove(DB_FILE_PATH)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Archivo de base de datos '{DB_FILE_PATH}' eliminado para una prueba limpia.")
else:
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Archivo de base de datos '{DB_FILE_PATH}' no encontrado, creando uno nuevo.")

# --- Paso 2: Conectar a la base de datos y crear las tablas ---
# Acá le digo a Peewee: "Abrí la conexión a la DB".
db.connect()
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Conexión a la base de datos establecida.")

try:
    # Intento crear todas las tablas que definí en modelo_orm.py.
    # Peewee es inteligente y las crea en el orden correcto si hay relaciones.
    db.create_tables(ALL_MODELS)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¡Tablas de la base de datos creadas correctamente!")

except Exception as e:
    # Si algo sale mal al crear las tablas, me lo avisa.
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ERROR al crear las tablas: {e}")

finally:
    # Siempre, SIEMPRE cerrar la conexión a la base de datos cuando terminamos.
    db.close()
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Conexión a la base de datos cerrada.")

# --- Paso 3: Probar la creación de objetos POO y su impresión ---
print("\n--- Probando la creación de objetos POO ---")

# Creo un objeto Ministerio de prueba
mi_ministerio = Ministerio(id_db=1, nombre="Ministerio de Desarrollo Urbano")
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Objeto Ministerio creado: {mi_ministerio}")

# Creo un objeto Empresa Contratista de prueba
mi_empresa = EmpresaContratista(id_db=1, nombre="Empresa Constructora XYZ S.A.")
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Objeto Empresa creado: {mi_empresa}")

# Creo un objeto Obra de prueba, usando los objetos Ministerio y Empresa.
# Usamos EstadoObra.from_string para convertir un texto a nuestro Enum.
mi_obra = Obra(
    id_obra_csv=12345,
    nombre="Renovación Plaza San Martín",
    etapa="En Ejecución",
    comuna=1,
    barrio="Retiro",
    estado=EstadoObra.from_string("en ejecucion"), # ¡Mira cómo usamos el método de nuestro Enum!
    ministerio=mi_ministerio,
    empresa_contratista=mi_empresa,
    fecha_inicio=datetime.date(2024, 1, 15), # Ejemplos de fechas.
    monto=15000000.50
)
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Objeto Obra creado: {mi_obra}")

# Probando un método de negocio de Obra
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¿La obra está finalizada? {mi_obra.esta_finalizada()}")
otra_obra = Obra(id_obra_csv=67890, nombre="Nueva Estación de Metrobus", estado=EstadoObra.from_string("Finalizada"))
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ¿La otra obra está finalizada? {otra_obra.esta_finalizada()}")

print("\n--- Prueba inicial finalizada ---")