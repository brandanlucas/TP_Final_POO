# src/modelo_poo.py
from enum import Enum # Esto me sirve para crear "listas fijas" de los estados de las obras
import datetime # para manejar fechas

# Lista de Estados que pueden tener Obra (usando Enum para que sea más fácil de manejar)
class EstadoObra(Enum):
    # Cada uno de estos es una opción. El valor de la derecha es lo que realmente se va a guardar en la DB.
    EN_EJECUCION = "EN EJECUCION"
    FINALIZADA = "FINALIZADA"
    PLAZO_VENCIDO = "PLAZO VENCIDO"
    RESGUARDADA = "RESGUARDADA"
    ADJUDICADA = "ADJUDICADA"
    OTRO = "OTRO"               # Si el CSV me tira un estado que no conozco, lo meto acá.

    # Este método hace que si el CSV me viene un texto como "en ejecucion" lo convierte a mi Enum
    # Lo pongo como '@staticmethod' porque no necesita un objeto 'EstadoObra' para funcionar.
    @staticmethod
    def from_string(estado_str: str):
        # Primero, limpio el texto del CSV (lo pongo en mayúsculas y le saco espacios
        estado_str_limpio = estado_str.upper().strip()
        # Recorro cada estado en mi lista (Enum)
        for estado_enum in EstadoObra:
            # Si el texto limpio del CSV coincide con alguno de mis valores de Enum...
            if estado_enum.value == estado_str_limpio:
                return estado_enum # Devuelvo el objeto Enum correcto
        return EstadoObra.OTRO # Si no lo encuentro, devuelvo 'OTRO'


class Ministerio:
    # Recibe el ID que viene de la base de datos, porque lo vamos a cargar de ahí y un 'nombre'
    def __init__(self, id_db: int, nombre: str):
        # Guardo esos datos que me pasaron en los atributos de este objeto.
        self.id_db = id_db
        self.nombre = nombre

    # Este método '__str__' es para que cuando yo imprima un objeto Ministerio
    def __str__(self):
        return f"Ministerio(ID DB: {self.id_db}, Nombre: {self.nombre})"

    # - Si comparo 'min1 == min2', solo va a ser 'True' si son EXACTAMENTE EL MISMO OBJETO en la memoria
    #   No va a comparar si tienen el mismo ID o nombre. Tendría que hacer 'min1.id_db == min2.id_db' a mano



# Clase para la Empresa Contratista
class EmpresaContratista:
    def __init__(self, id_db: int, nombre: str):
        self.id_db = id_db
        self.nombre = nombre

    def __str__(self):
        return f"EmpresaContratista(ID DB: {self.id_db}, Nombre: {self.nombre})"



