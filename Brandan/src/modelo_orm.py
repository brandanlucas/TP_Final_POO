from peewee import * # Esta es la librería "Peewee" para hablar con la base de datos
from src.config import DB_FILE_PATH # Ruta donde estará la base de datos

# 1. Conexión a la base de datos
db = SqliteDatabase(DB_FILE_PATH)

# 2. Clase Base para los Modelos ORM. Aca van todas las tablas de la base de datos. Heredan de BaseModel
class BaseModel(Model):
    class Meta:
        database = db # Aca le digo a qué base de datos se van a conectar nuestros modelos. Podría ser una base de datos PostgreSQL o MySQL.
        # si quisiera usar otra base de datos, solo cambiaria esta línea por la conexión a otra base de datos
        # para PostgreSQL podría usar: database = PostgresqlDatabase('nombre_db', user='usuario', password='contraseña', host='localhost', port=5432)

# 3. Modelos ORM: Cada una de estas CLASES representa una TABLA real en SQLite. Los ATRIBUTOS de cada clase, son las COLUMNAS de esa tabla

# Modelo para la tabla de Ministerios
class MinisterioORM(BaseModel):
    id = AutoField() # AutoField automáticamente crea una columna 'id' que será la "Primary Key" y autoincremental
    nombre = CharField(unique=True, index=True) #CharField es para texto corto
    
    class Meta:
        table_name = 'Ministerios' # Este es el nombre real de la tabla en mi base de datos


class EmpresaContratistaORM(BaseModel):
    id = AutoField()
    nombre = CharField(unique=True, index=True)
    
    class Meta:
        table_name = 'EmpresasContratistas'


class ObraORM(BaseModel):
    id = AutoField()
    id_obra_csv = IntegerField(unique=True, index=True) # IntegerField es para números enteros

    nombre = CharField() 
    etapa = CharField(null=True) # Puede que no siempre haya datos de etapa en el CSV, 'null=True' permite que esté vacío
    tipo = CharField(null=True)
    area_responsable = CharField(null=True)
    descripcion = TextField(null=True)
    monto = FloatField(null=True)
    comuna = IntegerField(null=True)
    barrio = CharField(null=True)
    direccion = CharField(null=True)
    latitud = DecimalField(null=True)
    longitud = DecimalField(null=True)

    # formato que usa Peewee es estándar de fecha en la DB (YYYY-MM-DD).
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    fecha_fin_real = DateField(null=True)

    porcentaje_avance = DecimalField(null=True)
    imagen = CharField(null=True)
    licitacion_anio = IntegerField(null=True)
    contrato_tipo = CharField(null=True)
    nro_contrato = CharField(null=True)
    nro_expediente = CharField(null=True)
    licitacion_presupuesto = DecimalField(auto_round=True, null=True)
    beneficiarios = CharField(null=True)
    observaciones = TextField(null=True)

    # 'estado': valor del estado de la obra como un texto (ej. "iniciada", "finalizada").
    estado = CharField(null=True)

    # Foreign Keys, esto conecta la tabla de Obras con las tablas de Ministerios y Empresas (a través del 'id')
    # 'backref='obras' sirve para que desde Ministerio y Empresa pueda acceder a sus Obras relacionadas
    ministerio = ForeignKeyField(MinisterioORM, backref='obras', null=True)
    empresa_contratista = ForeignKeyField(EmpresaContratistaORM, backref='obras', null=True)

    class Meta:
        table_name = 'Obras'

# --- Lista de todos los modelos para la creación de tablas --- Cuando queramos crear todas las tablas en la DB de golpe,
# podemos pasarle esta lista a Peewee. Nos asegura que se creen en el orden correcto
# (Ministerios y Empresas primero, porque Obras depende de ellas por las claves foráneas)
ALL_MODELS = [MinisterioORM, EmpresaContratistaORM, ObraORM]