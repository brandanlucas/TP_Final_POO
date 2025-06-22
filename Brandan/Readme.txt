2-Título:
feat: Definir modelos ORM con Peewee y conexión a la DB

Descripción:
Se implementa el módulo 'src/modelo_orm.py' para establecer la estructura de la base de datos relacional.

- Se configura la conexión a la base de datos SQLite 'obras_urbanas.db' utilizando la ruta de 'config.py'.
- Se definen los modelos Peewee (MinisterioORM, EmpresaContratistaORM y ObraORM) que mapearán a las tablas de la base de datos.
- Se establecen los tipos de campo adecuados (CharField, IntegerField, DecimalField, DateField) y las claves foráneas (ForeignKeyField) para Ministerio y Empresa Contratista.
- Se incluye la lista 'ALL_MODELS' para facilitar la creación de tablas.