# Acá va casi toda la data del CSV
class Obra:
    # Pongo un valor por defecto (como '', 0.0, 0, None) para los que pueden venir vacíos del CSV,
    # así mi código no explota si falta un dato
    # 'id_db: int = None' es el ID que me da la base de datos DESPUÉS de guardarla
    # 'ministerio: Ministerio = None' acá guardo un objeto Ministerio
    def __init__(self,
                id_obra_csv: int,       # El ID original que viene en el CSV
                nombre: str,
                etapa: str = '',
                tipo: str = '',
                area_responsable: str = '',
                descripcion: str = '',
                monto: float = 0.0,
                comuna: int = 0,
                barrio: str = '',
                direccion: str = '',
                latitud: float = 0.0,
                longitud: float = 0.0,
                fecha_inicio: datetime.date = None, # Uso 'None' para fechas que pueden faltar
                fecha_fin_inicial: datetime.date = None,
                fecha_fin_real: datetime.date = None,
                porcentaje_avance: float = 0.0,
                imagen: str = '',
                licitacion_anio: int = 0,
                contrato_tipo: str = '',
                nro_contrato: str = '',
                nro_expediente: str = '',
                licitacion_presupuesto: float = 0.0,
                beneficiarios: str = '',
                observaciones: str = '',
                estado: EstadoObra = EstadoObra.OTRO, # Acá uso mi Enum de EstadoObra
                ministerio: Ministerio = None,       # Guardo un objeto Ministerio (el que creamos antes)
                empresa_contratista: EmpresaContratista = None, # Y un objeto EmpresaContratista.
                id_db: int = None                    # El ID que me da la base de datos al guardar la obra.
                ):

        # Guardo todos esos datos en los atributos de mi objeto 'Obra'.
        self.id_db = id_db # Este es el ID que me da la base de datos después de guardar la obra
        self.id_obra_csv = id_obra_csv # El ID original que viene en el CSV, no cambia al guardar en la DB
        self.nombre = nombre # El nombre de la obra, que viene del CSV
        self.etapa = etapa # La etapa de la obra (puede ser '', si no viene del CSV)
        self.tipo = tipo # El tipo de obra (puede ser '', si no viene del CSV)
        self.area_responsable = area_responsable # El área responsable de la obra (puede ser '', si no viene del CSV)
        self.descripcion = descripcion # Una descripción de la obra (puede ser '', si no viene del CSV)
        self.monto = monto # El monto de la obra (puede ser 0.0, si no viene del CSV)
        self.comuna = comuna # La comuna donde está la obra (puede ser 0, si no viene del CSV)
        self.barrio = barrio # El barrio donde está la obra (puede ser '', si no viene del CSV)
        self.direccion = direccion # La dirección de la obra (puede ser '', si no viene del CSV)
        self.latitud = latitud # La latitud de la obra (puede ser 0.0, si no viene del CSV)
        self.longitud = longitud # La longitud de la obra (puede ser 0.0, si no viene del CSV)
        self.fecha_inicio = fecha_inicio # La fecha de inicio de la obra (puede ser None, si no viene del CSV)
        self.fecha_fin_inicial = fecha_fin_inicial # La fecha de fin inicial de la obra (puede ser None, si no viene del CSV)
        self.fecha_fin_real = fecha_fin_real # La fecha de fin real de la obra (puede ser None, si no viene del CSV)
        self.porcentaje_avance = porcentaje_avance # El porcentaje de avance de la obra (puede ser 0.0, si no viene del CSV)
        self.imagen = imagen # La URL de la imagen de la obra (puede ser '', si no viene del CSV)
        self.licitacion_anio = licitacion_anio # El año de la licitación (puede ser 0, si no viene del CSV)
        self.contrato_tipo = contrato_tipo # El tipo de contrato (puede ser '', si no viene del CSV)
        self.nro_contrato = nro_contrato # El número de contrato (puede ser '', si no viene del CSV)
        self.nro_expediente = nro_expediente # El número de expediente (puede ser '', si no viene del CSV)
        self.licitacion_presupuesto = licitacion_presupuesto # El presupuesto de la licitación (puede ser 0.0, si no viene del CSV)
        self.beneficiarios = beneficiarios # Los beneficiarios de la obra (puede ser '', si no viene del CSV)
        self.observaciones = observaciones # Las observaciones de la obra (puede ser '', si no viene del CSV)
        self.estado = estado # El estado de la obra, usando mi Enum EstadoObra (por defecto es 'OTRO')
        self.ministerio = ministerio # Guardo un objeto Ministerio (puede ser None si no viene del CSV)
        self.empresa_contratista = empresa_contratista # Guardo un objeto EmpresaContratista (puede ser None si no viene del CSV)

    def __str__(self):
        # Si 'ministerio' o 'empresa_contratista' son None, pongo 'N/A' para que no explote
        return (f"Obra(ID CSV: {self.id_obra_csv}, Nombre: {self.nombre}, "
                f"Barrio: {self.barrio}, Estado: {self.estado.value}, "
                f"Ministerio: {self.ministerio.nombre if self.ministerio else 'N/A'}, "
                f"Empresa: {self.empresa_contratista.nombre if self.empresa_contratista else 'N/A'})")


    # Estos son comportamientos de la obra, cosas que puede hacer o chequear
    def esta_finalizada(self) -> bool:
        # Una forma fácil de saber si una obra está finalizada
        return self.estado == EstadoObra.FINALIZADA

    def calcular_aumento_porcentaje(self) -> float:
        # Calcula cuánto aumentó el monto de la obra respecto al presupuesto inicial
        # Tengo que chequear que haya montos y que el presupuesto no sea cero
        if self.monto and self.licitacion_presupuesto and self.licitacion_presupuesto > 0:
            return ((self.monto - self.licitacion_presupuesto) / self.licitacion_presupuesto) * 100
        return 0.0 # Si no se puede calcular, devuelvo 0