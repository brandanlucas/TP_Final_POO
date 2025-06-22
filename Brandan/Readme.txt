2-Definir modelos ORM con Peewee y conexión a la DB

Descripción:
Se implementa el módulo 'src/modelo_orm.py' para establecer la estructura de la base de datos relacional.

- Se configura la conexión a la base de datos SQLite 'obras_urbanas.db' utilizando la ruta de 'config.py'.
- Se definen los modelos Peewee (MinisterioORM, EmpresaContratistaORM y ObraORM) que mapearán a las tablas de la base de datos.
- Se establecen los tipos de campo adecuados (CharField, IntegerField, DecimalField, DateField) y las claves foráneas (ForeignKeyField) para Ministerio y Empresa Contratista.
- Se incluye la lista 'ALL_MODELS' para facilitar la creación de tablas.


Aclaración por los valores Null: null=True en modelo_orm.py (capa de DB):
Le dice a la base de datos que está permitido que esa columna no tenga valor.
Es como decir "La puerta puede estar abierta si no hay nadie que pase".
Esto nos da flexibilidad para manejar datos faltantes del CSV sin que la DB nos dé un error de inmediato.
Limpieza de datos en gestionar_obras.py (lógica de aplicación):
Aquí es donde vamos a "limpiar" esos valores nulos o vacíos del CSV y convertirlos, por ejemplo,
en una cadena de texto vacía ('') o "N/A" ANTES de intentar guardarlos. Es como decir
"Si la puerta está abierta (null=True), pero no hay nadie, la cerramos y ponemos un cartel de 'no hay nadie'
(cadena vacía) en lugar de dejarla simplemente abierta"



3-
